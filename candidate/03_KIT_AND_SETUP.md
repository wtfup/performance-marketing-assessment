# The Kit and Lab Setup

## What the kit is

The repository is code and documentation; the kit is your copy of the world. It arrives as a zip from your hiring coordinator, generated for your candidate id — your window, your account, your journeys. Do not share it. `kit/README.md` explains where it comes from and why it is not in git.

## Install it — at the repo root

```bash
cd performance-marketing-assessment     # the repo root
unzip path/to/your-kit.zip -d .
bash lab/up.sh
```

`lab/up.sh` validates that the kit is present — kit.json, the data files, the tracking files — and refuses to start if anything is missing. If you see `MISSING: ...` followed by "The candidate kit is not installed", you unzipped in the wrong place: unzip again at the repository root.

When it starts, it boots the mock ad API on `http://127.0.0.1:8781` (loopback only) and prints your candidate id, your reporting window, and the two bearer tokens.

## What is inside the kit

- `kit.json` — your candidate id, seed, and the reporting window (`window_start`..`window_end`). Take the window from here; never assume example dates.
- `data/ads/meta_insights.json`, `data/ads/google_insights.json` — the platform data the mock API serves.
- `data/crm/leads.csv`, `data/crm/members.csv` — the CRM export. Timestamps are IST.
- `data/warehouse.sqlite` — the same world in a warehouse (`leads`, `members`, `ad_spend_daily`). Timestamps are UTC.
- `data/exports/*.csv` — the account export set for the Part 2 audit.
- `data/econ.json` — budget, marginal CPL bands, unit economics, channel constraints.
- `data/lab_credentials.json` — the bearer tokens the mock API checks.
- `tracking/journeys.jsonl` — the visitor journeys (the tracking input).
- `tracking/config/*.json` — the tracking configuration. These are **deliberately imperfect**; repairing them is your Section C deliverable.

## Day-to-day commands

```bash
bash lab/up.sh            # start the lab (validates kit, boots the API)
bash lab/status.sh        # API health, kit identity, artefacts present
bash lab/down.sh          # stop the mock API
bash lab/replay.sh        # tracking pipeline + the 9 acceptance checks
bash lab/checkpoint.sh "section B start"   # evidence marker → session/checkpoints.jsonl
python3 lab/checks.py --root . --section all     # everything, any time
```

## Environment requirements

- python3 (3.8+), bash, curl, git. macOS or Linux.
- No Docker, no Node, no pip installs — standard library plus `sqlite3` only.
- Port 8781 free on loopback. The lab never touches the internet.

## Troubleshooting

- `api NOT running` → `bash lab/up.sh`; if it fails, read `.lab/api.log`.
- HTTP 429 responses → you are hammering the mock API; wait the `Retry-After` seconds and slow down.
- Numbers look wrong → `bash lab/status.sh`; confirm you have not edited anything under `data/` (edits are pointless — the kit is replaced with canonical copies at review).
- Restarting is safe: `bash lab/down.sh` then `bash lab/up.sh`. Do not delete `session/` — it holds your evidence.

## What you may edit — the line

- **May:** `tracking/config/*.json` (required), `submission/**` (yours), anything you add under `session/`.
- **May not:** `lab/**`, `tracking/pipeline.py`, `scripts/**`, and the kit's data — `kit.json`, `data/**`, `tracking/journeys.jsonl`. At review these are replaced with canonical copies, so edits are ignored; tampering is noted.
