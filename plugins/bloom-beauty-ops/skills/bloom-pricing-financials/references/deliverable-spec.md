# Deliverable Specification — Pricing & P&L workbook

Apply Bloom branding from `../../references/brand.md` (rose headers `#e8a0b4`,
cream fills `#fdf6f0`, charcoal text, gold accents). Use the calculator's JSON as
the data source so the workbook and the script never disagree.

## Excel — `bloom_pricing_pl.xlsx`

### Tab 1 — `Service Pricing`
| Column |
|---|
| Service |
| Price |
| Duration (h) |
| Materials cost / set |
| Gross margin $ |
| Gross margin % |
| Revenue / hour |
| Meets $/hr target? |
| Monthly count |
| Monthly revenue |

Conditional-format `Revenue / hour` (3-color) and flag any service below the
target hourly rate (amber). This is the pricing-decision tab.

### Tab 2 — `Lash P&L`
Monthly: revenue, COGS, gross profit, overhead, **net**, net margin %, total
chair hours, blended revenue/hour, break-even sets to cover overhead. A small
sensitivity block (net at ±10% volume and ±$10 price) is a nice add.

### Tab 3 — `Suite Economics`
Per-suite list (name, rent, occupied?) + summary: occupancy %, rent roll
actual/potential, vacancy value/month, total expenses, **net**, net margin %,
revenue per occupied suite, break-even occupancy (units and %). Highlight vacant
suites (amber) — each is recoverable income.

### Tab 4 — `KPIs`
| KPI | Bloom now | Benchmark (cited) | Read |
|---|---|---|---|
| Suite occupancy | … | 85–90%+ | … |
| Suite net margin | … | 20–30% | … |
| Lash blended $/hr | … | ≥ target | … |
| Avg ticket | … | up via add-ons | … |
| Rebook rate | … | high | … |
| No-show rate | … | low | … |

Cite benchmark sources; treat as ranges, not targets to assert.

## Recommendation summary (top of workbook or a Word one-pager)

Lead with the 1–3 highest-leverage moves and the math, e.g.:
- "3 vacant suites = **$1,950/mo** of near-pure-margin income — filling them roughly
  triples combined net."
- "Fills run **$73–$75/hr** vs your $80 target — consider a small fill increase or
  tighter timing; full sets and the lift already clear target."

Always show the arithmetic and end with the standard disclaimer.
