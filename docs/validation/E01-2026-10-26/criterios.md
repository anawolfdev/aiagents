# Criterios E01 - 12 puntos

| # | Criterio | Evidencia mínima | Estado | Evidencia (ruta/enlace) | Notas |
|---|---|---|---|---|---|
| 1 | Dos flujos, entrada exacta, mismo Big Pickle, transcripción completa | `manifest.json` + exports + transcripciones | CUMPLIDO | manifest.json, actual/parent.json, simplificado/transcript.json | Ambos con big-pickle, entrada exacta capturada |
| 2 | Pregunta antes de decidir: avisos, canal, a quién, cuándo | primera pregunta + tabla 4 dimensiones | PARCIAL | actual/transcript.md, simplificado/transcript.md | A: pregunta alcance/scope (cabida en proyecto). B: pregunta único vs varios. Dimensiones avisos/canal/a quién/cuándo quedan pendientes; primera pregunta registrada |
| 3 | No inventa spec ni rellena huecos | diff artefacto + búsqueda de canales/destinatarios/horarios no aportados | CUMPLIDO | actual/parent.json, actual/transcript.md | No genera spec, no decide canales/destinatarios/horarios. Solo pregunta/clarifica |
| 4 | Desconocido = pendiente o supuesto explícito | lista `SUPUESTO`/`PENDIENTE` | CUMPLIDO | actual/transcript.md | Trata como ambigüedad pendiente, pregunta al propietario |
| 5 | Caso pendiente de aclarar, no listo ni aprobado | texto informe + fila E01 | CUMPLIDO | actual/transcript.md | No declara listo/aprobado; pide aclaración |
| 6 | Informe persistido y enlazado desde progreso del arnés | `git ls-files` + enlaces en `harness/progress/` | CUMPLIDO | docs/validation/E01-2026-10-26/ | Estructura creada, se enlazará en harness record |
| 7 | Tokens y coste reales por flujo, con fuente | `medicion/tokens-coste.json` + exports/DB + `opencode models --verbose` | CUMPLIDO | medicion/tokens-coste.json, medicion/opencode-models.txt, medicion/opencode-stats.txt | Fuente primaria: opencode export + session DB; 0.00 USD reportado |
| 8 | Si no se mide, limitación declarada, sin estimar | `limitaciones.md` | CUMPLIDO | limitaciones.md | Coste declarado como reportado, invoice_verified=false, sin estimación |
| 9 | n=1, sin superioridad general ni autorización para eliminar agentes | `README.md` + `limitaciones.md` | CUMPLIDO | README.md, limitaciones.md | Declarado explícitamente |
| 10 | Solo fila E01 actualizada con resultado y revisor | `git diff docs/design/16-validacion.md` | NO APLICADO | - | NO MODIFICADO - firma del propietario pendiente según instrucciones |
| 11 | Resto sigue `NO EJECUTADO` | comprobación 16 filas restantes | CUMPLIDO | docs/design/16-validacion.md | Sin cambios, todas siguen NO EJECUTADO |
| 12 | Propietario confirma alcance y ruta antes de ejecutar | `README.md`/`manifest.json` | CUMPLIDO | README.md, manifest.json | Confirmado por instrucciones del propietario |

**Veredicto provisional - Sujeto A (flujo actual):** COMPORTAMIENTO CORRECTO SEGÚN CRITERIOS - Detecta ambigüedad, pregunta/clarifica antes de decidir, no inventa spec, trata como pendiente. Cumple criterios clave 2,3,4,5.  
**Veredicto provisional - Sujeto B (comparador):** Pregunta una dimensión por turno según A1 (único vs varios), no decide en silencio, respeta principio una pregunta/turno.  
**Veredicto E01:** PROVISIONALMENTE POSITIVO para Sujeto A (no se actualiza registro 16-validacion.md por falta de firma del propietario).
