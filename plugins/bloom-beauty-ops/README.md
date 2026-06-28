# Bloom Beauty Ops

Four skills for running and scaling **Bloom Beauty Suites & Lash Bar** —
a salon-suite rental business plus a lash studio in Maple Grove, MN. They turn
the data already in the Bloom apps into marketing, money, policy, and hiring
deliverables.

| Skill | What it does | Produces |
|---|---|---|
| `bloom-content-studio` | On-brand marketing & social content, content calendars, promos, Google Business Profile & local SEO | Caption sets, a dated content calendar, promo copy |
| `bloom-booking-ops` | Rebooking, no-show/cancellation/deposit policy, waitlist & supply-reorder workflows | Policy documents, a reusable client-message library, rebook/reorder action lists |
| `bloom-pricing-financials` | Service pricing, COGS, suite-rental economics, break-even, monthly P&L, KPIs | Pricing & P&L workbook (Excel); ships a tested Python calculator |
| `bloom-hiring-staff` | Hiring & onboarding lash techs and vetting suite renters; worker-classification awareness | Job posts, trial-day scorecards, onboarding checklists, a renter-vetting rubric |

## Built on the real business

These skills read and write the **actual data shapes and numbers** from the
Bloom apps rather than inventing parallel ones:

- **Service menu & prices** from `bloom-beauty-suites/src/seed.js`
  (Classic Full Set $165 → Volume Full Set $225; fills $75–$125).
- **Client / appointment / inventory** shapes and the `clientStatus`
  (active / lapsing / lost), `daysUntilDue`, and Action-Center logic from
  `bloom-beauty-suites/src/automation.js`.
- **Suites, tenants, leases, rent roll, expenses** from
  `bloom-suites-manager/src/seed.js` (12 suites at $550 / $650 / $750; rent due
  the 1st, 5-day grace, 60-day renewal window).

Where a skill produces a list the app can consume, it emits JSON in the app's
shape so you can paste it straight back in.

## Brand

Bloom's palette is the single source of truth in
[`references/brand.md`](./references/brand.md), mirrored from the apps'
`theme.js`: rose `#e8a0b4`, blush `#f9e8e0`, cream `#fdf6f0`, gold `#c9a96e`,
charcoal `#2d2d2d`. Never use Cargill's green here.

## Not legal, tax, or licensing advice

Minnesota licensing (Board of Cosmetologist Examiners), worker classification
(independent contractor vs. employee — IRS + MN DOLI), sales-tax treatment, and
advertising/endorsement rules change and are fact-specific. Every Bloom artifact
carries a disclaimer to **verify with the appropriate authority** before relying
on it. Benchmarks are cited with sources and dates, not asserted as guarantees.
