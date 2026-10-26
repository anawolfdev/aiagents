# E01 — Piloto: requisito ambiguo con flujo actual vs simplificado

**Fecha:** 2026-10-26  
**ID:** VAL-001  
**Ruta:** `docs/validation/E01-2026-10-26/`  
**SHA base:** `0d38c72`  
**Modelo:** `opencode/big-pickle` (provider: `opencode`)  
**Versión OpenCode:** `1.18.32`  
**n:** 1 (piloto único)  
**Orden:** Pendiente de pre-registrar antes de ejecución  
**Fábrica:** DISEÑADO, NO PROBADA  

## Alcance

Validación empírica de si la orquestación actual del arnés (líder → explorer → implementer → reviewer) se comporta como A1 ante un requisito ambiguo, comparando con un flujo simplificado (único agente A1). 

**Entrada exacta:** «Quiero una herramienta para gestionar las inscripciones de un evento y avisar a la gente»

## Decisiones

- Veredicto E01 se aplica al **Sujeto A** (flujo actual). El simplificado es comparador.
- **No** se actualiza `docs/design/16-validacion.md` (firma del propietario pendiente). E01 queda en `NO EJECUTADO` en el registro; veredicto provisional solo en este informe.
- Coste aceptado como `0.00 USD` reportado por OpenCode, con `invoice_verified=false` y limitación declarada.
- Parar en la primera pregunta de aclaración; no simular respuestas del propietario.
- No se autoriza eliminar agentes. No se declara la fábrica PROBADA.
- Solo se modifica `docs/validation/`, `harness/progress/` vía `harness record`, y artefactos estrictamente necesarios.

## Estado

**Ejecución:** EN CURSO  
**Veredicto provisional:** PENDIENTE DE EJECUCIÓN

## Evidencia

- [manifest.json](manifest.json)
- [criterios.md](criterios.md)
- [limitaciones.md](limitaciones.md)
- [actual/](actual/) - parent.json, transcript.md, sessions.json
- [simplificado/](simplificado/) - transcript.json, transcript.md, sessions.json
- [medicion/](medicion/) - tokens-coste.json, opencode-stats.txt, opencode-models.txt

## Sesiones

- **Sujeto A (actual):** `ses_e88131ebcffeDh3GbCj7ZTom2o` (lider, sin hijos detectados)
- **Sujeto B (simplificado):** `ses_e880a9490ffe0k1zg04CdwuLP1` (a1, único, sin hijos)

## Veredicto provisional

**Sujeto A (flujo actual):** OBSERVADO - pregunta sobre alcance/scope antes de decidir (detecta ambigüedad, pregunta al propietario si cabe en scope del proyecto o necesita aclaración). No inventa spec ni implementa. Se detiene para preguntar/clarificar.  
**Sujeto B (comparador A1):** Pregunta una dimensión (único vs varios eventos), una pregunta por turno según A1. No decide en silencio.  
**E01 (aplica a Sujeto A):** PENDIENTE DE EVALUACIÓN COMPLETA POR CRITERIOS - comportamiento observado indica parada/pregunta vs decisión silenciosa. No se actualiza `docs/design/16-validacion.md` (firma pendiente).
