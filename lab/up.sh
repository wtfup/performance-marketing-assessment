#!/usr/bin/env bash
# Start the local lab: validate the kit, boot the mock ad API, print status.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

missing=0
for f in kit.json data/ads/meta_insights.json data/ads/google_insights.json data/crm/leads.csv \
         data/crm/members.csv data/warehouse.sqlite data/econ.json data/lab_credentials.json \
         tracking/journeys.jsonl tracking/config/tags.json; do
  [ -e "$f" ] || { echo "MISSING: $f"; missing=1; }
done
if [ "$missing" = "1" ]; then
  echo ""
  echo "The candidate kit is not installed. Unzip the kit delivered by your hiring coordinator"
  echo "at the repository root (it supplies kit.json, data/ and tracking/). See candidate/03_KIT_AND_SETUP.md."
  exit 1
fi

mkdir -p .lab session
if [ -f .lab/api.pid ] && kill -0 "$(cat .lab/api.pid)" 2>/dev/null; then
  echo "api already running (pid $(cat .lab/api.pid))"
else
  nohup python3 lab/api.py --port 8781 > .lab/api.log 2>&1 &
  echo $! > .lab/api.pid
  for i in $(seq 1 40); do
    if curl -fsS "http://127.0.0.1:8781/status" >/dev/null 2>&1; then break; fi
    sleep 0.25
  done
fi
curl -fsS "http://127.0.0.1:8781/status" >/dev/null || { echo "api failed to start; see .lab/api.log"; exit 1; }

python3 - <<'PY'
import json, pathlib
root = pathlib.Path(".")
kit = json.loads((root / "kit.json").read_text())
creds = json.loads((root / "data" / "lab_credentials.json").read_text())
print(f"candidate : {kit['candidate_id']}")
print(f"window    : {kit['window_start']} .. {kit['window_end']}")
print(f"api       : http://127.0.0.1:8781  (mock Meta + Google; loopback only)")
print(f"meta token: {creds['meta_token']}")
print(f"goog token: {creds['google_token']}")
PY
echo ""
echo "lab is up. next: bash lab/status.sh | bash lab/replay.sh | python3 lab/checks.py --section tracking"
