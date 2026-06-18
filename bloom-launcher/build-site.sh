#!/usr/bin/env bash
# Build BOTH apps and assemble a single deployable folder with the launcher.
#
# Result:  bloom-launcher/site/
#            index.html            ← this launcher (the home page)
#            app/                  ← the beauty professional's app
#            manager/              ← the suite owner's app
#
# Then deploy in one step: drag the `site/` folder onto https://app.netlify.com/drop
# The launcher's default links (./app/ and ./manager/) already match this layout.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
SITE="$HERE/site"

build() {  # $1 = app folder, $2 = destination subfolder
  echo "→ Building $1 …"
  ( cd "$ROOT/$1" && npm install --no-audit --no-fund --silent && npm run build --silent )
  rm -rf "${SITE:?}/$2"
  mkdir -p "$SITE/$2"
  cp -R "$ROOT/$1/dist/." "$SITE/$2/"
}

rm -rf "$SITE"
mkdir -p "$SITE"

build "bloom-beauty-suites" "app"
build "bloom-suites-manager" "manager"

# Copy the launcher itself to the site root.
cp "$HERE/index.html" "$SITE/index.html"
cp "$HERE/favicon.svg" "$SITE/favicon.svg"
cp "$HERE/apple-touch-icon.png" "$SITE/apple-touch-icon.png"

echo ""
echo "✓ Done. Deploy the folder:  $SITE"
echo "  • Netlify (no code): drag that folder onto https://app.netlify.com/drop"
echo "  • Or serve it with any static host."
