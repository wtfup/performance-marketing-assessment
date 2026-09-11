#!/usr/bin/env bash
# ============================================================================
# Supervisory verification — Performance Marketing Operator Lab.
#
# Usage:  bash scripts/verify-submission.sh <path-to-candidate-folder>
#
# What it does:
#   1. requires the candidate folder to contain the full handover, their kit
#      included (kit.json, data/, tracking/journeys.jsonl, tracking/config/)
#   2. clones the canonical public repo into a temp directory
#      (override PM_CANON_REPO only for offline rehearsal / debugging)
#   3. overlays ONLY the candidate's submission/ and tracking/config/
#   4. runs the public acceptance checks: tracking behaviour + submission shape
#
# Candidate edits to lab/, tracking/pipeline.py and scripts/ are ignored by
# construction — the canonical clone supplies them.
#
# The public checks are structural gates only. The numeric score (0-100) is
# produced separately from the private reviewer pack; nothing private lives
# in this repository.
# ============================================================================
set -euo pipefail

CAND="${1:?usage: bash scripts/verify-submission.sh <path-to-candidate-folder>}"
CANON="${PM_CANON_REPO:-https://github.com/wtfup/performance-marketing-assessment.git}"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/pm-verify.XXXXXX")"

die() { echo "ERROR: $*" >&2; exit 1; }

[ -d "$CAND" ] || die "candidate folder not found: $CAND"
for f in kit.json data tracking/journeys.jsonl tracking/config submission; do
  [ -e "$CAND/$f" ] || die "candidate handover is missing '$f' — hand over the whole repo folder with the kit installed"
done
compgen -G "$CAND/tracking/config/*.json" >/dev/null || die "no fixed tracking configs found under $CAND/tracking/config/"

echo "== candidate : $CAND"
echo "== workdir   : $WORK"
echo "== cloning canonical repo"
git clone --quiet "$CANON" "$WORK"

echo "== overlaying submission/ and tracking/config/"
rm -rf "$WORK/submission"
cp -R "$CAND/submission" "$WORK/submission"
mkdir -p "$WORK/tracking/config"
cp "$CAND"/tracking/config/*.json "$WORK/tracking/config/"

echo "== installing the candidate's kit"
cp "$CAND/kit.json" "$WORK/kit.json"
rm -rf "$WORK/data"
cp -R "$CAND/data" "$WORK/data"
cp "$CAND/tracking/journeys.jsonl" "$WORK/tracking/journeys.jsonl"

cd "$WORK"

PIPE_RC=0
echo ""
echo "== replaying the tracking pipeline with the candidate's configs"
python3 tracking/pipeline.py --root . || PIPE_RC=$?

TRACK_RC=0
echo ""
echo "===== acceptance: tracking ====="
python3 lab/checks.py --root . --section tracking || TRACK_RC=$?

SUB_RC=0
echo ""
echo "===== acceptance: submission shape ====="
python3 lab/checks.py --root . --section submission || SUB_RC=$?

echo ""
if [ "$PIPE_RC" = "0" ] && [ "$TRACK_RC" = "0" ] && [ "$SUB_RC" = "0" ]; then
  echo "== public checks: ALL GREEN"
else
  echo "== public checks: FAILURES above (pipeline rc=$PIPE_RC, tracking rc=$TRACK_RC, submission rc=$SUB_RC)"
fi
echo ""
echo "== These checks are structural gates only. The numeric score (0-100) is"
echo "== produced separately from the private reviewer pack, which also re-runs"
echo "== the candidate's submission/run.sh on a clean tree."
echo "== workdir kept for inspection: $WORK"

if [ "$PIPE_RC" = "0" ] && [ "$TRACK_RC" = "0" ] && [ "$SUB_RC" = "0" ]; then
  exit 0
else
  exit 1
fi
