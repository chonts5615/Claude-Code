---
name: bloom-content-studio
description: >
  Generate on-brand marketing and social content for Bloom Beauty Suites & Lash
  Bar — captions, content calendars, promos, before/after posts, Reels/TikTok
  ideas, Google Business Profile posts, review requests, and local SEO copy. Use
  this skill when the user asks for an "Instagram caption," "social post," "lash
  content," "before and after post," "content calendar," "reel idea," "TikTok
  idea," "story post," "promo," "booking promo," "seasonal campaign," "Google
  Business post," "review request text," "referral offer," "Bloom post,"
  "Maple Grove lash marketing," "caption for [service]," or "what should I post
  this week." Produces caption sets, a dated content calendar, and promo copy in
  Bloom's warm rose/cream brand voice — with FTC-compliant disclosure and consent
  reminders for testimonials and before/after images.
---

# Bloom Content Studio

Produce marketing content that sounds like Bloom and fills the calendar: captions,
a weekly/monthly content plan, promos, and Google Business Profile + local-SEO
copy — all in the salon's warm, personal voice.

## Why This Skill Exists

A lash studio lives or dies on a steady local presence: consistent posting,
fresh before/afters, easy rebooking prompts, and a Google Business Profile that
wins "Maple Grove lashes" searches. Doing that by hand every week is the thing
owners drop first. This skill turns a few inputs (this week's openings, a promo,
a new before/after) into a planned, on-brand content set — and bakes in the rules
that keep it compliant: FTC disclosure on anything gifted/sponsored, and explicit
client consent before posting their photos.

## Load the brand first

Read `../../references/brand.md` (plugin-level) for the palette and **voice**
before writing anything: warm, encouraging, personal, owner-to-client, first
names, short sentences, beauty-forward but never hypey. Owner: **Renee**;
business: **Bloom Beauty Suites & Lash Bar**, 9325 Upland Ln N, Maple Grove, MN.

## Required Inputs

Ask for whatever's missing; sensible defaults noted.

| Input | Required | Notes |
|---|---|---|
| What's the goal? | Yes | Fill openings / launch a service / promote a season / get reviews / referrals |
| Channel(s) | Optional | Instagram (default), TikTok/Reels, Google Business Profile, SMS/email |
| Specifics | Optional | The service, price, offer, before/after, openings this week |
| Timeframe | Optional | Single post (default) or a 1-week / 1-month calendar |
| Constraints | Optional | Any claims to avoid; whether photos have client consent |

Pull service names/prices from `../../references/brand.md` (e.g. Volume Full Set
$225, Classic Fill $75) so offers stay accurate.

## Process

### Step 1 — Pick the content type & cadence
Use `references/marketing-playbook.md` for the posting cadence, the local-SEO and
Google Business Profile guidance, and the content-pillar mix (educational,
social proof, behind-the-scenes, offer, rebooking nudge). Default cadence: 3–5
posts/week with at least one before/after and one rebooking/booking-CTA post.

### Step 2 — Draft in Bloom's voice
Write from `references/post-templates.md` patterns, adapted — never generic. Each
caption: a hook, value/story, a clear CTA (book link / DM / call), 5–12 relevant
hashtags mixing local ("#maplegrovelashes", "#twincitieslashes") and craft tags.

### Step 3 — Compliance pass (every time)
- **FTC**: if a post is gifted, comped, or an influencer collab, include a clear
  disclosure (#ad / "gifted"). The app even flags comped/influencer clients
  (e.g. Michelle Park-Davis) — disclose those.
- **Consent**: only use a client's photo/testimonial with explicit permission;
  add a one-line consent reminder to the deliverable when photos are involved.
- **Claims**: no medical/results guarantees; describe the look, not outcomes you
  can't promise.

### Step 4 — Assemble the deliverable
A single caption set, or a dated content calendar (see
`references/marketing-playbook.md` for the calendar layout), plus any promo copy
and a matching Google Business Profile post. Offer SMS/email variants when the
goal is rebooking or filling this week's openings (hand off scheduling logic to
`bloom-booking-ops`).

## References

- `references/marketing-playbook.md` — cadence, content pillars, Google Business
  Profile & local-SEO playbook, review-generation, referrals, seasonal calendar,
  and the calendar deliverable layout.
- `references/post-templates.md` — reusable caption/Reel/story/GBP/review-request
  templates in Bloom's voice, with hashtag sets.

## Deliverables

- **Caption set** — 1–N captions with hooks, CTAs, hashtags, and (if relevant)
  a consent/FTC line.
- **Content calendar** — a dated table (channel, pillar, hook, caption, asset
  needed, CTA) for the requested window.
- **Promo copy** — offer post + GBP post + optional SMS/email blurb.

## Not advice / guardrails

Marketing only — not legal advice. Follow FTC endorsement rules and get client
consent before posting anyone's image or words. Keep claims honest (look, not
guaranteed outcomes). Prices and service names come from the live menu in
`../../references/brand.md`.
