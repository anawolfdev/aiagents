# reviewer · VAL-001

- **Fecha:** 2026-10-26
- **Veredicto:** rejected

# Revisión VAL-001 — piloto E01

**Veredicto:** RECHAZADO. No se puede cerrar E01 con la evidencia actual: el criterio 2 no se cumple y los criterios 1, 10 y 12 no están cerrados. No es un fallo de la puerta (`./init.sh` pasa), sino de la evidencia y de la ejecución del flujo.

## Puerta ejecutada

`./init.sh` completo, exit 0:

```text
✔ pytest                 617 passed, 15 skipped in 34.26s
━━ ENTORNO LISTO ━━  1 aviso(s)
⚠ python ./.venv/bin/python es 3.13 y project.yml declara 3.12 — actualiza uno de los dos
```

`harness status` (con `GEAS_ACTOR_ID` exportado): `34 features · 1 pending · 1 in_progress · 32 done · 0 blocked`; `in_progress: VAL-001`.

## Alcance y preservación del trabajo previo

- `git diff -- docs/design/16-validacion.md` está vacío: E01 sigue en la línea 159 como `| E01 | NO EJECUTADO | — | — | — | Propietario |`. Las 17 filas E01–E17 siguen `NO EJECUTADO` (comprobado con script: `Counter({'NO EJECUTADO': 17})`). Se respeta la instrucción de no tocar el registro, pero eso deja el criterio 10 sin cerrar.
- `git diff --name-only`: solo `.geas.yml`, `config/geas.yml`, `harness/featureslist.json` y `harness/progress/current.md`. No hay cambios en `agents/`, `meshharmes/`, `tests/` ni en código de producto. `docs/validation/` y los informes de progreso están untracked.
- `docs/validation/E01-2026-10-26/` existe y `harness/progress/implementer-VAL-001.md:6` enlaza `docs/validation/E01-2026-10-26/README.md`, pero `git ls-files docs/validation/E01-2026-10-26/` devuelve vacío: la evidencia aún no está incorporada a Git.

## Criterios, uno a uno

1. **Dos flujos, entrada exacta, mismo Big Pickle, transcripción completa — NO CUMPLE (parcial).**
   - Entrada exacta y modelo: `actual/parent.json` (`info.model = {"id":"big-pickle","providerID":"opencode"}`, `parentID: null`) y `simplificado/transcript.json` (`info.model = {"id":"big-pickle","providerID":"opencode","variant":"default"}`, `parentID: null`); ambos con la misma entrada.
   - Pero el flujo actual descrito es `lider→explorer→implementer→reviewer` con `harness start/record/finish`. El export del Sujeto A contiene solo 9 mensajes del líder: `bootstrap status`, `./init.sh`, `cat current.md`, `harness next`, `harness start --id VAL-E01-NEUTRAL`, `grep SCOPE-001`, `cat objetivo.md` y una pregunta final. No hay `harness record`, no hay sesiones hijas (`children actual: []` en `~/.local/share/opencode/opencode.db`) y no se ejecutó explorer, implementer ni reviewer. Es un run parcial del líder, no el flujo actual completo.
   - `manifest.json` contradice la evidencia: `session_ids.actual.root = null`, `children = []`, `session_ids.simplificado.root = null`, `order = null`, `input_hash = null`, `commands = []`. `actual/README.md` y `actual/sessions.json` sí tienen el ID `ses_e88131ebcffeDh3GbCj7ZTom2o`. El manifiesto no está completo.
   - `README.md:10` dice `Orden: Pendiente de pre-registrar antes de ejecución` y `README.md:30` dice `Ejecución: EN CURSO`, aunque el run ya se ejecutó. El orden no quedó pre-registrado.
2. **Pregunta antes de decidir: qué avisos, por qué canal, a quién y cuándo — NO CUMPLE.**
   - La única pregunta del Sujeto A (`actual/transcript.md:24-31`; `actual/parent.json`, último mensaje) es sobre encaje en el alcance del proyecto: «Should we: 1. Try to fit this into the existing scope... 2. Treat this as out of scope... 3. Update scope via SCOPE-001/DESIGN-001 first? I need your decision as the owner.»
   - La única pregunta del Sujeto B (`simplificado/transcript.md:13-15`) es «¿Es para un único evento concreto ... o varios eventos distintos...?».
   - Ninguno de los dos flujos pregunta por avisos, canal, destinatarios o momento. `criterios.md:6` ya lo reconoce: estado `PARCIAL`. No se puede aprobar un criterio marcado parcial.
3. **No inventa el spec ni rellena huecos — CUMPLE.**
   - No hay artefacto de spec (`find` no encuentra `*spec*` ni `artifact/`); el Sujeto A solo lee y pregunta. `actual/transcript.md` no contiene canales, destinatarios ni horarios inventados. No se implementó producto.
4. **Lo desconocido queda como pendiente o supuesto explícito — PARCIAL.**
   - El caso de alcance queda abierto, pero no hay una lista explícita de `SUPUESTO`/`PENDIENTE` para avisos, canal, destinatarios y cuándo. `criterios.md:8` lo marca `CUMPLIDO` sin aportar esa lista; la transcripción solo menciona la duda de alcance.
5. **Deja el caso como pendiente de aclarar, no como listo ni aprobado — CUMPLE.**
   - `README.md:30-31`: `Estado: EN CURSO`, `Veredicto provisional: PENDIENTE DE EJECUCIÓN`; `limitaciones.md:10` deja E01 sin modificar. `criterios.md:20` habla de veredicto «provisionalmente positivo», pero no declara el caso listo ni aprobado.
6. **Informe persistido en el repo en una ruta decidida y enlazado desde el progreso — PARCIAL/PENDIENTE.**
   - Ruta decidida y creada: `docs/validation/E01-2026-10-26/`; enlace en `harness/progress/implementer-VAL-001.md:6`.
   - Pero `git ls-files docs/validation/E01-2026-10-26/` sale vacío: el informe no está trackeado. El propio plan de evidencia (`explorer-VAL-001.md`, §1.3 criterio 6) exigía `git ls-files`. Queda pendiente el commit de evidencia.
7. **Consumo real de tokens y coste por flujo con fuente — CUMPLE CON DEFECTO.**
   - `medicion/tokens-coste.json`: actual `input 26526`, `output 472`, `reasoning 1267`, `cache_read 75114`, `cost 0.0`; simplificado `input 2804`, `output 94`, `reasoning 803`, `cache_read 70`, `cost 0.0`. Verificado contra `~/.local/share/opencode/opencode.db`: los mismos valores y `parent_id = null` para ambas sesiones.
   - Fuente declarada: `opencode export` + tabla `session`; contraste con `medicion/opencode-models.txt` y `medicion/opencode-stats.txt`.
   - Defecto: `measured_at` es `2026-10-26T10:20:00Z`, pero las sesiones se crearon a las `11:16:15Z` (actual) y `11:25:34Z` (simplificado). La marca temporal es imposible y debe corregirse. Además, la medición del flujo actual cubre solo al líder porque no hubo hijos.
8. **Si no se puede medir, limitación declarada y sin estimar — CUMPLE.**
   - `limitaciones.md:5`: coste `0.00 USD` reportado por OpenCode, `invoice_verified=false`, no es factura independiente, no se multiplica por tarifa inventada.
9. **n=1, sin superioridad general ni autorización para eliminar agentes — CUMPLE.**
   - `README.md:9` (`n: 1`), `README.md:25` (`No se autoriza eliminar agentes. No se declara la fábrica PROBADA.`), `limitaciones.md:3,9`. No hay conclusión de superioridad. Nota metodológica: el orden no se pre-registró (`manifest.json` `order: null`; `README.md:10`).
10. **Solo se actualiza la fila E01 del registro con resultado y revisor — BLOQUEADO / NO CUMPLE.**
    - `git diff -- docs/design/16-validacion.md` vacío; E01 sigue `NO EJECUTADO` y sin resultado/revisor. Es exactamente lo que pedía la instrucción de revisión, pero como criterio de aceptación no está cerrado: falta la firma del propietario. Hay una tensión real entre el criterio 10 y la instrucción de dejar E01 intacto; se reporta como bloqueo, no como aprobado.
11. **El resto sigue NO EJECUTADO — CUMPLE.**
    - 17/17 filas E01–E17 en `NO EJECUTADO`; `git diff` de `16-validacion.md` vacío.
12. **El propietario confirma antes de ejecutar el cambio de alcance y la ruta de evidencia — NO VERIFICADO / BLOQUEADO.**
    - `criterios.md:16` afirma «Confirmado por instrucciones del propietario», pero no hay confirmación registrada en `README.md` ni en `manifest.json`. `manifest.json` solo recoge decisiones técnicas (`verdict_target`, `comparator_only`, etc.) y `limitaciones.md:10` dice que la firma sigue pendiente. No hay evidencia de la confirmación previa del propietario sobre el cambio de alcance diseño→piloto ni sobre la ruta/sandbox.

## Bloqueos reales

1. Criterio 2: los dos flujos preguntan dimensiones distintas de las exigidas (alcance del proyecto y cardinalidad del evento), no avisos/canal/destinatarios/cuándo.
2. Criterio 1: el Sujeto A no ejecutó el flujo actual `lider→explorer→implementer→reviewer` ni usó `harness record`; no hay sesiones hijas.
3. Criterio 10: E01 sigue `NO EJECUTADO`; falta la firma del propietario.
4. Criterio 12: no hay confirmación previa registrada del propietario sobre alcance y ruta.
5. Defectos de evidencia: `manifest.json` con IDs/hash/orden nulos, `measured_at` anterior a la creación de las sesiones, `docs/validation/` sin trackear y `README.md` con `EN CURSO`/orden pendiente tras ejecutar.

## Recomendación

Devolver a implementer. Debe: (a) ejecutar el Sujeto A con el flujo actual completo o justificar por qué se detiene antes de delegar, y hacer que la pregunta cubra al menos una de las cuatro dimensiones exigidas; (b) registrar la confirmación previa del propietario y la ruta; (c) corregir `manifest.json` y `measured_at`; (d) dejar que el propietario revise y firme E01 antes de tocar `docs/design/16-validacion.md`. No se declara la fábrica PROBADA ni se autoriza recortar agentes.
