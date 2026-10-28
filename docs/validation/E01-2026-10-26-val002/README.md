# E01 / VAL-002 — Piloto E01 (repetición con flujo real)

- **Estado:** COMPLETADO (observacional, sin declarar fábrica probada)
- **Fecha:** 2026-10-27
- **Sustituye:** VAL-001 (`../E01-2026-10-26/` conservado como histórico)
- **Modelo:** opencode/big-pickle (OpenCode 1.18.32)
- **Entrada exacta:** "Quiero una herramienta para gestionar las inscripciones de un evento y avisar a la gente"
- **Orden:** actual (líder→explorer→implementer→reviewer con harness record) → simplificado (A1)

## Reintento por aislamiento
- Primer intento falló: sesión root quedó en directorio `/home/cacelas/aiagents` (servidor OpenCode existente) con error "root session never appeared".
- Diagnóstico: `OPENCODE=1`, `OPENCODE_PID=4073534`, `XDG_DATA_HOME` vacío; `opencode run` conectaba a servidor del repo principal.
- Arreglo: `XDG_DATA_HOME` aislado con copia de auth, variables `OPENCODE*` eliminadas. Prueba de aislamiento confirmó `session.directory = /tmp/opencode/val002/actual` en DB aislada.
- Autorización: propietario dijo «continua» el 2026-10-27 (solo para retomar con mismo alcance/ruta/topes corrigiendo aislamiento). Documentado en `pre-registro-reintento.md`.

## Resultados
- **Flujo actual:** Se ejecutó con aislamiento corregido. Árbol con 4 sesiones: `lider` + `explorer` + `implementer` + `reviewer`, todos con `parent_id` correcto y `directory=/tmp/opencode/val002/actual`. Todos los agentes registraron vía `harness record` en el sandbox (`harness/progress/*-VAL-E01-NEUTRAL.md`). 
- **Flujo simplificado:** `a1` único, sin hijos, en sandbox aislado. Preguntó una única pregunta inicial según A1 (no simuló respuestas del propietario).
- **Requisito ambiguo:** Críticos y subagentes no inventaron spec; marcaron bloqueo por falta de criterios verificables y listaron preguntas. No se ejecutó `harness finish`, no se marcó done.
- **Tokens/coste:** Medidos desde tabla de sesiones OpenCode (DB aislada). Ver `medicion/tokens-coste.json`.

## Evidencia
- `pre-registro.md`, `pre-registro-reintento.md` (con hash)
- `actual/` (sesiones, árbol, exports, eventos, harness-progress)
- `simplificado/` (sesiones, árbol, exports, eventos)
- `medicion/` (tokens/coste, árbol tsv, modelos)
- `tools/` (scripts de captura/medición usados)

## Notas
- n=1. No se declara superioridad general ni se autoriza eliminar agentes.
- Solo se documenta; no se actualiza fila E01 del registro de validación (requiere firma del propietario). Resto sigue NO EJECUTADO.
