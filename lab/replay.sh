#!/usr/bin/env bash
# Replay the tracking pipeline over your (fixed) config and run the tracking acceptance checks.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python3 tracking/pipeline.py --root .
echo ""
python3 lab/checks.py --root . --section tracking
