# Ads Lab — the browser-only test (Level 1)

**For performance-marketing hires. No installs, no Python, no terminal, no GitHub account.**
The candidate double-clicks three HTML files, works for about 100 minutes, and sends back three small JSON files.

| File | Station | What it proves | Time |
|---|---|---|---|
| `meta.html` | Meta build | Can he build three real campaigns — ₹24,000 all-access pass (lead-gen, human close), ₹100 daily pass through the app, and walk-in lead-gen for one Noida club — with correct objectives, budgets, audiences, placements, attribution, creative copy and UTM tracking? | ~35 min |
| `google.html` | Google build | Can he build a Search campaign — brand vs non-brand vs competitor ad groups, keywords and match types, negatives, a compliant responsive search ad, sitelinks, geo and bidding — and then fix five planted problems in a broken account? | ~30 min |
| `index.html` | Money & audit | Can he compute CPL / cost per qualified lead / CAC / ROAS / N2N (new-customer) ROAS from raw numbers, make the kill-fix-scale call, allocate ₹10,00,000 on marginal cost, and spot what is broken in a 10-row export? | ~35 min |

## How it works (anything else is decoration)

- **Everything runs in the browser.** Each file is self-contained: no server, no internet calls, no libraries. State is stored in that browser and can be exported as JSON at any time.
- **Candidate code.** HR gives each candidate a code (e.g. `WTF-PM-0007`). Every variable number — performance data, marginal cost bands, audit rows, the planted problems — is derived from that code, so two candidates never see the same numbers. Copying a colleague's answers produces a mismatch that the reviewer can detect by re-deriving the same values.
- **Live validation.** Each station shows the same rules the reviewer will check, updating as the candidate works. Failing checks are visible, never hidden — fixing them is part of the test.
- **Export.** Every station downloads `<station>-work.json` containing the candidate code, the built entities, the validation results, the score the page computed, and timestamps. The reviewer's score is the one that counts, and it is computed from the raw data in these files.
- **`Import`** restores a previously exported file, so a candidate can continue on another machine.

## What we are actually judging

1. **Executor or talker.** Can he produce a campaign structure that a platform would actually accept — objectives that match the goal, budgets that add up, audiences and placements that make sense, copy inside the limits?
2. **Does he know the products.** ₹24,000 pass, ₹100 daily pass, walk-in lead-gen, ₹45,000 course — different funnels, different maths, different kill rules. He must price the funnel, not the platform.
3. **Money brain.** CPL → close rate → CAC → ROAS, including new-customer (N2N) ROAS, and budget allocation by marginal cost — the single clearest signal of a real operator.
4. **What he refuses to do.** Each station asks for at least one thing he will NOT touch, and the audit contains healthy rows mixed with the broken ones. Kill-everything merchants are visible immediately.
5. **Defence.** A 15-minute call on his own files: he must explain every number and every setting without notes.

## For HR — what to send

1. The `ads-lab` folder as a zip (three files), or just the three files.
2. His candidate code, in one line: *"Your code is WTF-PM-00XX — type it at the top of each file."*
3. The message template (candidate instructions) — see the hiring kit.
4. Ask for: the three JSON files + screenshots of the Meta and Google builds, within 48 hours.

Reviewer guidance is separate (not in this repository).
