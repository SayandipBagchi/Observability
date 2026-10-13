#!/usr/bin/env python3
"""Validate a tenant alert registry. No third-party dependencies. Exit 1 on any error.

Run:  python3 scripts/validate_registry.py tenants/<name>/alert-registry.csv

Schema and rationale: skills/observability/references/registry-schema.md.
Secret patterns are assembled from fragments so this file never matches a grep for them.
"""
from __future__ import annotations

import csv
import re
import sys
from collections import Counter

ENUMS = {
    "build_type": {"native_alert", "sentinel_flow", "system_alert_subscription", "out_of_moengage"},
    "build_status": {"live", "paused", "not_built", "build_ask", "retired", "unverified"},
    "severity": {"P1", "P2", "P3", "Build ask", ""},
}
REQUIRED = ["alert_id", "prd_ref", "module", "kpi", "severity", "build_type", "trigger",
            "threshold_decision", "baseline", "cadence_or_wait", "journey", "moengage_name",
            "moengage_id", "replaced_ids", "build_status", "verified_on", "verified_how",
            "acquisition_dependent", "notes"]
ID_RE = re.compile(r"^[A-Z]{3}-[A-Z]?\d{1,2}[a-z]?$")
HEX24_FULL = re.compile(r"[0-9a-f]{24}")
HEX24 = re.compile(r"\b[0-9a-f]{24}\b")
# URL, the intake signature parameter, Logic Apps / Power Automate hosts, SAS-style params.
SECRET = re.compile(
    r"(https?://|\bs" r"ig=|logic[.]azure|power" r"automate[.]com|[?&]sv=|[?&]sp=)", re.I)
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:[.][\w-]+)+")
# Qualifying filters must be positive enumerations (gate A2b).
NEGATIVE = re.compile(r"(is not empty|\bnot in\b|!=|does not contain)", re.I)
WAIVER = "exclusion-approved:"
ONE_DOT_LEADER = "․"


def split_chain(value: str) -> list[str]:
    """Split replaced_ids on ';' outside parentheses: a reason may itself contain ';'."""
    parts, depth, cur = [], 0, []
    for ch in value:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if ch == ";" and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    return [p for p in parts if p.strip()]


def main(path: str) -> int:
    errs: list[str] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED if c not in (reader.fieldnames or [])]
        if missing:
            print(f"ERROR missing columns: {missing}")
            return 1
        rows = list(reader)

    ids = Counter(x["alert_id"] for x in rows)
    for dup in [k for k, v in ids.items() if v > 1]:
        errs.append(f"duplicate alert_id {dup}")

    for i, x in enumerate(rows, start=2):
        aid = x["alert_id"]
        if not ID_RE.match(aid):
            errs.append(f"L{i} bad alert_id {aid!r}")
        for col, allowed in ENUMS.items():
            if x[col] not in allowed:
                errs.append(f"L{i} {aid} {col}={x[col]!r} not in {sorted(allowed)}")

        live = x["build_status"] == "live"
        flow = x["build_type"] == "sentinel_flow"
        if flow and live:
            if not HEX24_FULL.fullmatch(x["moengage_id"]):
                errs.append(f"L{i} {aid} live flow needs a 24-hex moengage_id")
            if not x["journey"]:
                errs.append(f"L{i} {aid} live flow needs a journey")
            neg = NEGATIVE.search(x["trigger"])
            if neg and WAIVER not in x["notes"]:
                errs.append(f"L{i} {aid} live flow trigger uses a negative filter ({neg.group(0)!r}); "
                            f"rewrite as a positive enumeration or record '{WAIVER}' in notes (gate A2b)")
            if "ref=" not in x["notes"] and "no ref" not in x["notes"]:
                errs.append(f"L{i} {aid} live flow notes must record the payload decision "
                            f"('ref=<stored path>' or 'no ref')")
        if live and not x["moengage_name"]:
            errs.append(f"L{i} {aid} live object needs moengage_name")
        if x["build_status"] in {"live", "retired", "unverified"} and not (x["verified_on"] and x["verified_how"]):
            errs.append(f"L{i} {aid} needs verified_on and verified_how")

        if x["replaced_ids"].strip():
            for n, entry in enumerate(split_chain(x["replaced_ids"]), start=1):
                if not HEX24.search(entry):
                    errs.append(f"L{i} {aid} replaced_ids entry {n} has no 24-hex MoEngage ID: {entry.strip()!r}")
            if x["moengage_id"] and x["moengage_id"] in x["replaced_ids"]:
                errs.append(f"L{i} {aid} live moengage_id also appears in replaced_ids")

        for col, val in x.items():
            if not val:
                continue
            if SECRET.search(val):
                errs.append(f"L{i} {aid} {col} contains a URL or secret-like pattern")
            if EMAIL.search(val):
                errs.append(f"L{i} {aid} {col} contains an email address; recipients live only in config.json")
            if ONE_DOT_LEADER in val:
                errs.append(f"L{i} {aid} {col} contains U+2024; stored ref paths use ASCII dots")

    counts = Counter((x["build_type"], x["build_status"]) for x in rows)
    for e in errs:
        print("ERROR", e)
    print(f"{len(rows)} rows; " + "; ".join(f"{k[0]}/{k[1]}={v}" for k, v in sorted(counts.items())))
    chains = sum(1 for x in rows if x["replaced_ids"].strip())
    links = sum(len(split_chain(x["replaced_ids"])) for x in rows)
    waivers = sum(1 for x in rows if WAIVER in x["notes"])
    print(f"replace chains: {chains} rows, {links} links; exclusion waivers: {waivers}")
    print("OK" if not errs else f"{len(errs)} error(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: validate_registry.py tenants/<name>/alert-registry.csv")
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
