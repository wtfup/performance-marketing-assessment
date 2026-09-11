# Tracking — pipeline, config, output contract

This folder is the tracking world of the lab. `pipeline.py` is the engine; `config/` is the configuration it reads; `journeys.jsonl` (supplied by your kit) is the input.

**The engine is frozen.** At review `tracking/pipeline.py` is replaced with the canonical copy, so edits to it are discarded by construction. **Fix the config, not the engine.** And never edit `journeys.jsonl` — it is input, and the kit replaces it at review.

## Running it

```bash
bash lab/replay.sh                       # pipeline + the 9 acceptance checks — the loop that matters
python3 tracking/pipeline.py --root .    # pipeline only → tracking/out/events.jsonl (prints counts)
python3 lab/checks.py --root . --section tracking
```

## The contract

A journey is one visitor session: utm params, a consent state, a `via_redirect` flag, and a list of steps (`page_view`, `form_view`, `form_submit`). The pipeline turns journeys + config into the events our CRM / GA4 / Meta pixel / Conversions API would receive.

1. Destinations are exactly `crm | ga4 | meta_pixel | capi`.
2. Event names are fixed: crm → `lead_created`, ga4 → `generate_lead`, meta_pixel → `Lead`, capi → `Lead`.
3. Every non-test journey that carries a `form_submit` step reaches the CRM **exactly once**.
4. Marketing destinations (`meta_pixel`, `capi`) fire **only** when `consent_state == "granted"`.
5. Test journeys (`is_test: true`) emit **nothing**.
6. A journey with two `form_submit` steps is one conversion, not two — deduplicate on `journey_id + destination + event_name`.
7. `occurred_at` is stored as a **UTC instant** (`YYYY-MM-DDTHH:MM:SSZ`). Journeys carry IST (`+05:30`) strings — convert them, never copy them.
8. `source` is normalised: trimmed, lowercased, and aliased — `fb→facebook`, `ig→instagram`, `googleads→google`.
9. `utm_campaign` survives the `/go/` redirect hop: when `via_redirect` is true, the hop strips any parameter not on the preserve list.
10. Only `form_submit` triggers emit events; `page_view` / `form_view` never do.

## Config schema — every field and its correct value

The kit ships `tracking/config/*.json` deliberately imperfect. Each file below is documented with the value it must hold; where your copy disagrees, your copy is wrong.

### tags.json

```json
{"tags": [
  {"tag_id": "tag-crm-lead",  "destination": "crm",        "trigger": "form_submit", "enabled": true},
  {"tag_id": "tag-ga4-lead",  "destination": "ga4",        "trigger": "form_submit", "enabled": true},
  {"tag_id": "tag-meta-lead", "destination": "meta_pixel", "trigger": "form_submit", "enabled": true},
  {"tag_id": "tag-capi-lead", "destination": "capi",       "trigger": "form_submit", "enabled": true}
]}
```

One tag per destination, every destination `enabled: true`, trigger `form_submit`. A disabled tag — or a missing destination — silently drops that destination's events.

### mapping.json

```json
{"form_submit": {"crm": "lead_created", "ga4": "generate_lead", "meta_pixel": "Lead", "capi": "Lead"}}
```

`mapping.json` is the authoritative event-name table. The four names above are the only conversion names in the contract; a destination mapped to any other name (e.g. `Purchase`) is wrong.

### dedup.json

```json
{"enabled": true, "key_fields": ["journey_id", "destination", "event_name"], "window_minutes": 10}
```

Deduplication must be enabled and keyed exactly on `journey_id + destination + event_name` — the double-submitting journeys must collapse to one event per destination (about 10% of journeys double-submit; without dedup the CRM receives two leads for one person).

### utm.json

```json
{"preserve_params": ["utm_source", "utm_medium", "utm_campaign", "utm_content"],
 "strip_on_redirect_paths": ["/go/"],
 "normalize_case": true,
 "source_aliases": {"fb": "facebook", "ig": "instagram", "googleads": "google"}}
```

- `preserve_params` must carry `utm_campaign` across the redirect hop; a preserve list missing it loses campaign attribution for every redirect journey.
- `normalize_case: true` lowercases values before they are stored.
- `source_aliases` must fold `fb→facebook`, `ig→instagram`, `googleads→google` so one source is one value.

### consent.json

```json
{"require_consent_for": ["meta_pixel", "capi"], "denied_behavior": "drop", "unknown_behavior": "drop_marketing"}
```

Marketing destinations require consent; denied journeys are dropped, unknown consent drops marketing only.

### filters.json

```json
{"exclude_test_journeys": true}
```

### timing.json

```json
{"store_as": "utc"}
```

## Output contract

`tracking/out/events.jsonl` — one JSON object per line:

```json
{"campaign_id": "m-1002", "destination": "crm", "event_id": "evt_00007", "event_name": "lead_created",
 "journey_id": "j-0003", "occurred_at": "2026-09-03T05:08:20Z", "source": "google"}
```

- `event_id` — assigned by the pipeline, sequential from `evt_00001`.
- `campaign_id` — the normalised `utm_campaign` (empty string when the journey carried none).
- `source` — the normalised `utm_source` (empty string when absent).
- `occurred_at` — the first `form_submit` step's timestamp, converted to UTC.

## Acceptance

`bash lab/replay.sh` must end with `9/9 checks passed` and exit 0. The nine checks are named after the rules above: `schema_valid`, `no_duplicate_events`, `event_name_contract`, `crm_completeness`, `consent_respected`, `test_journeys_excluded`, `campaign_preserved`, `timestamps_utc`, `source_normalized`. Passing is required but not sufficient — reviewers run a stricter private pass on top.
