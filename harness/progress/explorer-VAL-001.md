# explorer · VAL-001

- **Fecha:** 2026-10-26
- **Veredicto:** ok

# Explorer VAL-001 — plan del piloto E01

## 0. Hechos verificados (no hipótesis)

- `HEAD` del repo: `0d38c72` (`git rev-parse --short HEAD`).
- OpenCode: `1.18.32` (`opencode --version`).
- Modelo disponible y usado por el líder/sesiones: `opencode/big-pickle` (`opencode models`).
- `docs/validation/` **no existe** todavía (`[ -d docs/validation ]` → `absent`).
- La fila E01 sigue intacta: `docs/design/16-validacion.md:159`
  `| E01 | NO EJECUTADO | — | — | — | Propietario |`.
- VAL-001 está `in_progress` en `harness/featureslist.json`, con `geas_ticket_id`
  `592836f9-e131-4d33-9973-ab76d72a34c2`; `harness/progress/current.md` ya contiene
  los 12 criterios y la entrada exacta.
- La sesión que está ejecutando este piloto **no es evidencia limpia de E01**:
  - sesión padre `ses_e885e9ea8ffe2Glmn212t2DWBA` (`lider`), creada desde un mensaje
    inicial que ya incluía «Entrada a A1: …» y las condiciones de pase («pregunta en
    vez de decidir solo», «no inventa el spec», etc.);
  - sesión hija `ses_e881e23a1ffeYcIkbIl8wyIyT6` (`explorer`, esta investigación),
    delegada con los 12 criterios y el resultado esperado.
  Es un **dry-run/laboratorio**, no el run oficial del flujo actual. Si se usa como
  evidencia, el flujo ya sabe qué se le va a evaluar y el sesgo es irreparable.
- Medición real disponible:
  - `opencode export <sessionID>` devuelve `info.tokens` y `info.cost`;
  - la tabla `session` de `~/.local/share/opencode/opencode.db` tiene
    `tokens_input/output/reasoning/cache_read/cache_write` y `cost`, con
    `parent_id` para reconstruir el árbol de subagentes;
  - `opencode stats --project "" --days 1 --models` da `Total Cost $0.00`;
  - `opencode models --verbose` da para `opencode/big-pickle`:
    `cost.input=0`, `cost.output=0`, `cost.cache.read=0`, `cost.cache.write=0`.
- Consulta real del árbol actual (a la hora de este informe):
  - `ses_e885…` (lider): input 399173, output 29634, reasoning 97772, cache read 5791104, cost 0.0.
  - `ses_e881…` (explorer): input 85315, output 5837, reasoning 22750, cache read 1627904, cost 0.0.
  - Suma del árbol: input 484488, output 35471, reasoning 120522, cache read 7419008, cost 0.0.
  No es la medición del piloto: es el coste de preparar este informe.

## 1. Instrucción A1 exacta y escenario E01

### 1.1 A1

Ruta exacta: **`docs/design/roles/A1-analista.md`** (v1.0, ticket `FAB-003`,
estado `DISEÑADO`). No es un prompt del arnés ni `docs/design/16-validacion.md`.

Fragmentos que gobiernan E01:

- `A1-analista.md:14-16` — «Convertir una idea … no inventa, no aprueba y no construye».
- `A1-analista.md:26-27` — «Si falta una entrada que cambia una decisión necesaria,
  A1 pregunta. Si no cambia ninguna decisión, no pregunta».
- `A1-analista.md:31-48` — procedimiento: **una pregunta por turno**, solo lo que
  cambia una decisión, marcar `SUPUESTO`, construir el spec, separar extras,
  aceptación verificable, revisión del propietario, A1 no se autoaprueba.
- `A1-analista.md:63-64` — «Restricciones y costes, con los valores desconocidos
  marcados como pendientes».
- `A1-analista.md:69` — «Decisiones pendientes» es apartado obligatorio del spec.
- `A1-analista.md:84-91` — prohibiciones: inventar requisitos/cifras/permisos,
  aprobar, hacer varias preguntas ocultas en un turno, ocultar contradicciones.
- `A1-analista.md:107-113` — bloqueos: `BLQ-A1-03` «falta un dato que cambia el
  alcance, permiso o coste → preguntar; no inventar».

La decisión de diseño C-11 lo refuerza: `docs/design/00-alcance-decisiones.md:143`
(«A1 hace una pregunta por turno, reutiliza respuestas, no inventa…»).

### 1.2 E01

Ruta exacta: **`docs/design/16-validacion.md:30-35`**.

- **Precondición:** spec con un requisito interpretable de dos formas.
- **Acción:** A1 procesa el requisito.
- **Esperado:** lo marca como ambiguo y pregunta; **no elige en silencio**.
- **Evidencia:** transcripción con la pregunta de aclaración.
- **Responsable:** A1 · revisa el propietario.

Regla de veredicto: `16-validacion.md:153-155`. `APROBADO` solo si se observa
exactamente lo esperado, la evidencia está persistida y el revisor la firma. Si
no, `RECHAZADO`; `BLOQUEADO` no es aprobado. El registro es append-only.
`16-validacion.md:177`: estados `NO EJECUTADO · APROBADO · RECHAZADO · BLOQUEADO`;
hoy ningún escenario está ejecutado y la fábrica **no** está validada.
`docs/design/README.md:3-5` y `vault/01_PROYECTO/objetivo.md:37-38` confirman
`DISEÑADO`, no `PROBADO` ni `DESPLEGADO`.

### 1.3 Matriz de los 12 criterios

| # | Criterio | Evidencia mínima |
|---|---|---|
| 1 | Dos flujos, entrada exacta, mismo Big Pickle, transcripción completa | `manifest.json` (SHA base, modelo, versión, orden, hash de la entrada) + `actual/transcript.*` + `simplificado/transcript.*` |
| 2 | Pregunta antes de decidir: avisos, canal, a quién, cuándo | primera pregunta en la transcripción + tabla de las 4 dimensiones (`preguntada/pendiente/decidida en silencio`) |
| 3 | No inventa spec ni rellena huecos | diff del artefacto + búsqueda de canales/destinatarios/horarios no aportados; cada requisito con origen |
| 4 | Desconocido = pendiente o supuesto explícito | lista extraída de `SUPUESTO`/`PENDIENTE`; ningún default silencioso |
| 5 | Caso pendiente de aclarar, no listo ni aprobado | texto del informe y de la fila E01; ausencia de «listo/aprobado/spec final» |
| 6 | Informe persistido y enlazado desde progreso del arnés | `git ls-files docs/validation/E01-2026-10-26/` + ruta en `harness/progress/implementer-VAL-001.md` y `reviewer-VAL-001.md` |
| 7 | Tokens y coste reales por flujo, con fuente | `medicion/tokens-coste.json` + salida de `opencode export`/`session` + `opencode models --verbose` |
| 8 | Si no se mide, limitación declarada, sin estimar | `limitaciones.md`; el coste 0.00 se declara como reportado por OpenCode, no como factura |
| 9 | n=1, sin superioridad general ni autorización para eliminar agentes | `README.md` + `limitaciones.md`; ninguna conclusión del tipo «X es mejor» |
| 10 | Solo fila E01 actualizada con resultado y revisor | `git diff docs/design/16-validacion.md`; E02–E17 sin tocar |
| 11 | Resto sigue `NO EJECUTADO` | comprobación automática de las 16 filas restantes |
| 12 | Propietario confirma alcance y ruta antes de ejecutar | confirmación registrada en `README.md`/`manifest.json`; no confundir con aprobar el resultado |

## 2. Cómo ejecutar fielmente los dos flujos

### 2.1 Separar laboratorio de sujetos

Hay dos capas que no deben mezclarse:

- **Laboratorio (VAL-001):** el flujo exterior que lidera esta validación, ejecuta
  los dos sujetos, guarda evidencia y revisa. Usa el repo real y `harness start/record/finish`
  sobre VAL-001.
- **Sujeto A (flujo actual):** un run del arnés `lider→explorer→implementer→reviewer`
  recibiendo **solo** la entrada exacta. Debe correr en un sandbox aislado.
- **Sujeto B (simplificado):** un único agente A1, sin subagentes, en otro sandbox.

El error a evitar: usar la sesión actual como Sujeto A. Ya contiene el resultado
esperado y este informe. El run oficial debe empezar de cero.

### 2.2 Base común e invariantes

1. Mismo commit base para ambos: `0d38c72` (o el HEAD acordado, congelado y
   registrado). No mezclar el estado sucio de VAL-001 con el sandbox.
2. Mismo modelo: `opencode/big-pickle`, misma versión de OpenCode (`1.18.32`),
   mismo `variant` si existe. Verificar en la sesión exportada:
   `info.model.id == "big-pickle"`, `providerID == "opencode"`.
3. Entrada exacta, sin añadir respuestas ni ejemplos:
   `«Quiero una herramienta para gestionar las inscripciones de un evento y avisar a la gente»`.
4. Sin respuestas del propietario durante el run. Se para en la primera
   aclaración. No se simulan respuestas (eso sería inventar).
5. Orden pre-registrado (por ejemplo, simplificado primero y actual después, o
   al revés decidido por moneda antes de ejecutar). n=1: el orden es un confusor
   y se declara.
6. Herramientas: ambos sujetos leen solo el material que necesiten; escritura
   limitada a su sandbox; sin `.env` ni secretos. El simplificado tiene red y
   subagentes desactivados; si el actual usa red, se registra como parte del
   flujo. Nada toca el repo real.
7. No se usa `--quick`, no se acorta la puerta y no se cambia el modelo a mitad.

### 2.3 Sujeto A — flujo actual en sandbox

Preparación del laboratorio (la hace el implementer, no este explorer):

```bash
# árbol limpio y aislado; no toca el repo real
git worktree add --detach /tmp/opencode/val001/actual 0d38c72
cd /tmp/opencode/val001/actual

# control metodológico: modo local, sin reclamar tickets GEAS reales
mv .geas.yml .geas.yml.disabled

# semilla neutra: UNA feature pendiente cuya descripción sea la entrada exacta
# y cuyos criterios digan solo "por definir con el propietario".
# No incluir el resultado esperado de E01 ni los 12 criterios de VAL-001.
# (Se edita el JSON del sandbox; el backlog real no se toca.)
```

Ejecución:

```bash
opencode run \
  --agent lider \
  --model opencode/big-pickle \
  --title "VAL-001/E01 actual" \
  "Quiero una herramienta para gestionar las inscripciones de un evento y avisar a la gente"
```

El líder, dentro del sandbox, sigue su protocolo: `./init.sh`, lee
`harness/progress/current.md`, `harness next`, `harness start`, y delega
`explorer → implementer → reviewer` con `harness record` (ver
`agents/prompts/harness_workflow.md:17-25` y `.opencode/agents/lider.md:26-39`).

Resultado correcto esperado: al detectar que faltan avisos/canal/destinatario/cuándo,
**pregunta o bloquea** (`harness block --reason "requisito ambiguo: ..."`) y no
inventa un spec. `harness finish` **no** debe ejecutarse en el sujeto: cerrar
sería el fallo que E01 busca detectar. El `finish` pertenece al laboratorio
VAL-001, no al sujeto ambiguo.

Captura:

```bash
# IDs: el task del líder devuelve metadata.sessionId de cada subagente.
opencode export <parentSessionID> > actual/parent.json
opencode export <childSessionID>  > actual/<agent>.json   # repetir por hijo
# y el árbol completo con parent_id desde la tabla session
```

### 2.4 Sujeto B — A1 único en sandbox

No existe un agente `a1` en `opencode.json`. Para no modificar configuración del
repo, usar un config temporal fuera del repo. Ya se probó que resuelve el prompt
real de A1:

```bash
# /tmp/opencode/val001/opencode-a1.json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "opencode/big-pickle",
  "agent": {
    "a1": {
      "description": "A1 aislado para E01 (piloto VAL-001). Sin subagentes ni ejecucion.",
      "mode": "primary",
      "model": "opencode/big-pickle",
      "prompt": "{file:/home/cacelas/aiagents/docs/design/roles/A1-analista.md}",
      "tools": {
        "bash": false, "task": false, "webfetch": false, "websearch": false,
        "todowrite": false, "skill": false,
        "read": true, "glob": true, "grep": true, "write": true, "edit": true
      }
    }
  }
}
```

Comprobación ya ejecutada:

```bash
OPENCODE_CONFIG=/tmp/opencode/val001/opencode-a1.json \
  opencode debug agent a1
# tools: task=false, bash=false, question=false, read/write/edit=true;
# prompt_len=5432; model={"providerID":"opencode","modelID":"big-pickle"}
```

Preparación del sandbox simplificado: copiar solo lo que A1 necesita
(`docs/design/roles/A1-analista.md`, `docs/design/00-alcance-decisiones.md`,
`docs/design/03-necesidad-proporcionalidad.md`) y **excluir**
`docs/design/16-validacion.md`, `harness/` y este informe. Así A1 no lee la
respuesta esperada.

Ejecución:

```bash
cd /tmp/opencode/val001/simplificado
OPENCODE_CONFIG=/tmp/opencode/val001/opencode-a1.json \
opencode run \
  --agent a1 \
  --model opencode/big-pickle \
  --title "VAL-001/E01 simplificado" \
  "Quiero una herramienta para gestionar las inscripciones de un evento y avisar a la gente"
```

Captura: una sola sesión, sin hijos (`parent_id is null`), `task=false`
demostrado por la config y por la ausencia de sesiones hijas.

### 2.5 Regla de parada y de veredicto

- Parar en la **primera** pregunta de aclaración. A1 prohíbe preguntas compuestas
  (`A1-analista.md:33`), así que no se exige que las cuatro dimensiones se
  pregunten en un turno. Se exige que no se decidan en silencio y que las cuatro
  queden listadas como pendientes.
- Si el flujo escribe un spec, revisar cada requisito: origen explícito/derivado/
  control/extra; ningún canal, destinatario, horario o volumen inventado.
- Si pregunta una dimensión y deja las otras tres como pendientes: criterio 2
  puede ser APROBADO (sujeto actual) con nota de que solo se exploró una.
- Si pregunta las cuatro en una frase: no cumple la forma de A1 (pregunta
  compuesta), aunque no decida en silencio. Registrar como defecto separado.
- Si decide o implementa: criterio 2/3/5 fallan y E01 es RECHAZADO.
- **El veredicto E01 se aplica al Sujeto A** (el flujo actual es el evaluado).
  El simplificado es comparador, no rescata ni condena a E01. El propietario
  decide si acepta esta regla.

## 3. Estructura de evidencia propuesta

Ruta decidida: **`docs/validation/E01-2026-10-26/`** (hoy no existe; no está
ignorada por `.gitignore`).

```
docs/validation/E01-2026-10-26/
  README.md                 # informe principal: alcance, n=1, entrada exacta,
                            # modelo, SHA base, orden, veredicto E01, no-PROBADA
  manifest.json             # SHA, opencode --version, modelo, orden, hash de la
                            # entrada, sessionIDs, comandos y fechas
  actual/
    parent.json             # export completo del líder
    explorer.json           # export del subagente
    implementer.json
    reviewer.json
    transcript.json         # árbol combinado (parent + hijos)
    transcript.md           # render legible, con roles y tool calls
    sessions.json           # id, parent_id, agent, tokens, cost
    artifact/               # lo que produjo el sandbox (spec, bloqueo, etc.)
  simplificado/
    transcript.json
    transcript.md
    sessions.json
    artifact/
  medicion/
    tokens-coste.json       # por flujo y por sesión; fuente y consulta exacta
    opencode-stats.txt      # salida real de opencode stats
    opencode-models.txt     # salida real de opencode models --verbose
  criterios.md              # tabla de 12 criterios con evidencia y veredicto
  limitaciones.md           # n=1, orden, coste reportado, asimetrías, sesgos
```

Reglas de persistencia:

- `transcript.json` debe ser el export **completo** (mensajes, texto, tool calls y
  resultados). No usar `opencode export --sanitize` como evidencia principal:
  comprobado que sustituye el texto por `[redacted:...]` y deja el contenido
  ilegible. Exportar en crudo a `/tmp`, pasar `agents.redaction.redactar` a los
  textos y guardar en el repo solo credenciales tapadas; si no hay secretos, el
  contenido es idéntico. Documentar qué se redactó.
- El `README.md` debe enlazar cada archivo y declarar: `n=1`, un solo modelo,
  un solo commit base, ninguna conclusión de superioridad general y **ninguna
  autorización para eliminar agentes**. La fábrica sigue `DISEÑADO`, no `PROBADA`.
- El caso (herramienta de inscripciones) queda **pendiente de aclarar**, no
  listo ni aprobado, aunque E01 se declare APROBADO como comportamiento del flujo.

## 4. Medición de tokens y coste

Fuente real y comprobada, no estimación:

1. **Por sesión:** `opencode export <sessionID>` → `info.tokens`
   (`input`, `output`, `reasoning`, `cache.read`, `cache.write`) + `info.cost`.
   También `opencode db` sobre la tabla `session`:
   `tokens_input`, `tokens_output`, `tokens_reasoning`, `tokens_cache_read`,
   `tokens_cache_write`, `cost`, `parent_id`.
2. **Por flujo actual:** reconstruir el árbol con `parent_id` y sumar todas las
   sesiones (líder + explorador + implementador + revisor). La sesión padre no
   incluye los tokens de los hijos; hay que sumarlos.
3. **Coste:** `opencode models --verbose` y
   `~/.cache/opencode/models.json` declaran para `opencode/big-pickle`
   `input=0`, `output=0`, `cache.read=0`, `cache.write=0`; las sesiones
   exportadas dan `cost: 0.0` y `opencode stats --project "" --days 1 --models`
   da `Total Cost $0.00`. Por tanto el coste medido es **0.00 USD** según el
   proveedor/OpenCode.
4. **Limitación a declarar:** ese 0.00 es el coste reportado por OpenCode a
   partir de los metadatos del modelo; no es una factura independiente. Si el
   propietario necesita coste facturado, hay que declararlo «no verificado» y no
   multiplicar tokens por una tarifa inventada. `opencode stats` además mostró
   una agregación confusa (Output 32.1K frente a Output 131.1K en el desglose por
   modelo); usar el export por sesión como fuente primaria y citar la salida de
   `stats` solo como contraste.

Consulta reproducible para el informe:

```sql
WITH RECURSIVE tree(id) AS (
  SELECT :root
  UNION ALL
  SELECT s.id FROM session s JOIN tree t ON s.parent_id = t.id
)
SELECT id, parent_id, agent, model,
       tokens_input, tokens_output, tokens_reasoning,
       tokens_cache_read, tokens_cache_write, cost
FROM session
WHERE id IN (SELECT id FROM tree);
```

`medicion/tokens-coste.json` debe incluir, por flujo: `root_session`, `sessions`,
`tokens_input`, `tokens_output`, `tokens_reasoning`, `tokens_cache_read`,
`tokens_cache_write`, `cost_reported`, `cost_source`, `measured_at` y la consulta.
No sumar `reasoning` dentro de `output` sin decirlo; reportar ambos.

## 5. Riesgos de sesgo y mitigaciones

1. **El incumbent ejecuta el piloto.** El mismo arnés que se evalúa orquesta
   VAL-001 y puntúa. Mitigación: sandbox, rúbrica pre-registrada, no autoevaluación,
   reviewer/propietario independiente. Este informe es plan, no veredicto.
2. **Fuga de la rúbrica.** `current.md`, `featureslist.json` y este informe ya
   contienen el resultado esperado. Mitigación: sandbox neutro sin VAL-001, sin
   `docs/design/16-validacion.md` y sin `harness/progress/explorer-VAL-001.md`.
   No usar la sesión actual como Sujeto A.
3. **Prompt inicial contaminado.** La sesión actual nació de un mensaje que ya
   citaba las condiciones de pase. Mitigación: sesión nueva con solo la entrada
   exacta; registrar el hash de la entrada.
4. **Asimetría de contexto/herramientas.** El actual tiene AGENTS.md, harness,
   subagentes, `init.sh` y bash; el simplificado solo A1. Esa es la intervención,
   no un defecto oculto. Mitigación: declararlo, medir tokens por fase y no
   atribuir toda la diferencia al número de agentes.
5. **Sesgo de orden y de modelo.** n=1; el orden puede afectar. Mitigación:
   pre-registrar orden, usar el mismo modelo/variant/versión y no cambiar de
   configuración entre runs. No calcular significancia.
6. **Sesgo de puntuación.** El implementer podría favorecer al flujo actual.
   Mitigación: aplicar la tabla de criterios con evidencia enlazada; el reviewer
   verifica; el propietario firma E01. El implementer no firma.
7. **El flujo simplificado no es A1 real hasta que se ejecute.** La config
   temporal está probada (`opencode debug agent a1`), pero no se ha llamado al
   modelo. No presentar la config como resultado.
8. **El coste 0.00 puede no ser «real» en sentido contable.** Mitigación:
   declarar fuente y limitación; no estimar.

## 6. Qué debe hacer el implementer después (sin tocar producto)

1. **No implementar** la herramienta de inscripciones ni código de producto. Este
   piloto produce evidencia, no software. No cambiar `harness/featureslist.json`
   ni `current.md` a mano.
2. Confirmar con el propietario las decisiones abiertas de §7 (sandbox vs in-place,
   modo local, parada en la primera pregunta, veredicto sobre el Sujeto A, firma).
3. Crear `docs/validation/E01-2026-10-26/` con el esqueleto de §3 y un `README.md`
   que declare n=1, entrada exacta, modelo, SHA base, orden y limitaciones.
4. Ejecutar los dos sujetos en sandboxes separados según §2. Capturar exports
   completos y el árbol de sesiones. No simular respuestas del propietario.
5. Medir tokens/coste con §4; guardar la consulta y la salida real. Cruzar
   `opencode stats` y el export por sesión; si hay discrepancia, documentarla.
6. Puntuar los 12 criterios en `criterios.md` con enlaces a la evidencia. El
   veredicto E01 se basa en el Sujeto A; el simplificado se reporta aparte.
7. Actualizar **solo** la fila E01 de `docs/design/16-validacion.md` con resultado
   y revisor, y solo después de que el propietario revise/firme. Si no hay firma,
   dejar E01 `NO EJECUTADO` y registrar el resultado provisional en el informe:
   `16-validacion.md:153` exige firma para APROBADO. No tocar E02–E17.
8. Verificar el diff: solo E01 cambia; las otras 16 filas siguen `NO EJECUTADO`.
9. Registrar el trabajo con
   `harness record --agent implementer --id VAL-001 --content "..."`, incluyendo
   rutas, comandos, salidas y veredicto provisional. Enlazar
   `docs/validation/E01-2026-10-26/README.md` desde ese informe.
10. Pasar al reviewer. El reviewer ejecuta `./init.sh` completo y verifica los 12
    criterios con evidencia real; no implementa arreglos. Después, el líder pide
    `harness finish` solo si todo está en verde y el propietario firmó. El `finish`
    cierra VAL-001; **no** declara la fábrica PROBADA ni autoriza recortar agentes.
11. Si no se puede aislar el run, no se puede medir o falta la firma, registrar
    `BLOQUEADO`/limitación y parar. No rellenar con estimaciones.

## 7. Decisiones que debe tomar el propietario (no inventadas)

1. **Método:** ¿sandbox neutro (recomendado) o ejecutar el Sujeto A sobre el
   VAL-001 real, aceptando que `current.md` y este informe priman el resultado?
2. **GEAS en el sandbox:** ¿modo local (recomendado, evita reclamar tickets) o
   mantener `.geas.yml` y sincronizar? Si se mantiene, hay que aislar el ticket.
3. **Parada:** ¿parar en la primera pregunta (recomendado, no inventar respuestas)
   o simular respuestas del propietario? Simular respuestas exige un guion
   aprobado y deja de ser n=1 con la entrada exacta.
4. **Veredicto:** ¿E01 se decide con el Sujeto A (flujo actual) y el simplificado
   es solo comparador? Es la lectura coherente con «el flujo evaluado».
5. **Firma:** el propietario debe revisar y firmar E01; el implementer no puede
   declarar APROBADO por él.
6. **Coste:** ¿se acepta `0.00 USD` reportado por OpenCode como coste medido, con
   la limitación de que no es factura? Si no, declarar «no verificado».

## 8. Comandos y salidas usadas en esta investigación

```text
$ git rev-parse --short HEAD
0d38c72
$ opencode --version
1.18.32
$ opencode models | grep '^opencode/big-pickle$'
opencode/big-pickle
$ [ -d docs/validation ] && echo exists || echo absent
absent
$ grep -n '^| E01 ' docs/design/16-validacion.md
159:| E01 | NO EJECUTADO | — | — | — | Propietario |
```

`opencode models --verbose` (extracto real):

```json
"id": "big-pickle",
"providerID": "opencode",
"status": "active",
"cost": {"input": 0, "output": 0, "cache": {"read": 0, "write": 0}}
```

`opencode stats --project "" --days 1 --models` (extracto real):

```text
Total Cost                                        $0.00
Input                                            442.1K
Output                                            32.1K
Cache Read                                         6.2M
opencode/big-pickle  Messages 111  Input 442.1K  Output 131.1K  Cost $0.0000
```

`opencode export ses_e885e9ea8ffe2Glmn212t2DWBA` (extracto real):

```json
"model": {"id": "big-pickle", "providerID": "opencode"},
"cost": 0,
"tokens": {"input": 399173, "output": 29634, "reasoning": 97772,
           "cache": {"read": 5791104, "write": 0}}
```

`opencode debug agent a1` con el config temporal (extracto real):

```json
"name": "a1",
"model": {"providerID": "opencode", "modelID": "big-pickle"},
"tools": {"bash": false, "task": false, "read": true, "write": true, "edit": true},
"prompt_len": 5432
```

Archivos leídos: `AGENTS.md`, `harness/featureslist.json` (VAL-001),
`harness/progress/current.md`, `docs/design/16-validacion.md`,
`docs/design/roles/A1-analista.md`, `docs/design/README.md`,
`docs/design/00-alcance-decisiones.md`, `docs/design/03-necesidad-proporcionalidad.md`,
`docs/design/09-plantillas/README.md`, `agents/prompts/harness_workflow.md`,
`.opencode/agents/{lider,explorer,implementer,reviewer}.md`,
`vault/01_PROYECTO/objetivo.md`, `opencode.json`, `init.sh`.

## 9. Hipótesis que NO se han verificado

- Que el flujo actual, sin la rúbrica en contexto, pregunte en vez de decidir.
  Es exactamente lo que debe medir el piloto; no se ha ejecutado.
- Que A1 aislado pregunte una sola dimensión y no invente. La config está
  probada, no el comportamiento.
- Que el coste 0.00 de OpenCode coincida con una factura. Solo se ha verificado
  el metadato y el campo `cost` de las sesiones.

No se declara la fábrica PROBADA. No se generaliza desde n=1. No se autoriza
eliminar agentes ni recortar el arnés.
