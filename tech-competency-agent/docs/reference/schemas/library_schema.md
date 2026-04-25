# Library Master Schema (23 columns)

Source of truth: `src/schemas/library.py :: LIBRARY_COLUMNS`.

Sheet name: **Library Master**. One row per `TechnicalCompetency`.

| # | Field | Type | Validation | Example |
|---|-------|------|------------|---------|
| 1 | `competency_id` | str | Stable ID, family prefix recommended (`FIN-014`) | `FIN-014` |
| 2 | `name` | str | 3-6 words | `Financial Statement Consolidation` |
| 3 | `family` | str | One of the 15 Cargill families | `Finance` |
| 4 | `boundary_class` | enum | `V_AND_B` \| `COMMON` \| `TECHNICAL` \| `MIXED` | `TECHNICAL` |
| 5 | `definition` | str | 15-25 words, exactly one sentence ending with `.` | `Consolidates legal-entity financials into group statements aligned to IFRS, including intercompany elimination and currency translation steps.` |
| 6 | `why_it_matters` | str | Free text, 1-3 sentences | `Required for monthly close and external reporting.` |
| 7 | `L1_description` | str | Single sentence describing L1 | `Performs straightforward consolidation steps with supervision.` |
| 8 | `L1_indicators` | str | Pipe-delimited, exactly 3 items | `Maps trial balances to consolidation chart \| Runs FX translation under guidance \| Flags variances for review` |
| 9 | `L2_description` | str | Single sentence describing L2 | `Independently consolidates a region with moderate complexity.` |
| 10 | `L2_indicators` | str | Pipe-delimited, exactly 3 items | (3 indicator strings, pipe-delimited) |
| 11 | `L3_description` | str | Single sentence describing L3 | `Leads consolidation for a multi-region segment.` |
| 12 | `L3_indicators` | str | Pipe-delimited, exactly 3 items | (3 indicator strings, pipe-delimited) |
| 13 | `L4_description` | str | Single sentence describing L4 | `Owns enterprise consolidation policy and external audit response.` |
| 14 | `L4_indicators` | str | Pipe-delimited, exactly 3 items | (3 indicator strings, pipe-delimited) |
| 15 | `applied_tools` | str | Pipe-delimited tools/methods/tech | `OneStream \| SAP S/4HANA \| Excel` |
| 16 | `applied_standards` | str | Pipe-delimited frameworks/standards | `IFRS \| US GAAP` |
| 17 | `applied_outputs` | str | Pipe-delimited typical outputs | `Consolidated balance sheet \| FX translation memo` |
| 18 | `criticality_score` | float | 0.0-1.0, weighted (0.40 Cov / 0.30 Crit / 0.20 Dist / 0.10 Asses) | `0.7825` |
| 19 | `integrity_tag` | enum | `CONFIRMED` \| `CORRECTED` \| `UNVERIFIABLE` \| `FLAGGED` | `CONFIRMED` |
| 20 | `source_refs` | str | Pipe-delimited source IDs | `SRC-FIN-001 \| SRC-FIN-014` |
| 21 | `rosetta_aliases` | str | Pipe-delimited cross-family aliases | `Financial Close (Operations) \| Group Reporting (Strategy)` |
| 22 | `first_published_run` | str | Run ID of first publish | `Finance_R1_20260201_a1b2c3d` |
| 23 | `last_modified_run` | str | Run ID of latest edit | `Finance_R2_20260415_d4e5f6a` |

## Workbook conventions

- Sheet name: **Library Master**
- Header row styled with Cargill Leaf Green fill (`#00843D`), bold white text
- Even body rows shaded White Green (`#F5F9ED`)
- Body font Arial 10pt with wrap and top vertical alignment
- Freeze pane at `C2` (header row + first 2 columns locked)
- Column widths: `name`=20, `definition`=60, all `*_indicators`=80,
  others tuned to content
