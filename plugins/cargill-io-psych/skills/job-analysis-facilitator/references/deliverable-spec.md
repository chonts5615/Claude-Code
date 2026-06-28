# Deliverable Specification — Analysis of Work

Exact structure for the two outputs. Apply `cargill-branding` (Leaf Green
`#00843D` headers, White Green `#F5F9ED` zebra fill, Arial body, Georgia titles).

## Excel workbook — `analysis_of_work_<role>.xlsx`

Four tabs, frozen header rows, auto-filters on data tabs.

### Tab 1 — `Task Inventory`
| Column | Notes |
|---|---|
| Task ID | `T01`, `T02`, … |
| Duty Area | One of the 4–8 clusters |
| Task Statement | Verb + object + context + purpose |
| Frequency (1–5) | |
| Importance (1–5) | |
| Difficulty (1–5) | |
| Criticality | `=(Importance*Frequency)+Difficulty` |
| Essential? | `=IF(Importance>=4,"ESSENTIAL","")` |
| SME n / Agreement | Raters and agreement note; blank → UNVALIDATED |

Conditional format Criticality (3-color scale) and Essential (Leaf Green fill).

### Tab 2 — `KSAO Inventory`
| Column | Notes |
|---|---|
| KSAO ID | `K01`, `S01`, `A01`, `O01` (prefix encodes class) |
| Class | Knowledge / Skill / Ability / Other |
| KSAO Statement | Observable, verb-led |
| Required at Entry? | YES / Developed on job |
| Credential/License? | Flag bona-fide requirements |

### Tab 3 — `Task×KSAO Matrix`
Rows = KSAOs, Columns = Task IDs. Cell = linkage strength (blank/1/2/3). Add a
right-hand `Links` count per KSAO and a bottom `Links` count per task.
Conditional-format any KSAO row summing to 0 (orphan KSAO → red) and any task
column summing to 0 among essential tasks (uncovered essential task → amber).

### Tab 4 — `Summary`
- Essential functions list (filtered from Tab 1).
- Top KSAOs by link count and at-entry status.
- Method, SME roster, agreement summary, validation status.
- Orphan report (both directions).

## Word report — `analysis_of_work_<role>.docx`

1. **Title & purpose** — role, level, purpose, date, analyst.
2. **Method** — task+KSAO hybrid, source material, SME participation,
   rating scales used.
3. **Task inventory** — by duty area, with criticality.
4. **Essential functions** — the tasks clearing the importance threshold.
5. **KSAO requirements at entry** — by class, with credential flags.
6. **Content-validity statement** — explicit narrative that the required KSAOs
   are linked to representative essential tasks (cite Uniform Guidelines §14C and
   SIOP Principles 5th ed.).
7. **Validation status** — SME agreement or the UNVALIDATED label.
8. **Disclaimer** — the standard block from SKILL.md.

## Hand-off note

End both artifacts with a short "Feeds" line: this analysis is the input to
competency modeling (TCB v3.1), selection design (`selection-method-advisor`),
assessment-center dimensions (`assessment-center-designer`), and career levels
(`career-architecture-builder`).
