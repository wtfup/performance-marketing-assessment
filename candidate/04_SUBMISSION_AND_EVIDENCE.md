# Submission and Evidence

## The handover

Hand over the **whole repo folder** — do not cherry-pick files. The reviewer needs:

- your kit — `kit.json`, `data/`, `tracking/journeys.jsonl` (git-ignored, so a clone-only handover loses it);
- your fixed `tracking/config/*.json` (fixed in place, not copied elsewhere);
- your `submission/` — every deliverable below;
- your `session/` — checkpoints plus any logs you kept.

Hand it over privately through the hiring coordinator. Never push this work to a public remote.

## Deliverables checklist

- `submission/pull_proof.json` + `submission/raw/meta_pages.jsonl` + `submission/raw/google_pages.jsonl`
- `submission/answers.json`
- `submission/decisions.json`
- `submission/plan.json`
- `submission/run.sh` — the scaffold replaced with your working runner
- `submission/RECON.md`, `submission/TRACKING_REPORT.md`, `submission/AUDIT.md` — 150+ words each, real numbers
- `submission/NOTES.md` — AI disclosure for Part 2 (recommended, not optional if you used AI)
- `tracking/config/*.json` — repaired in place

## Exact shapes

`pull_proof.json`:

```json
{"meta_spend": 0, "google_spend": 0, "meta_platform_leads": 0, "google_platform_leads": 0}
```

`answers.json` — field-by-field definitions live in `01_PART1_OPERATOR.md`, Section B:

```json
{
  "candidate_id": "<candidate_id from kit.json>",
  "window": {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"},
  "totals": {"meta_spend": 0, "google_spend": 0, "platform_meta_leads": 0, "platform_google_leads": 0,
             "crm_leads_raw": 0, "crm_leads_clean": 0, "paid_leads": 0, "paid_walkins": 0,
             "paid_members": 0, "net_revenue": 0},
  "metrics": {"meta_cpl": 0, "google_cpl": 0, "blended_cpl": 0, "cost_per_walkin": 0, "cac": 0, "roas_net": 0},
  "per_campaign": [{"campaign_id": "m-1001", "spend": 0, "clean_leads": 0, "cpl": 0, "walkins": 0, "cost_per_walkin": 0}],
  "data_issues": {"duplicate_rows_removed": 0, "test_rows_excluded": 0, "invalid_phone_rows_excluded": 0,
                  "leads_created_after_window_end": 0, "refunded_members_count": 0, "refund_amount_inr": 0,
                  "members_with_no_attributed_lead": 0, "platform_vs_crm_lead_gap": 0}
}
```

Extra keys are allowed; the listed ones are required.

`decisions.json` — one entry per issue found in the export set:

```json
{"decisions": [{"entity": "…", "campaign": "…", "adset": "…", "ad": "…",
                "action": "kill|pause|scale|keep|fix|investigate",
                "evidence_numbers": {"metric": 0}, "expected_impact_inr": 0, "why": "…"}]}
```

`plan.json`:

```json
{"allocation": {"meta": 0, "google": 0, "influencer": 0},
 "expected": {"leads": 0, "walkins": 0, "members": 0, "blended_cac": 0},
 "kill_rules": [{"metric": "…", "threshold": 0, "window_days": 0, "action": "…"}],
 "assumptions": ["…"]}
```

Allocation must sum exactly to `budget_inr`; `expected` must follow from your allocation via the marginal bands; `kill_rules` must be a non-empty list.

## run.sh — the reproducibility contract

- Runs as `bash submission/run.sh` from the repository root.
- python3 standard library only; no pip; no network beyond the loopback lab API.
- Regenerates `answers.json`, `decisions.json`, `plan.json` — and `pull_proof.json` (loopback pulls inside your script are fine) — from the lab data.
- **Reviewers re-run it** on a clean checkout with your `submission/` and fixed configs overlaid. Anything your script does not regenerate will be missing; hand-computed numbers with no working script score zero.
- Helper files are welcome — keep them under `submission/`; `run.sh` is the entrypoint. The shipped `run.sh` is a scaffold that exits 1 until you replace it.

## Evidence discipline

- Checkpoints: `bash lab/checkpoint.sh "<label>"` at the start and end of every section (more is fine).
- Raw pulls: pages exactly as served, plus the pull script or commands you used.
- Logs: keep terminal evidence under `session/`, e.g. `bash lab/replay.sh 2>&1 | tee session/replay-final.txt`.
- No fabrication. Doctored evidence is disqualifying; an honest, labelled gap is not.
- Before handover: `python3 lab/checks.py --root . --section all` green, and `bash submission/run.sh` working end to end.

Passing the public checks is required but not sufficient — reviewers grade the numbers, the decisions and the configs on top. Write every write-up as if the reader will check it against the raw data, because they will.
