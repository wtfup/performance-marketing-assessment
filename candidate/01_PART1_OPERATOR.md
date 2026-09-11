# Part 1 — Operator (closed-book, ~130 minutes)

**Closed-book:** no AI assistants, no internet beyond the local lab. The mock API on `127.0.0.1:8781` keeps working — that is the one allowed "network". Your supervisor may enforce this at the machine level. Everything else (editor, terminal, python3) is yours.

You have three sections. The clock is real; the markers are evidence. Run `bash lab/checkpoint.sh "<label>"` at the start and end of every section.

## What you produce in Part 1

- Section A: `submission/pull_proof.json` + raw API pages under `submission/raw/`.
- Section B: `submission/answers.json` + `submission/RECON.md` (150+ words).
- Section C: fixed `tracking/config/*.json` + `submission/TRACKING_REPORT.md` (150+ words).

---

## Section A — Pull & environment (~20 min)

1. Start the lab and note your identity:

   ```bash
   bash lab/up.sh        # validates the kit, boots the mock API, prints candidate id + window + tokens
   bash lab/status.sh    # same, any time you forget
   ```

2. Put the credentials into your shell (they are also printed by the commands above):

   ```bash
   META_TOKEN=$(python3 -c "import json;print(json.load(open('data/lab_credentials.json'))['meta_token'])")
   GOOGLE_TOKEN=$(python3 -c "import json;print(json.load(open('data/lab_credentials.json'))['google_token'])")
   START=<window_start from kit.json>   # e.g. 2026-08-10
   END=<window_end from kit.json>       # e.g. 2026-09-08
   ```

   Check the API answers: `curl -s http://127.0.0.1:8781/status`.

3. Pull the Meta side. It is cursor-paginated; one page will not contain the window. Responses look like
   `{"data":[{"campaign_id","campaign_name","date","spend","impressions","clicks","results"}...],"next_cursor":...,"total_count":...}`.

   ```bash
   curl -s -H "Authorization: Bearer $META_TOKEN" \
     "http://127.0.0.1:8781/meta/v1/insights?level=campaign&since=$START&until=$END&limit=50"
   ```

   Follow `next_cursor` (append `&cursor=<value>`) until it is `null`. `limit` caps at 50.

4. Pull the Google side. It is token-paginated; responses look like
   `{"rows":[{"campaign_id","campaign_name","date","cost_micros","impressions","clicks","conversions"}...],"nextPageToken":...,"totalRows":...}`.
   `cost_micros` is spend × 1,000,000 — divide before you think.

   ```bash
   curl -s -H "Authorization: Bearer $GOOGLE_TOKEN" \
     "http://127.0.0.1:8781/google/v1/reports?dateFrom=$START&dateTo=$END&pageSize=100"
   ```

   Follow `nextPageToken` (append `&pageToken=<value>`) until it is `null`. `pageSize` caps at 100.

5. Save the evidence, page by page: raw responses exactly as served, one page per line, in
   `submission/raw/meta_pages.jsonl` and `submission/raw/google_pages.jsonl`. Keep the pull script or commands you used under `session/` as well.

6. Compute the four verdict numbers and write `submission/pull_proof.json`:

   ```json
   {"meta_spend": 0, "google_spend": 0, "meta_platform_leads": 0, "google_platform_leads": 0}
   ```

   - `meta_spend` / `google_spend`: sum of `spend` (Google: `cost_micros` ÷ 1e6) over every pulled row in the window.
   - `meta_platform_leads`: sum of Meta `results`. `google_platform_leads`: sum of Google `conversions`.

7. Etiquette: the mock API rate-limits bursts — HTTP 429 with a `Retry-After` header. If you see it, wait the stated seconds and continue; do not hammer it in a loop.

The mock API serves the same numbers as `data/ads/*.json`, so you can sanity-check your pull against the files — but the deliverable is the pull (pagination + raw pages included), and your totals must match what the API served.

Close the section with `bash lab/checkpoint.sh "section A done"`.

---

## Section B — Truth reconciliation (~55 min)

The platform lies a little, the CRM lies differently, and the warehouse speaks another timezone. Your job: reconcile everything to one documented truth and report the damage.

### The rules (these define "correct")

Window: leads **created within `window_start..window_end` inclusive, IST** (your kit's window; never assume the example dates).

Cleaning `data/crm/leads.csv` — apply in this order, and count what each step removes:

1. **Drop test rows** (`is_test = 1`) → `test_rows_excluded`.
2. **Drop invalid phones** → `invalid_phone_rows_excluded`. Valid = exactly 10 digits, starting 6–9, and not a single-digit-repeated number (e.g. `9999999999` is invalid).
3. **Drop rows dated after `window_end`** (IST) → `leads_created_after_window_end`. The export runs a day behind; late conversions land outside scope.
4. **Deduplicate** on the same phone + same IST calendar day, keeping the earliest row → `duplicate_rows_removed`.

Everything left is your **clean leads**.

Classification, from the clean set:

- **Organic** sources (case-insensitive, trimmed): `{walk-in, walkin, referral, instagram-organic}`. Anything else non-empty in `source` is a **paid-platform lead**. Use the `source` column, not `utm_source`.
- **Paid walk-in**: a paid lead with status `visited` or `joined`.
- **Members** (from `data/crm/members.csv`) are attributed **through their lead**: a member is in scope when their `lead_id` belongs to a clean paid lead (the member's own `joined_at` is not re-filtered against the window). Members with no `lead_id` at all are organic walk-ins — count them under `members_with_no_attributed_lead`, and keep them out of paid revenue.
- **Refunds are reported separately**: gross = membership + PT across paid members; refunds = the same sum for refunded paid members; `net_revenue = gross − refunds`.
- **Per-campaign metrics use campaign-attributed leads only** (clean leads whose `campaign_id` matches). **Blended metrics use ALL paid leads** — attributed plus the ones with no campaign at all.

Warehouse: `data/warehouse.sqlite` stores timestamps in **UTC** (`created_at_utc`, `joined_at_utc`, no suffix); the CRM CSV is **IST**. Convert before comparing. Never join the two naively, and never mix the two when counting a window.

### What to produce — `submission/answers.json`

```json
{
  "candidate_id": "<your candidate_id from kit.json>",
  "window": {"start": "<YYYY-MM-DD>", "end": "<YYYY-MM-DD>"},
  "totals": {
    "meta_spend": 0, "google_spend": 0,
    "platform_meta_leads": 0, "platform_google_leads": 0,
    "crm_leads_raw": 0, "crm_leads_clean": 0,
    "paid_leads": 0, "paid_walkins": 0, "paid_members": 0, "net_revenue": 0
  },
  "metrics": {
    "meta_cpl": 0, "google_cpl": 0, "blended_cpl": 0,
    "cost_per_walkin": 0, "cac": 0, "roas_net": 0
  },
  "per_campaign": [
    {"campaign_id": "m-1001", "spend": 0, "clean_leads": 0, "cpl": 0, "walkins": 0, "cost_per_walkin": 0}
  ],
  "data_issues": {
    "duplicate_rows_removed": 0, "test_rows_excluded": 0, "invalid_phone_rows_excluded": 0,
    "leads_created_after_window_end": 0, "refunded_members_count": 0, "refund_amount_inr": 0,
    "members_with_no_attributed_lead": 0, "platform_vs_crm_lead_gap": 0
  }
}
```

Exact meanings:

- `crm_leads_raw` — every row in the CRM export, before any cleaning. Raw means raw.
- `crm_leads_clean` — rows remaining after the four cleaning steps.
- `paid_leads` — clean leads classified paid (attributed + unattributed); `paid_walkins` — paid leads that visited or joined; `paid_members` — members attributed through a paid lead; `net_revenue` — gross minus refunds across those members.
- `meta_cpl` = Meta spend ÷ clean leads attributed to Meta campaigns. `google_cpl` = Google spend ÷ clean leads attributed to Google campaigns.
- `blended_cpl` = total ad spend ÷ `paid_leads` (all paid, attributed or not).
- `cost_per_walkin` = total ad spend ÷ `paid_walkins`. `cac` = total ad spend ÷ `paid_members`. `roas_net` = `net_revenue` ÷ total ad spend.
- `per_campaign` — one entry per campaign in the account: `spend` (window sum), `clean_leads` (attributed), `cpl`, `walkins` (of those), `cost_per_walkin`. Null when a denominator is zero.
- `data_issues` — the eight counters above; `platform_vs_crm_lead_gap` = (platform Meta leads + platform Google leads) − `paid_leads`.

Extra keys are allowed (`gross_revenue`, `organic_leads`, `paid_leads_missing_attribution`, …) — the listed ones are required.

### Working notes

- Script it in python3 (standard library only) and keep the script under `session/`. Hand-counting thousands of rows never ends well.
- The warehouse is there so you can cross-check; if the two sources disagree for a lead, the CRM export is the operational truth and the warehouse shows what the dashboards would see.
- Report money in rupees; one-to-three decimals is plenty for ratios.

Then write `submission/RECON.md` (150+ words, real numbers): the window, the method, the headline numbers, the data issues, and the caveats. Close with `bash lab/checkpoint.sh "section B done"`.

---

## Section C — Tracking forensics (~55 min)

The tracking world lives in `tracking/`. The pipeline (`tracking/pipeline.py`) is **frozen** — at review it is replaced with the canonical copy, so engine edits are discarded by construction. The configs under `tracking/config/` are yours to fix, and they do not all honour the contract. That is deliberate.

The contract, in one breath: destinations are `crm | ga4 | meta_pixel | capi`; event names are fixed (crm → `lead_created`, ga4 → `generate_lead`, meta_pixel → `Lead`, capi → `Lead`); every non-test journey with a `form_submit` must reach the CRM exactly once; marketing destinations (`meta_pixel`, `capi`) fire only with `consent_state == granted`; the ~10% of journeys that double-submit must be deduplicated; `occurred_at` is stored as a UTC instant (`...Z`); utm values are normalised to lowercase and aliased (`fb→facebook`, `ig→instagram`, `googleads→google`); `utm_campaign` must survive the `/go/` redirect hop; test journeys emit nothing.

`tracking/README.md` documents every config file, every field, the correct value of each field, and the exact output contract. Read it, then:

1. Read each file in `tracking/config/` against that spec and find what is wrong.
2. Fix the file in place. Change config only — never the engine, never `tracking/journeys.jsonl`.
3. Run the acceptance loop:

   ```bash
   bash lab/replay.sh
   ```

   It replays the pipeline over your config and runs the 9 tracking checks. Iterate until you see `9/9 checks passed`.

4. Write `submission/TRACKING_REPORT.md` (150+ words): the verdict, each config file you changed (what it said → what it says now → which contract rule the old value violated, one line each), the evidence (your final replay output), and residual risk (what the checks do not cover).

Close with `bash lab/checkpoint.sh "section C done"` and hand back to your supervisor for Part 2.

## Section close-out

- `bash lab/replay.sh` green (9/9) — required, not sufficient; reviewers grade the content on top.
- `python3 lab/checks.py --root . --section all` once your submission files exist.
- Markers in `session/checkpoints.jsonl` for A, B, C.
