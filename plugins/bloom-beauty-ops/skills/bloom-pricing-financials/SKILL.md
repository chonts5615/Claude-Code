---
name: bloom-pricing-financials
description: >
  Price services and model the money for Bloom Beauty Suites & Lash Bar — service
  pricing and margins, cost of goods (lash materials per set), suite-rental
  economics (rent roll, occupancy, break-even), a simple monthly P&L, and the
  KPIs that matter. Use this skill when the user asks "what should I charge,"
  "service pricing," "price the menu," "raise prices," "profit margin," "cost per
  set," "cost of goods," "suite rent," "booth rental rate," "what rent should I
  charge," "occupancy," "break-even," "monthly P&L," "is this profitable," "how
  much do I make per hour," "package pricing," "KPIs," or "financial model." It
  reads the real Bloom numbers (service menu, 12 suites at $550/$650/$750,
  ~$5,780/mo building expenses) and ships a tested Python calculator
  (scripts/bloom_calc.py). Benchmarks are cited, not asserted; not tax advice.
---

# Bloom Pricing & Financials

Make the money legible: what each service should cost, the margin after lash
materials, what the suites earn against the mortgage, where break-even sits, and
the handful of KPIs to watch. Output an **Excel pricing & P&L workbook**, computed
by the bundled, tested `scripts/bloom_calc.py`.

## Why This Skill Exists

Two businesses share one roof: the **lash studio** (per-service revenue, material
costs, time-per-set) and the **suite-rental** operation (rent roll vs the
mortgage and building costs). Owners usually carry these numbers in their head and
under-price or miss that one empty suite is the difference between a good month
and a thin one. This skill puts real arithmetic on both — grounded in the actual
menu and suite structure already in the Bloom apps — so pricing and occupancy
decisions are made on numbers, not vibes.

## Load the brand & real numbers first

Read `../../references/brand.md` for the live service menu/prices and the suite
structure and expense baseline. Use those as defaults so the model matches the
real business:

- **Lash menu**: Classic Full $165, Hybrid Full $195, Volume Full $225; fills
  $75–$125; Lash Lift $85; Brow Lam $75.
- **Suites**: 12 total — 100 sqft @ $550, 140 sqft @ $650, 180 sqft @ $750.
- **Building expenses** ≈ $5,780/mo (mortgage $4,200 + utilities $680 + insurance
  $240 + cleaning $320 + internet $140 + other $200).

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Question | Yes | Price a service / model suites / full P&L / break-even / KPI snapshot |
| Lash inputs | If pricing | Service times, materials cost/set, target $/hour, monthly volume |
| Suite inputs | If modeling suites | Which suites occupied, rents, expenses (defaults above) |
| Goal | Optional | Target take-home, target margin, desired hourly rate |

If the user has an app export, use its real `services`, `appointments`, `suites`,
`tenants`, and settings; otherwise use the defaults and label assumptions.

## Process

### Step 1 — Frame the question
Lash pricing, suite economics, or both. Read `references/pricing-and-cogs.md` for
pricing methods (cost-plus, time-based, value/market), the lash COGS model
(adhesive + trays + consumables per set), and the KPI definitions/benchmarks.

### Step 2 — Run the calculator
Use `scripts/bloom_calc.py` (pure Python, no dependencies). It computes, per the
input JSON:
- **Lash:** per-service materials cost, gross margin $ and %, **revenue per hour**
  vs the target hourly rate, and a monthly lash P&L + break-even sets.
- **Suites:** rent roll (occupied), full potential, **occupancy %**, total
  expenses, net, net margin, **break-even occupancy** (how many suites cover
  costs), and revenue per suite.

```bash
python3 scripts/bloom_calc.py --input model.json
python3 scripts/bloom_calc.py --demo          # runs on the real seed numbers
```

### Step 3 — Interpret with benchmarks
Compare against the cited benchmarks in `references/pricing-and-cogs.md`
(e.g. suite occupancy target ~85–90%; net margin 20–30% is healthy for a
well-run suite operation; revenue/hour as the lash north-star). Flag where Bloom
is below benchmark and what moves the number (fill a vacant suite, nudge price,
cut a material cost, raise rebook rate).

### Step 4 — Recommend, with the math shown
Give a concrete recommendation (e.g. "Volume Full at $225 yields $X/hr — at your
$80/hr target you have room; the real lever is the 3 empty suites worth
$1,950/mo"). Always show the arithmetic.

### Step 5 — Generate the workbook
Produce the Excel pricing & P&L workbook per `references/deliverable-spec.md`.
Append the disclaimer.

## References

- `references/pricing-and-cogs.md` — pricing methods, the lash COGS model, KPI
  definitions and cited benchmarks, and the suite-rental economics.
- `references/deliverable-spec.md` — the Excel workbook structure.

## Deliverables

- **Excel — Pricing & P&L workbook.** Tabs: `Service Pricing` (price, time,
  materials, margin, $/hr), `Lash P&L` (monthly revenue/COGS/overhead/net,
  break-even), `Suite Economics` (rent roll, occupancy, expenses, net, break-even
  occupancy), `KPIs` (vs benchmark).
- **Recommendation summary** — the key numbers and the 1–3 highest-leverage moves.

## Standard Disclaimer

> Estimates for planning only — **not tax, accounting, or legal advice**. Figures
> depend on your real costs and bookings; benchmarks are general industry
> references, not guarantees. Verify sales-tax treatment (services vs retail),
> worker classification, and any licensing/fees with a qualified Minnesota
> professional before relying on these numbers.

## Guardrails

- Use **real menu/suite/expense numbers** from `../../references/brand.md` as
  defaults; label any assumption you add.
- Show the arithmetic; never hand over a number without how it was computed.
- Cite benchmarks with their source and treat them as ranges, not targets to
  assert as fact.
