# Supervisor Guide

For the person running the day and collecting the handover. Candidates read everything else — read this, sanity-check, and don't coach.

## Before the day

- Hand each candidate two things: the repository URL and their kit zip. **One kit per candidate** — if a kit leaks or gets reused, flag it; the hiring team can regenerate a fresh kit.
- Ask the candidate to complete setup before the day, while internet is still available: clone, unzip the kit at the repo root, `bash lab/up.sh`, `bash lab/status.sh`.
- Confirm the machine has python3, bash and curl, and that port 8781 is free on loopback. No Docker is needed.

## Running the day

- **Part 1 (~130 min, closed-book).** Remove internet and AI tooling from the machine: Wi-Fi off **and** close AI apps, editor extensions and local models. The local lab keeps working. Candidates mark section boundaries with `bash lab/checkpoint.sh "<label>"` — spot-check that `session/checkpoints.jsonl` exists and grows.
- **Break.** Restore internet and AI tools only when Part 1 is closed out.
- **Part 2 (~70 min, AI allowed).** Remind candidates their AI use must be disclosed in `submission/NOTES.md`.
- **Handover.** Take the **whole repo folder** — kit, fixed `tracking/config/`, `submission/`, `session/`. Reject clone-only handovers: they lack the git-ignored kit.
- **Defence (15 min, separate, closed-book).** Screen-share; the format is in `06_DEFENCE.md`.

## Verifying a handover

On a machine with network + git + python3:

```bash
bash scripts/verify-submission.sh /path/to/candidate-folder
```

It clones the canonical public repo into a temp directory, overlays the candidate's `submission/` and `tracking/config/`, installs their kit, runs the tracking pipeline, then runs the public acceptance checks (tracking behaviour + submission shape). Candidate edits to `lab/`, `tracking/pipeline.py` and `scripts/` are ignored by construction — the canonical clone supplies them.

Green output means the structural gates pass. **It is not the score.** The numeric score (0–100) is produced separately from the private reviewer pack, which also re-runs the candidate's `submission/run.sh` on a clean tree. Nothing private lives in this repository.

The script clones the canonical GitHub repo by default; the `PM_CANON_REPO` override exists for offline rehearsal and debugging only — a real verification must clone the canonical repo.

## Integrity notes

- The lab's canonical files (`lab/api.py`, `lab/checks.py`, `tracking/pipeline.py`) are hash-checked during review; ask candidates not to touch them.
- Watch for fabricated raw pulls (pages that do not look like the API's), shared kits, and public pushes of assessment work.
- Collect the candidate folder and hand it to the hiring team unmodified; verification only reads.
