# Bloom Beauty Suites

A simple, private business app for a solo lash & beauty professional. It keeps
your clients, schedule, finances, and supplies in one place — and **does the
repetitive thinking for you**: who's due for a rebook, what to reorder, who to
follow up with. Open it in the morning, glance at **Today's To-Dos**, and you're
caught up.

> **Beta.** This is an early version meant for real day-to-day use by one owner.
> Your data lives privately on your own phone or computer (nothing is uploaded
> to any server). Please **back up regularly** (see below).

---

## What it does

- **Today's To-Dos (the Action Center).** Automatically builds your daily list:
  - 🔔 **Rebook reminders** — clients who are past their usual visit rhythm and
    have nothing booked. One tap to rebook, or copy a ready-to-send text.
  - 📦 **Reorder alerts** — supplies at or below your reorder level, with a
    "Mark ordered" button.
  - 🕐 **Expiring products** — adhesives and solutions nearing their date.
  - 📋 **Waitlist follow-ups** — people who've been waiting too long.
- **Clients.** Profiles with lash specs, allergy flags, lifetime value, and a
  **health status** (Active / Lapsing / Lost) that updates itself based on how
  long it's been since their last visit.
- **Schedule.** A day-by-day timeline. Mark a visit **Complete** and the app
  automatically updates that client's visit count, lifetime value, and rhythm —
  then offers a one-tap rebook.
- **Finances.** A plain-language monthly profit estimate from your real logged
  revenue, a revenue trend chart, a tax set-aside helper, and service
  performance.
- **More.** Inventory, Waitlist, your Service Menu, and **Settings** (business
  info, monthly expenses, and Backup/Restore).
- **Works offline & installs like an app.** Add it to your phone's home screen
  and it opens full-screen, even without internet.

Everything **saves automatically** — there is no "save" button to forget.

---

## For the owner: how to use it day to day

1. **Open the app each morning** and look at **Today's To-Dos** on the Home
   screen. Tap the buttons to rebook, reorder, or copy a message to send.
2. **After each client**, go to **Schedule**, find the appointment, and tap
   **✓ Complete**. The app updates everything else for you.
3. **Book new appointments** with the **Book** button on Schedule or a client's
   profile.
4. **Back up your data weekly:** go to **More → Settings & Backup → Back Up My
   Data**. Save the file somewhere safe (email it to yourself, or save to your
   phone's files / cloud). To move to a new phone, install the app there and use
   **Restore from Backup**.

When you first open the app it's filled with **sample data** so you can explore.
When you're ready to use it for real: **More → Settings → Clear & Start Fresh**
(back up first if you want to keep the sample around).

---

## For whoever sets it up (deployment)

This is a static web app — no server, no database, no accounts. Host the
`dist/` folder anywhere that serves static files.

### Run locally

```bash
cd bloom-beauty-suites
npm install
npm run dev        # open the printed http://localhost:5173 URL
```

### Build for deployment

```bash
npm run build      # outputs a self-contained ./dist folder
npm run preview    # optional: preview the production build locally
```

### Deploy (pick one — all free for this size)

- **Netlify / Vercel:** drag-and-drop the `dist/` folder, or connect the repo
  and set **build command** `npm run build` and **publish directory** `dist`.
- **GitHub Pages / any static host:** upload the contents of `dist/`. The build
  uses relative paths, so it works from a sub-folder too.

Once it's hosted over HTTPS, the owner can open the link on her phone and choose
**"Add to Home Screen"** to install it.

> **Privacy/data note:** data is stored in the browser's local storage on the
> device. It is not shared between devices and not backed up automatically —
> that's what the in-app **Back Up My Data** button is for. Clearing the
> browser's site data will erase it, so keep backups.

---

## How it's built

- **React + Vite**, a single-page app. Charts via **Recharts**. Installable via
  **vite-plugin-pwa**. No backend.
- Source layout:

  | Path | What's there |
  |------|--------------|
  | `src/seed.js` | Sample data; generates a fresh demo relative to today |
  | `src/store.jsx` | Auto-saving data store + every action (the only place that writes data) |
  | `src/automation.js` | Pure logic: client health, the daily task list, message templates |
  | `src/format.js` / `src/theme.js` / `src/icons.jsx` | Helpers, colors, icons |
  | `src/ui.jsx` | Shared building blocks (cards, badges, modal, buttons) |
  | `src/pages/` | Dashboard, ActionCenter, Clients, Schedule, Finances, More, BookAppointmentModal |
  | `scripts/make-icons.mjs` | Regenerates the app icons |
  | `scripts/smoke.mjs` | Quick logic check (`npx esbuild scripts/smoke.mjs --bundle --platform=node --outfile=/tmp/smoke.cjs && node /tmp/smoke.cjs`) |

### Adjusting the business defaults

Owner name, location, monthly expenses, and tax set-aside live in **Settings**
in-app (and as defaults in `src/seed.js → DEFAULT_SETTINGS`). The visit-rhythm
thresholds that drive client health and rebook reminders are in
`src/automation.js`.

---

## Known limits (beta)

- **Single device, single user.** No cloud sync or multi-staff support yet —
  back up to move between devices.
- **Texts are copy-to-clipboard**, not sent automatically (no SMS integration in
  beta). Tap "Copy", then paste into your Messages app.
- The monthly finance figure is an **estimate** projected from the current
  week's logged revenue.
