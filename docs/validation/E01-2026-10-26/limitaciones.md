# Limitaciones

- **n=1:** Un solo piloto. No hay significancia estadística. No se concluye superioridad general.
- **Orden:** A registrar al ejecutar (puede introducir sesgo). 
- **Coste:** `0.00 USD` reportado por OpenCode (`opencode models --verbose`, `session.cost`, `opencode stats`). `invoice_verified=false`. No es factura independiente. No se multiplica por tarifa inventada.
- **Asimetrías:** Sujeto A usa arnés completo (AGENTS.md, harness, subagentes, `init.sh`, bash). Sujeto B usa solo A1 con herramientas restringidas según config. Esto es parte de la intervención.
- **Fuga de rúbrica:** `harness/progress/current.md`, `featureslist.json` e `explorer-VAL-001.md` contienen información sobre la validación. Se mitiga con sandboxes aislados sin esos ficheros/contexto contaminado.
- **Sesgo de incumbente:** Mismo arnés orquesta y puntúa. Mitigado con rúbrica pre-registrada, sandbox, evidencia enlazada, revisión independiente.
- **Fábrica:** Sigue `DISEÑADO`, no `PROBADA`. Ninguna autorización para eliminar agentes.
- **Sin firma:** `docs/design/16-validacion.md` no modificado (firma del propietario pendiente). Veredicto provisional solo en este informe.
- **Medición:** Fuente primaria = `opencode export` + tabla `session` de `~/.local/share/opencode/opencode.db`. `opencode stats` puede mostrar agregaciones confusas - usar export por sesión.
