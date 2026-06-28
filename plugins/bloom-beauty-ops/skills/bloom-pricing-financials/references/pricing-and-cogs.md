# Pricing, COGS & KPIs

## Pricing methods (use together, not alone)

1. **Cost-plus** — materials + a fair return on your time. Floor, not the answer.
2. **Time-based (the lash north-star)** — every service should clear a target
   **revenue per hour**. A $225 Volume Full in 2.5h = $90/hr; a $75 Classic Fill
   in 1h = $75/hr. Compare services on $/hr, not sticker price — a well-priced
   fill can out-earn a full set per hour.
3. **Value / market** — what the Maple Grove / Twin Cities market bears and what
   your skill, retention, and experience justify. Local full sets commonly run
   ~$120–$225+ (premium volume higher); fills ~$50–$125. Bloom's menu sits in the
   mid-premium band, which is consistent with a suite (not a discount chain).

Combine: never price below cost-plus; aim above your target $/hr; sanity-check
against market and your rebook/retention strength.

## Lash COGS model (materials per set)

Estimate cost of goods per service as the consumed materials:

```
materials_per_set ≈ lash trays used + adhesive (per-use share)
                    + eye pads + tape + micro-brushes + primer/sealant share
```

Typical rough range: **$5–$20** per set depending on classic vs volume (volume
uses more lash and time). Pull real unit costs from the app inventory
(`bloom-beauty-suites` seed): trays $12.99–$15.99, adhesive $19.99–$24.99 (many
uses per bottle), eye pads $8.99/50, micro-brushes $4.99/100. Allocate the
per-use share, don't expense a whole bottle per client.

Gross margin per service = price − materials_per_set. For lash work this is high
(materials are a small fraction of price); the real "cost" is **time** — which is
why $/hr matters more than $ margin.

## Lash KPIs (north-stars)

| KPI | What it is | Healthy direction |
|---|---|---|
| Revenue per hour | Service revenue ÷ chair hours | The single best pricing test |
| Average ticket | Revenue ÷ visits | Up via add-ons (lift, tint, brow) |
| Rebook rate | % leaving with next fill booked | High; rebooking-at-checkout is the retention lever |
| Retention / client health | active vs lapsing vs lost | Keep clients in their fill rhythm |
| Retail % | retail ÷ total revenue | A bonus margin lever (aftercare) |
| No-show rate | no-shows ÷ booked | Down (deposits + reminders) |

## Suite-rental economics

This is the landlord side (`bloom-suites-manager`):

```
rent_roll (actual)   = sum(rent of OCCUPIED suites)
rent_roll (potential)= sum(rent of ALL suites)
occupancy %          = occupied_suites ÷ total_suites
net                  = rent_roll_actual − total_monthly_expenses
net margin %         = net ÷ rent_roll_actual
break-even occupancy = expenses ÷ average_rent  (suites that must be rented)
revenue per suite    = rent_roll_actual ÷ occupied_suites
```

Real Bloom baseline: 12 suites (4×$550, 4×$650, 4×$750 by tier — actual seed has
3 per tier occupied + 1 vacant each), building expenses ≈ $5,780/mo. Each empty
suite is **$550–$750/month of lost, near-pure-margin income** — filling vacancies
is almost always the highest-leverage financial move.

## Suite KPI benchmarks (cited, treat as ranges)

- **Occupancy:** established suite locations often run **85–90%+**. Below that,
  filling suites beats almost any other lever.
- **Net profit margin:** a well-run suite operation can reach **20–30%**.
- **Booth/suite rent (US):** commonly **$400–$600/mo** for a booth; suites and
  high-demand metros run higher — Bloom's $550–$750 is a premium-suite band.
- **Revenue per square foot:** track it to compare suite sizes' efficiency.

Sources: industry guides on salon-suite/booth economics (e.g. mysalonsuite,
salonstudios, indiesalons) and salon-profitability references; verify current
local figures before acting.

## Putting it together for Bloom

- Lash pricing is usually *fine on margin* — focus on **$/hr**, **add-ons**, and
  **rebook rate**.
- The suite side is where the big, near-pure-margin dollars are — **occupancy is
  king**. Model vacancies explicitly.
- The combined monthly picture = lash net + suite net. Show both, then the total.
