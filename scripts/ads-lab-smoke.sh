#!/usr/bin/env bash
# Smoke-check the three Ads Lab station files. Run after ANY edit to ads-lab/*.html.
#   bash scripts/ads-lab-smoke.sh
# Checks per file: no external URLs, no network calls, inline JS parses, page renders from file://.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LAB="$ROOT/ads-lab"
CHROME="${CHROME_BIN:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/adslab-smoke.XXXXXX")"
fail=0

for f in index.html meta.html google.html; do
  path="$LAB/$f"
  printf '\n===== %s (%s bytes)\n' "$f" "$(wc -c < "$path" | tr -d ' ')"
  [ -f "$path" ] || { echo "MISSING $path"; fail=1; continue; }

  if grep -qE 'https?://' "$path"; then
    echo "FAIL external URL reference"; grep -nE 'https?://' "$path" | head -3; fail=1
  else echo "ok   no external URL references"; fi

  if grep -qE 'fetch\(|XMLHttpRequest' "$path"; then
    echo "FAIL network call present"; fail=1
  else echo "ok   no network calls"; fi

  python3 - "$path" "$TMP/$f.js" <<'PY'
import re, sys, pathlib
h = pathlib.Path(sys.argv[1]).read_text()
m = re.findall(r'<script>([\s\S]*?)</script>', h)
pathlib.Path(sys.argv[2]).write_text("\n".join(m))
PY
  if command -v node >/dev/null 2>&1; then
    if node --check "$TMP/$f.js" >/dev/null 2>&1; then echo "ok   inline JS parses"; else echo "FAIL inline JS syntax"; fail=1; fi
  else echo "skip node not installed (JS parse check)"; fi

  if [ -x "$CHROME" ]; then
    "$CHROME" --headless=new --disable-gpu --virtual-time-budget=4000 --dump-dom "file://$path" \
      > "$TMP/$f.dom" 2>/dev/null || true
    bytes=$(wc -c < "$TMP/$f.dom" | tr -d ' ')
    if [ "${bytes:-0}" -gt 20000 ]; then echo "ok   renders from file:// ($bytes bytes of DOM)"; else echo "FAIL render too small ($bytes bytes)"; fail=1; fi
  else echo "skip chrome not found (render check)"; fi
done

echo ""
if [ "$fail" = "0" ]; then echo "SMOKE: all checks passed"; else echo "SMOKE: FAILURES above"; fi
exit "$fail"
