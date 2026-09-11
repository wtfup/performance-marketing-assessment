#!/usr/bin/env bash
# Write a timestamped checkpoint marker (evidence that you actually ran the lab).
# Usage: bash lab/checkpoint.sh "section-B start"
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p session
NAME="${1:-checkpoint}"
printf '{"ts":"%s","label":"%s"}\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$NAME" >> session/checkpoints.jsonl
tail -1 session/checkpoints.jsonl
