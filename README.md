# WTF Performance Marketing Assessment

Two levels. **Start with Level 1** — it is the one that matches a performance-marketing hire.

## Level 1 — Ads Lab (browser only, no installs) → [`ads-lab/`](ads-lab/)

The candidate opens three HTML files on any laptop and builds real campaign structures, does the
money maths on our products, and audits a messy account. No Python, no terminal, no accounts, no
internet. ~90 minutes, then a 15-minute defence call.

- `ads-lab/meta.html` — build the ₹24,000 all-access pass campaign, the ₹100 daily-pass app campaign, and Noida walk-in lead-gen.
- `ads-lab/google.html` — build a Search campaign (brand / non-brand / competitor, keywords, negatives, RSA, sitelinks, geo, bidding) and fix five planted account problems.
- `ads-lab/index.html` — CPL/CAC/ROAS maths on real-looking numbers, the kill-fix-scale call, ₹10,00,000 budget allocation by marginal cost, and a 10-row account audit.

Candidate code drives every variable number, so no two candidates see the same data.

## Level 2 — Operator Lab (advanced / senior hires, optional)

The deeper, terminal-based lab for candidates where data work and tracking forensics are part of the
job description (senior growth engineer, tracking lead, head of performance). Requires python3 and a
terminal: pull from a mock ad API, reconcile three messy sources, fix a broken tracking pipeline,
audit an export, build a plan, and defend it.

Start at [`candidate/00_START_HERE.md`](candidate/00_START_HERE.md). Everything is synthetic and
local; nothing here spends money or touches real accounts.

## Layout

- `ads-lab/` — Level 1: the three browser stations + their README (`ads-lab/README.md`). **Start here.**
- `candidate/` — Level 2 candidate documentation.
- `lab/` — Level 2 engine (mock ad API, acceptance checks, lab scripts) and `lab/ui/` (station design contract).
- `tracking/` — Level 2 tracking pipeline + fixed-config work.
- `submission/` — Level 2 artefact templates.
- `scripts/verify-submission.sh` — supervisor-side structural verification for Level 2.

## Rules that always apply

- Synthetic data only; no real customer data, credentials or ad accounts; nothing is ever deployed.
- Do not publish assessment work; do not share a kit or a candidate code.
- AI tools: allowed in Level 1 only if disclosed, and you must be able to explain your own numbers on the call. Level 2 has its own rules (Part 1 closed-book).
