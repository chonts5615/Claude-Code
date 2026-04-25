"""SkillMappingPipeline — sequential SM1→SM8 orchestrator.

Stages:
    SM1 catalog_loader      → list[TrainingItem]
    SM2 library_loader      → list[dict] (23-col)
    SM3 bloom_classifier    → BloomLevelEstimate per item
    SM4 semantic_matcher    → top-k (entry, score) per item
    SM5 level_resolver      → SkillCompetencyMapping[]
    GATE                    → unmapped %, zero-training %
    SM6 coverage_aggregator → CoverageCell[]
    SM7 gap_reporter        → GapFinding[], SurplusFinding[]
    SM8 excel_writer        → xlsx path
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import yaml

from src.skill_mapping.bloom_classifier import classify
from src.skill_mapping.catalog_loader import load_catalog
from src.skill_mapping.coverage_aggregator import aggregate
from src.skill_mapping.excel_writer import write_crosswalk
from src.skill_mapping.gap_reporter import report_gaps, report_surplus
from src.skill_mapping.level_resolver import resolve
from src.skill_mapping.library_loader import load_library
from src.skill_mapping.schemas import (
    CoverageCell,
    GapFinding,
    SkillCompetencyMapping,
    SurplusFinding,
    TrainingItem,
)
from src.skill_mapping.semantic_matcher import match


@dataclass
class PipelineGateMetrics:
    total_courses: int = 0
    mapped_courses: int = 0
    unmapped_pct: float = 0.0
    zero_training_pct: float = 0.0
    warnings: list[str] = field(default_factory=list)


class SkillMappingPipeline:
    """Sequential pipeline runner.

    Config file is optional; if present, recognised keys are
    ``threshold`` (float), ``top_k`` (int), and ``min_confidence`` (float).
    """

    def __init__(self, config_path: Optional[Path | str] = None) -> None:
        self.config: dict = {}
        if config_path:
            cfg_path = Path(config_path)
            if cfg_path.exists():
                with cfg_path.open("r", encoding="utf-8") as fh:
                    self.config = yaml.safe_load(fh) or {}
        self.threshold: float = float(self.config.get("threshold", 0.55))
        self.top_k: int = int(self.config.get("top_k", 5))

        # Filled per run for caller introspection.
        self.last_items: list[TrainingItem] = []
        self.last_mappings: list[SkillCompetencyMapping] = []
        self.last_coverage: list[CoverageCell] = []
        self.last_gaps: list[GapFinding] = []
        self.last_surplus: list[SurplusFinding] = []
        self.last_metrics: PipelineGateMetrics = PipelineGateMetrics()
        self.catalog_warnings: list[str] = []

    def run(
        self,
        library_path: Path | str,
        catalog_path: Path | str,
        family: str,
        out_dir: Path | str,
        llm_tiebreak: bool = True,
        min_confidence: float = 0.55,
    ) -> Path:
        # SM1
        items, warnings = load_catalog(catalog_path)
        self.catalog_warnings = warnings
        self.last_items = items

        # SM2
        library = load_library(library_path)

        # SM3 + SM4 + SM5 (per item)
        all_mappings: list[SkillCompetencyMapping] = []
        for item in items:
            bloom = classify(item, llm_tiebreak=llm_tiebreak)
            candidates = match(item, library, top_k=self.top_k, threshold=self.threshold)
            row_mappings = resolve(item, candidates, bloom, llm_tiebreak=llm_tiebreak)
            row_mappings = [m for m in row_mappings if m.confidence >= min_confidence]
            all_mappings.extend(row_mappings)
        self.last_mappings = all_mappings

        # GATE
        mapped_ids = {m.course_id for m in all_mappings}
        total = len(items)
        unmapped_pct = (100.0 * (total - len(mapped_ids)) / total) if total else 0.0

        # SM6
        coverage = aggregate(all_mappings, library)
        self.last_coverage = coverage

        by_comp: dict[str, int] = {}
        for c in coverage:
            by_comp[c.competency_id] = by_comp.get(c.competency_id, 0) + c.count
        zero_training_pct = (
            100.0 * sum(1 for v in by_comp.values() if v == 0) / len(by_comp)
            if by_comp
            else 0.0
        )

        self.last_metrics = PipelineGateMetrics(
            total_courses=total,
            mapped_courses=len(mapped_ids),
            unmapped_pct=round(unmapped_pct, 2),
            zero_training_pct=round(zero_training_pct, 2),
            warnings=list(warnings),
        )

        # SM7
        gaps = report_gaps(coverage, library)
        surplus = report_surplus(all_mappings, items, library)
        self.last_gaps = gaps
        self.last_surplus = surplus

        # SM8
        out_dir_path = Path(out_dir)
        out_dir_path.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        safe_family = family.replace("/", "_").replace(" ", "_")
        out_file = out_dir_path / f"skill_crosswalk_{safe_family}_{ts}.xlsx"
        return write_crosswalk(
            out_path=out_file,
            mappings=all_mappings,
            coverage=coverage,
            gaps=gaps,
            surplus=surplus,
            items=items,
            family=family,
        )
