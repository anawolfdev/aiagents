"""Hoja compartida init → sync y harness → sync; nunca invoca la puerta."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from agents.exceptions import MissingDependencyError, ToolExecutionError
from agents.tools.geas_tool import GeasClient, GeasError
from agents.tools.git_tool import GitTool


@dataclass
class Synced:
    client: GeasClient | None
    git: dict
    remote: dict

    def as_dict(self) -> dict:
        return {"mode": "remote" if self.client else "local", "git": self.git, "geas": self.remote}


def synchronize(root: Path) -> Synced:
    client = GeasClient.from_root(root)
    if client is None:
        return Synced(None, {}, {})
    remote = client.context()  # identidad/permisos antes de tocar Git
    try:
        git = GitTool(root).sync_upstream()
    except (MissingDependencyError, ToolExecutionError, ValueError, OSError) as exc:
        raise GeasError("GIT_SYNC", str(exc)) from exc
    if GeasClient.from_root(root) != client:
        raise GeasError("CONFIG_CHANGED", ".geas.yml cambió durante el pull; repite la sincronización.")
    # Estado remoto fresco DESPUÉS del pull, antes de tomar decisiones.
    remote = client.context()
    return Synced(client, git, remote)


def main() -> int:
    try:
        state = synchronize(Path.cwd())
        report = {"success": True, "message": "Git + GEAS sincronizados" if state.client else "Modo local (sin .geas.yml)",
                  "data": state.as_dict()}
    except GeasError as exc:
        report = {"success": False, "code": exc.code, "message": str(exc)}
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
