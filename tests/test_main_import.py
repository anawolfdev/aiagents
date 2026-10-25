"""Importar el paquete meshharmes no ejecuta la CLI ni mata el proceso (FIX-001)."""

from __future__ import annotations

import pkgutil

import meshharmes
import meshharmes.__main__  # noqa: F401 — regresión: importar no debe ejecutar la CLI


def test_walk_packages_sobre_meshharmes_no_mata_el_proceso() -> None:
    modulos = [m.name for m in pkgutil.walk_packages(meshharmes.__path__, prefix="meshharmes.")]
    assert "meshharmes.__main__" in modulos
    assert "meshharmes.cli" in modulos
