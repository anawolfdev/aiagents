# explorer · REPAIR-001

- **Fecha:** 2026-10-22
- **Veredicto:** ok

Faltan todas las definiciones .opencode/agents/. init.sh requiere lider, implementer, reviewer y explorer. opencode.json también referencia orquestador y doc_agent. agents/prompts_sync.py solo espeja OpenCode a Claude, no reconstruye fuentes. AGENTS.md, agents/prompts/harness_workflow.md, orchestrator.md y doc_agent.md permiten reconstrucción. instructions a nivel agent en opencode.json es opción desconocida reenviada al proveedor y explica invalid openai provider options. Usar prompt {file:...} o definiciones markdown válidas. make opencode-check comprueba cinco archivos y omite doc. Verificar uv run pytest (ambas suites), make opencode-check, prompts_sync y ./init.sh completo. Python 3.13 frente a declarado 3.12 es aviso, no bloqueo. No hay fuentes recuperables en git. Informe de explorer de solo lectura registrado por líder.
