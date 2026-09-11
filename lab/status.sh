#!/usr/bin/env bash
# Lab status: API health, kit identity, credentials, current artefacts.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
echo "== api =="
curl -fsS "http://127.0.0.1:8781/status" 2>/dev/null || echo "api NOT running (bash lab/up.sh)"
echo ""
echo "== kit =="
python3 - <<'PY'
import json, pathlib
root = pathlib.Path(".")
kit = json.loads((root / "kit.json").read_text())
creds = json.loads((root / "data" / "lab_credentials.json").read_text())
print(f"candidate_id : {kit['candidate_id']}")
print(f"window       : {kit['window_start']} .. {kit['window_end']}")
print(f"generated_at : {kit['generated_at']}")
print(f"meta token   : {creds['meta_token']}")
print(f"google token : {creds['google_token']}")
PY
echo ""
echo "== artefacts =="
for f in submission/answers.json submission/decisions.json submission/plan.json tracking/out/events.jsonl; do
  if [ -f "$f" ]; then echo "  present  $f"; else echo "  missing  $f"; fi
done
