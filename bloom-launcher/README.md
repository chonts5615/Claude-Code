# Bloom Launcher

A tiny home page that lets the owner open either Bloom app from one place:

- **Bloom Beauty Suites** — the beauty professional's app (`../bloom-beauty-suites`)
- **Bloom Suites Manager** — the suite owner's rental app (`../bloom-suites-manager`)

It's a single self-contained `index.html` — **no build, no dependencies**. Open
it directly or host it anywhere static.

---

## Easiest deploy: one site, one drag-and-drop

From this folder, run:

```bash
./build-site.sh
```

This builds both apps and assembles everything into **`bloom-launcher/site/`**:

```
site/
├── index.html      ← this launcher (home page)
├── app/            ← Bloom Beauty Suites
└── manager/        ← Bloom Suites Manager
```

Then deploy in one step:

- **Netlify (no code):** drag the `site/` folder onto <https://app.netlify.com/drop>.
- **Any static host:** upload the contents of `site/`.

The launcher's default links (`./app/` and `./manager/`) already match this
layout, so it works immediately — the owner gets one link, taps a card, and
optionally **Adds to Home Screen**.

---

## Hosting the apps separately instead

If you deploy each app to its own URL, just edit the two links near the bottom
of `index.html`:

```js
var BLOOM_LINKS = {
  app: "https://your-beauty-app-url/",
  manager: "https://your-manager-app-url/"
};
```

Everything else (styling, layout) stays the same.

---

## Notes

- The two apps store data separately in the browser (different storage keys), so
  they never interfere — even when served from the same site.
- Each app is its own installable PWA; installing one from its page adds just
  that app to the home screen.
