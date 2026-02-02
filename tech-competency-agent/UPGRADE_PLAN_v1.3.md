# Technical Competency Agent System - v1.3 Upgrade Plan

## Executive Summary

This document outlines the upgrade path from v1.0 (current) to v1.3 (enterprise-grade with multi-specialization support, tiered sources, and functional model integration).

**Estimated Effort**: 3-4 weeks
**Impact**: High - adds enterprise features while maintaining backward compatibility
**Risk**: Low - incremental changes with extensive testing

---

## Current State vs Target State

### Current v1.0 Capabilities
✅ Single job file processing (Excel/CSV)
✅ Basic competency mapping with hybrid scoring
✅ Quality gates and overlap detection
✅ Knowledge base for reference documents
✅ LangGraph workflow orchestration
✅ Complete CLI interface
✅ File analysis and validation

### Target v1.3 Enhancements
🎯 Multi-specialization input handling (ZIP/multi-tab/column-based)
🎯 Tiered source priority system (Tier 0-3)
🎯 Field-level extraction confidence scoring
🎯 Formal source registry with full provenance
🎯 Chunk-level evidence tracking (resolvable refs)
🎯 Functional competency model ingestion (Tier-0)
🎯 Functional model coverage & gap analysis
🎯 Specialization-aware output generation

---

## Implementation Phases

### Phase 1: Foundation (Week 1-2) - CRITICAL

#### 1.1 Source Registry System

**New Schema**: `src/schemas/source_registry.py`

```python
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime
from pathlib import Path

class SourceMetadata(BaseModel):
    """Individual source metadata."""
    source_id: str = Field(..., pattern="^SRC-[0-9]{4}$")
    source_type: Literal["XLSX", "DOCX", "PPTX", "PDF", "CSV", "TXT", "WEB"]
    origin: Literal["JOB_ESSENTIAL", "FUNCTIONAL_MODEL", "INTERNAL_TECH_SOURCE", "EXTERNAL_BENCHMARK"]
    source_title: str
    file_path_or_locator: str
    extraction_method: Literal["TEXT_ONLY", "VISUAL_RETRIEVAL", "NATIVE_STRUCTURE"]
    extraction_confidence: Literal["HIGH", "MEDIUM", "LOW"]
    retrieval_date_utc: str
    notes: Optional[str] = None

class SourceRegistry(BaseModel):
    """Registry of all input sources."""
    registry_version: str = "1.0"
    created_utc: str
    sources: List[SourceMetadata]

    def get_source(self, source_id: str) -> Optional[SourceMetadata]:
        """Retrieve source by ID."""
        return next((s for s in self.sources if s.source_id == source_id), None)

    def get_sources_by_origin(self, origin: str) -> List[SourceMetadata]:
        """Get all sources of a specific origin."""
        return [s for s in self.sources if s.origin == origin]
```

**New Utility**: `src/utils/source_registry_manager.py`

```python
from pathlib import Path
from typing import List, Dict
from src.schemas.source_registry import SourceRegistry, SourceMetadata
from datetime import datetime

class SourceRegistryManager:
    """Manages source registry lifecycle."""

    def __init__(self):
        self.registry: Optional[SourceRegistry] = None
        self.source_counter = 0

    def create_registry(self) -> SourceRegistry:
        """Initialize new registry."""
        self.registry = SourceRegistry(
            created_utc=datetime.utcnow().isoformat(),
            sources=[]
        )
        return self.registry

    def register_source(
        self,
        file_path: Path,
        source_type: str,
        origin: str,
        extraction_method: str = "NATIVE_STRUCTURE",
        extraction_confidence: str = "HIGH",
        notes: str = None
    ) -> str:
        """Register a new source and return source_id."""
        if not self.registry:
            self.create_registry()

        self.source_counter += 1
        source_id = f"SRC-{self.source_counter:04d}"

        source = SourceMetadata(
            source_id=source_id,
            source_type=source_type,
            origin=origin,
            source_title=file_path.name,
            file_path_or_locator=str(file_path),
            extraction_method=extraction_method,
            extraction_confidence=extraction_confidence,
            retrieval_date_utc=datetime.utcnow().isoformat(),
            notes=notes
        )

        self.registry.sources.append(source)
        return source_id

    def save_registry(self, output_path: Path):
        """Save registry to JSON."""
        if not self.registry:
            raise ValueError("No registry to save")

        with open(output_path, 'w') as f:
            f.write(self.registry.json(indent=2))

    def load_registry(self, registry_path: Path) -> SourceRegistry:
        """Load existing registry."""
        with open(registry_path, 'r') as f:
            self.registry = SourceRegistry.parse_raw(f.read())
        return self.registry
```

#### 1.2 Chunk-Level Evidence System

**New Schema**: `src/schemas/evidence.py`

```python
from typing import Optional
from pydantic import BaseModel, Field

class EvidenceChunk(BaseModel):
    """Individual evidence chunk with resolvable reference."""
    chunk_id: str = Field(..., pattern="^CH-[0-9]{4}-[0-9]{4}$")
    source_id: str = Field(..., pattern="^SRC-[0-9]{4}$")
    location: str  # "page 5", "slide 12", "row 45", "section 2.3"
    text_excerpt: str = Field(..., min_length=10, max_length=2000)
    extraction_confidence: str = Field(..., pattern="^(HIGH|MEDIUM|LOW)$")
    metadata: dict = Field(default_factory=dict)

class EvidenceReference(BaseModel):
    """Resolvable evidence reference."""
    evidence_ref: str = Field(..., pattern="^SRC-[0-9]{4}:CH-[0-9]{4}-[0-9]{4}$")

    @property
    def source_id(self) -> str:
        return self.evidence_ref.split(':')[0]

    @property
    def chunk_id(self) -> str:
        return self.evidence_ref.split(':')[1]

class ChunkIndex(BaseModel):
    """Index of all evidence chunks across all sources."""
    index_version: str = "1.0"
    total_chunks: int
    chunks: List[EvidenceChunk]

    def resolve_reference(self, evidence_ref: str) -> Optional[EvidenceChunk]:
        """Resolve evidence_ref to chunk."""
        chunk_id = evidence_ref.split(':')[1] if ':' in evidence_ref else evidence_ref
        return next((c for c in self.chunks if c.chunk_id == chunk_id), None)
```

**New Utility**: `src/utils/chunk_manager.py`

```python
from pathlib import Path
from typing import List
from src.schemas.evidence import EvidenceChunk, ChunkIndex

class ChunkManager:
    """Manages evidence chunks and indexing."""

    def __init__(self):
        self.chunks: List[EvidenceChunk] = []
        self.chunk_counter_by_source = {}

    def create_chunk(
        self,
        source_id: str,
        location: str,
        text_excerpt: str,
        extraction_confidence: str = "HIGH",
        metadata: dict = None
    ) -> str:
        """Create and register a new chunk."""
        # Increment counter for this source
        if source_id not in self.chunk_counter_by_source:
            self.chunk_counter_by_source[source_id] = 0

        self.chunk_counter_by_source[source_id] += 1

        # Extract numeric part from SRC-0001
        source_num = source_id.split('-')[1]
        chunk_num = self.chunk_counter_by_source[source_id]
        chunk_id = f"CH-{source_num}-{chunk_num:04d}"

        chunk = EvidenceChunk(
            chunk_id=chunk_id,
            source_id=source_id,
            location=location,
            text_excerpt=text_excerpt,
            extraction_confidence=extraction_confidence,
            metadata=metadata or {}
        )

        self.chunks.append(chunk)
        return chunk_id

    def create_evidence_ref(self, source_id: str, chunk_id: str) -> str:
        """Create resolvable evidence reference."""
        return f"{source_id}:{chunk_id}"

    def build_index(self) -> ChunkIndex:
        """Build complete chunk index."""
        return ChunkIndex(
            total_chunks=len(self.chunks),
            chunks=self.chunks
        )

    def save_index_jsonl(self, output_path: Path):
        """Save chunks as JSONL for easy streaming."""
        with open(output_path, 'w') as f:
            for chunk in self.chunks:
                f.write(chunk.json() + '\n')

    def load_index_jsonl(self, index_path: Path):
        """Load chunks from JSONL."""
        self.chunks = []
        with open(index_path, 'r') as f:
            for line in f:
                chunk = EvidenceChunk.parse_raw(line)
                self.chunks.append(chunk)
```

#### 1.3 Tiered Source System

**Updated Schema**: `src/schemas/competency.py` (additions)

```python
# Add to existing competency.py

class SourceTier(str, Enum):
    """Competency source tier for priority weighting."""
    TIER_0_FUNCTIONAL_MODEL = "TIER_0_FUNCTIONAL_MODEL"
    TIER_1_INTERNAL_TECH = "TIER_1_INTERNAL_TECH"
    TIER_2_EXTERNAL_BENCHMARK = "TIER_2_EXTERNAL_BENCHMARK"
    TIER_3_GENERATED_PROVISIONAL = "TIER_3_GENERATED_PROVISIONAL"

class ExtractionConfidence(BaseModel):
    """Field-level extraction confidence."""
    name_confidence: Literal["HIGH", "MEDIUM", "LOW"]
    definition_confidence: Literal["HIGH", "MEDIUM", "LOW"]
    indicators_confidence: Literal["HIGH", "MEDIUM", "LOW"]
    overall: Literal["HIGH", "MEDIUM", "LOW"]

# Update CompetencyLibraryEntry to include:
class CompetencyLibraryEntry(BaseModel):
    """Enhanced competency library entry with tiering."""
    competency_id: str
    name: str
    definition: str
    indicators: List[str] = Field(default_factory=list)

    # New fields for v1.3
    source_tier: SourceTier
    source_priority_weight: float = Field(ge=0.0, le=1.0)
    extraction_confidence: Optional[ExtractionConfidence] = None
    evidence_refs: List[str] = Field(default_factory=list)  # source_id:chunk_id format

    proficiency_levels: List[ProficiencyLevel] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    source_evidence: List[SourceEvidence]  # Legacy, will migrate to evidence_refs
```

---

### Phase 2: Multi-Specialization Support (Week 2-3)

#### 2.1 Input Discovery Agent (S0)

**New Agent**: `src/agents/input_discovery.py`

```python
"""S0: Input Discovery Agent - Detects and manifests specialization structure."""

from pathlib import Path
from typing import List, Dict, Optional
import zipfile
import openpyxl
from pydantic import BaseModel

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState
from src.utils.source_registry_manager import SourceRegistryManager

class SpecializationUnit(BaseModel):
    """A detected specialization unit."""
    unit_id: str
    representation_mode: Literal["TAB", "FILE", "COLUMN"]
    specialization_name: str
    specialization_id: str
    locator: Dict
    detected_layout: Dict
    parse_confidence: Literal["HIGH", "MEDIUM", "LOW"]
    warnings: List[str] = Field(default_factory=list)

class JobsInputManifest(BaseModel):
    """Manifest of detected job input structure."""
    input_type: Literal["XLSX", "ZIP"]
    specialization_units: List[SpecializationUnit]
    total_units: int

class InputDiscoveryAgent(BaseAgent):
    """Discovers input structure and creates extraction manifest."""

    def __init__(self, agent_id: str, step_name: str):
        super().__init__(agent_id, step_name)
        self.source_registry_mgr = SourceRegistryManager()

    def execute(self, state: RunState) -> RunState:
        """
        Discover input structure.

        Creates:
        - source_registry_v1.json
        - jobs_input_manifest_v3.json
        - jobs_input_manifest_report_v3.json
        """
        state.current_step = self.agent_id

        jobs_input = state.inputs.jobs_file

        # Create source registry
        self.source_registry_mgr.create_registry()

        # Detect input type
        if jobs_input.suffix.lower() == '.zip':
            manifest = self._discover_zip_structure(jobs_input)
        elif jobs_input.suffix.lower() in ['.xlsx', '.xls']:
            manifest = self._discover_xlsx_structure(jobs_input)
        else:
            raise ValueError(f"Unsupported input type: {jobs_input.suffix}")

        # Save artifacts
        output_dir = Path(f"data/output/{state.run_id}")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save source registry
        registry_path = output_dir / "source_registry_v1.json"
        self.source_registry_mgr.save_registry(registry_path)
        state.artifacts.source_registry = registry_path

        # Save manifest
        manifest_path = output_dir / "jobs_input_manifest_v3.json"
        with open(manifest_path, 'w') as f:
            f.write(manifest.json(indent=2))
        state.artifacts.jobs_input_manifest = manifest_path

        # Create report
        report = self._create_discovery_report(manifest)
        report_path = output_dir / "jobs_input_manifest_report_v3.json"
        with open(report_path, 'w') as f:
            f.write(report.json(indent=2))

        return state

    def _discover_xlsx_structure(self, file_path: Path) -> JobsInputManifest:
        """Discover structure of XLSX file."""
        # Register source
        source_id = self.source_registry_mgr.register_source(
            file_path,
            source_type="XLSX",
            origin="JOB_ESSENTIAL",
            extraction_method="NATIVE_STRUCTURE"
        )

        wb = openpyxl.load_workbook(file_path, data_only=True)
        units = []

        # Check if multiple sheets = TAB mode
        if len(wb.sheetnames) > 1:
            for idx, sheet_name in enumerate(wb.sheetnames):
                unit = self._analyze_sheet(wb[sheet_name], source_id, sheet_name, idx)
                units.append(unit)
        else:
            # Single sheet - check for COLUMN mode
            sheet = wb.active
            column_mode_unit = self._detect_column_specialization(sheet, source_id)
            if column_mode_unit:
                units.extend(column_mode_unit)
            else:
                # No specialization detected
                units.append(self._analyze_sheet(sheet, source_id, sheet.title, 0))

        wb.close()

        return JobsInputManifest(
            input_type="XLSX",
            specialization_units=units,
            total_units=len(units)
        )

    def _discover_zip_structure(self, zip_path: Path) -> JobsInputManifest:
        """Discover structure of ZIP file."""
        # TODO: Implement ZIP discovery
        # - Extract to temp
        # - Enumerate XLSX/CSV files
        # - Each file = FILE mode specialization
        # - Register each as separate source
        pass

    def _analyze_sheet(
        self,
        sheet,
        source_id: str,
        sheet_name: str,
        unit_idx: int
    ) -> SpecializationUnit:
        """Analyze a sheet for structure."""
        # Detect header row
        headers = []
        for cell in sheet[1]:
            if cell.value:
                headers.append(str(cell.value).strip())

        # Detect column purposes
        column_mapping = {}
        for col_name in headers:
            col_lower = col_name.lower()
            if 'title' in col_lower or 'job' in col_lower:
                column_mapping['job_title'] = col_name
            elif 'summary' in col_lower or 'description' in col_lower:
                column_mapping['summary'] = col_name
            elif 'responsib' in col_lower or 'duties' in col_lower:
                column_mapping['responsibilities'] = col_name

        # Determine confidence
        confidence = "HIGH" if len(column_mapping) >= 3 else "MEDIUM" if len(column_mapping) >= 2 else "LOW"

        return SpecializationUnit(
            unit_id=f"UNIT-{unit_idx:04d}",
            representation_mode="TAB",
            specialization_name=sheet_name,
            specialization_id=f"SPEC-{unit_idx:04d}",
            locator={
                "source_id": source_id,
                "sheet_name": sheet_name,
                "range_hint": f"A1:{sheet.max_column}{sheet.max_row}"
            },
            detected_layout={
                "header_row_index": 0,
                "columns": column_mapping
            },
            parse_confidence=confidence,
            warnings=[] if confidence == "HIGH" else [f"Low confidence: only detected {len(column_mapping)} columns"]
        )

    def _detect_column_specialization(self, sheet, source_id: str) -> Optional[List[SpecializationUnit]]:
        """Detect if sheet has column-based specializations."""
        # Look for "Specialization" or "Job Family" column
        # Group rows by that column value
        # Create one unit per unique value
        # TODO: Implement column mode detection
        return None

    def get_system_prompt(self) -> str:
        return """You are the Input Discovery Agent.

Your task is to deterministically interpret variable job input structures.

Detect:
- TAB mode: specialization per sheet
- FILE mode: specialization per file in ZIP
- COLUMN mode: specialization per column value grouping

Output stable source_ids and specialization units with confidence scores."""
```

#### 2.2 Functional Model Ingestion Agent (S2A)

**New Agent**: `src/agents/functional_model_ingestion.py`

```python
"""S2A: Functional Model Ingestion Agent - Ingests functional competency model as Tier-0."""

from pathlib import Path
from typing import List
import anthropic

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState
from src.schemas.competency import ExtractionConfidence, SourceTier
from src.utils.chunk_manager import ChunkManager
from src.utils.source_registry_manager import SourceRegistryManager

class FunctionalModelIngestionAgent(BaseAgent):
    """Ingests functional competency model as critical Tier-0 source."""

    def __init__(self, agent_id: str, step_name: str):
        super().__init__(agent_id, step_name)
        self.client = anthropic.Anthropic()
        self.chunk_mgr = ChunkManager()
        self.source_registry_mgr = SourceRegistryManager()

    def execute(self, state: RunState) -> RunState:
        """
        Ingest functional model.

        Creates:
        - functional_competency_model_raw_v3.json
        - functional_model_ingestion_report_v3.json
        - source_chunks_functional_model_v2.jsonl
        """
        state.current_step = self.agent_id

        # Check if functional model files provided
        if not state.inputs.functional_model_files:
            # Optional step - skip if no files
            return state

        # Load source registry
        self.source_registry_mgr.load_registry(state.artifacts.source_registry)

        competencies = []

        for model_file in state.inputs.functional_model_files:
            # Register source
            source_id = self.source_registry_mgr.register_source(
                model_file,
                source_type=self._detect_file_type(model_file),
                origin="FUNCTIONAL_MODEL",
                extraction_method=self._select_extraction_method(model_file)
            )

            # Extract competencies with chunking
            file_competencies = self._extract_from_file(model_file, source_id)
            competencies.extend(file_competencies)

        # Save artifacts
        output_dir = Path(f"data/output/{state.run_id}")

        # Update source registry
        self.source_registry_mgr.save_registry(state.artifacts.source_registry)

        # Save functional model competencies
        functional_model = {
            "competencies": [c.dict() for c in competencies],
            "total_competencies": len(competencies),
            "source_tier": "TIER_0_FUNCTIONAL_MODEL"
        }

        fm_path = output_dir / "functional_competency_model_raw_v3.json"
        with open(fm_path, 'w') as f:
            import json
            json.dump(functional_model, f, indent=2)
        state.artifacts.functional_model_raw = fm_path

        # Save chunks
        chunks_path = output_dir / "source_chunks_functional_model_v2.jsonl"
        self.chunk_mgr.save_index_jsonl(chunks_path)

        # Create ingestion report
        report = self._create_ingestion_report(competencies)
        report_path = output_dir / "functional_model_ingestion_report_v3.json"
        with open(report_path, 'w') as f:
            f.write(report.json(indent=2))

        return state

    def _extract_from_file(self, file_path: Path, source_id: str) -> List[CompetencyLibraryEntry]:
        """Extract competencies from file with confidence scoring."""
        # Implementation depends on file type
        # For PDF/PPTX: use Claude vision for better extraction
        # For XLSX/DOCX: use structured parsing

        # TODO: Implement extraction with field-level confidence
        # Return competencies with evidence_refs to chunks
        pass

    def get_system_prompt(self) -> str:
        return """You are the Functional Model Ingestion Agent.

Ingest functional competency models (PDF/PPTX/DOCX/XLSX) as Tier-0 critical sources.

For each competency:
- Extract name, definition, indicators
- Assign field-level confidence (HIGH/MEDIUM/LOW)
- Create evidence chunks with location references
- Link competency to chunk via evidence_refs

Flag low-confidence extraction for SME review."""
```

---

### Phase 3: Enhanced Mapping & Coverage (Week 3)

#### 3.1 Update Competency Mapping Agent

Enhance existing `src/agents/competency_mapping.py` to:
- Prioritize Tier-0 sources
- Weight by extraction confidence
- Store evidence_refs in mappings

#### 3.2 Add Functional Model Coverage Agent (S2D)

**New Agent**: `src/agents/functional_model_coverage.py`

```python
"""S2D: Functional Model Coverage Agent - Proves model incorporation."""

from pathlib import Path
from typing import Dict, List
from pydantic import BaseModel

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState

class JobVariantCoverage(BaseModel):
    """Coverage metrics for one job variant."""
    job_variant_id: str
    tier0_mapping_rate: float
    responsibilities_uncovered: List[str]
    functional_model_competencies_unused: List[str]
    failure_cause_category: str
    notes: str

class FunctionalModelCoverageReport(BaseModel):
    """Overall functional model coverage report."""
    job_variant_coverage: List[JobVariantCoverage]
    overall_summary: Dict
    requires_SME_validation: bool

class FunctionalModelCoverageAgent(BaseAgent):
    """Quantifies functional model incorporation."""

    def execute(self, state: RunState) -> RunState:
        """
        Analyze functional model coverage.

        Creates:
        - functional_model_coverage_report_v2.json
        """
        state.current_step = self.agent_id

        # Load mapping and functional model
        # Calculate tier0_mapping_rate per job variant
        # Identify gaps
        # Classify failure causes

        # Save report
        output_dir = Path(f"data/output/{state.run_id}")
        report_path = output_dir / "functional_model_coverage_report_v2.json"

        # Quality gate: enforce minimum tier0_mapping_rate
        # If failed, flag for SME review and enhanced benchmarking

        return state

    def get_system_prompt(self) -> str:
        return """You are the Functional Model Coverage Agent.

Prove incorporation of the functional competency model by:
- Computing tier0_mapping_rate per job variant
- Identifying uncovered responsibilities
- Finding unused functional model competencies
- Classifying failure causes

Quality gate: tier0_mapping_rate >= 60% (configurable)"""
```

---

### Phase 4: Configuration & Integration (Week 4)

#### 4.1 Update Configuration Files

**config/workflow_config.yaml** additions:

```yaml
# Add to existing config

# Specialization handling
specialization_handling:
  mode: PER_SPECIALIZATION  # or CONSOLIDATED
  representation_modes_allowed: [TAB, FILE, COLUMN]
  output_strategy: ONE_FILE_PER_SPECIALIZATION  # or ONE_WORKBOOK_MULTI_SHEETS

# Tiered source weights
source_tier_weights:
  TIER_0_FUNCTIONAL_MODEL: 1.0
  TIER_1_INTERNAL_TECH: 0.8
  TIER_2_EXTERNAL_BENCHMARK: 0.6
  TIER_3_GENERATED_PROVISIONAL: 0.4

# Extraction confidence impact
extraction_confidence_multipliers:
  HIGH: 1.0
  MEDIUM: 0.7
  LOW: 0.4

# Functional model thresholds
functional_model:
  min_tier0_mapping_rate: 0.60
  require_coverage_report: true
  enhanced_benchmarking_for_gaps: true
```

**config/thresholds.yaml** additions:

```yaml
# Add to existing thresholds

# Specialization
min_responsibilities_per_variant: 5

# Functional model coverage
min_tier0_mapping_rate_if_model_present: 0.60

# Evidence requirements
min_evidence_chunks_per_competency: 1
min_evidence_chunks_per_mapping: 1
```

#### 4.2 Update LangGraph Workflow

Modify `src/orchestrator/graph.py` to include new steps:

```python
# Add new agents to workflow

from src.agents.input_discovery import InputDiscoveryAgent
from src.agents.source_normalization import SourceNormalizationAgent
from src.agents.functional_model_ingestion import FunctionalModelIngestionAgent
from src.agents.functional_model_coverage import FunctionalModelCoverageAgent

# Update _build_graph():

# Add S0
workflow.add_node("s0_input_discovery", agents["input_discovery"].execute)
workflow.add_node("s0_gate", self._gate_s0)

# Add S0.5
workflow.add_node("s0_5_source_normalization", agents["source_normalization"].execute)

# Update S1 to use manifest

# Add S2A (conditional)
workflow.add_node("s2a_functional_model", agents["functional_model_ingestion"].execute)
workflow.add_conditional_edges(
    "s2a_check",
    lambda state: "ingest" if state.inputs.functional_model_files else "skip",
    {"ingest": "s2a_functional_model", "skip": "s2b_unify_library"}
)

# Add S2D (conditional)
workflow.add_node("s2d_coverage", agents["functional_model_coverage"].execute)
workflow.add_node("s2d_gate", self._gate_s2d)
```

---

## Testing Strategy

### Unit Tests
- Source registry creation and lookup
- Chunk manager indexing and resolution
- Tiered source priority calculation
- Extraction confidence weighting

### Integration Tests
- Multi-tab XLSX processing
- ZIP file unpacking
- Functional model ingestion (PDF/PPTX)
- Coverage report generation
- Evidence ref resolution

### End-to-End Tests
- Full workflow with functional model
- Per-specialization output generation
- Coverage gate enforcement

---

## Migration Path for Existing Users

### Backward Compatibility

v1.3 maintains backward compatibility:
- Single-file XLSX input still supported
- Functional model is optional
- Default behavior unchanged if not using new features

### Opt-in Enhancements

Users can adopt v1.3 features incrementally:
1. Start with source registry (improves traceability)
2. Add chunk-level evidence (improves audit)
3. Enable multi-specialization (handles complex inputs)
4. Add functional model ingestion (proves incorporation)

---

## Success Criteria

### Phase 1 Complete When:
✅ Source registry working
✅ Chunk index resolvable
✅ Tiered source system functional
✅ Tests passing

### Phase 2 Complete When:
✅ Multi-tab XLSX supported
✅ ZIP input supported
✅ Functional model ingestion working
✅ Evidence refs traceable

### Phase 3 Complete When:
✅ Coverage report generated
✅ Quality gates enforcing thresholds
✅ Gap analysis accurate

### Phase 4 Complete When:
✅ All features integrated
✅ Documentation updated
✅ Migration guide complete
✅ Production ready

---

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Breaking existing workflows | High | Maintain backward compatibility |
| Complex specialization detection | Medium | Confidence scoring + SME review flags |
| PDF/PPTX extraction quality | High | Field-level confidence + downgrade low quality |
| Performance with many specializations | Medium | Parallel processing + pagination |

---

## Resource Requirements

**Development**: 1 developer, 3-4 weeks
**Testing**: 1 week concurrent
**Documentation**: Ongoing
**Infrastructure**: No additional (uses existing stack)

---

## Next Steps

1. **Review this plan** with stakeholders
2. **Prioritize phases** based on business needs
3. **Set up feature branch**: `feature/v1.3-upgrade`
4. **Begin Phase 1** with source registry
5. **Iterate with testing** after each phase

---

## Questions for Decision

1. **Priority**: Should all phases be implemented or just Phase 1-2?
2. **Timeline**: Is 4-week timeline acceptable or needs acceleration?
3. **Backward Compatibility**: Any existing workflows that need special handling?
4. **Functional Model**: What formats are most critical (PDF, PPTX, DOCX, XLSX)?
5. **Specialization Modes**: Which modes are highest priority (TAB, FILE, COLUMN)?

---

**Status**: Draft for Review
**Version**: 1.0
**Date**: January 18, 2026
**Author**: Claude AI
