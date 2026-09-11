# Rules and Scoring

Read this before the day. Everything here is enforced, not decorative.

## Hard rules

- **Synthetic data only.** This lab contains no real people, accounts, spend, or credentials. Never add any.
- **Python 3 standard library only.** No `pip install`, no third-party packages, no vendored libraries. `sqlite3` is part of the standard library and is fine.
- **Do not edit `lab/`, `tracking/pipeline.py`, `scripts/`, or the kit's data.** Among kit files, the only things you change are `tracking/config/*.json` (that is the Section C deliverable). Everything else from the kit — `kit.json`, `data/**`, `tracking/journeys.jsonl` — is input. At review these are replaced with canonical copies, so edits to them are ignored by construction and count for nothing.
- **No public deploy and no publishing.** Do not push this work to any public remote, do not post screenshots or numbers anywhere. Hand your folder to the hiring coordinator privately.
- **No fabricated evidence.** Raw API pages, command output, and checkpoints must come from real runs on your machine. Invented numbers or doctored evidence are disqualifying. Honest, labeled gaps are not.
- **Stay on loopback.** The only network calls are to `http://127.0.0.1:8781` (the mock ad API). Nothing else, on your machine or outside it.

## AI policy

- **Part 1 (Sections A–C): closed-book.** No AI assistants, no internet beyond the local lab. Your supervisor may enforce this at the machine level (Wi-Fi off, AI tools and extensions closed).
- **Part 2 (Sections D–E): AI allowed and expected.** Use whatever helps. Disclose it in `submission/NOTES.md` — which tools, for what, and how you verified their output. You own the correctness of everything you submit; "the model said so" is not defence.

## Scoring (high level)

The written submission is scored out of 100; the live defence is scored separately in a second round.

- **Part 1 correctness — 45 points.** Section A pull & environment 5; Section B truth reconciliation 25; Section C tracking forensics 20 (configs included).
- **Part 2 — 35 points.** Section D account audit 20; Section E scale plan 15.
- **run.sh reproducibility — 5 points.** Reviewers re-run your script on a clean checkout and compare what it regenerates. Hand-computed numbers with no working script score zero for this and weaken everything else.
- **Evidence docs — 5 points.** `RECON.md`, `TRACKING_REPORT.md`, `AUDIT.md`, each 150+ words with real numbers.
- **Live defence — 10 points, separate round.**

The detailed rubric stays private. Verdict bands: **80+** strong; **65–79** hire (trial); **50–64** only with trial; **<50** reject.

## The acceptance checks

`python3 lab/checks.py --root . --section tracking|submission|all` (exit 1 on failure) is the public contract: 9 tracking checks plus submission-shape checks. Green is **required but not sufficient** — passing them proves structure and tracking behaviour, not that your numbers or decisions are right. Reviewers grade the content.

## Integrity notes

- One kit per candidate; do not share your kit or reuse someone else's.
- Keep your work local. If you want version control, commit locally; never push to a public place.
- If something in the lab is broken or unclear, say so to your coordinator — do not silently work around it, and do not "fix" lab code.
