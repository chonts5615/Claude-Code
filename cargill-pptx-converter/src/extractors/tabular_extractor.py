"""
Tabular data (CSV, Excel) content extractor.
"""

import re
from pathlib import Path
from uuid import uuid4

from src.extractors.base import BaseExtractor
from src.schemas.content import (
    ContentBlock,
    ContentType,
    DocumentMetadata,
    ExtractedContent,
)


class TabularExtractor(BaseExtractor):
    """Extract content from CSV and Excel files."""

    def supported_extensions(self) -> list[str]:
        return [".csv", ".xlsx", ".xls"]

    def extract(self, file_path: Path) -> ExtractedContent:
        import pandas as pd

        ext = file_path.suffix.lower()
        blocks: list[ContentBlock] = []
        warnings: list[str] = []
        word_count = 0

        try:
            if ext == ".csv":
                dfs = {"Sheet1": pd.read_csv(str(file_path))}
            else:
                xls = pd.ExcelFile(str(file_path))
                dfs = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}
        except Exception as e:
            return ExtractedContent(
                source_file=str(file_path),
                source_format=ext.lstrip("."),
                blocks=[],
                extraction_warnings=[f"Failed to read file: {e}"],
            )

        for sheet_name, df in dfs.items():
            if df.empty:
                warnings.append(f"Sheet '{sheet_name}' is empty")
                continue

            # Clean up dataframe
            df = df.dropna(how="all").reset_index(drop=True)
            df.columns = [str(c).strip() for c in df.columns]

            # Add sheet name as heading if multiple sheets
            if len(dfs) > 1:
                blocks.append(ContentBlock(
                    block_id=f"tab_h_{uuid4().hex[:6]}",
                    content_type=ContentType.HEADING,
                    text=sheet_name,
                    level=2,
                ))

            # Convert to table block
            headers = list(df.columns)
            rows = []
            for _, row in df.iterrows():
                row_data = [str(v).strip() if pd.notna(v) else "" for v in row]
                rows.append(row_data)
                word_count += sum(len(cell.split()) for cell in row_data)

            block_id = f"tab_{uuid4().hex[:8]}"
            blocks.append(ContentBlock(
                block_id=block_id,
                content_type=ContentType.TABLE,
                table_data=rows,
                table_headers=headers,
                metadata={
                    "sheet": sheet_name,
                    "row_count": len(rows),
                    "col_count": len(headers),
                },
            ))

            # Detect numeric columns that could be charted
            numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
            non_numeric_cols = [c for c in df.columns if c not in numeric_cols]

            if numeric_cols and non_numeric_cols and len(df) <= 20:
                # Create a chart data block
                category_col = non_numeric_cols[0]
                chart_data = {
                    "categories": [str(v) for v in df[category_col].tolist()],
                    "series": [],
                }
                for col in numeric_cols[:5]:  # Max 5 series
                    chart_data["series"].append({
                        "name": col,
                        "values": [float(v) if pd.notna(v) else 0.0 for v in df[col].tolist()],
                    })

                chart_block_id = f"tab_chart_{uuid4().hex[:6]}"
                blocks.append(ContentBlock(
                    block_id=chart_block_id,
                    content_type=ContentType.CHART_DATA,
                    chart_data=chart_data,
                    metadata={
                        "sheet": sheet_name,
                        "chart_type_hint": self._suggest_chart_type(df, numeric_cols, category_col),
                    },
                ))

            # Extract key statistics from numeric columns
            for col in numeric_cols[:4]:
                try:
                    total = df[col].sum()
                    mean_val = df[col].mean()
                    max_val = df[col].max()

                    # Format nicely
                    if abs(total) >= 1_000_000:
                        formatted = f"${total/1_000_000:.1f}M" if total > 0 else f"{total/1_000_000:.1f}M"
                    elif abs(total) >= 1_000:
                        formatted = f"{total:,.0f}"
                    else:
                        formatted = f"{total:.1f}"

                    blocks.append(ContentBlock(
                        block_id=f"stat_{uuid4().hex[:6]}",
                        content_type=ContentType.STATISTIC,
                        text=formatted,
                        metadata={
                            "label": f"Total {col}",
                            "raw_value": float(total),
                            "mean": float(mean_val),
                            "max": float(max_val),
                            "column": col,
                        },
                    ))
                except Exception:
                    pass

        metadata = DocumentMetadata(
            title=file_path.stem.replace("_", " ").replace("-", " ").title(),
            word_count=word_count,
            has_tables=True,
            has_charts=any(b.content_type == ContentType.CHART_DATA for b in blocks),
        )

        return ExtractedContent(
            source_file=str(file_path),
            source_format=ext.lstrip("."),
            blocks=blocks,
            metadata=metadata,
            extraction_warnings=warnings,
        )

    def _suggest_chart_type(self, df, numeric_cols: list, category_col: str) -> str:
        """Suggest appropriate chart type based on data characteristics."""
        row_count = len(df)

        # Time series detection
        cat_values = df[category_col].astype(str).tolist()
        time_patterns = [
            r"\d{4}", r"Q[1-4]", r"Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec",
            r"Week\s*\d+", r"\d{1,2}/\d{1,2}",
        ]
        is_time_series = any(
            sum(1 for v in cat_values if re.search(p, v, re.IGNORECASE)) > len(cat_values) * 0.5
            for p in time_patterns
        )

        if is_time_series:
            return "line"

        # Proportion detection (values sum to approximately 100)
        if len(numeric_cols) == 1:
            total = df[numeric_cols[0]].sum()
            if 95 <= total <= 105 and row_count <= 8:
                return "pie"

        # Few categories = bar chart
        if row_count <= 10:
            return "bar"

        # More categories = horizontal bar
        if row_count <= 20:
            return "horizontal_bar"

        return "column"
