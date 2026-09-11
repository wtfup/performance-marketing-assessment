# Performance Marketing Operator Lab

A two-part hiring work sample for a hands-on performance-marketing operator at WTF Gyms (an Indian gym chain). You run a synthetic acquisition account locally — a mock ad API, a CRM export, a warehouse, account exports, and a tracking pipeline that must honour a written contract — and you produce the numbers, the fixes, and the growth plan an operator would be expected to ship.

Everything is synthetic, offline, and local. Start with `candidate/00_START_HERE.md`.

## Quickstart

```bash
git clone https://github.com/wtfup/performance-marketing-assessment.git
cd performance-marketing-assessment
# unzip the kit your hiring coordinator sent you, AT THE REPO ROOT
# (it supplies kit.json, data/ and tracking/ — see kit/README.md)
unzip path/to/your-kit.zip -d .
bash lab/up.sh        # validates the kit, boots the mock ad API on http://127.0.0.1:8781
bash lab/status.sh    # API health, candidate id, window, credentials
```

Then work through `candidate/01_PART1_OPERATOR.md` and `candidate/02_PART2_GROWTH_AI.md`. Stop the lab with `bash lab/down.sh` when you are done.

## What you deliver

- `submission/pull_proof.json` + `submission/raw/` — the API data you pulled yourself.
- `submission/answers.json` — the reconciled truth: totals, metrics, per-campaign, data issues.
- `submission/decisions.json` — one decision per issue found in the account export set.
- `submission/plan.json` — how you would spend the next budget across channels.
- `submission/run.sh` — a python3-stdlib-only script that regenerates all of the above. Reviewers re-run it.
- `submission/{RECON,TRACKING_REPORT,AUDIT}.md` — your evidence write-ups (150+ words each).
- your fixed `tracking/config/*.json`.

## Repo layout

- `lab/` — mock ad API, lab control scripts, acceptance checks. Do not edit.
- `tracking/` — the tracking pipeline (frozen engine) and the configs you must repair. See `tracking/README.md`.
- `candidate/` — your briefs; start at `00_START_HERE.md`. The supervisor guide is `07_SUPERVISOR_GUIDE.md`.
- `submission/` — templates and your deliverables. See `submission/README.md`.
- `scripts/` — supervisor tooling.
- `data/`, `kit.json`, `tracking/journeys.jsonl` — supplied by your kit, not in git. See `kit/README.md`.

## Rules at a glance

- Synthetic data only. No real people, accounts, or credentials anywhere.
- Python 3 standard library only (sqlite3 included). No pip installs.
- Never edit `lab/`, `tracking/pipeline.py`, `scripts/`, or the kit's data; the only kit files you change are `tracking/config/*.json`.
- Part 1 is closed-book (no AI, no internet beyond the local lab). Part 2 allows AI — disclose it in `submission/NOTES.md`.
- No public deploy, and do not publish anything from this assessment. Hand your work to the hiring coordinator privately.

Full rules and scoring: `candidate/05_RULES_AND_SCORING.md`.
