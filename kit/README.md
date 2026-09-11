# kit/ — what the candidate kit is

This folder is documentation only. The kit itself never lives in git.

## What the kit is

A per-candidate, generated bundle that supplies the lab's world: `kit.json` (identity + reporting window), `data/**` (ads, CRM, warehouse, exports, economics, credentials), and `tracking/journeys.jsonl` plus `tracking/config/*.json`. It is produced by the hiring team for one candidate id with a fixed seed — same generator, a different world per candidate.

## Why it is not in git

1. **Per-candidate data.** Committing one candidate's world would hand it to every other candidate — the numbers are the assessment.
2. **Credentials and identity.** It contains loopback-only bearer tokens and a personal candidate id; neither belongs in a public repository.
3. **Hygiene.** The repo stays a pure code-and-docs artifact. `.gitignore` excludes `kit.json`, `data/`, `tracking/journeys.jsonl`, `tracking/config/*.json` and `tracking/out/`, so neither the kit nor your work outputs can be committed by accident.

## How you get it

Your hiring coordinator sends you a zip. Unzip it **at the repo root** (see `candidate/03_KIT_AND_SETUP.md`):

```bash
unzip path/to/your-kit.zip -d .
```

`lab/up.sh` validates the kit before anything runs; if it is missing, the lab refuses to start and tells you exactly why.

## What you may change

Inside the kit, only `tracking/config/*.json` is yours to edit — it is a deliverable. Everything else (`kit.json`, `data/**`, `tracking/journeys.jsonl`) is input; at review it is replaced with a canonical copy, so edits are ignored.
