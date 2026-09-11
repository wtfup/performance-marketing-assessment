# Live Defence (15 minutes, separate round)

A short, closed-book drill-down after your submission is reviewed. It is scored separately (10 points, see `05_RULES_AND_SCORING.md`) and it is where hand-built numbers fall apart or hold up.

## Format

- Screen-share your repository. Closed-book: no AI, no internet, no notes beyond what is in your repo.
- The reviewer drives; you walk through your own artefacts while they drill into detail.
- 15 minutes. Answer with numbers, not adjectives. "I don't know, here is how I would find out" beats guessing.

## What you will be asked to do

- Run `bash lab/replay.sh` live and explain what it proves (and what it does not).
- Take one metric — e.g. blended CPL or CAC — end to end from raw data: show the rows, the filters, the arithmetic, the result. Your `answers.json` number must match what you just did live.
- Show a raw page under `submission/raw/` and reconcile it to `pull_proof.json`.
- Walk each tracking config you changed: what it said, what it says now, which contract rule the old value violated, and what would have shipped to GA4 / Meta / the CRM if you had left it.
- Defend two decisions from `decisions.json`: the evidence numbers first, then the action, then the expected impact. Expect a follow-up of the form "what would change your mind?"
- Defend the allocation in `plan.json`: which band segments you funded and why, how the expected numbers were computed, and where the plan breaks if your assumptions are wrong.
- One open question: "what would you do with another week?"

## How to prepare

- Make `submission/run.sh` regenerate everything end to end, then run it once more the night before. You will be asked to demonstrate reproducibility.
- Know your headline numbers cold: totals, the six metrics, biggest data issue, top two decisions, and the allocation with its expected block.
- Be able to show your work for anything you assert. If you scripted a computation, be ready to explain the script line by line.
- Prepare for at least one adversarial question. The reviewer will push on the places where candidates most often slip; if you avoided one, be able to say why without hedging.
