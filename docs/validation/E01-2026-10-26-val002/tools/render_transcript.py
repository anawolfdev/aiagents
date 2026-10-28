#!/usr/bin/env python3
"""Render the full OpenCode exports of a captured tree to Markdown.

The JSON exports are the primary transcript. This Markdown is a readable
representation and keeps every message and part, including tool inputs/outputs.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def ts(value) -> str:
    if value is None:
        return "-"
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value / 1000, tz=timezone.utc).isoformat()
    return str(value)


def fence(text: str, lang: str = "") -> str:
    text = "" if text is None else str(text)
    return f"```{lang}\n{text}\n```"


def render_part(part: dict, out: list[str]) -> None:
    ptype = part.get("type", "?")
    if ptype in {"text", "reasoning"}:
        label = "Texto" if ptype == "text" else "Razonamiento"
        out.append(f"#### {label}\n")
        out.append(part.get("text", ""))
        out.append("")
        return
    if ptype == "tool":
        tool = part.get("tool", "?")
        state = part.get("state") or {}
        out.append(f"#### Tool `{tool}` — estado `{state.get('status')}`\n")
        inp = state.get("input")
        if inp is not None:
            out.append("Entrada:\n")
            out.append(fence(json.dumps(inp, indent=2, ensure_ascii=False), "json"))
        meta = state.get("metadata")
        if meta:
            out.append("Metadata:\n")
            out.append(fence(json.dumps(meta, indent=2, ensure_ascii=False), "json"))
        output = state.get("output")
        if output is not None:
            out.append("Salida:\n")
            out.append(fence(output))
        error = state.get("error")
        if error:
            out.append("Error:\n")
            out.append(fence(json.dumps(error, indent=2, ensure_ascii=False), "json"))
        out.append("")
        return
    if ptype in {"step-start", "step-finish", "snapshot", "patch", "file", "agent", "subtask"}:
        out.append(f"#### Part `{ptype}`\n")
        out.append(fence(json.dumps(part, indent=2, ensure_ascii=False), "json"))
        out.append("")
        return
    # Unknown part: preserve it, never drop content.
    out.append(f"#### Part `{ptype}`\n")
    out.append(fence(json.dumps(part, indent=2, ensure_ascii=False), "json"))
    out.append("")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sessions", required=True, help="sessions.json from capture_sessions.py")
    ap.add_argument("--exports", required=True, help="exports directory")
    ap.add_argument("--out", required=True, help="transcript.md path")
    ap.add_argument("--flow", required=True, help="flow label")
    args = ap.parse_args()

    data = json.loads(Path(args.sessions).read_text())
    exports = Path(args.exports)
    lines = [
        f"# Transcripción completa — {args.flow}",
        "",
        f"- **Root session:** `{data['root']}`",
        f"- **Sandbox:** `{data['sandbox']}`",
        f"- **Capturada:** {data.get('captured_at')}",
        f"- **Sesiones:** {len(data['sessions'])}",
        "",
        "> Fuente primaria: `exports/*.json` (export íntegro de OpenCode).",
        "> Este Markdown conserva todos los mensajes y partes; no se recorta texto.",
        "",
        "## Árbol",
        "",
        "```text",
    ]
    for s in data["sessions"]:
        indent = "  " if s["parent_id"] else ""
        lines.append(
            f"{indent}{s['id']} agent={s['agent']} parent={s['parent_id']} "
            f"model={s['model'].get('id')}/{s['model'].get('providerID')} "
            f"directory={s['directory']}"
        )
    lines += ["```", ""]

    for s in data["sessions"]:
        export_path = exports / f"{s['id']}.json"
        if not export_path.exists():
            lines += [f"## {s['id']}", "", "_Export ausente._", ""]
            continue
        export = json.loads(export_path.read_text())
        info = export.get("info") or {}
        lines += [
            f"## Sesión `{s['id']}` — `{s['agent']}`",
            "",
            f"- **parentID:** `{info.get('parentID')}`",
            f"- **directory:** `{info.get('directory')}`",
            f"- **title:** {info.get('title')!r}",
            f"- **model:** `{(info.get('model') or {}).get('providerID')}/{(info.get('model') or {}).get('id')}`",
            f"- **created:** {ts((info.get('time') or {}).get('created'))}",
            f"- **updated:** {ts((info.get('time') or {}).get('updated'))}",
            f"- **tokens:** `{json.dumps(info.get('tokens'), ensure_ascii=False)}`",
            f"- **cost:** `{info.get('cost')}`",
            "",
        ]
        messages = export.get("messages", [])
        if not messages:
            lines += ["_Sin mensajes._", ""]
        for index, message in enumerate(messages, 1):
            minfo = message.get("info") or {}
            lines += [
                f"### Mensaje {index} — `{minfo.get('role')}`",
                "",
                f"- **agent:** `{minfo.get('agent')}`",
                f"- **model:** `{json.dumps(minfo.get('model'), ensure_ascii=False)}`",
                f"- **created:** {ts((minfo.get('time') or {}).get('created'))}",
                "",
            ]
            for part in message.get("parts", []):
                render_part(part, lines)
        lines.append("")
    Path(args.out).write_text("\n".join(lines) + "\n")
    print(f"wrote {args.out} ({len(lines)} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
