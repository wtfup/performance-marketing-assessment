#!/usr/bin/env bash
# Stop the mock ad API.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
if [ -f .lab/api.pid ]; then
  PID="$(cat .lab/api.pid)"
  kill "$PID" 2>/dev/null || true
  rm -f .lab/api.pid
  echo "api stopped (pid $PID)"
else
  echo "no api pid file"
fi
