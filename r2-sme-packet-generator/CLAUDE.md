# Round 2 SME Review Packet — locked format

Guidance for Claude / AI assistants generating or editing Round 2 SME Focus
Group Packets in this component. When asked to create, update, or regenerate a
packet, follow this contract exactly. Change **content** (names, competencies,
quotes, counts, coverage cells, dispositions, indicators); never change the
**section order, taxonomy values, or visual system**.

## Section order (do not omit or reorder)

1. **Cover** — eyebrow `Technical Competency`, title `Round 2 SME Review Packet`,
   sub-family + specializations line, subtitle, function, prepared-by, date,
   confidentiality band.
2. **Reviewer information** — editable rows: name, specialization/group,
   return-by, time required.
3. **How this packet works** — `What we did` / `What we need from you` /
   `Where your feedback went`, then the status-legend table with live counts.
4. **Ground rules for the session** — bold-lead paragraphs; one names the
   sub-family owner / weighting rule.
5. **Start here** — the alignment step (design-vs-administration split, or rating
   guidance + intake model), with a table, an optional highlighted quote, and a
   `Decide.` prompt.
6. **Specialization coverage matrix** — `# | competency | <spec columns>`, plus
   legend and a note. A blank cell = no role, never "omitted."
7. **How to read the Round 1 ratings** — the 1–5 importance scale (optional;
   include where Round 1 ratings are surfaced).
8. **Part A — modifications already applied (read and confirm)** — each item has
   a status strip, `What changed`, `Round 1 signal`, the full L1–L4 indicator
   table, and a confirm/acknowledge prompt.
9. **Part B — for the focus group (decisions and proposals)** — each item has a
   status strip, owners/time line, optional `Note.`, a `What each group said`
   table, a drafted neutral `Recommendation.`, and a `Decide.` prompt.
10. **Boundaries to note** — `Item | What Round 1 said | Where it goes`.
11. **Decision capture and sign-off** — one row per Start-here + Part A + Part B
    item, columns `Item | Decision | Owner | Date`.
12. **Reference appendix** —
    - **Appendix A · disposition register** (the feedback appendix): every Round 1
      comment grouped by competency, with a disposition badge
      (`Applied` / `Synthesized / Used` / `Via level` / `Deferred` / `Corrected` /
      `Kept`) and the outcome. Nothing is dropped on a statistic.
    - **Appendix B · competency definitions and full L1–L4 indicators** for every
      competency in play, with accepted Round 1 edits applied.

Footer on every page: `Proprietary — SME reviewers and project stakeholders
only | Assessment, Competency & Career Framework Team · 2026`.

## Locked taxonomies (exact values — never rename, recolor, or invent)

### Status badges
| Badge | Color | Meaning |
|---|---|---|
| `PROPOSED` | blue `#0F49C5` | New or expanded competency, drafted in full |
| `NEEDS YOUR DECISION` | amber `#FEA800` | Reviewers disagreed or scope shifts ownership |
| `NEEDS YOUR CONFIRMATION` | green `#00843D` | Change applied; read and confirm |
| `KEPT, NO ACTION` | gray `#707773` | Strongly supported and unchanged |
| `NEEDS A QUICK ANSWER` | red `#C50F1F` | One specific question only the reviewer can answer |

The status legend always lists all five; the "You have" counts are computed
from the actual Part A / Part B blocks (the generator does this automatically).

### Coverage matrix codes
`D` Designs & owns (L3–L4) · `C` Carries with specialization lens · `F`
Facilitates · `U` Uses & applies (L1–L2) · `A` Advises · `S` Shared anchor ·
`Aw` Awareness (L1–L2) · `def` Deferred. A blank cell = no role.

### Disposition codes (in the disposition register)
`Applied` · `Synthesized / Used` · `Via level` · `Deferred` · `Corrected`.

## Visual system

Cargill green `#00843D` (deep `#01632D`); amber `#FEA800`; proposed blue
`#0F49C5`; alert red `#C50F1F`; tints `#F5F9ED` / `#FCFDFB`; ink `#1C2722` /
`#707773`. Display/headings use a serif (Georgia); body uses Arial. Sentence
case everywhere. Every competency uses the L1·L2·L3·L4 indicator structure;
changed levels are flagged `· updated`; L3–L4 get the elevated tint.

## CRITICAL RULE — complete coverage (non-negotiable)

A packet MUST include **every** technical competency that **any** participating
specialization touches — both the **shared (union)** competencies and the
**specialization-specific (non-shared)** ones. None may be dropped because
another group owns it, rates it lower, only uses it, or it is "held in the
library." Each such competency appears in the coverage matrix **with a role**,
in the disposition register, and (unless deferred) in Appendix B. Settled or
carried competencies still appear — they are simply not raised as Part A /
Part B items.

This is enforced, not advisory. In each data file declare every
specialization's full competency set under `coverage.specialization_sets`
(keyed by the exact specialization column name). `audit.py` verifies, per
specialization, that every competency in the set is present in the matrix with
a non-blank role, and fails **CRITICAL** on any gap. Never generate a packet
from a data file that does not pass `audit.py`.

## Writing rules
- **Voice.** Sentence case. Direct Round 1 quotes in "What each group said"
  (italic). Recommendations are neutral — never advocate a position.
- **Traceability.** Every decision traces to Round 1 feedback; every
  confirmation states what changed and why. Never invent a recommendation
  without grounding in stakeholder input.
- **Weighting when views conflict.** SVP version governs → sub-family owner's
  edit → contributor views honored via level (not wording) → ground rules break
  remaining ties.

## Data shape

Each packet is one JSON file in `data/` consumed by `generator.py`. Top-level
keys: `metadata`, `how_this_works`, `ground_rules`, `start_here`, `coverage`,
`ratings_legend` (optional), `part_a`, `part_b`, `boundaries`, `sign_off`,
`appendix`. See the two committed files for the authoritative example of every
field. To add a sub-family, copy one and replace the content.
