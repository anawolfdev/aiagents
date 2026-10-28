#!/usr/bin/env python3
"""Run `opencode run` under a real token/time cap.

The cap is checked against the recursive session tree in the OpenCode database
(input + output + reasoning + cache_read + cache_write). At 80% it records a
warning; at 100% it sends SIGINT, waits, then SIGKILL. It never estimates.
"""
from __future__ import annotations

import argparse
import json
import os
import signal
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

DB = Path.home() / ".local/share/opencode/opencode.db"
FIELDS = [
    "tokens_input",
    "tokens_output",
    "tokens_reasoning",
    "tokens_cache_read",
    "tokens_cache_write",
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def find_root(directory: str, title: str, timeout: float = 90.0) -> str | None:
    end = time.time() + timeout
    while time.time() < end:
        conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
        row = conn.execute(
            "select id from session where directory=? and title=? "
            "order by time_created desc limit 1",
            (directory, title),
        ).fetchone()
        conn.close()
        if row:
            return row[0]
        time.sleep(1)
    return None


def tree_tokens(root: str) -> int:
    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    sql = """
    WITH RECURSIVE tree(id) AS (
      SELECT ?
      UNION ALL
      SELECT s.id FROM session s JOIN tree t ON s.parent_id = t.id
    )
    SELECT coalesce(sum(tokens_input),0), coalesce(sum(tokens_output),0),
           coalesce(sum(tokens_reasoning),0), coalesce(sum(tokens_cache_read),0),
           coalesce(sum(tokens_cache_write),0)
    FROM session WHERE id IN (SELECT id FROM tree)
    """
    row = conn.execute(sql, (root,)).fetchone()
    conn.close()
    return sum(int(x or 0) for x in row)


def tree_sessions(root: str) -> list[tuple]:
    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    sql = """
    WITH RECURSIVE tree(id) AS (
      SELECT ?
      UNION ALL
      SELECT s.id FROM session s JOIN tree t ON s.parent_id = t.id
    )
    SELECT id, parent_id, agent FROM session WHERE id IN (SELECT id FROM tree)
    ORDER BY time_created
    """
    rows = list(conn.execute(sql, (root,)))
    conn.close()
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--agent", required=True)
    ap.add_argument("--model", default="opencode/big-pickle")
    ap.add_argument("--title", help="title for a new root session")
    ap.add_argument("--continue-session", help="continue this session id")
    ap.add_argument("--root-session", help="known root session id")
    ap.add_argument("--input-file", required=True)
    ap.add_argument("--out-events", required=True)
    ap.add_argument("--out-stderr", required=True)
    ap.add_argument("--monitor-log", required=True)
    ap.add_argument("--status-json", required=True)
    ap.add_argument("--cap-tokens", type=int, required=True)
    ap.add_argument("--cap-seconds", type=int, required=True)
    ap.add_argument("--poll-seconds", type=float, default=10.0)
    args = ap.parse_args()

    directory = os.path.realpath(args.dir)
    message = Path(args.input_file).read_text().rstrip("\n")
    cmd = ["opencode", "run", "--agent", args.agent, "--model", args.model, "--format", "json"]
    if args.continue_session:
        cmd += ["--session", args.continue_session]
    elif args.title:
        cmd += ["--title", args.title]
    cmd.append(message)

    root = args.root_session or args.continue_session

    events = Path(args.out_events)
    stderr = Path(args.out_stderr)
    monitor = Path(args.monitor_log)
    for p in (events, stderr, monitor):
        p.parent.mkdir(parents=True, exist_ok=True)

    started = time.time()
    status = {
        "root": root,
        "directory": directory,
        "agent": args.agent,
        "model": args.model,
        "title": args.title,
        "continue_session": args.continue_session,
        "command": cmd[:-1] + ["<input>"],
        "input_file": args.input_file,
        "input_sha256_note": "see pre-registro.md",
        "cap_tokens": args.cap_tokens,
        "cap_seconds": args.cap_seconds,
        "started_at": now(),
        "warnings": [],
        "aborted_by_cap": None,
        "exit_code": None,
        "final_tokens": None,
        "elapsed_seconds": None,
        "sessions": [],
    }

    env = os.environ.copy()
    with events.open("wb") as out_fh, stderr.open("wb") as err_fh, monitor.open("a") as mon:
        mon.write(f"{now()} start root={root} cap_tokens={args.cap_tokens} cap_seconds={args.cap_seconds}\n")
        proc = subprocess.Popen(
            cmd,
            cwd=directory,
            env=env,
            stdout=out_fh,
            stderr=err_fh,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )
        warned80 = False
        aborted = None
        while proc.poll() is None:
            elapsed = time.time() - started
            if not root and args.title:
                root = find_root(directory, args.title, timeout=1.0)
                if root:
                    status["root"] = root
                    mon.write(f"{now()} root discovered {root}\n")
                    mon.flush()
            if not root:
                time.sleep(args.poll_seconds)
                continue
            tokens = tree_tokens(root)
            frac = tokens / args.cap_tokens if args.cap_tokens else 0
            if frac >= 0.8 and not warned80:
                warned80 = True
                msg = (f"{now()} WARN_80 tokens={tokens} cap={args.cap_tokens} "
                       f"fraction={frac:.4f} elapsed={elapsed:.1f}s")
                status["warnings"].append(msg)
                mon.write(msg + "\n")
                mon.flush()
            if tokens >= args.cap_tokens:
                aborted = "tokens"
            elif elapsed >= args.cap_seconds:
                aborted = "time"
            if aborted:
                status["aborted_by_cap"] = aborted
                mon.write(f"{now()} ABORT cap={aborted} tokens={tokens} elapsed={elapsed:.1f}s\n")
                mon.flush()
                try:
                    os.killpg(proc.pid, signal.SIGINT)
                except ProcessLookupError:
                    pass
                deadline = time.time() + 60
                while proc.poll() is None and time.time() < deadline:
                    time.sleep(1)
                if proc.poll() is None:
                    try:
                        os.killpg(proc.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                break
            time.sleep(args.poll_seconds)
        try:
            rc = proc.wait(timeout=30)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            rc = proc.wait()
        mon.write(f"{now()} exit rc={rc} aborted={aborted}\n")

    elapsed = time.time() - started
    if not root and args.title:
        root = find_root(directory, args.title, timeout=5.0)
        status["root"] = root
    if not root:
        status.update({
            "finished_at": now(),
            "exit_code": rc,
            "final_tokens": 0,
            "elapsed_seconds": round(elapsed, 3),
            "error": "root session never appeared",
        })
        Path(args.status_json).write_text(json.dumps(status, indent=2, ensure_ascii=False) + "\n")
        print(json.dumps(status, indent=2, ensure_ascii=False))
        return 2
    tokens = tree_tokens(root)
    status.update({
        "finished_at": now(),
        "exit_code": rc,
        "final_tokens": tokens,
        "final_cap_fraction": tokens / args.cap_tokens if args.cap_tokens else None,
        "elapsed_seconds": round(elapsed, 3),
        "sessions": [
            {"id": r[0], "parent_id": r[1], "agent": r[2]} for r in tree_sessions(root)
        ],
        "events_file": str(events),
        "stderr_file": str(stderr),
        "monitor_log": str(monitor),
    })
    Path(args.status_json).write_text(json.dumps(status, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(status, indent=2, ensure_ascii=False))
    return 0 if aborted is None else 3


if __name__ == "__main__":
    sys.exit(main())
