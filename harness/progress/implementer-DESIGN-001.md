# implementer · DESIGN-001

- **Fecha:** 2026-10-25
- **Veredicto:** ok

vault/01_PROYECTO/arquitectura.md: piezas y flujo (propietario -> docs/design -> harness -> agentes -> init.sh -> paquete/tests/CI), reglas que no se saltan, estructura, TRES alternativas descartadas con motivo (sexto agente coordinador; orquestador de terceros con estado en BD; layout src/), tabla de 7 riesgos con mitigacion y 6 decisiones aplazadas. Renombrado app/ -> meshharmes/ con git mv y coherencia total: project.yml proyecto_slug=meshharmes, pyproject name/scripts/packages/coverage=meshharmes, Makefile MODULE=meshharmes, FUENTES del RAG, imports de tests, README y docstrings. __version__ ahora se lee de pyproject via importlib.metadata (0.1.11) en vez de la 0.1.0 de plantilla. Real: uv run meshharmes --version -> 'meshharmes 0.1.11'; uv run pytest tests/ -> 7 passed.
