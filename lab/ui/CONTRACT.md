# Station contract (v2 — STANDALONE / browser-only). Supersedes v1 entirely.

**The candidate is a performance marketer, not a developer.** No server, no python, no terminal, no
install. Each station is ONE self-contained HTML file that works by double-clicking it (file://).
All state and all validation live inside the file. External network calls are forbidden; there must
be no `http://` or `https://` resource loads anywhere in the file.

Deliverable files (siblings in the same folder, e.g. `ads-lab/`):
- `index.html` — instructions + money station + audit station + "what to send back" (parent-owned)
- `meta.html` — the Meta build station (you own this)
- `google.html` — the Google build station (you own this)

## How a station works (all three behave the same)

1. **Candidate code** — a text box at the top (`e.g. WTF-PM-0007`). Everything variable in the file
   is derived from it with the shared helper below, so no two candidates see the same numbers.
   Persisted with `localStorage.setItem('adsLab.code', code)`; read on load. If a station has no
   candidate-variable content it still shows the code box in the header.
2. **Brief panel** — the task, in plain language, with the exact deliverables listed.
3. **The work surface** — the mock product UI (table + create/edit drawer), fully client-side.
4. **Live validation** — the same rules the reviewer will check, shown as a pass/fail list that
   updates on every change. Do NOT hide failures; show the field-level reason.
5. **Export** — a button that downloads `<station>-work.json` containing everything (candidate code,
   the built entities, the validation results, the timestamps) plus a "Print / Save as PDF" hint.
   The candidate sends back the one JSON file per station and (optionally) screenshots.
6. **Autosave** — `localStorage.setItem('adsLab.<station>', JSON.stringify(state))` on every change,
   restored on load, with a "Reset station" button that asks for confirmation first.

## Candidate-code seeding helper (copy verbatim into every station)

```js
function adsLabSeed(code){
  const s = String(code || 'WTF-PM-0000').trim().toUpperCase();
  let h = 2166136261 >>> 0;
  for (let i = 0; i < s.length; i++){ h ^= s.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; }
  return function(){ // mulberry32
    h |= 0; h = h + 0x6D2B79F5 | 0;
    let t = Math.imul(h ^ h >>> 15, 1 | h);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}
const rnd = adsLabSeed(code);           // rnd() → 0..1, deterministic per candidate code
const pick = (arr) => arr[Math.floor(rnd() * arr.length)];
```

## Meta station (`meta.html`) — what the candidate must produce

Three build tasks, each shown as its own tab, each with its own validation list. All three are
Meta-UI work: objective, budget, bid strategy, audiences, placements, attribution, creative, UTM.

- **T1 — High-ticket ₹24,000 all-access pass (sold online, human closes on WhatsApp/call).**
  Objective Leads; optimisation goal Lead; WhatsApp or call CTA; 7-day-click/1-day-view attribution;
  two ad sets (a broad prospecting set and a retargeting set using the excluded-customers list);
  three ads with different angles; URL parameters that survive (`utm_source=facebook`,
  `utm_medium=paid_social`, `utm_campaign`, `utm_content`).
- **T2 — ₹100 daily all-access pass sold through the app.** Objective Sales/Leads per the brief's
  instruction; app-friendly CTA; broader audience; budget scaled to the brief's per-day target;
  creative written for impulse purchase (₹100 framing); correct conversion event.
- **T3 — Gym walk-in lead generation for one Noida club.** Instant-form-style lead flow
  (Lead optimisation, lower-funnel placement choice), geo radius targeting, attribution set, and
  the exclusion of current members.

**Meta rules the station must validate client-side** (mirror the real product):
- primary text recommended ≤125 (hard 2200), headline ≤40 (hard 255), description ≤25 (hard 255) —
  show live counters and mark over-recommendation amber, over-hard-limit red (block export until
  hard limits are respected).
- campaign → ad set → ad hierarchy must be respected; a campaign with campaign-level budget must not
  also carry ad-set budgets.
- auction buying; bid strategy from {Highest volume, Cost per result goal, ROAS goal, Bid cap};
  Cost per result goal requires a value > 0.
- ad set needs: optimisation goal, billing event, attribution setting, conversion event, target
  geo (non-empty), age range inside 18–65, at least one excluded audience for the retargeting-trap
  check.
- placements: the brief for T3 requires Advantage+ placements OFF and Audience Network excluded;
  the station flags otherwise.
- URL parameters: must contain utm_source and utm_campaign; the file must warn when a parameter is
  missing (that is the planted trap: `{{campaign.name}}` dynamic tokens are expected).

## Google station (`google.html`) — what the candidate must produce

- **G1 — Search campaign for walk-in leads (one club, Noida NCR).** Ad groups split by intent
  (brand vs non-brand vs competitor), ≥5 keywords per group with correct match types, ≥8 negatives
  for the non-brand group (brand terms + irrelevant terms), RSA with ≥8 headlines (≤30 chars) and
  ≥3 descriptions (≤90 chars), ≥4 sitelinks, geo = Noida + NCR districts, language = English,
  networks = Search only, and the bid strategy the brief dictates given the stated conversion volume.
- **G2 — The account-health fixes** on a pre-loaded, broken account (planted): RSA with 2 headlines,
  a broad keyword with no negatives, geo set to all of India, a conversion action that is not primary
  for the goal, and a target CPA of 0. The station must show the broken account and let the candidate
  fix it in place; validation re-checks after every edit.

**Google rules to validate client-side:** RSA max 15 headlines (30 chars each) / max 4 descriptions
(90 chars each) and min 3 headlines / 2 descriptions; sitelink text ≤25 chars; match types
{broad, phrase, exact} plus negatives; `Target CPA` requires target_cpa > 0; Search campaigns need
geo + language + network settings; conversion actions carry a primary-for-goal flag.

## Anti-cheat & scoring (both stations)

- Per-candidate numbers and the planted-problem set derive from the candidate code — copying a
  friend's answers produces a mismatch, and the reviewer re-derives the same values to check.
- The station computes its own score for the objective checks and writes it into the export
  (`"score": {...}`) — but the reviewer's score is the one that counts; the export carries the raw
  entity data so a human can re-check every field.
- No external requests, no analytics, no CDN, no fonts from the internet. Everything inline.
