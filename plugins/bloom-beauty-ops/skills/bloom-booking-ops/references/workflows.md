# Booking Ops — data shapes, logic, and message library

## App data shapes (from `bloom-beauty-suites`)

Parse the app export in these shapes (see `src/seed.js`, `src/automation.js`):

```jsonc
// client
{ "id": 1, "name": "Sarah Mitchell", "phone": "612-555-0101",
  "firstVisit": "2024-03-15", "curl": "C", "length": "11-13mm",
  "allergies": "None", "visits": 28, "ltv": 2380,
  "avgInterval": 17, "lastVisit": "2026-06-24" }

// appointment
{ "id": 10, "clientId": 1, "clientName": "Sarah Mitchell", "date": "2026-07-05",
  "time": "10:00", "serviceId": "volume-fill", "serviceName": "Volume Fill (2wk)",
  "price": 110, "status": "scheduled", "rebooked": false }

// inventory item
{ "id": 6, "name": "Stacy Lash Adhesive — Extra Strong", "category": "Adhesive",
  "qty": 3, "reorder": 2, "cost": 22.99, "supplier": "Amazon",
  "expires": "2026-07-29", "onOrder": false }

// waitlist entry
{ "id": 1, "name": "Christina Meyers", "phone": "612-555-2001",
  "service": "Volume Full Set", "preferred": "Weekday mornings",
  "added": "2026-06-24", "status": "waiting" }
```

## Prioritization logic (mirror the app)

- **Client health** (`clientStatus`): days since `lastVisit` vs `avgInterval`.
  `active` if within interval+10; `lapsing` if interval+10 < since ≤ a larger
  window; `lost` beyond that.
- **Due for rebook**: `daysUntilDue ≤ 0` (since ≥ avgInterval) AND no future
  `scheduled` appointment. Sort most-overdue first; bump `lapsing` clients up.
- **Reorder**: `qty ≤ reorder` and not `onOrder`.
- **Expiring**: `expires` within ~30 days and not `onOrder` (adhesives/solutions
  matter most — they degrade).
- **Waitlist follow-up**: `added` more than ~5 days ago and `status` = waiting.

Output one prioritized list: rebooks → win-backs (lapsing/lost) → waitlist →
reorder → expiring. Each row: who/what, why (the trigger), suggested action, and
a ready message.

## Message library (warm, first-name, owner-to-client)

**Rebook (due, healthy)**
> "Hi [first]! You're about due for your [next service] 🤍 I've got [day]
> openings this week — want me to save you a spot? — Renee"

**Rebook (lapsing — gentle)**
> "Hey [first]! It's been a little bit since your last set and I'd love to get
> you back in 🌸 Want me to grab you a [service] this week?"

**Win-back (lost — warm, with a nudge)**
> "Hi [first]! I was just thinking of you — would love to have you back at Bloom.
> Here's $[X] off your next [service] if you book this month 💕 — Renee"

**Waitlist opening**
> "Hi [first]! A [service] spot just opened [day/time] — you were on my list 🙌
> Want it? First to reply gets it."

**Booking confirmation + policy (one-liner)**
> "You're booked: [service], [date] at [time] 🤍 Heads up — I hold spots with a
> [deposit]% deposit and ask for [24/48]h notice to reschedule. See you then!"

**Reminder (48h / 24h)**
> "Reminder: your [service] is [day] at [time] 🌸 Reply C to confirm or R to
> reschedule (please give 24h so I can offer the spot to someone waiting)."

**Reorder reminder (to self / supplier)**
> "Reorder: [item] — down to [qty] (reorder at [reorder]) from [supplier]."

**Expiring product (to self)**
> "[item] expires [date] — use first or replace."

## Output JSON (app-consumable)

When asked for an action list the app could ingest, emit:

```json
{ "rebook": [ { "clientId": 1, "reason": "overdue 6d", "message": "..." } ],
  "winback": [], "waitlist": [], "reorder": [ { "id": 6, "message": "..." } ] }
```
