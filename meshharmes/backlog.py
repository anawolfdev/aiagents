"""
meshharmes.backlog — lectura del backlog del arnés.

Es la primera pieza funcional de punta a punta: la CLI lee
`harness/featureslist.json`, cuenta estados y dice qué toca hacer. No escribe
nada (eso es de `harness`) y no ejecuta la fábrica: solo informa.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from meshharmes.paths import ROOT_DIR

DEFAULT_BACKLOG: Path = ROOT_DIR / "harness" / "featureslist.json"


class BacklogError(Exception):
    """El backlog no se puede leer o no tiene la forma esperada."""


@dataclass(frozen=True)
class Summary:
    total: int
    pending: int
    in_progress: int
    done: int
    blocked: int
    next_id: str | None

    def render(self) -> str:
        siguiente = self.next_id or "—"
        return (
            f"{self.total} features · {self.pending} pending · "
            f"{self.in_progress} in_progress · {self.done} done · "
            f"{self.blocked} blocked\nSiguiente: {siguiente}"
        )


def load_features(path: Path | None = None) -> list[dict[str, Any]]:
    ruta = path or DEFAULT_BACKLOG
    try:
        raw = ruta.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise BacklogError(f"No existe el backlog: {ruta}") from exc
    except OSError as exc:
        raise BacklogError(f"No se pudo leer {ruta}: {exc}") from exc

    try:
        doc = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise BacklogError(f"{ruta} no es JSON válido: {exc}") from exc

    features = doc.get("features") if isinstance(doc, dict) else None
    if not isinstance(features, list):
        raise BacklogError(f"{ruta} no tiene una lista 'features'.")
    if not all(isinstance(f, dict) and "id" in f and "status" in f for f in features):
        raise BacklogError(f"{ruta}: hay features sin 'id' o sin 'status'.")
    return features


def summarize(features: list[dict[str, Any]]) -> Summary:
    estados = [str(f["status"]) for f in features]
    done = {str(f["id"]) for f in features if f["status"] == "done"}
    # La primera pendiente cuyas dependencias ya están cerradas: el mismo
    # criterio que usa `harness next`, sin duplicar su lógica de escritura.
    siguiente = next(
        (
            str(f["id"])
            for f in features
            if f["status"] == "pending" and all(str(dep) in done for dep in f.get("depends_on", []))
        ),
        None,
    )
    return Summary(
        total=len(features),
        pending=estados.count("pending"),
        in_progress=estados.count("in_progress"),
        done=estados.count("done"),
        blocked=estados.count("blocked"),
        next_id=siguiente,
    )


def read_summary(path: Path | None = None) -> Summary:
    return summarize(load_features(path))
