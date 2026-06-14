# Bloom Suites Manager

The **owner's** companion app for running **Bloom Beauty Suites** as a
suite-rental business. Where *Bloom Beauty Suites* (the sister app) is for a
beauty professional running her own books inside a rented suite, **this app is
for the person who owns the suites and rents them out** — tracking suites,
tenants, rent, leases, applicants, and maintenance, and **doing the repetitive
landlord work for you**.

Open it in the morning, glance at **Today's To-Dos**, and you know exactly who
to bill, who to renew, which suites to fill, and what to fix.

> **Beta.** Early version for real day-to-day use by one owner. Data lives
> privately on your own device — **back up regularly** (see below).

---

## What it does

- **Today's To-Dos (the Action Center).** Built automatically each day:
  - 💵 **Rent to collect** — who hasn't paid this month (flagged **late** past
    your grace period). One tap to mark paid, or copy a friendly reminder text.
  - 🔁 **Lease renewals** — tenants whose lease ends soon. One tap to renew a
    year, or copy a renewal message.
  - 🚪 **Vacancies** — empty suites and upcoming move-outs to fill.
  - 🔧 **Maintenance** — open repair requests.
  - 👥 **Applicant follow-ups** — leads waiting to hear back.
- **Suites.** A color-coded board of every suite (occupied / notice / vacant),
  each with its rent, current tenant, and open maintenance.
- **Tenants.** Profiles with lease terms, deposit, full **payment history**, and
  one-tap rent reminders, renewals, notice, and move-out.
- **Rent.** A month-by-month rent roll: collected vs. outstanding, mark payments,
  and **bill a new month** for all tenants in one tap.
- **More.** Applicant pipeline, Maintenance log, and **Settings** (business info,
  rules, monthly expenses, and Backup/Restore).
- **Works offline & installs like an app** — add it to your home screen.

Everything **saves automatically**.

---

## For the owner: day to day

1. **Each morning**, open the app and work **Today's To-Dos**.
2. **When rent comes in**, tap **Mark Paid** (on the to-do, on the Rent tab, or
   on the tenant). Outstanding totals update instantly.
3. **At the start of a new month**, go to **Rent → "Bill … tenants for [month]"**
   to generate that month's rent roll in one tap.
4. **When someone's interested in a suite**, add them under **More → Applicants**
   and move them along New → Toured → Applied → Approved.
5. **Back up weekly:** **More → Settings & Backup → Back Up My Data**, and keep
   the file safe (email it to yourself or save to the cloud).

The app starts with **sample data** to explore. To go live: back up if you want,
then **More → Settings → Clear & Start Fresh** (your suites are kept and set to
vacant) and add your real tenants.

---

## Run it / deploy it

Static web app — no server, no accounts. Same setup as the sister app.

```bash
cd bloom-suites-manager
npm install
npm run dev        # local: open the printed URL
npm run build      # -> ./dist (host anywhere static)
```

**One-click deploy:**
- **Netlify (no code):** run `npm run build`, then drag the `dist/` folder onto
  <https://app.netlify.com/drop>.
- **Netlify / Vercel (from the repo):** both read the included `netlify.toml` /
  `vercel.json`. Because the app is in a sub-folder, set the **base directory**
  to `bloom-suites-manager` in the dashboard; build command `npm run build`,
  output `dist`.

Run the logic self-test:
```bash
npx esbuild scripts/smoke.mjs --bundle --platform=node --outfile=/tmp/smoke.cjs && node /tmp/smoke.cjs
```

---

## How it's built

React + Vite, single-page, installable PWA, no backend. It mirrors the sister
app's structure and shares its visual style (here with a gold header to tell the
two apart on your phone).

| Path | What's there |
|------|--------------|
| `src/seed.js` | Sample suites/tenants/ledger, generated relative to today |
| `src/store.jsx` | Auto-saving store + every action (rent, leases, maintenance) |
| `src/automation.js` | Occupancy, rent status, the daily task list, messages |
| `src/pages/` | Dashboard, ActionCenter, Suites, Tenants, Rent, More |
| `scripts/smoke.mjs` | Quick logic check |

Business defaults (owner name, expenses, late-grace and renewal-window rules)
live in **Settings** in-app and in `src/seed.js → DEFAULT_SETTINGS`.

## Known limits (beta)

- Single device, single user — back up to move between devices.
- Reminder texts are **copy-to-clipboard**, not auto-sent.
- Online rent payment isn't integrated; you record payments as they arrive.
