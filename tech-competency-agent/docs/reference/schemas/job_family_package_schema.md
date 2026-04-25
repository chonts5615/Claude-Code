# Job Family Package Schema

File: `{family}_Job_Family_Package.xlsx`
Writer: `src/deliverables/job_family_package.py :: write_family_package`

## Sheets

| Sheet | Purpose |
|-------|---------|
| Overview | Family-level metadata, run id, counts |
| Jobs | One row per job in scope |
| Competencies | One row per technical competency (subset of library cols) |
| EF Coverage Map | Job x competency matrix marking primary/secondary/supporting |

## Sheet: Overview

Two-column key/value layout. Freeze `A2`.

| Field | Value |
|-------|-------|
| Family | (string) |
| Run ID | (string) |
| Job count | (int) |
| Competency count | (int) |
| Schema version | `v3.1` |

## Sheet: Jobs

Freeze `C2`. One row per job dict supplied by the caller.

| Column | Type | Notes |
|--------|------|-------|
| `job_id` | str | Stable identifier |
| `job_title` | str | Cargill job title |
| `job_family` | str | Family name (matches package) |
| `sub_family` | str | Optional sub-grouping |
| `level` | str | Cargill job level (e.g. M3, P4) |
| `ef_count` | int | Number of essential functions parsed |
| `source_doc` | str | Filename or path of source job doc |

## Sheet: Competencies

Freeze `C2`. One row per `TechnicalCompetency`.

| Column | Type | Notes |
|--------|------|-------|
| `competency_id` | str | Library ID |
| `name` | str | 3-6 words |
| `boundary_class` | enum | `V_AND_B` \| `COMMON` \| `TECHNICAL` \| `MIXED` |
| `definition` | str | 15-25 words, one sentence |
| `why_it_matters` | str | 1-3 sentences |
| `criticality_score` | float | Weighted CTIC score |
| `integrity_tag` | enum | `CONFIRMED` \| `CORRECTED` \| `UNVERIFIABLE` \| `FLAGGED` |

## Sheet: EF Coverage Map

Matrix view: rows are competencies, columns are jobs.

- First two columns: `competency_id`, `name`
- Remaining columns: one per `job_id`
- Cell value: contribution code from `ResponsibilityTrace` —
  `PRIMARY`, `SECONDARY`, `SUPPORTING`, or empty
- Freeze `C2`

## Branding

All sheets use the same Cargill brand styling as the Library Master:
Leaf Green header fill, White Green alternating body rows, Arial body font,
header row height 26.
