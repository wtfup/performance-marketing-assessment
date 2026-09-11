# submission/ — your deliverables

What is in here now are **templates and a scaffold**. Replace them.

## Required

- `pull_proof.json` — Section A.
- `raw/meta_pages.jsonl`, `raw/google_pages.jsonl` — the raw API pages, one page per line (create `raw/` when you pull).
- `answers.json` — Section B; definitions in `candidate/01_PART1_OPERATOR.md`.
- `decisions.json` — Section D, one entry per issue found in the export set.
- `plan.json` — Section E.
- `run.sh` — replace the scaffold with a python3-stdlib-only runner that regenerates the JSON artefacts from the lab data. Reviewers re-run it.
- `RECON.md`, `TRACKING_REPORT.md`, `AUDIT.md` — 150+ words each, real numbers.
- `NOTES.md` — AI disclosure for Part 2 (required if you used AI).

Not here: the fixed tracking configs. Those live in `tracking/config/` — repair them in place.

## The templates pass the public checks — that means nothing

The shipped templates are structurally valid, so `python3 lab/checks.py --root . --section submission` will already show green. That is a shape check, not a grade. Replace every placeholder, then keep the checks green.

## How this gets replayed

Reviewers take this folder plus your fixed configs onto a clean canonical checkout, re-run your `run.sh`, regenerate your artefacts, and grade them against the rules you were given. Anything your script cannot regenerate will be missing at review; hand-computed numbers with no working script score zero.

## Commands

```bash
bash submission/run.sh                            # must regenerate the JSON artefacts
python3 lab/checks.py --root . --section submission
python3 lab/checks.py --root . --section all
```
