"""Comprueba los prompts locales de OpenCode sin depender de su instalación."""

from __future__ import annotations

import json
import re
from pathlib import Path

from agents.prompts_sync import HARNESS_AGENTS

REQUIRED_AGENTS = (*HARNESS_AGENTS, "orquestador", "doc")


def check(root: Path) -> list[str]:
    """Detecta definiciones perdidas y opciones que no cargan el prompt."""
    errors = []
    for name in REQUIRED_AGENTS:
        path = root / ".opencode" / "agents" / f"{name}.md"
        if not path.is_file():
            errors.append(f"falta {path.relative_to(root)}")

    try:
        config = json.loads((root / "opencode.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [*errors, f"opencode.json: {exc}"]

    agents = config.get("agent") if isinstance(config, dict) else None
    if not isinstance(agents, dict):
        return [*errors, "opencode.json: agent debe ser un objeto"]

    for name in REQUIRED_AGENTS:
        if name not in agents:
            errors.append(f"falta agent.{name} en opencode.json")

    for name, agent in agents.items():
        if not isinstance(agent, dict):
            errors.append(f"agent.{name} debe ser un objeto")
            continue
        options = agent.get("options", {})
        if "instructions" in agent or (isinstance(options, dict) and "instructions" in options):
            errors.append(f"agent.{name}: usa prompt, no instructions (opción del proveedor inválida)")
        prompt = agent.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            errors.append(f"agent.{name}: falta prompt")
            continue
        for filename in re.findall(r"\{file:([^}]+)\}", prompt):
            try:
                text = (root / filename).read_text(encoding="utf-8")
            except (OSError, ValueError) as exc:
                errors.append(f"agent.{name}: no se puede leer {filename}: {exc}")
            else:
                if not text.strip():
                    errors.append(f"agent.{name}: prompt vacío en {filename}")
    return errors


def main() -> int:
    errors = check(Path.cwd())
    for error in errors:
        print(f"  ✘ {error}")
    if not errors:
        print("  ✔ Definiciones y referencias de prompts OpenCode válidas.")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
