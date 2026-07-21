# cargill-bloom-suite — Claude Code plugin marketplace

A personal, two-plugin marketplace for an industrial-organizational (I-O)
psychologist who leads Talent Assessment, Competency Modeling, and Career
Frameworks at Cargill — and who helps run **Bloom Beauty Suites & Lash Bar**
(a salon-suite rental + lash business in Maple Grove, MN).

The marketplace manifest lives at the repo root: [`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json).

| Plugin | What it's for | Skills |
|---|---|---|
| [`cargill-io-psych`](./cargill-io-psych) | Defensible talent-systems work | `job-analysis-facilitator`, `selection-method-advisor`, `assessment-center-designer`, `career-architecture-builder`, `adverse-impact-analyzer` |
| [`bloom-beauty-ops`](./bloom-beauty-ops) | Running & scaling the salon | `bloom-content-studio`, `bloom-booking-ops`, `bloom-pricing-financials`, `bloom-hiring-staff` |

## Install

From any Claude Code session:

```
/plugin marketplace add chonts5615/Claude-Code
/plugin install cargill-io-psych@cargill-bloom-suite
/plugin install bloom-beauty-ops@cargill-bloom-suite
```

Each skill registers a `/skill-name` shortcut and is also invoked automatically
when your request matches its description. Verify a plugin locally with:

```
claude plugin validate ./plugins/cargill-io-psych --strict
claude plugin validate ./plugins/bloom-beauty-ops --strict
```

## How this fits the rest of the repo

These plugins **complement** — they do not duplicate — what the monorepo already
ships:

- The Cargill plugin assumes the **TCB v3.1 competency builder**
  (`tech-competency-agent/`) owns *competency authoring*, and the existing
  `structured-interview-generator`, `coverage-audit`, and `sme-validation-package`
  skills own interview guides, coverage matrices, and SME packages. The new
  skills add the *surrounding* talent-system steps: analysis of work, method
  selection, assessment-center design, career architecture, and adverse-impact
  analysis.
- The Bloom plugin assumes the **Bloom React apps** (`bloom-beauty-suites/`,
  `bloom-suites-manager/`) own the *day-to-day record-keeping*. The new skills
  read and write those apps' data shapes and turn them into marketing,
  financial, policy, and hiring deliverables.

## Two brand systems — never mixed

- **Cargill** outputs use Leaf Green `#00843D` / White Green `#F5F9ED`, Arial body /
  Georgia headings (see `tech-competency-agent/src/utils/branding.py`).
- **Bloom** outputs use the salon palette — rose `#e8a0b4`, blush `#f9e8e0`,
  cream `#fdf6f0`, gold `#c9a96e`, charcoal `#2d2d2d` (see
  `bloom-beauty-ops/references/brand.md`, mirrored from the apps' `theme.js`).

## Not professional advice

The Cargill skills generate **drafts** that a qualified I-O psychologist and
legal counsel must review before operational use. The Bloom skills are **not**
legal, tax, or licensing advice — verify Minnesota licensing, worker
classification, and tax treatment with the appropriate authority. Every
generated artifact carries the relevant disclaimer.
