# Part 2 — Growth (AI-assisted, ~70 minutes)

**AI is allowed and expected in Part 2.** Internet is back. Use whatever helps you think — then declare what you used in `submission/NOTES.md` (which tools, for what, how you verified their output). You own the correctness of everything you submit. The file rules from Part 1 still hold: never edit `lab/`, `tracking/pipeline.py`, `scripts/`, or the kit's data; your fixed `tracking/config/*.json` stay as you left them; python3 standard library only.

Two sections. Same discipline: checkpoints, real numbers, no filler.

---

## Section D — Account audit (~40 min)

The account export set sits in `data/exports/`. It is messy on purpose, and several things in it are wrong — operationally wrong, not cosmetically wrong. Find what the numbers support, and act.

The files and what they are for:

- `campaign_export.csv` — ad-level rows for the account: `level, campaign, adset, ad, status, spend, impressions, clicks, ctr, cpm, frequency, platform_results, crm_leads, crm_walkins`. The only place platform claims and CRM outcome sit side by side at ad level.
- `geo_report.csv` — spend, leads and walk-ins by location: the target radius versus everything outside it.
- `placement_report.csv` — where each campaign's delivery actually landed (Facebook Feed, Instagram Feed, Audience Network, Marketplace…), with spend, leads, walk-ins and cost per walk-in.
- `audience_overlap.csv` — pair-wise overlap between audiences. High overlap means budgets are bidding against each other.
- `creative_calendar.csv` — offer/creative per ad with `offer_ends` and status. Compare the calendar against today.
- `search_terms_sample.csv` — a search-terms sample for the search campaigns: term, spend, conversions, average CPC.

### What to produce — `submission/decisions.json`

```json
{
  "decisions": [
    {
      "entity": "REPLACE — the campaign / adset / ad / placement the decision is about",
      "campaign": "",
      "adset": "",
      "ad": "",
      "action": "investigate",
      "evidence_numbers": {"example": "the export numbers that justify the action"},
      "expected_impact_inr": 0,
      "why": "REPLACE — one paragraph tying the action to the numbers."
    }
  ]
}
```

Rules for the shape and the thinking:

- **One entry per issue you find in the export set.** The example above is a shape demo, not one of the issues.
- `action` must be one of: `kill`, `pause`, `scale`, `keep`, `fix`, `investigate`.
- `evidence_numbers` — the actual export numbers that justify the action. Every decision carries them.
- `expected_impact_inr` — your honest estimate of the monthly rupee impact if your action is taken.
- Name the entity precisely (`campaign`, `adset`, `ad` as applicable) so the reviewer can find it in the exports.
- **Never kill or pause a healthy entity.** Some things look bad for reasons that are not performance — check the tracking layer before you cut. An entity whose platform numbers look great but never reached the CRM is a measurement problem.
- **A dramatic platform-vs-CRM gap is a tracking problem, not a performance problem.** The action for those is `fix` or `investigate`, aimed at the measurement — not a blind spend cut.
- Use `keep` or `investigate` to document entities you looked at and deliberately left alone. Auditing is also about what you did not touch.

Then write `submission/AUDIT.md` (150+ words): scope, one block per decision with its numbers, why you left the rest alone, and the platform-vs-CRM gaps you saw. Close with `bash lab/checkpoint.sh "section D done"`.

---

## Section E — Scale plan (~30 min)

The budget and the economics are in `data/econ.json`: `budget_inr`, per-channel `cpl_bands`, `lead_to_walkin`, `walkin_to_join`, and the `economics` block. Allocate the budget across `meta`, `google`, `influencer`.

The model — this is the published maths, use it exactly:

- The `cpl_bands` are **marginal**: every rupee of spend inside a channel consumes the bands in order, cheapest first. Spend inside band *i* buys `band_spend ÷ band_cpl` leads. You cannot spend past a channel's last band.
- From an allocation: `leads` = Σ over consumed bands of `take ÷ cpl`; `walkins` = `leads × lead_to_walkin` for that channel; `members` = `walkins × walkin_to_join`; sum across channels.
- `expected.blended_cac` = total budget ÷ total expected members.
- Constraints: the allocation must sum to **exactly** `budget_inr`; a funded channel gets at least `min_spend_per_channel`; no channel exceeds `max_spend_per_channel`.
- Objective: maximise expected contribution = `members × (membership_arpu + pt_attach_rate × pt_arpu) × (1 − payment_fee_pct/100 − refund_rate) − total_spend − walkins × bca_cost_per_walkin`. Concretely: rank band segments by expected cost per member (`cpl ÷ lead_to_walkin ÷ walkin_to_join`), fund the cheapest first within the constraints, then do the arithmetic carefully.

### What to produce — `submission/plan.json`

```json
{
  "allocation": {"meta": 0, "google": 0, "influencer": 0},
  "expected": {"leads": 0, "walkins": 0, "members": 0, "blended_cac": 0},
  "kill_rules": [
    {"metric": "cost_per_walkin", "threshold": 0, "window_days": 14, "action": "pause"}
  ],
  "assumptions": ["..."]
}
```

- `allocation` must sum to exactly `budget_inr`.
- `expected` must follow from **your** allocation and the published band maths — reviewers recompute it from your numbers.
- `kill_rules`: at least one, each `{metric, threshold, window_days, action}` — rules you would actually operate by (metric, numeric threshold, lookback in days, an action from the same enum).
- `assumptions`: what must hold for the plan to deliver.

Close with `bash lab/checkpoint.sh "section E done"`.

---

## Wrap-up before handover

- Update `submission/run.sh` so that `bash submission/run.sh` regenerates `answers.json`, `decisions.json` and `plan.json` (and `pull_proof.json` — pulling from the loopback API inside your script is fine) from the lab data. It must be python3-stdlib-only and runnable from the repository root. Reviewers re-run it; hand-written numbers with no working script score zero.
- Confirm your AI use for Part 2 is declared in `submission/NOTES.md`.
- Full run: `python3 lab/checks.py --root . --section all`, then hand the repo folder to your coordinator (`04_SUBMISSION_AND_EVIDENCE.md` has the checklist).
