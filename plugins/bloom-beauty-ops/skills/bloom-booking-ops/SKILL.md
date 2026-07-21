---
name: bloom-booking-ops
description: >
  Run Bloom's booking and retention operations — rebooking due/overdue clients,
  no-show / cancellation / deposit policy, waitlist follow-ups, and supply
  reorder prompts — and draft the client messages for each. Use this skill when
  the user asks "who's due for a rebook," "rebook reminders," "follow up with
  clients," "no-show policy," "cancellation policy," "deposit policy," "booking
  fee," "reduce no-shows," "fill this week's openings," "waitlist follow-up,"
  "reorder supplies," "what to reorder," "win back lapsing clients," "today's
  to-dos," "client retention," or "rebooking text." It complements the Bloom
  Beauty Suites app: it reads the app's exported data (clients, appointments,
  inventory, waitlist) in its real shape, applies the same active/lapsing/lost
  and due-date logic, and produces policy documents plus ready-to-send messages.
---

# Bloom Booking Ops

Turn the day's state into action: who to rebook, who's lapsing, what to reorder,
who's on the waitlist — plus the exact text to send and the policies that keep
the calendar full. This is the **outreach and policy** layer on top of the Bloom
Beauty Suites app, which already tracks the data.

## Why This Skill Exists

No-shows and un-rebooked clients are the quiet drain on a lash business — the
average salon loses thousands a year to no-shows, and a client who leaves without
the next fill booked is the most likely to lapse. The app surfaces *what* needs
attention (the Action Center). This skill does the *words and policies*: it
writes the rebooking and win-back messages, drafts a clear no-show/deposit
policy, and prioritizes the outreach so the owner can clear it in one sitting.

## Load the brand first

Read `../../references/brand.md` for voice (warm, first-name, owner-to-client)
and the real service menu/prices used in messages.

## Works with the app's data

The skill mirrors the app's logic (`bloom-beauty-suites/src/automation.js`) so
its outputs are consistent with what the owner sees:

- **Client health:** `active` (within rhythm), `lapsing` (overdue by >10 days
  past expected interval), `lost` (well past). Based on `lastVisit`, `avgInterval`.
- **Due for rebook:** `daysUntilDue` ≤ 0 and no upcoming appointment booked.
- **Reorder:** inventory `qty ≤ reorder` and not already `onOrder`.
- **Expiring:** products within ~30 days of `expires` (adhesives/solutions).
- **Waitlist follow-up:** entries waiting longer than ~5 days.

If given the app's exported JSON, parse it directly. If not, ask for it or work
from a pasted client/appointment list. See `references/workflows.md` for the
exact field shapes.

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Task | Yes | Rebook outreach / write a policy / waitlist / reorder / win-back |
| Data | For outreach | App export JSON, or a pasted list of clients/appointments/inventory |
| Policy params | For policy | Cancellation window, fee %, deposit %, grace — defaults below |
| Tone/limits | Optional | Any clients to skip; promo to include |

## Process

### Step 1 — Identify what needs attention
From the data, build the prioritized lists per `references/workflows.md`: rebooks
(most overdue + lapsing first), lapsing/lost win-backs, reorders, expiring
products, waitlist follow-ups.

### Step 2 — Draft the messages
For each item, write a short, warm, ready-to-send text/DM from
`references/workflows.md` templates — personalized with first name, last
service, and the natural next service/date. Offer SMS and DM variants.

### Step 3 — Policy work (when asked)
Draft or refine the no-show / cancellation / deposit policy from
`references/policies.md`. Defaults grounded in industry norms: **24–48h
cancellation notice**, **late-cancel fee 50%**, **no-show fee 100%** of the
service (or a flat fee), **deposit 20–50%** to book, applied to the service.
Always include a Minnesota-licensing-and-consumer-notice caveat (verify locally).

### Step 4 — Assemble the deliverable
A prioritized action list (with copy-paste messages), and/or a policy document.
Where the output is a list the app can use, emit JSON in the app's shape.

## References

- `references/workflows.md` — the app data shapes, the prioritization logic, and
  the message library (rebook, win-back, waitlist, reorder reminder, deposit
  request, confirmation/reminder).
- `references/policies.md` — no-show/cancellation/deposit policy templates,
  enforcement tactics, and the MN consumer-notice caveat.

## Deliverables

- **Today's outreach list** — prioritized, each row with client, why, suggested
  action, and a ready-to-send message.
- **Policy document** — clear, client-facing no-show/cancellation/deposit policy
  + a short version for booking confirmations and social bios.
- **Reorder/expiring list** — items at/below reorder or expiring, with a supplier
  note.

## Not advice / guardrails

Operational help, not legal advice. A cancellation/deposit/no-show fee policy and
how it's disclosed and charged can have consumer-protection and payment-rule
implications — verify enforceability and disclosure with the appropriate
Minnesota authority and the booking/payment processor before relying on it.
Messaging should respect SMS consent (only text clients who've opted in).
