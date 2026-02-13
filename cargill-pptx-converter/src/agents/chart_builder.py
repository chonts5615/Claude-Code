"""
Agent 5: Data Visualization Agent

Transforms data tables and statistics into brand-compliant charts.
Uses matplotlib to generate chart images for embedding in slides.
"""

import io
from uuid import uuid4

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from src.agents.base import BaseAgent
from src.brand.constants import (
    HEX_CARGILL_LEAF_GREEN,
    HEX_NEUTRAL_200,
    HEX_NEUTRAL_700,
    HEX_WHITE,
    get_chart_colors,
)
from src.schemas.chart import ChartSpec, ChartType, DataSeries
from src.schemas.slide import SlideLayout
from src.schemas.run_state import RunState


# Configure matplotlib defaults for Cargill brand
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": HEX_NEUTRAL_200,
    "axes.labelcolor": HEX_NEUTRAL_700,
    "xtick.color": HEX_NEUTRAL_700,
    "ytick.color": HEX_NEUTRAL_700,
    "grid.color": HEX_NEUTRAL_200,
    "grid.linewidth": 0.5,
    "font.size": 12,
})


class ChartBuilderAgent(BaseAgent):
    """Create brand-compliant data visualizations."""

    def __init__(self):
        super().__init__("S5", "Chart Building")

    def execute(self, state: RunState) -> RunState:
        state.current_step = self.agent_id
        self.logger.info("Building data visualizations")

        if not state.presentation_plan:
            self._add_flag(state, "CRITICAL", "No presentation plan for chart building")
            return state

        chart_count = 0
        for slide in state.presentation_plan.slides:
            if slide.layout != SlideLayout.CHART:
                continue

            for element in slide.elements:
                if element.element_type != "chart" or not element.chart_spec:
                    continue

                try:
                    chart_spec = self._build_chart_spec(element.chart_spec, element.metadata)
                    chart_image = self._render_chart(chart_spec)

                    # Store rendered chart image in element
                    element.image_data = chart_image
                    element.metadata["chart_rendered"] = True
                    element.metadata["chart_type"] = chart_spec.chart_type.value
                    chart_count += 1

                except Exception as e:
                    self._add_flag(state, "WARNING", f"Failed to render chart: {e}")
                    element.metadata["chart_rendered"] = False

        self.logger.info(f"Built {chart_count} charts")
        return state

    def _build_chart_spec(self, raw_data: dict, metadata: dict) -> ChartSpec:
        """Build a ChartSpec from raw chart data."""
        chart_type_hint = metadata.get("chart_type_hint", "bar")

        try:
            chart_type = ChartType(chart_type_hint)
        except ValueError:
            chart_type = ChartType.BAR

        categories = raw_data.get("categories", [])
        series_data = raw_data.get("series", [])

        series = []
        colors = get_chart_colors(len(series_data))

        for i, s in enumerate(series_data):
            color = colors[i] if i < len(colors) else colors[-1]
            series.append(DataSeries(
                name=s.get("name", f"Series {i + 1}"),
                values=[float(v) if v is not None else 0.0 for v in s.get("values", [])],
                color=color,
            ))

        return ChartSpec(
            chart_id=f"chart_{uuid4().hex[:6]}",
            chart_type=chart_type,
            title=raw_data.get("title"),
            categories=categories,
            series=series,
            show_legend=len(series) > 1,
            show_data_labels=len(categories) <= 6,
            show_grid_lines=True,
        )

    def _render_chart(self, spec: ChartSpec) -> bytes:
        """Render a chart to PNG bytes using matplotlib."""
        fig, ax = plt.subplots(figsize=(spec.width_inches, spec.height_inches))

        if spec.chart_type in (ChartType.BAR, ChartType.COLUMN):
            self._render_bar_chart(ax, spec)
        elif spec.chart_type == ChartType.HORIZONTAL_BAR:
            self._render_horizontal_bar(ax, spec)
        elif spec.chart_type == ChartType.LINE:
            self._render_line_chart(ax, spec)
        elif spec.chart_type in (ChartType.PIE, ChartType.DONUT):
            self._render_pie_chart(ax, spec)
        elif spec.chart_type == ChartType.STACKED_BAR:
            self._render_stacked_bar(ax, spec)
        elif spec.chart_type == ChartType.AREA:
            self._render_area_chart(ax, spec)
        else:
            self._render_bar_chart(ax, spec)

        # Apply common styling
        if spec.chart_type not in (ChartType.PIE, ChartType.DONUT):
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_color(HEX_NEUTRAL_200)
            ax.spines["bottom"].set_color(HEX_NEUTRAL_200)

            if spec.show_grid_lines:
                ax.grid(axis="y", alpha=0.3)
                ax.set_axisbelow(True)

        if spec.title:
            ax.set_title(
                spec.title,
                fontsize=16,
                fontweight="bold",
                color=HEX_CARGILL_LEAF_GREEN,
                pad=20,
            )

        if spec.show_legend and len(spec.series) > 1:
            ax.legend(
                frameon=False,
                fontsize=10,
                loc="upper right",
            )

        plt.tight_layout()

        # Save to bytes
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor="white")
        plt.close(fig)
        buf.seek(0)
        return buf.getvalue()

    def _render_bar_chart(self, ax, spec: ChartSpec):
        """Render a vertical bar chart."""
        import numpy as np

        x = np.arange(len(spec.categories))
        width = 0.8 / max(len(spec.series), 1)

        for i, series in enumerate(spec.series):
            offset = (i - len(spec.series) / 2 + 0.5) * width
            bars = ax.bar(
                x + offset,
                series.values,
                width,
                label=series.name,
                color=series.color or HEX_CARGILL_LEAF_GREEN,
                edgecolor="none",
                zorder=3,
            )

            if spec.show_data_labels:
                for bar in bars:
                    height = bar.get_height()
                    ax.text(
                        bar.get_x() + bar.get_width() / 2.,
                        height,
                        f"{height:,.0f}" if height == int(height) else f"{height:,.1f}",
                        ha="center", va="bottom",
                        fontsize=9, color=HEX_NEUTRAL_700,
                    )

        ax.set_xticks(x)
        ax.set_xticklabels(spec.categories, fontsize=10)

    def _render_horizontal_bar(self, ax, spec: ChartSpec):
        """Render a horizontal bar chart."""
        import numpy as np

        y = np.arange(len(spec.categories))
        height = 0.8 / max(len(spec.series), 1)

        for i, series in enumerate(spec.series):
            offset = (i - len(spec.series) / 2 + 0.5) * height
            bars = ax.barh(
                y + offset,
                series.values,
                height,
                label=series.name,
                color=series.color or HEX_CARGILL_LEAF_GREEN,
                edgecolor="none",
                zorder=3,
            )

            if spec.show_data_labels:
                for bar in bars:
                    w = bar.get_width()
                    ax.text(
                        w, bar.get_y() + bar.get_height() / 2.,
                        f"  {w:,.0f}" if w == int(w) else f"  {w:,.1f}",
                        ha="left", va="center",
                        fontsize=9, color=HEX_NEUTRAL_700,
                    )

        ax.set_yticks(y)
        ax.set_yticklabels(spec.categories, fontsize=10)
        ax.invert_yaxis()

    def _render_line_chart(self, ax, spec: ChartSpec):
        """Render a line chart."""
        for series in spec.series:
            ax.plot(
                spec.categories,
                series.values,
                marker="o",
                markersize=6,
                linewidth=2.5,
                label=series.name,
                color=series.color or HEX_CARGILL_LEAF_GREEN,
                zorder=3,
            )

            if spec.show_data_labels:
                for x, y in zip(spec.categories, series.values):
                    ax.annotate(
                        f"{y:,.0f}" if y == int(y) else f"{y:,.1f}",
                        (x, y), textcoords="offset points",
                        xytext=(0, 10), ha="center",
                        fontsize=9, color=HEX_NEUTRAL_700,
                    )

        plt.xticks(fontsize=10, rotation=45 if len(spec.categories) > 6 else 0)

    def _render_pie_chart(self, ax, spec: ChartSpec):
        """Render a pie or donut chart."""
        if not spec.series:
            return

        values = spec.series[0].values
        colors = get_chart_colors(len(values))
        # Extend colors if needed
        while len(colors) < len(values):
            colors.append(HEX_NEUTRAL_700)

        wedge_props = {"linewidth": 2, "edgecolor": "white"}

        if spec.chart_type == ChartType.DONUT:
            wedges, texts, autotexts = ax.pie(
                values,
                labels=spec.categories,
                colors=colors[:len(values)],
                autopct="%1.0f%%",
                pctdistance=0.8,
                wedgeprops=dict(**wedge_props, width=0.4),
                textprops={"fontsize": 10},
            )
        else:
            wedges, texts, autotexts = ax.pie(
                values,
                labels=spec.categories,
                colors=colors[:len(values)],
                autopct="%1.0f%%",
                wedgeprops=wedge_props,
                textprops={"fontsize": 10},
            )

        for text in autotexts:
            text.set_fontsize(9)
            text.set_color("white")
            text.set_fontweight("bold")

    def _render_stacked_bar(self, ax, spec: ChartSpec):
        """Render a stacked bar chart."""
        import numpy as np

        x = np.arange(len(spec.categories))
        bottom = np.zeros(len(spec.categories))

        for series in spec.series:
            ax.bar(
                x, series.values,
                bottom=bottom,
                label=series.name,
                color=series.color or HEX_CARGILL_LEAF_GREEN,
                edgecolor="none",
                zorder=3,
            )
            bottom += np.array(series.values)

        ax.set_xticks(x)
        ax.set_xticklabels(spec.categories, fontsize=10)

    def _render_area_chart(self, ax, spec: ChartSpec):
        """Render an area chart."""
        for series in spec.series:
            ax.fill_between(
                spec.categories,
                series.values,
                alpha=0.3,
                color=series.color or HEX_CARGILL_LEAF_GREEN,
                zorder=2,
            )
            ax.plot(
                spec.categories,
                series.values,
                linewidth=2,
                label=series.name,
                color=series.color or HEX_CARGILL_LEAF_GREEN,
                zorder=3,
            )

        plt.xticks(fontsize=10, rotation=45 if len(spec.categories) > 6 else 0)
