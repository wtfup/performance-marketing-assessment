# Start Here — Performance Marketing Operator Lab

A two-part, hands-on work sample for a performance-marketing operator role at WTF Gyms. You get a synthetic gym-acquisition account that runs entirely on your machine: a mock ad API, a CRM export, a warehouse, campaign exports, and a tracking pipeline you must repair. Read the repository `README.md` first, then this folder in order.

## What this is

- **Part 1 — Operator (~130 min, closed-book).** No AI, no internet beyond the local lab. You pull the ad data yourself, reconcile platform truth against the CRM with a documented rule set, and repair a broken tracking configuration until the acceptance checks go green.
- **Part 2 — Growth (~70 min, AI-assisted).** Internet and AI tools are allowed and expected; declare your use in `submission/NOTES.md`. You audit a messy account export set, write the decisions you would actually take, and build a budget plan off published marginal-cost curves.
- **Live defence (15 min, separate round).** Screen-share, closed-book drill-downs on your own numbers. Scored separately.

The public acceptance checks are required but not sufficient — reviewers run a stricter private grading pass. See `05_RULES_AND_SCORING.md`.

## The two parts at a glance

| | Part 1 — Operator | Part 2 — Growth |
|---|---|---|
| Duration | ~130 min | ~70 min |
| Mode | Closed-book: no AI, no internet beyond the local lab | AI tools allowed and expected (disclose in NOTES.md) |
| Sections | A pull & environment (20) · B truth reconciliation (55) · C tracking forensics (55) | D account audit (40) · E scale plan (30) |
| You produce | `pull_proof.json` + raw pulls, `answers.json`, `RECON.md`, fixed tracking configs, `TRACKING_REPORT.md` | `decisions.json`, `plan.json`, `AUDIT.md`, `NOTES.md` |
| Acceptance | `bash lab/replay.sh` → 9/9, then `python3 lab/checks.py --root . --section all` | same checks, submission section |

## Prerequisites

- Python 3 (3.8+), `bash`, `curl`, `git`. macOS or Linux.
- Port 8781 free on loopback — the mock ad API binds `127.0.0.1` only.
- Nothing else: no Docker, no Node, no `pip install`. `sqlite3` ships with Python.
- Your kit zip from the hiring coordinator (see `03_KIT_AND_SETUP.md`).

## One-time setup

Do this before the day and confirm it works — then tell your coordinator.

```bash
git clone https://github.com/wtfup/performance-marketing-assessment.git
cd performance-marketing-assessment
unzip path/to/your-kit.zip -d .   # AT THE REPO ROOT — supplies kit.json, data/, tracking/
bash lab/up.sh                    # boots the mock API; prints your candidate id, window and tokens
bash lab/status.sh                # sanity check: API health, kit identity, artefacts
```

If `lab/up.sh` reports a missing file, the kit is not unzipped at the repo root. Full detail in `03_KIT_AND_SETUP.md`.

## How the day runs

1. **Setup check** — your supervisor confirms the lab is up and the tree is clean.
2. **Part 1 (~130 min)** — internet and AI tools are taken away; the local lab keeps running. Work Sections A, B, C. Record going-in and coming-out markers with `bash lab/checkpoint.sh "<label>"`.
3. **Break** — Part 1 closes out; internet and AI tools return.
4. **Part 2 (~70 min)** — AI allowed and expected; you own every number you submit. Finish `decisions.json`, `plan.json`, `AUDIT.md`, `NOTES.md`, and make sure `submission/run.sh` regenerates your artefacts.
5. **Handover** — hand the whole repo folder (kit, `tracking/config/`, `submission/`, `session/`) to your coordinator, privately.
6. **Defence** — a separate 15-minute session; see `06_DEFENCE.md`.

## Evidence and submission (summary)

- Markers: `bash lab/checkpoint.sh "section B start"` appends to `session/checkpoints.jsonl`.
- Raw pulls: keep the API pages you save under `submission/raw/`; keep a copy of your pull commands under `session/`.
- Write-ups: `submission/RECON.md`, `submission/TRACKING_REPORT.md`, `submission/AUDIT.md` — 150+ words each, real numbers, no filler.
- Run `python3 lab/checks.py --root . --section all` before you hand over. Full details in `04_SUBMISSION_AND_EVIDENCE.md`.

## Where to go next

- `01_PART1_OPERATOR.md` — before and during Part 1.
- `02_PART2_GROWTH_AI.md` — before and during Part 2.
- `03_KIT_AND_SETUP.md` — the kit, the environment, troubleshooting.
- `04_SUBMISSION_AND_EVIDENCE.md` — exact deliverable shapes and handover checklist.
- `05_RULES_AND_SCORING.md` — read before the day: rules, AI policy, scoring bands.
- `06_DEFENCE.md` — what the live defence looks like.
- `07_SUPERVISOR_GUIDE.md` — supervisors only.
- `tracking/README.md` — the tracking contract and config schema. `kit/README.md` — what the kit is.

Rules that always apply: synthetic data only; never edit `lab/`, `tracking/pipeline.py`, `scripts/`, or the kit's data; no public deploy; do not publish anything from this assessment.
