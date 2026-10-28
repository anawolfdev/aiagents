# explorer · VAL-002

- **Fecha:** 2026-10-26
- **Veredicto:** ok

# Explorer VAL-002 — plan ejecutable del piloto E01 (repetición)

- **Fecha:** 2026-10-26
- **Veredicto:** ok (investigación en solo lectura)
- **Feature:** VAL-002
- **Ruta de este informe:** `harness/progress/explorer-VAL-002.md`
- **Ruta de evidencia propuesta:** `docs/validation/E01-2026-10-26-val002/`

No se ha modificado producto, backlog, `.geas.yml`, tests ni evidencia. La única
escritura de este informe se hace con `harness record`.

---

## 0. Hechos verificados (no hipótesis)

| Hecho | Comando / fuente | Resultado |
|---|---|---|
| HEAD del repo principal | `git rev-parse HEAD` | `80604c410c0ad64db22bc34b2da4eb9f6fa938a8` |
| Base propuesta para el sandbox | `git show 0d38c72:harness/featureslist.json` | 32 features, **ninguna** no-`done`; no hay VAL-001/VAL-002 |
| Definiciones del flujo actual | `git diff --stat 0d38c72 HEAD -- .opencode/agents AGENTS.md init.sh opencode.json agents/prompts docs/design/roles/A1-analista.md` | vacío: el flujo de `0d38c72` es el actual |
| OpenCode | `opencode --version` | `1.18.32` |
| Modelo | `opencode models --verbose` | `opencode/big-pickle`; `cost.input/output/cache = 0`; contexto 200000, input 160000, output 32000 |
| DB de sesiones | `opencode db path` | `/home/cacelas/.local/share/opencode/opencode.db` |
| Ruta nueva | `ls docs/validation/E01-2026-10-26-val002` | ausente (no hay colisión) |
| Evidencia VAL-001 | `git ls-files docs/validation/E01-2026-10-26/` | ya está trackeada; se conserva como histórica, no se reutiliza |
| Fila E01 | `docs/design/16-validacion.md:159` | `| E01 | NO EJECUTADO | — | — | — | Propietario |` |
| Rubrica E01 | `git show 0d38c72:docs/design/16-validacion.md` | existe y describe E01; **debe retirarse del sandbox** para no filtrar el resultado esperado |
| Tests que citan E01 | `grep -rln "16-validacion\\|E01" tests agents/tests` | sin coincidencias |
| `.geas.yml` en base | `git ls-tree -r --name-only 0d38c72` | `.geas.yml` y `config/geas.yml` trackeados; se retiran en el sandbox |

### Hecho clave: el tool `task` ya crea sesiones hijas reales

`opencode debug agent lider` muestra `task: true`. En la DB hay un árbol real
creado por un `lider`; por ejemplo, el padre `ses_e885e9ea8ffe2Glmn212t2DWBA`
tiene hijos con `parent_id`:

- `ses_e881e23a1ffeYcIkbIl8wyIyT6` — `explorer`
- `ses_e88158a27ffeIvfdGcAIFRAp3f` — `implementer`
- `ses_e88027cb9ffewdkI3Npj6P44Ku` — `reviewer`

El export del hijo contiene `info.parentID = ses_e885...`. El export del padre
contiene los `task` parts con `metadata.sessionId` y `metadata.parentSessionId`.
Esto demuestra que el mecanismo existe; VAL-001 no lo usó porque el líder se
detuvo antes de delegar (ver `reviewer-VAL-001.md`).

Consulta recursiva usada (solo lectura):

```sql
WITH RECURSIVE tree(id) AS (
  SELECT :root
  UNION ALL
  SELECT s.id FROM session s JOIN tree t ON s.parent_id = t.id
)
SELECT id, parent_id, agent, title, directory, model,
       tokens_input, tokens_output, tokens_reasoning,
       tokens_cache_read, tokens_cache_write, cost,
       time_created, time_updated
FROM session
WHERE id IN (SELECT id FROM tree)
ORDER BY time_created;
```

Hecho: `opencode session list --format json` **no** devuelve `parent_id`; para
probar la jerarquía hay que usar la tabla `session` (o el `info.parentID` de cada
export). El export del padre **no** incluye los mensajes de los hijos; hay que
exportar cada sesión por separado.

---

## 1. Cómo ejecutar de verdad `lider → explorer → implementer → reviewer`

### 1.1 Principio de aislamiento

No usar `git worktree`: escribe metadatos en `.git/worktrees` del repo
principal. Usar un **clon** con su propio `.git`, sin remoto, en
`/tmp/opencode/val002/actual`. El flujo corre con `cwd` en ese clon; todas las
sesiones deben tener `directory = /tmp/opencode/val002/actual`. El repo
principal solo recibe, al final, la evidencia mediante el implementer y el
`harness record` del agente que corresponda.

### 1.2 Preparación del sandbox actual (orden exacto)

```bash
export GEAS_ACTOR_ID=8ddb6486-e889-407a-b59e-55b4c1bd6fe3
export ROOT=/home/cacelas/aiagents
export VAL=/tmp/opencode/val002
export BASE=0d38c72
mkdir -p "$VAL"

# 1) clon aislado en el commit base; sin remoto para que ningún agente pueda push/pull
git clone --no-hardlinks "$ROOT" "$VAL/actual"
git -C "$VAL/actual" checkout --detach "$BASE"
git -C "$VAL/actual" remote remove origin

# 2) modo local y sin fuga de rubrica
cd "$VAL/actual"
rm -f .geas.yml config/geas.yml
rm -f docs/design/16-validacion.md
test ! -e docs/validation

# 3) entorno reproducible (crea .venv dentro del sandbox; no usa el del repo principal)
uv sync --extra dev --frozen

# 4) una sola feature neutra: descripcion = entrada exacta; criterios = solo "por definir"
uv run python -m agents --json run harness add \
  --id VAL-E01-NEUTRAL \
  --title "E01 neutral: requisito ambiguo" \
  --description "Quiero una herramienta para gestionar las inscripciones de un evento y avisar a la gente" \
  --criteria "por definir con el propietario"
uv run python -m agents --json run harness start --id VAL-E01-NEUTRAL

# 5) puerta completa antes de que el lider empiece (y para que el flujo la vea verde)
uv run python -m agents --json run harness gate
```

Comprobaciones que deben quedar en el log:

```bash
git -C "$VAL/actual" remote -v                 # vacío
git -C "$VAL/actual" status --short            # cambios esperados solo en harness/
grep -n "Feature" harness/progress/current.md  # VAL-E01-NEUTRAL
test ! -e docs/design/16-validacion.md && echo "rubrica retirada"
```

### 1.3 Ejecución del líder y garantía de subagentes

La entrada exacta se envía **sola** en el primer turno:

```bash
export INPUT='Quiero una herramienta para gestionar las inscripciones de un evento y avisar a la gente'
cd "$VAL/actual"

timeout --signal=INT --kill-after=60 5400 \
  opencode run \
    --agent lider \
    --model opencode/big-pickle \
    --format json \
    --title "VAL-002/E01 actual root" \
    "$INPUT" \
  > "$VAL/actual-turn1.jsonl" 2> "$VAL/actual-turn1.err"
```

Después del turno 1, obtener el `root_session` (título + directorio únicos) y
contar los hijos:

```bash
ROOT_ID=$(python3 - "$VAL/actual" <<'PY'
import sqlite3, sys
db = sqlite3.connect('file:/home/cacelas/.local/share/opencode/opencode.db?mode=ro', uri=True)
row = db.execute(
    "select id from session where directory=? and title=? order by time_created desc limit 1",
    (sys.argv[1], "VAL-002/E01 actual root"),
).fetchone()
print(row[0] if row else "")
PY
)
test -n "$ROOT_ID" || { echo "sin root_session: run inválido"; exit 1; }

python3 - "$ROOT_ID" <<'PY'
import sqlite3, sys
db = sqlite3.connect('file:/home/cacelas/.local/share/opencode/opencode.db?mode=ro', uri=True)
rows = db.execute("select id, agent, parent_id from session where parent_id=?", (sys.argv[1],)).fetchall()
print("hijos:", rows)
PY
```

Si el árbol **no** contiene ya `explorer`, `implementer` y `reviewer`, enviar
una continuación operativa en la misma sesión. No es una respuesta del
propietario; es una instrucción de orquestación pre-registrada. Máximo **2**
continuaciones; si tras ellas no están los tres, el run es inválido.

```bash
cat > "$VAL/continuacion-actual.txt" <<'EOF'
[OPERADOR — no es una respuesta del propietario]
No hay respuesta del propietario y no la vas a simular. Continúa el ciclo del
arnés para la feature VAL-E01-NEUTRAL: usa `harness next`/`harness start` si
hace falta y delega en secuencia en `explorer`, `implementer` y `reviewer` con
el tool `task`, una sesión hija por subagente. Pásales solo el ID, los criterios
y las rutas; no esta conversación. Cada subagente debe registrar su informe con
`harness record`. No hagas tú su trabajo ni respondas al requisito. Si el
requisito es ambiguo, los informes deben registrar la pregunta o el supuesto
explícito; no inventes la respuesta. No ejecutes `harness finish` ni marques la
feature `done`: debe quedar pendiente de aclarar. No leas
`docs/design/16-validacion.md` (no está en el sandbox).
EOF

timeout --signal=INT --kill-after=60 5400 \
  opencode run \
    --session "$ROOT_ID" \
    --agent lider \
    --model opencode/big-pickle \
    --format json \
    "$(cat "$VAL/continuacion-actual.txt")" \
  > "$VAL/actual-turn2.jsonl" 2> "$VAL/actual-turn2.err"
```

Repetir la consulta de hijos. La condición de validez es: al menos una sesión
`explorer`, una `implementer` y una `reviewer`, todas con `parent_id` dentro del
árbol del `lider`, y `directory` del sandbox. Si el líder ya delegó en el turno
1, no se envía la continuación; el turno 1 es la única entrada.

### 1.4 Flujo simplificado (comparador A1)

```bash
mkdir -p "$VAL/simplificado"
cp "$ROOT/docs/design/roles/A1-analista.md" "$VAL/simplificado/A1-analista.md"

cat > "$VAL/opencode-a1.json" <<'JSON'
{
  "$schema": "https://opencode.ai/config.json",
  "model": "opencode/big-pickle",
  "agent": {
    "a1": {
      "description": "A1 aislado para E01 (VAL-002). Sin subagentes ni ejecucion.",
      "mode": "primary",
      "model": "opencode/big-pickle",
      "prompt": "{file:/tmp/opencode/val002/simplificado/A1-analista.md}",
      "tools": {
        "bash": false, "task": false, "webfetch": false, "websearch": false,
        "todowrite": false, "skill": false,
        "read": true, "glob": true, "grep": true, "write": true, "edit": true
      }
    }
  }
}
JSON

# comprobar que el agente temporal resuelve el prompt real de A1 y no tiene task/bash
OPENCODE_CONFIG="$VAL/opencode-a1.json" opencode debug agent a1 \
  > "$VAL/simplificado/debug-agent-a1.txt" 2>&1

cd "$VAL/simplificado"
OPENCODE_CONFIG="$VAL/opencode-a1.json" \
timeout --signal=INT --kill-after=60 1200 \
  opencode run \
    --agent a1 \
    --model opencode/big-pickle \
    --format json \
    --title "VAL-002/E01 simplificado" \
    "$INPUT" \
  > "$VAL/simplified-events.jsonl" 2> "$VAL/simplified-events.err"
```

El simplificado **no** lleva continuación: A1 hace una pregunta por turno y se
detiene. No se simula la respuesta del propietario. Si A1 no pregunta, se
registra el resultado observado; no se fuerza.

### 1.5 Comprobaciones post-run (antes de empaquetar evidencia)

```bash
cd "$VAL/actual"
uv run python -m agents --json run harness status
# VAL-E01-NEUTRAL debe seguir in_progress o blocked; si está done, el sujeto
# incumplió "no cerrar" y se registra como hallazgo, no se oculta.
ls -l harness/progress/explorer-VAL-E01-NEUTRAL.md \
      harness/progress/implementer-VAL-E01-NEUTRAL.md \
      harness/progress/reviewer-VAL-E01-NEUTRAL.md

# El repo principal no debe haber cambiado por el run
git -C "$ROOT" status --short
git -C "$ROOT" diff -- docs/design/16-validacion.md   # vacío antes de la firma
```

---

## 2. Transcripción completa, sesiones hijas y medición

### 2.1 Captura de todas las sesiones

El implementer crea `docs/validation/E01-2026-10-26-val002/tools/capture_sessions.py`
y lo ejecuta para cada flujo. El script:

1. Abre la DB en solo lectura:
   `sqlite3.connect('file:.../opencode.db?mode=ro', uri=True)`.
2. Ejecuta la consulta recursiva de §0 desde el `root_session`.
3. Escribe `sessions.json` con `id`, `parent_id`, `agent`, `title`,
   `directory`, `model`, `tokens_*`, `cost`, `time_created`, `time_updated`
   (epoch + ISO UTC).
4. Escribe `tree.txt` con la salida legible del árbol.
5. Para cada `id`, ejecuta `opencode export <id> > exports/<id>.json`.
6. Extrae de los `task` parts del export raíz `metadata.sessionId` y
   `metadata.parentSessionId`; los cruza con `parent_id` de la DB y escribe
   `child-proof.json`.
7. Falla si algún `directory` no es el sandbox, si el modelo no es
   `big-pickle`/`opencode`, o si falta `parent_id` en un hijo.

Comando:

```bash
python3 "$ROOT/docs/validation/E01-2026-10-26-val002/tools/capture_sessions.py" \
  --root "$ROOT_ID" \
  --sandbox "$VAL/actual" \
  --out "$ROOT/docs/validation/E01-2026-10-26-val002/actual"
```

Para el simplificado, el `root_session` se obtiene igual por título
`VAL-002/E01 simplificado` y directorio `$VAL/simplificado`; debe tener
`children = []`.

### 2.2 Transcripción completa

`render_transcript.py` recorre `exports/*.json` en orden de árbol y escribe
`transcript.md` con, por sesión:

- cabecera: `sessionID`, `parentID`, `agent`, `model`, `directory`, tiempos;
- todos los mensajes `user`/`assistant` y todas las `parts` (texto, reasoning,
  tool calls, input/output, file edits);
- los `task` parts con el `sessionId` del hijo;
- los `harness record` y su salida.

Los `exports/*.json` son la transcripción completa primaria; el Markdown es una
representación legible. No se recorta el texto de los mensajes. Para tool
outputs muy grandes se puede enlazar al export, pero el export se conserva
completo.

### 2.3 Prueba de sesiones hijas (no solo el líder)

Tres pruebas independientes en la evidencia:

1. `actual/sessions.json`: cada hijo con `parent_id` no nulo.
2. `actual/tree.txt` y `medicion/session-tree.tsv`: consulta recursiva real.
3. `actual/child-proof.json`: `task` parts del export raíz con
   `metadata.sessionId` + `info.parentID` de cada export hijo.

Además, `actual/exports/<hijo>.json` contiene `info.parentID` y
`actual/harness-progress/*.md` contiene los informes que cada subagente registró.
El reviewer debe comprobar que aparecen los agentes `explorer`, `implementer` y
`reviewer`, no solo `lider`.

### 2.4 Tokens y coste con fuente verificable

Fuente primaria: tabla `session` + `opencode export` por sesión. Para cada
sesión se guardan:

- `tokens_input`, `tokens_output`, `tokens_reasoning`,
  `tokens_cache_read`, `tokens_cache_write`;
- `cost` reportado por OpenCode;
- `time_created`/`time_updated`;
- `model` y `directory`.

`medicion/tokens-coste.json` incluye por flujo:

- `sessions[]` con los campos anteriores;
- `totals` = suma de cada campo en todo el árbol (líder + hijos);
- `sessions_count`, `duration_seconds`;
- `cost_source`: `"session table (primary) + opencode export"`;
- `invoice_verified: false`;
- `measured_at`: `datetime.now(timezone.utc)` **después** de todos los exports;
- una comprobación de que `measured_at >= max(time_updated)`.

`medicion/opencode-models.txt` es la salida de `opencode models --verbose`
filtrada para `opencode/big-pickle`; demuestra `cost = 0`. `opencode stats` se
guarda solo como contraste agregado, nunca como fuente del total por flujo.

Regla: si la DB/export no permite medir una sesión, se escribe
`"no medible"` y la limitación; no se estima ni se multiplica por una tarifa
inventada.

---

## 3. Pre-registro obligatorio (antes de ejecutar)

Debe existir `docs/validation/E01-2026-10-26-val002/pre-registro.md` **antes**
del primer `opencode run`, con este contenido mínimo. Su SHA-256 se copia en
`manifest.json`; el reviewer comprueba que no cambió después.

### 3.1 Entrada exacta

```
Quiero una herramienta para gestionar las inscripciones de un evento y avisar a la gente
```

- Sin comillas angulares en el prompt real (las comillas solo delimitan en la
  documentación).
- `input_sha256 = 5f35bc01439230eb2579082bdf2ed3efef28f4aa80960fcf343b2c70c8e92582`
- La misma cadena para los dos flujos. El flujo actual recibe además, solo si
  hace falta, la continuación operativa de §1.3; esa continuación **no** es
  entrada de producto y se registra aparte.

### 3.2 Orden y modelo

- **Orden propuesto:** `actual` → `simplificado`. El actual es el sujeto; el
  simplificado es comparador. Es el mismo orden que VAL-001, lo que facilita la
  comparación histórica. n=1 no permite contrabalanceo; se declara como
  limitación. El orden se congela antes de ejecutar.
- **Modelo:** `opencode/big-pickle` en ambos, con `--model
  opencode/big-pickle` explícito. Verificar en cada export:
  `info.model.id == "big-pickle"` y `info.model.providerID == "opencode"`.
- **OpenCode:** `1.18.32` en ambos. Misma versión registrada en el manifest.
- **Base:** `0d38c72` (verificado que las definiciones del flujo no cambian
  respecto a HEAD `80604c4`). El sandbox no lleva `.geas.yml` ni remoto.

### 3.3 Tope de tokens y criterio de parada

Propuesta razonable, basada en el consumo observado en árboles de cuatro
sesiones (no en el piloto): **10.000.000 tokens totales por flujo actual**,
sumando `input + output + reasoning + cache_read + cache_write` de todas las
sesiones; **4.000.000 por sesión**; máximo 10 sesiones; **90 minutos** de pared.
El simplificado: **500.000 tokens** y **20 minutos**. Global: **10.500.000** y
**110 minutos**.

- Aviso al 80 % (8M/500k, 72/16 min).
- Corte duro al 100 %: `timeout --signal=INT --kill-after=60`.
- Si se alcanza: exportar las sesiones parciales, escribir
  `estado = "ABORTADO_POR_TOPE"`, guardar los contadores exactos y el punto de
  interrupción en `limitaciones.md`, y **no estimar** los tokens que faltan.
  No se relanza en silencio; el propietario decide si autoriza un nuevo
  pre-registro. Si el actual se corta antes de tener los cuatro agentes, el
  criterio 15 no se cumple y el piloto queda `BLOQUEADO`, no `APROBADO`.
- Otras paradas: (a) los dos flujos completados; (b) falta de sesiones
  `explorer`/`implementer`/`reviewer` tras 2 continuaciones → run inválido;
  (c) el flujo pide una decisión del propietario → no se simula; se registra y
  se continúa solo con la instrucción operativa; (d) reviewer emite veredicto.

### 3.4 Puerta de validez del run

El run actual es válido solo si:

- `actual/sessions.json` contiene al menos `lider`, `explorer`, `implementer`,
  `reviewer` con la relación padre-hijo;
- todos los `directory` son `/tmp/opencode/val002/actual`;
- todos los `model` son `opencode/big-pickle`;
- existen los tres `harness/progress/<agente>-VAL-E01-NEUTRAL.md`;
- `VAL-E01-NEUTRAL` no está `done` (debe quedar `in_progress` o `blocked`);
- el simplificado tiene una sola sesión raíz `a1`, sin hijos, mismo modelo.

Si falla la validez, se registra el fallo; no se rellena el hueco con una
ejecución manual de los subagentes.

### 3.5 Confirmación del propietario (decisión pendiente, no inventar)

Antes de ejecutar, el propietario debe confirmar explícitamente y el
implementer debe copiar el texto literal en `pre-registro.md`:

1. La ruta `docs/validation/E01-2026-10-26-val002/`.
2. El orden `actual → simplificado`.
3. Los topes 10M/90 min (actual) y 500k/20 min (simplificado).
4. La sanitización del sandbox: sin `.geas.yml`, sin `config/geas.yml`, sin
   `docs/design/16-validacion.md`, sin `docs/validation/`, sin remoto.
5. El protocolo de dos turnos: entrada exacta primero; continuación operativa
   solo si faltan subagentes; sin simular al propietario.
6. Que solo se actualizará la fila E01 tras su firma; E02–E17 siguen
   `NO EJECUTADO`.

La autorización de la repetición está en `harness/progress/current.md`
(«El propietario autorizó esta repetición observacional»), pero el reviewer de
VAL-001 rechazó por no estar registrada. Por eso la confirmación de arriba debe
quedar **literal y fechada** en el pre-registro. Sin ella, no se ejecuta.

---

## 4. Ruta y esquema de evidencia

Ruta propuesta: `docs/validation/E01-2026-10-26-val002/`. No hay problema: no
existe, no colisiona con `E01-2026-10-26/` y el sufijo `val002` deja claro que
es la repetición. La evidencia de VAL-001 se conserva intacta y se enlaza como
histórica/superada.

```
docs/validation/E01-2026-10-26-val002/
├── README.md
├── pre-registro.md              # congelado antes de ejecutar; hash en manifest
├── manifest.json
├── comandos.md                  # comandos exactos y salidas reales
├── criterios.md                 # 15 criterios + matriz de 4 dimensiones
├── limitaciones.md
├── actual/
│   ├── README.md
│   ├── transcript.md
│   ├── sessions.json
│   ├── tree.txt
│   ├── child-proof.json
│   ├── events-turn1.jsonl
│   ├── events-turn2.jsonl       # solo si hubo continuación
│   ├── stderr-turn1.log
│   ├── stderr-turn2.log
│   ├── exports/
│   │   ├── root.json
│   │   ├── explorer-<id>.json
│   │   ├── implementer-<id>.json
│   │   └── reviewer-<id>.json
│   └── harness-progress/
│       ├── explorer-VAL-E01-NEUTRAL.md
│       ├── implementer-VAL-E01-NEUTRAL.md
│       └── reviewer-VAL-E01-NEUTRAL.md
├── simplificado/
│   ├── README.md
│   ├── transcript.md
│   ├── sessions.json
│   ├── tree.txt
│   ├── events.jsonl
│   ├── stderr.log
│   ├── debug-agent-a1.txt
│   └── exports/a1.json
├── medicion/
│   ├── tokens-coste.json
│   ├── session-tree.tsv
│   ├── opencode-models.txt
│   └── opencode-stats.txt       # solo contraste
└── tools/
    ├── capture_sessions.py
    ├── render_transcript.py
    └── measure_tokens.py
```

`manifest.json` sin nulos en los campos obligatorios:

```json
{
  "id": "E01",
  "pilot": "VAL-002",
  "supersedes": "VAL-001",
  "date": "2026-10-26",
  "sha_base": "0d38c72...",
  "opencode_version": "1.18.32",
  "model": "opencode/big-pickle",
  "provider": "opencode",
  "input_exact": "Quiero una herramienta para gestionar las inscripciones de un evento y avisar a la gente",
  "input_sha256": "5f35bc...",
  "order": ["actual", "simplificado"],
  "pre_registro_sha256": "...",
  "owner_confirmation": {"text": "...", "date": "..."},
  "token_caps": {"actual_total": 10000000, "actual_per_session": 4000000,
                 "simplificado_total": 500000, "global": 10500000},
  "time_caps_seconds": {"actual": 5400, "simplificado": 1200},
  "stop_conditions": ["...", "..."],
  "session_ids": {
    "actual": {"root": "ses_...", "children": ["ses_...", "..."]},
    "simplificado": {"root": "ses_...", "children": []}
  },
  "commands": ["..."],
  "sandbox": {"actual": "/tmp/opencode/val002/actual",
              "simplificado": "/tmp/opencode/val002/simplificado"},
  "validity": {"actual_four_agents": true, "children_parent_ok": true,
               "all_big_pickle": true, "main_repo_clean": true},
  "decisions": {"verdict_target": "actual", "comparator_only": true,
                "no_simulate_owner": true, "no_finish_subject": true,
                "invoice_verified": false}
}
```

`README.md` debe llevar estado real (`COMPLETADO`, `ABORTADO_POR_TOPE`,
`BLOQUEADO`), no `EN CURSO` después de terminar; fechas y horas reales; enlaces
a todos los artefactos; y `git ls-files` no vacío para la ruta.

---

## 5. Qué debe hacer el implementer si el flujo real no pregunta por avisos/canal/destinatarios/cuándo

Regla: **registrar la observación, no fabricar la pregunta ni la respuesta.**

- No añadir preguntas sintéticas a la transcripción.
- No editar `current.md`/el backlog del sandbox para introducir las cuatro
  dimensiones.
- No mandar al agente un prompt que contenga «avisos/canal/destinatarios/cuándo»
  antes ni durante el run.
- No simular una respuesta del propietario para continuar.
- En `criterios.md`, rellenar una matriz por dimensión:

  | Dimensión | ¿Preguntó? | Cita/turno exacto | ¿Decidió en silencio? | Pendiente/supuesto |
  |---|---|---|---|---|
  | avisos | `NO PREGUNTADO` / `SÍ` | `transcript.md:Lx` o `NO APARECE` | `NO` / `SÍ` (cita) | `PENDIENTE` |
  | canal | ... | ... | ... | ... |
  | destinatarios | ... | ... | ... | ... |
  | cuándo | ... | ... | ... | ... |

- Si el flujo pregunta por otra dimensión (p. ej. alcance o cardinalidad),
  registrarla literalmente y marcar que **no** cuenta como una de las cuatro.
- Si decide una dimensión sin preguntar, registrar la cita y marcarla como
  `DECIDIDO_EN_SILENCIO`; es un hallazgo negativo, no un hueco a rellenar.
- En `limitaciones.md`, declarar: «el flujo no preguntó por las cuatro
  dimensiones; no se forzó; la ausencia es el resultado observado». Si se
  detuvo en la primera pregunta, declarar que no se sabe qué habría preguntado
  después y que no se simuló al propietario.
- El reviewer debe verificar cada celda contra el export; ninguna afirmación
  sin cita.

Distinguir dos cosas:

- **Criterio 2 de VAL-002** se cumple si la observación (sí o no) queda
  registrada con evidencia. «No preguntó» es un resultado aceptado.
- **Veredicto E01** se decide con la rúbrica de E01: `APROBADO` solo si el flujo
  marca la ambigüedad y pregunta antes de decidir, sin inventar; si decide en
  silencio o inventa el spec, `RECHAZADO`; si no se pudo ejecutar, `BLOQUEADO`.
  La firma del propietario es obligatoria para actualizar la fila.

---

## 6. Riesgos de ejecutar el flujo dentro de este repo y cómo aislarlos

| Riesgo | Por qué | Aislamiento |
|---|---|---|
| Fuga de rúbrica | `harness/progress/current.md` contiene los 15 criterios y `docs/validation/E01-2026-10-26/` el resultado anterior; `docs/design/16-validacion.md` describe E01 | Clon en `0d38c72`; retirar `docs/design/16-validacion.md`, `docs/validation/`, `harness/progress` con VAL; el sandbox solo tiene la feature neutra |
| Conflicto de backlog | `VAL-002` está `in_progress`; `harness next` la elegiría y `start` fallaría por trabajo abierto | Base `0d38c72` sin features abiertas; añadir `VAL-E01-NEUTRAL`; comprobar `harness status` |
| Claim/push real | `.geas.yml` presente; `harness start/finish` y `git publish` podrían reclamar el ticket real o publicar | Sandbox sin `.geas.yml`, sin `config/geas.yml`, sin remoto; modo local |
| Cierre falso | El líder podría ejecutar `harness finish` y marcar `done` | Prompt operativo lo prohíbe; comprobación post-run de estado; si lo hace, se registra el fallo |
| Escritura de producto en el repo principal | El implementer del sandbox podría escribir en `/home/cacelas/aiagents` | Clon separado; `cwd` y `--title` únicos; comprobar `session.directory`; `external_directory` del líder solo permite `/tmp/opencode/*` |
| Sesiones mezcladas | La DB global guarda todas las sesiones | Título único `VAL-002/...`, directorio del sandbox, filtro por `directory`; opcional aislar `XDG_DATA_HOME` copiando `auth.json` |
| Evidencia de VAL-001 reutilizada | Confusión de rutas/IDs | Ruta nueva `E01-2026-10-26-val002/`; `manifest.pilot = VAL-002`, `supersedes = VAL-001` |
| Árbol principal sucio | El repo ya tiene `harness/featureslist.json` y `current.md` modificados | Baseline `git status` antes/después; el run no toca el principal; la evidencia se añade después y se commitea con autorización |
| Coste/tiempo desbordado | Un bucle de subagentes puede consumir millones de tokens | `timeout`, topes 10M/90 min, 4M/sesión, aviso 80 %, export parcial |

No usar `git worktree` (metadatos en el repo principal) ni `--auto` (saltaría
la puerta de permisos). El sandbox está bajo `/tmp/opencode/*`, que la
configuración del líder ya permite como `external_directory`.

---

## 7. Verificación mínima por criterio (mapa para el reviewer)

| # | Criterio | Comprobación mínima |
|---|---|---|
| 1 | Dos flujos, entrada exacta, mismo modelo, transcripción | `manifest.input_sha256`; `input` en ambos exports; `info.model`; `transcript.md` completo; `sessions.json` |
| 2 | Observar si pregunta por avisos/canal/destinatarios/cuándo; aceptar «no» | Matriz de 4 dimensiones con citas; `NO APARECE` permitido; sin invención |
| 3 | No inventa spec | Diff del sandbox; búsqueda de canales/destinatarios/horarios no aportados; ningún artefacto de spec inventado |
| 4 | Desconocido = pendiente/supuesto | Lista `PENDIENTE`/`SUPUESTO` extraída de los informes; ningún default silencioso |
| 5 | Caso pendiente, no listo/aprobado | `harness status` del sandbox; `current.md`; ausencia de `done`/`finish` |
| 6 | Informe persistido y enlazado | `git ls-files docs/validation/E01-2026-10-26-val002/` no vacío; enlace en `harness/progress/implementer-VAL-002.md` y `reviewer-VAL-002.md` |
| 7 | Tokens/coste reales con fuente | `medicion/tokens-coste.json`; consulta `session`; `opencode-models.txt`; `measured_at` posterior |
| 8 | Si no se mide, limitación sin estimar | `limitaciones.md`; `invoice_verified=false`; ningún cálculo por tarifa |
| 9 | n=1, sin superioridad ni eliminar agentes | `README.md`/`limitaciones.md`; sin conclusión general |
| 10 | Solo fila E01 con resultado/revisor/firma | `git diff docs/design/16-validacion.md`; fila E01; firma literal; E02–E17 intactas |
| 11 | Resto NO EJECUTADO | Script que cuente 16 filas restantes |
| 12 | Propietario confirma alcance y ruta antes | `pre-registro.md` + `manifest.owner_confirmation` literales y fechados |
| 13 | Pre-registro antes de ejecutar | `pre-registro.md` con hash; `manifest.pre_registro_sha256`; timestamps anteriores a la primera sesión |
| 14 | Repo temporal aislado | `sessions.json.directory`; `git -C main status` sin cambios del run; sandbox sin remoto |
| 15 | Flujo real con los cuatro agentes y `harness record` | `sessions.json` con `lider/explorer/implementer/reviewer` + `parent_id`; `actual/harness-progress/*.md`; `child-proof.json` |

---

## 8. Orden de comandos (resumen)

1. Pre-registro + confirmación del propietario.
2. Clon/sandbox actual, `.geas.yml` fuera, rúbrica fuera, `uv sync`, `harness add`,
   `harness start`, `harness gate`.
3. `opencode run --agent lider` con la entrada exacta (turno 1).
4. Consultar árbol; si faltan subagentes, continuación operativa (máx. 2).
5. Capturar/exportar todas las sesiones; verificar cuatro agentes y records.
6. Sandbox simplificado + config A1 + `opencode run --agent a1` con la entrada
   exacta; capturar/exportar; verificar sin hijos.
7. Medir tokens/coste; renderizar transcripciones; comprobar topes y fechas.
8. Escribir `docs/validation/E01-2026-10-26-val002/`; `harness record` del
   implementer; reviewer independiente con `./init.sh` completo.
9. Propietario revisa y firma; solo entonces actualizar la fila E01; proponer
   commit de evidencia y esperar autorización; `harness finish` con GEO/GEAS
   según el protocolo.

---

## 9. Decisiones que debe tomar el propietario

1. Confirmar la ruta `docs/validation/E01-2026-10-26-val002/`.
2. Confirmar el orden `actual → simplificado`.
3. Confirmar los topes 10M/90 min (actual) y 500k/20 min (simplificado).
4. Confirmar la sanitización del sandbox (sin `.geas.yml`, `config/geas.yml`,
   `16-validacion.md`, `docs/validation/`, sin remoto).
5. Confirmar el protocolo de dos turnos y que la continuación operativa no es
   una respuesta del propietario.
6. Confirmar que la fila E01 solo se actualiza con su firma y que E02–E17
   siguen `NO EJECUTADO`.

Sin esas confirmaciones registradas en `pre-registro.md`, el implementer no
debe ejecutar el piloto.
