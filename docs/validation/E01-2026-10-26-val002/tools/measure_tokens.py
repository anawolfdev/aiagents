#!/usr/bin/env python3
"""Measure token/cost usage from captured session tables.

Source: the `session` table (primary), captured by capture_sessions.py and
cross-checked with `opencode export`. No estimation, no invented rates.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

FIELDS = [
    "tokens_input",
    "tokens_output",
    "tokens_reasoning",
    "tokens_cache_read",
    "tokens_cache_write",
]


def totals(sessions: list[dict]) -> dict:
    out = {f: sum(s.get(f, 0) for s in sessions) for f in FIELDS}
    out["tokens_total"] = sum(out[f] for f in FIELDS)
    out["cost"] = sum(s.get("cost", 0) or 0 for s in sessions)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--actual-sessions", required=True)
    ap.add_argument("--simplificado-sessions", required=True)
    ap.add_argument("--out", required=True, help="medicion directory")
    ap.add_argument("--actual-cap", type=int, required=True)
    ap.add_argument("--simplificado-cap", type=int, required=True)
    ap.add_argument("--global-cap", type=int, required=True)
    args = ap.parse_args()

    actual = json.loads(Path(args.actual_sessions).read_text())
    simplificado = json.loads(Path(args.simplificado_sessions).read_text())
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    measured_at = datetime.now(timezone.utc)
    actual_totals = totals(actual["sessions"])
    simplificado_totals = totals(simplificado["sessions"])
    global_totals = {
        f: actual_totals[f] + simplificado_totals[f] for f in FIELDS
    }
    global_totals["tokens_total"] = actual_totals["tokens_total"] + simplificado_totals["tokens_total"]
    global_totals["cost"] = actual_totals["cost"] + simplificado_totals["cost"]

    max_updated = max(
        [s["time_updated"] for s in actual["sessions"] + simplificado["sessions"]]
    )
    max_updated_iso = datetime.fromtimestamp(max_updated / 1000, tz=timezone.utc)

    payload = {
        "measured_at": measured_at.isoformat(),
        "max_session_updated_at": max_updated_iso.isoformat(),
        "measured_at_after_all_exports": measured_at >= max_updated_iso,
        "source": "session table (primary) + opencode export",
        "cost_source": "OpenCode session.cost (reported, not an invoice)",
        "invoice_verified": False,
        "fields": FIELDS + ["tokens_total", "cost"],
        "caps": {
            "actual_total": args.actual_cap,
            "simplificado_total": args.simplificado_cap,
            "global": args.global_cap,
        },
        "flows": {
            "actual": {
                "root": actual["root"],
                "sandbox": actual["sandbox"],
                "sessions_count": len(actual["sessions"]),
                "duration_seconds": round(
                    (max(s["time_updated"] for s in actual["sessions"])
                     - min(s["time_created"] for s in actual["sessions"])) / 1000,
                    3,
                ),
                "sessions": actual["sessions"],
                "totals": actual_totals,
                "cap_used_fraction": actual_totals["tokens_total"] / args.actual_cap,
                "within_cap": actual_totals["tokens_total"] <= args.actual_cap,
            },
            "simplificado": {
                "root": simplificado["root"],
                "sandbox": simplificado["sandbox"],
                "sessions_count": len(simplificado["sessions"]),
                "duration_seconds": round(
                    (max(s["time_updated"] for s in simplificado["sessions"])
                     - min(s["time_created"] for s in simplificado["sessions"])) / 1000,
                    3,
                ),
                "sessions": simplificado["sessions"],
                "totals": simplificado_totals,
                "cap_used_fraction": simplificado_totals["tokens_total"] / args.simplificado_cap,
                "within_cap": simplificado_totals["tokens_total"] <= args.simplificado_cap,
            },
        },
        "global_totals": global_totals,
        "global_cap_used_fraction": global_totals["tokens_total"] / args.global_cap,
        "global_within_cap": global_totals["tokens_total"] <= args.global_cap,
    }
    (out / "tokens-coste.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")

    tsv = ["flow\tsession_id\tparent_id\tagent\tdirectory\tmodel\t" + "\t".join(FIELDS) + "\tcost\ttime_created\ttime_updated"]
    for flow, data in (("actual", actual), ("simplificado", simplificado)):
        for s in data["sessions"]:
            tsv.append("\t".join(str(x) for x in [
                flow,
                s["id"],
                s["parent_id"],
                s["agent"],
                s["directory"],
                f"{s['model'].get('providerID')}/{s['model'].get('id')}",
                *[s[f] for f in FIELDS],
                s["cost"],
                s["time_created_iso"],
                s["time_updated_iso"],
            ]))
    (out / "session-tree.tsv").write_text("\n".join(tsv) + "\n")

    with (out / "opencode-models.txt").open("w") as fh:
        subprocess.run(["opencode", "models", "--verbose"], stdout=fh, stderr=subprocess.STDOUT, check=False)
    with (out / "opencode-stats.txt").open("w") as fh:
        subprocess.run(["opencode", "stats"], stdout=fh, stderr=subprocess.STDOUT, check=False)

    print(json.dumps({
        "measured_at": payload["measured_at"],
        "max_session_updated_at": payload["max_session_updated_at"],
        "actual": actual_totals,
        "simplificado": simplificado_totals,
        "global": global_totals,
        "global_within_cap": payload["global_within_cap"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
