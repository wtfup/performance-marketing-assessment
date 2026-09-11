#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Acceptance checks for the Performance Marketing Operator Lab.

These are the CONTRACT, not the full grading. Passing every check means your artefacts are
structurally correct and the tracking pipeline honours the documented rules. Reviewers run a
stricter private grading pass on top of this.

Usage:
  python3 lab/checks.py --root . --section tracking
  python3 lab/checks.py --root . --section submission
  python3 lab/checks.py --root . --section all
Exit code: 0 when every selected check passes, 1 otherwise.
"""
import argparse, json, re, sys
from pathlib import Path

ALLOWED_EVENT_NAMES = {"lead_created", "generate_lead", "Lead"}
MARKETING = {"meta_pixel", "capi"}
DESTINATIONS = {"crm", "ga4", "meta_pixel", "capi"}


def load_events(root: Path):
    p = root / "tracking" / "out" / "events.jsonl"
    if not p.exists():
        raise SystemExit("no tracking/out/events.jsonl — run `bash lab/replay.sh` first")
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def load_journeys(root: Path):
    p = root / "tracking" / "journeys.jsonl"
    return {json.loads(l)["journey_id"]: json.loads(l)
            for l in p.read_text().splitlines() if l.strip()}


class Report:
    def __init__(self):
        self.rows = []

    def check(self, name, failures, detail=""):
        ok = not failures
        self.rows.append((name, ok, len(failures), detail))
        return ok

    def render(self):
        print(f"{'CHECK':38} {'RESULT':7} {'VIOLATIONS':>10}  DETAIL")
        print("-" * 100)
        for name, ok, n, detail in self.rows:
            print(f"{name:38} {'PASS' if ok else 'FAIL':7} {n:>10}  {detail}")
        bad = [r for r in self.rows if not r[1]]
        print("-" * 100)
        print(f"{len(self.rows) - len(bad)}/{len(self.rows)} checks passed")
        return 0 if not bad else 1


def check_tracking(root: Path):
    ev = load_events(root)
    jr = load_journeys(root)
    rep = Report()

    # 1 — schema
    bad = [e for e in ev if not isinstance(e, dict)
           or any(k not in e for k in ("event_id", "journey_id", "destination", "event_name", "occurred_at"))
           or e.get("destination") not in DESTINATIONS]
    rep.check("schema_valid", bad[:5], f"{len(bad)} malformed events")

    # 2 — no duplicate deliveries per (journey, destination, event)
    seen, dups = {}, []
    for e in ev:
        k = (e.get("journey_id"), e.get("destination"), e.get("event_name"))
        seen[k] = seen.get(k, 0) + 1
        if seen[k] == 2:
            dups.append(k)
    rep.check("no_duplicate_events", dups[:5], f"{len(dups)} duplicated (journey,destination,event) triples")

    # 3 — event-name contract
    bad = [e.get("event_name") for e in ev if e.get("event_name") not in ALLOWED_EVENT_NAMES]
    rep.check("event_name_contract", bad[:5], "allowed: " + ", ".join(sorted(ALLOWED_EVENT_NAMES)))

    # 4 — CRM completeness: every non-test form_submit journey reaches the CRM exactly once
    have = {}
    for e in ev:
        if e.get("destination") == "crm":
            have[e.get("journey_id")] = have.get(e.get("journey_id"), 0) + 1
    missing = [jid for jid, j in jr.items()
               if not j.get("is_test") and any(s.get("type") == "form_submit" for s in j.get("steps", []))
               and have.get(jid, 0) == 0]
    rep.check("crm_completeness", missing[:5], f"{len(missing)} form-submit journeys never reached the CRM")

    # 5 — consent: no marketing destination events for non-granted journeys
    viol = [e for e in ev if e.get("destination") in MARKETING
            and jr.get(e.get("journey_id"), {}).get("consent_state") != "granted"]
    rep.check("consent_respected", viol[:5], f"{len(viol)} marketing events fired without granted consent")

    # 6 — test journeys excluded
    viol = [e for e in ev if jr.get(e.get("journey_id"), {}).get("is_test")]
    rep.check("test_journeys_excluded", viol[:5], f"{len(viol)} events came from test journeys")

    # 7 — campaign attribution preserved for journeys that carried utm_campaign
    def expected_campaign(j):
        for p in j.get("params", []):
            if p.get("name") == "utm_campaign":
                return p.get("value")
        return None
    viol = []
    for e in ev:
        want = expected_campaign(jr.get(e.get("journey_id"), {}))
        if want and e.get("campaign_id") != want:
            viol.append((e.get("journey_id"), want, e.get("campaign_id")))
    rep.check("campaign_preserved", viol[:5], f"{len(viol)} events lost utm_campaign")

    # 8 — timestamps stored as UTC
    bad = [e.get("occurred_at") for e in ev
           if not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", str(e.get("occurred_at", "")))]
    rep.check("timestamps_utc", bad[:5], f"{len(bad)} events not in UTC ISO (…Z)")

    # 9 — source normalisation
    viol = []
    for e in ev:
        s = e.get("source", "")
        j = jr.get(e.get("journey_id"), {})
        raw = next((p.get("value") for p in j.get("params", []) if p.get("name") == "utm_source"), "")
        if raw and s != s.lower():
            viol.append((e.get("journey_id"), s))
    rep.check("source_normalized", viol[:5], f"{len(viol)} events carry a non-normalised source")

    return rep


REQUIRED_ANSWERS_KEYS = ["candidate_id", "window", "totals", "metrics", "per_campaign", "data_issues"]


def check_submission(root: Path):
    sub = root / "submission"
    rep = Report()
    for fname in ("answers.json", "decisions.json", "plan.json", "run.sh",
                  "RECON.md", "TRACKING_REPORT.md", "AUDIT.md"):
        rep.check(f"file_present::{fname}", [] if (sub / fname).exists() else [fname], "required submission artefact")
    for fname in ("answers.json", "decisions.json", "plan.json"):
        p = sub / fname
        if not p.exists():
            continue
        try:
            doc = json.loads(p.read_text())
            rep.check(f"json_valid::{fname}", [], "")
            if fname == "answers.json":
                missing = [k for k in REQUIRED_ANSWERS_KEYS if k not in doc]
                rep.check("answers_keys", missing[:5], "required top-level keys")
            if fname == "decisions.json":
                rows = doc.get("decisions") if isinstance(doc, dict) else None
                rep.check("decisions_shape", [] if isinstance(rows, list) and rows else ["decisions"],
                          "must be a non-empty list under 'decisions'")
            if fname == "plan.json":
                ok = isinstance(doc, dict) and isinstance(doc.get("allocation"), dict) \
                     and isinstance(doc.get("expected"), dict) and isinstance(doc.get("kill_rules"), list)
                rep.check("plan_shape", [] if ok else ["plan"], "needs allocation / expected / kill_rules")
        except Exception as ex:
            rep.check(f"json_valid::{fname}", [str(ex)], "invalid JSON")
    return rep


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--section", choices=["tracking", "submission", "all"], default="all")
    a = ap.parse_args()
    root = Path(a.root).resolve()
    rc = 0
    if a.section in ("tracking", "all"):
        print("== tracking acceptance ==")
        rc |= check_tracking(root).render()
    if a.section in ("submission", "all"):
        print("== submission acceptance ==")
        rc |= check_submission(root).render()
    sys.exit(rc)
