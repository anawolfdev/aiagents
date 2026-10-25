"""
meshharmes — paquete del proyecto.

Es la pieza ejecutable que acompaña al diseño: la CLI del arnés
(`python -m meshharmes`), no la fábrica de agentes en marcha. El arnés
(`agents/`, `harness/`, `init.sh`) solo espera dos cosas de este paquete:

- que exista y sea importable (lo comprueba `./init.sh`),
- que su nombre coincida con `project_slug` en `project.yml`.

Renombrarlo: `git mv meshharmes <tu_paquete>` y cambia `project_slug` en
`project.yml`, `name`/`packages`/`[project.scripts]` en `pyproject.toml`,
`MODULE` en `Makefile`, `source` en `[tool.coverage.run]` y la primera fila de
`FUENTES` en `agents/tools/rag_tool.py`. `./init.sh` avisa si algo no cuadra.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

#: La versión vive en `pyproject.toml`: leerla del paquete instalado evita que
#: `--version` se quede en la de la plantilla cuando el arnés sube el patch.
try:
    __version__ = version("meshharmes")
except PackageNotFoundError:  # paquete importado sin instalar (tests sueltos)
    __version__ = "0.0.0"
