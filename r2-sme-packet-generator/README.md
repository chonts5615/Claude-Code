# Round 2 SME Review Packet Generator

Generates Cargill-branded **Round 2 SME Feedback Focus Group Packets** (DOCX)
for the Technical Competency Development program. One JSON data file per
sub-family in, one fully formatted Word packet out — the structure, status
taxonomy, coverage codes, and visual system are locked (see `CLAUDE.md`); only
the content changes.

## Layout

```
r2-sme-packet-generator/
├── generator.py   # JSON → DOCX renderer (python-docx)
├── CLAUDE.md      # the locked packet format / contract
├── data/          # one JSON per sub-family (the editable input)
│   ├── benefits_and_leave_benefits_administration.json
│   └── lnd_strategy_design_and_training_delivery.json
└── outputs/       # generated .docx packets
```

## Install

```bash
pip install python-docx
```

## Usage

```bash
# Render every data/*.json into outputs/
python generator.py --all

# Render one file (output name auto-derived from the sub-family)
python generator.py data/benefits_and_leave_benefits_administration.json

# Render one file to an explicit path
python generator.py data/lnd_strategy_design_and_training_delivery.json out.docx
```

Output files follow the naming convention
`HR_R2_SME_Review_Packet_<Sub_Family_Underscored>.docx`.

## What a packet contains

Cover + confidentiality · reviewer information · how this packet works (with the
five-status legend and live counts) · ground rules · "start here" alignment
step · specialization coverage matrix · how to read the Round 1 ratings ·
**Part A** applied changes (read and confirm, with full L1–L4 indicator tables)
· **Part B** decisions and proposals (with "what each group said" and a drafted
recommendation) · boundaries to note · decision capture and sign-off ·
appendix of competency indicators.

The status-legend "You have" counts are computed automatically from the Part A /
Part B items, so they never drift from the actual blocks.

## Audit (quality gate / test)

`audit.py` checks every data file against the completeness contract before you
generate, and exits non-zero on any failure (so it doubles as a test):

```bash
python audit.py            # audit every data/*.json
python audit.py data/x.json
```

It enforces:
- **Complete coverage (CRITICAL)** — every competency that *any* participating
  specialization touches must appear in the matrix **with a role**: both the
  shared (union) competencies and the specialization-specific (non-shared)
  ones. Declare each specialization's full set under
  `coverage.specialization_sets`; the audit checks the matrix against it per
  specialization and fails CRITICAL on any gap. This is what catches a packet
  that silently drops a competency another group owns, uses, or carries.
- **Appendix completeness** — every non-deferred coverage competency has a full
  L1–L4 indicator table (≥3 indicators per level).
- **Feedback appendix** — a `disposition_register` exists and has an entry for
  every coverage competency, each with a valid disposition
  (`Applied` / `Synthesized / Used` / `Via level` / `Deferred` / `Corrected` /
  `Kept`).

Run `audit.py` and `generator.py --all` together; a packet should never be
generated from a data file that fails the audit.

## Authoring a new sub-family

Copy an existing file in `data/`, then change **content only** — sub-family
name, specializations, coverage cells, Round 1 quotes, recommendations,
dispositions, and indicator tables. Do not change the section order, the status
values, the coverage codes, or the colors; those are the locked contract
documented in `CLAUDE.md`.

### Complete-coverage rule (CRITICAL)

When a packet spans more than one specialization, it must include **every**
technical competency belonging to any participating specialization — both the
shared (union) and the specialization-specific (non-shared) competencies, never
a per-group subset. Declare each specialization's full set under
`coverage.specialization_sets` so `audit.py` can enforce it per specialization.
A blank coverage cell means "no role," never "omitted."
