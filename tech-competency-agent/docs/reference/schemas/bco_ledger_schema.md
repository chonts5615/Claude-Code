# BCO Ledger Schema

File: `BCO_Ledger.xlsx`
Writer: `src/deliverables/bco_ledger_writer.py :: write_bco_ledger`
Source schema: `src/schemas/bco_ledger.py :: BCOLedger`

The BCO Ledger is the system of record for **B**oundary classification,
**C**overage analysis, and **O**verlap detection across the technical library.

## Sheets

| Sheet | Source field | Row schema |
|-------|--------------|-----------|
| Boundary | `BCOLedger.boundary` | `BoundaryEntry` |
| Coverage | `BCOLedger.coverage` | `CoverageEntry` |
| Overlap | `BCOLedger.overlap` | `OverlapEntry` |

## Sheet: Boundary

| Column | Type | Notes |
|--------|------|-------|
| `competency_id` | str | Library ID |
| `competency_name` | str | 3-6 words |
| `classification` | enum | `V_AND_B` \| `COMMON` \| `TECHNICAL` \| `MIXED` |
| `confidence` | float | 0.0-1.0 (rounded to 4 decimals) |
| `rationale` | str | Free-text justification |

## Sheet: Coverage

| Column | Type | Notes |
|--------|------|-------|
| `job_id` | str | Stable job identifier |
| `job_title` | str | Cargill job title |
| `family` | str | Family name |
| `technical_ef_count` | int | Total essential functions for the job |
| `technical_ef_covered` | int | EFs hit by at least one technical competency |
| `coverage_rate` | float | `covered / count`, 0.0-1.0 |
| `uncovered_ef_ids` | str | Pipe-delimited list of uncovered EF IDs |
| `meets_90_threshold` | bool | True when `coverage_rate >= 0.90` |

The 90% threshold is a hard gate — runs below 90% coverage cannot advance
past the deliverable-generation stage.

## Sheet: Overlap

| Column | Type | Notes |
|--------|------|-------|
| `competency_id_a` | str | Library ID (lexicographically first) |
| `competency_id_b` | str | Library ID (lexicographically second) |
| `similarity_score` | float | 0.0-1.0 (rounded to 4 decimals) |
| `severity` | enum | `NONE` \| `MINOR` \| `MATERIAL` |
| `resolution` | str | Free text — how the overlap was resolved (or empty if open) |

`MATERIAL` overlaps must be resolved (merge, differentiate, or rename)
before FINAL stage.

## Branding

Leaf Green header fill, White Green alternating rows, Arial body font,
freeze pane at `B2` on each sheet, header row height 26.
