# implementer · REPAIR-001

- **Fecha:** 2026-10-22
- **Veredicto:** ok

## Entrega

Implementación de REPAIR-001 lista para reviewer. Reparación autorizada del bloqueo actual; no se ha ejecutado harness finish. Solo harness escribe el estado y este informe.

## Cambios y archivos

- opencode.json: sustituidas las seis instructions de agente por prompt {file:./.opencode/agents/<nombre>.md}. Se conserva el modelo opencode/deepseek-v4-flash-free y los nombres y modos configurados.
- .opencode/agents/lider.md, explorer.md, implementer.md, reviewer.md: restaurado el protocolo desde AGENTS.md y agents/prompts/harness_workflow.md: bootstrap sin inventar objetivo, parada ante puerta roja, harness único dueño del estado, implementer único escritor de producto, reviewer con puerta completa y evidencia, contexto mínimo y registro antes de devolver control.
- .opencode/agents/orquestador.md y doc.md: restaurados desde agents/prompts/orchestrator.md y doc_agent.md. El archivo doc.md mantiene el nombre doc en el descubrimiento automático y evita añadir el alias doc_agent. CLI real: ask para ruteo; verdict rejected para activar los rechazos del arnés.
- .claude/agents/lider.md, explorer.md, implementer.md, reviewer.md: restaurados los espejos exactos esperados por agents.prompts_sync; el espejo de explorer conserva herramientas de solo lectura.
- agents/opencode_check.py y Makefile: opencode-check comprueba las seis definiciones, agentes del JSON, referencias legibles y no vacías, y rechaza instructions reenviadas al proveedor. Antes solo comprobaba existencia de cinco definiciones y aceptaba el JSON que causaba el bloqueo. Comprobación local stdlib, sin instalar OpenCode ni duplicar su esquema completo.
- agents/tests/test_opencode_check.py: 17 regresiones para pérdida de cada definición incluida doc, instructions tanto a nivel agente como en options, referencias inexistentes/vacías, JSON inválido y exit no cero del validador.
- Entorno: uv sync --python 3.12 --extra dev creó .venv con CPython 3.12.15 e instaló 56 paquetes dev. pyproject.toml y project.yml no se han modificado. uv.lock conserva exactamente el diff previo: revision 5 y app 0.1.1.

Se restauraron primero las definiciones y después se ejecutó la puerta completa en verde antes de modificar el validador o los tests. La puerta inicial había indicado ENTORNO BLOQUEADO por las cuatro definiciones ausentes; la reparación se hizo con la autorización explícita indicada en la tarea.

## Evidencia real por criterio

### 1. Definiciones presentes y referencias válidas

$ make opencode-check
▶  Verificando configuración opencode...
  ✔ Definiciones y referencias de prompts OpenCode válidas.
  ✔ 33 prompts fuente disponibles.

$ uv run python -m agents.prompts_sync
✔ Prompts y subagentes sincronizados con el código y con los contratos.

### 2. OpenCode carga prompts válidos

$ opencode --version
1.18.35

$ opencode debug config | uv run python -c <comprobación de JSON resuelto, modelo, modos, prompt no vacío, ausencia de instructions y options vacías>
model: opencode/deepseek-v4-flash-free
lider: mode=primary, prompt=2996 caracteres, options={}
explorer: mode=subagent, prompt=1260 caracteres, options={}
implementer: mode=subagent, prompt=1622 caracteres, options={}
reviewer: mode=subagent, prompt=1512 caracteres, options={}
orquestador: mode=subagent, prompt=1519 caracteres, options={}
doc: mode=subagent, prompt=1394 caracteres, options={}

Exit 0; assertions también comprueban que no aparece el alias doc_agent. opencode debug agent implementer se ejecutó con exit 0, mode subagent, options {} y el cuerpo completo del prompt. La comprobación usa el cargador real de OpenCode; no solicita una inferencia al proveedor.

### 3. Suites de proyecto y agents

$ uv run pytest tests/ agents/tests/ -q -rs
538 passed, 15 skipped in 17.68s

Verificación final con testpaths configurados para tests y agents/tests:
$ uv run pytest -q -rs
538 passed, 15 skipped in 18.14s

Skips reales: 1 en agents/tests/test_api_agent.py:9 por fastapi opcional; 14 en agents/tests/test_rag_agent.py por chromadb no instalado, extra rag. No hay tests fallidos ni verificaciones rebajadas.

### 4. Puerta completa

$ ./init.sh
✔ python                 ./.venv/bin/python 3.12
✔ subagentes             lider, implementer, reviewer, explorer
✔ featureslist           12 features · 6 pending · 1 in_progress · 5 done · 0 blocked
✔ siguiente tarea        REPAIR-001 — Recuperar las definiciones y el entorno del arnés [in_progress]
✔ pytest                 7 passed in 0.47s
━━ ENTORNO LISTO ━━  0 aviso(s)

Se muestran extractos de la salida real sin secuencias ANSI. init.sh verifica la suite del proyecto; las dos suites completas se han comprobado además con pytest arriba.

### Calidad del cambio

$ uv run ruff check agents/opencode_check.py agents/tests/test_opencode_check.py
All checks passed!

$ git diff --check
Exit 0, sin salida.

## Advertencias y siguiente paso

- Los 15 skips dependen de extras opcionales ausentes; el extra dev está instalado y ambas suites se ejecutan.
- Hay que salir y reiniciar OpenCode para que las sesiones carguen la configuración reparada.
- bootstrap status devolvió first_run false, onboarding_tickets_seeded true y description_pending true. No se inventó objetivo ni se cerraron SCOPE/ONBOARD.
- Sin cambios GEAS, commits, push ni ajustes de git config del repositorio. Se preservan los cambios previos de backlog/progreso y uv.lock. Pendiente la revisión independiente del reviewer.
