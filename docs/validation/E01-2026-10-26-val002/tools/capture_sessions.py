#!/usr/bin/env python3
"""Capture an OpenCode session tree, exports and child-session proof.

Read-only over the OpenCode database. Writes JSON/Markdown artifacts to --out.
Fails (exit 1) when the captured tree does not satisfy the validity checks.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

DB = Path.home() / ".local/share/opencode/opencode.db"
EXPECTED_MODEL = {"id": "big-pickle", "providerID": "opencode"}


def iso(epoch_ms: int | None) -> str | None:
    if epoch_ms is None:
        return None
    return datetime.fromtimestamp(epoch_ms / 1000, tz=timezone.utc).isoformat()


def connect() -> sqlite3.Connection:
    return sqlite3.connect(f"file:{DB}?mode=ro", uri=True)


def tree_rows(conn: sqlite3.Connection, root: str) -> list[sqlite3.Row]:
    conn.row_factory = sqlite3.Row
    sql = """
    WITH RECURSIVE tree(id) AS (
      SELECT ?
      UNION ALL
      SELECT s.id FROM session s JOIN tree t ON s.parent_id = t.id
    )
    SELECT id, parent_id, agent, title, directory, model,
           tokens_input, tokens_output, tokens_reasoning,
           tokens_cache_read, tokens_cache_write, cost,
           time_created, time_updated
    FROM session
    WHERE id IN (SELECT id FROM tree)
    ORDER BY time_created
    """
    return list(conn.execute(sql, (root,)))


def find_root(conn: sqlite3.Connection, directory: str, title: str) -> str:
    row = conn.execute(
        "select id from session where directory=? and title=? "
        "order by time_created desc limit 1",
        (directory, title),
    ).fetchone()
    if not row:
        raise SystemExit(f"no root session for directory={directory!r} title={title!r}")
    return row[0]


def parse_model(raw: str | None) -> dict:
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw": raw}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", help="root session id (overrides --directory/--title)")
    ap.add_argument("--directory", help="sandbox directory used to find the root")
    ap.add_argument("--title", help="unique title used to find the root")
    ap.add_argument("--sandbox", required=True, help="expected sandbox directory")
    ap.add_argument("--out", required=True, help="output directory")
    ap.add_argument("--expect-agent", action="append", default=[],
                    help="agent that must be present (repeatable)")
    ap.add_argument("--allow-root-only", action="store_true",
                    help="for the comparator: only one a1 session, no children")
    args = ap.parse_args()

    sandbox = os.path.realpath(args.sandbox)
    out = Path(args.out)
    exports = out / "exports"
    exports.mkdir(parents=True, exist_ok=True)

    conn = connect()
    root_id = args.root
    if not root_id:
        if not args.directory or not args.title:
            raise SystemExit("--root or (--directory and --title) is required")
        root_id = find_root(conn, args.directory, args.title)

    rows = tree_rows(conn, root_id)
    if not rows:
        raise SystemExit(f"root session not found: {root_id}")

    sessions = []
    for row in rows:
        model = parse_model(row["model"])
        sessions.append({
            "id": row["id"],
            "parent_id": row["parent_id"],
            "agent": row["agent"],
            "title": row["title"],
            "directory": row["directory"],
            "model": model,
            "tokens_input": row["tokens_input"],
            "tokens_output": row["tokens_output"],
            "tokens_reasoning": row["tokens_reasoning"],
            "tokens_cache_read": row["tokens_cache_read"],
            "tokens_cache_write": row["tokens_cache_write"],
            "cost": row["cost"],
            "time_created": row["time_created"],
            "time_created_iso": iso(row["time_created"]),
            "time_updated": row["time_updated"],
            "time_updated_iso": iso(row["time_updated"]),
        })

    payload = {
        "root": root_id,
        "sandbox": sandbox,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "sessions": sessions,
        "children_count": len(sessions) - 1,
    }
    (out / "sessions.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")

    lines = [f"root {root_id} ({sessions[0]['agent']}) directory={sessions[0]['directory']}"]
    for s in sessions[1:]:
        lines.append(
            f"  child {s['id']} agent={s['agent']} parent={s['parent_id']} "
            f"directory={s['directory']} model={s['model'].get('id')}/{s['model'].get('providerID')}"
        )
    (out / "tree.txt").write_text("\n".join(lines) + "\n")

    export_errors = []
    for s in sessions:
        target = exports / f"{s['id']}.json"
        with target.open("wb") as fh:
            proc = subprocess.run(
                ["opencode", "export", s["id"]],
                stdout=fh,
                stderr=subprocess.PIPE,
                check=False,
            )
        if proc.returncode != 0:
            export_errors.append({
                "id": s["id"],
                "returncode": proc.returncode,
                "stderr": proc.stderr.decode("utf-8", "replace"),
            })

    # Child proof: task parts in the root export that point to real child sessions.
    root_export = json.loads((exports / f"{root_id}.json").read_text())
    task_links = []
    for message in root_export.get("messages", []):
        for part in message.get("parts", []):
            if part.get("type") != "tool" or part.get("tool") != "task":
                continue
            state = part.get("state") or {}
            metadata = state.get("metadata") or {}
            inp = state.get("input") or {}
            task_links.append({
                "callID": part.get("callID"),
                "description": inp.get("description"),
                "subagent_type": inp.get("subagent_type"),
                "child_session_id": metadata.get("sessionId"),
                "parent_session_id": metadata.get("parentSessionId"),
                "status": state.get("status"),
            })

    child_ids = {s["id"] for s in sessions if s["parent_id"]}
    linked_ids = {t["child_session_id"] for t in task_links if t.get("child_session_id")}
    export_parent_ids = {}
    for s in sessions[1:]:
        try:
            child_export = json.loads((exports / f"{s['id']}.json").read_text())
            export_parent_ids[s["id"]] = (child_export.get("info") or {}).get("parentID")
        except Exception as exc:  # pragma: no cover - evidence path
            export_parent_ids[s["id"]] = f"ERROR: {exc}"

    proof = {
        "root": root_id,
        "task_links": task_links,
        "db_children": sorted(child_ids),
        "linked_children": sorted(linked_ids),
        "missing_in_task_parts": sorted(child_ids - linked_ids),
        "missing_in_db": sorted(linked_ids - child_ids),
        "export_parent_ids": export_parent_ids,
        "all_exports_present": not export_errors and all(
            (exports / f"{s['id']}.json").exists() for s in sessions
        ),
        "export_errors": export_errors,
    }
    (out / "child-proof.json").write_text(json.dumps(proof, indent=2, ensure_ascii=False) + "\n")

    problems = []
    if export_errors:
        problems.append(f"export errors: {export_errors}")
    for s in sessions:
        if os.path.realpath(s["directory"]) != sandbox:
            problems.append(f"{s['id']} directory={s['directory']!r} != {sandbox!r}")
        model = s["model"]
        if model.get("id") != EXPECTED_MODEL["id"] or model.get("providerID") != EXPECTED_MODEL["providerID"]:
            problems.append(f"{s['id']} model={model!r}")
    if sessions[0]["parent_id"]:
        problems.append(f"root has parent_id={sessions[0]['parent_id']!r}")
    for cid in child_ids:
        if cid not in linked_ids:
            problems.append(f"child {cid} is not linked from a root task part")
    for cid, pid in export_parent_ids.items():
        if pid != root_id:
            problems.append(f"export of {cid} has parentID={pid!r}, expected {root_id!r}")

    if args.allow_root_only:
        if len(sessions) != 1:
            problems.append(f"expected exactly one session, got {len(sessions)}")
        if sessions[0]["agent"] != "a1":
            problems.append(f"expected agent a1, got {sessions[0]['agent']!r}")
    elif args.expect_agent:
        present = {s["agent"] for s in sessions}
        missing = sorted(set(args.expect_agent) - present)
        if missing:
            problems.append(f"missing agents: {missing}; present={sorted(present)}")
        for a in args.expect_agent:
            sid = next((s["id"] for s in sessions if s["agent"] == a), None)
            if sid and sid != root_id:
                s = next(s for s in sessions if s["id"] == sid)
                if not s["parent_id"]:
                    problems.append(f"agent {a} session {sid} has no parent_id")

    summary = {
        "root": root_id,
        "sessions": len(sessions),
        "children": len(sessions) - 1,
        "agents": [s["agent"] for s in sessions],
        "sandbox": sandbox,
        "valid": not problems,
        "problems": problems,
    }
    (out / "capture-summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
