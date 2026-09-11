#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Canonical tracking pipeline — DO NOT EDIT.

Reads tracking/journeys.jsonl + tracking/config/*.json and writes tracking/out/events.jsonl,
the events our CRM / GA4 / Meta pixel / Conversions API would receive.

The pipeline is frozen: during verification it is replaced with the canonical copy, so
candidate edits to this file are ignored by construction. Fix the CONFIG, not the engine.

Config (tracking/config/):
  tags.json     {"tags":[{"tag_id","destination","trigger","enabled"}]}
  mapping.json  {event_type: {destination: event_name}}  — authoritative event names
  dedup.json    {"enabled": bool, "key_fields": [...], "window_minutes": int}
  utm.json      {"preserve_params":[...], "strip_on_redirect_paths":[...], "normalize_case": bool,
                 "source_aliases": {"fb":"facebook", ...}}
  consent.json  {"require_consent_for":[...], "denied_behavior":"drop|fire", "unknown_behavior":"drop_marketing|fire"}
  filters.json  {"exclude_test_journeys": bool}
  timing.json   {"store_as":"utc|local"}

Usage: python3 tracking/pipeline.py [--root .]
"""
import argparse, json
from pathlib import Path

DESTINATIONS = ("crm", "ga4", "meta_pixel", "capi")


def load_json(p: Path, default=None):
    if not p.exists():
        if default is None:
            raise SystemExit(f"missing config file: {p}")
        return default
    return json.loads(p.read_text())


def normalize_source(value, utm_cfg):
    v = value
    if utm_cfg.get("normalize_case", True):
        v = v.strip().lower()
    aliases = utm_cfg.get("source_aliases") or {}
    return aliases.get(v, v)


def collect_params(journey, utm_cfg):
    """Return {param_name: normalized_value} after redirect-strip + case rules."""
    preserve = set(utm_cfg.get("preserve_params") or [])
    via_redirect = bool(journey.get("via_redirect"))
    out = {}
    for p in journey.get("params", []):
        name = p.get("name", "")
        value = p.get("value", "")
        if via_redirect and name not in preserve:
            continue  # stripped by the redirect hop
        if utm_cfg.get("normalize_case", True):
            value = value.strip().lower()
        out[name] = value
    return out


def to_occurred_at(ts_iso, timing_cfg):
    if timing_cfg.get("store_as", "utc") == "utc":
        # journeys carry +05:30 ISO strings; store the UTC instant
        if ts_iso.endswith("+05:30"):
            hh, mm, ss = ts_iso[11:19].split(":")
            import datetime as dt
            local = dt.datetime(int(ts_iso[0:4]), int(ts_iso[5:7]), int(ts_iso[8:10]),
                                int(hh), int(mm), int(ss),
                                tzinfo=dt.timezone(dt.timedelta(hours=5, minutes=30)))
            return local.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        return ts_iso
    return ts_iso


def run(root: Path):
    cfg = root / "tracking" / "config"
    tags = load_json(cfg / "tags.json", {"tags": []})["tags"]
    mapping = load_json(cfg / "mapping.json", {})
    dedup = load_json(cfg / "dedup.json", {"enabled": False})
    utm_cfg = load_json(cfg / "utm.json", {})
    consent = load_json(cfg / "consent.json", {})
    filters = load_json(cfg / "filters.json", {"exclude_test_journeys": True})
    timing = load_json(cfg / "timing.json", {"store_as": "utc"})

    journeys = [json.loads(line) for line in (root / "tracking" / "journeys.jsonl").read_text().splitlines() if line.strip()]

    events = []
    seen = set()
    counts = {"journeys": 0, "events": 0, "skipped_test": 0, "skipped_consent": 0, "deduped": 0}

    for j in journeys:
        counts["journeys"] += 1
        if filters.get("exclude_test_journeys", True) and j.get("is_test"):
            counts["skipped_test"] += 1
            continue
        params = collect_params(j, utm_cfg)
        campaign_id = params.get("utm_campaign", "")
        source = normalize_source(params.get("utm_source", ""), utm_cfg) if params.get("utm_source") else ""
        for tag in tags:
            if not tag.get("enabled", True):
                continue
            trigger = tag.get("trigger")
            dest = tag.get("destination")
            matching_steps = [s for s in j.get("steps", []) if s.get("type") == trigger]
            if not matching_steps:
                continue
            if trigger != "form_submit":
                # non-conversion triggers never emit conversion events
                continue
            name = (mapping.get(trigger) or {}).get(dest)
            if not name:
                continue
            state = j.get("consent_state", "unknown")
            if dest in (consent.get("require_consent_for") or []):
                if state == "denied" and consent.get("denied_behavior", "drop") != "fire":
                    counts["skipped_consent"] += 1
                    continue
                if state == "unknown" and consent.get("unknown_behavior", "drop_marketing") != "fire":
                    counts["skipped_consent"] += 1
                    continue
            for step in matching_steps:
                if dedup.get("enabled", False):
                    kf = dedup.get("key_fields") or ["journey_id", "destination", "event_name"]
                    values = {"journey_id": j.get("journey_id"), "destination": dest, "event_name": name}
                    key = tuple((k, values.get(k, "")) for k in kf)
                    if key in seen:
                        counts["deduped"] += 1
                        continue
                    seen.add(key)
                events.append(dict(
                    event_id=f"evt_{len(events)+1:05d}",
                    journey_id=j.get("journey_id"),
                    destination=dest,
                    event_name=name,
                    occurred_at=to_occurred_at(step.get("ts", ""), timing),
                    campaign_id=campaign_id,
                    source=source,
                ))
                counts["events"] += 1

    out = root / "tracking" / "out"
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "events.jsonl", "w") as f:
        for e in events:
            f.write(json.dumps(e, sort_keys=True) + "\n")
    return counts


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    a = ap.parse_args()
    c = run(Path(a.root).resolve())
    print(json.dumps(c, indent=1))
