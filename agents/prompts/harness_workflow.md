# Harness Workflow — Ciclo del arnés

Capa que gobierna a las demás: decide **qué** se hace y **cuándo está hecho**.
Los workflows de dominio (`data`, `ml`, `dev`...) dicen **cómo**.

## Pipeline
```
init.sh → harness/progress/ → harness/featureslist.json → explorer → implementer → reviewer → done
   │                                                                      │
   └────────────────── si init.sh falla: PARAR ───────────────────────────┘
```

## Paso a paso

| Paso | Comando | Quién | Verificación |
|------|---------|-------|-------------|
| Puerta | `run harness gate` (o `make init`) | `harness` | `success=true` = se puede trabajar |
| Elegir | `run harness next` | `harness` | retoma lo abierto o la primera con deps en `done` |
| Abrir | `run harness start --id <ID>` | `harness` | criterios volcados en `current.md` |
| Investigar | subagente `explorer` (solo lectura) | `explorer` | `run harness record --agent explorer` |
| Descomponer | `run plan brief --text "<feature>"` | `plan` | orden de trabajo con pasos y agentes |
| Implementar | subagente `implementer` | `implementer` | código + tests + `harness record` |
| Revisar | subagente `reviewer` | `reviewer` | `harness gate` en verde + criterios uno a uno |
| Cerrar | `run harness finish --id <ID> --evidence "..."` | `harness` | **rechaza** si la puerta falla o no hay evidencia |
| Commit del cierre | `run git commit_feature --id <ID> --title "..." [--dry-run true]` | `git` | bump + CHANGELOG + commit, con confirmación del usuario |

El `lider` decide en qué orden pasa todo esto; `harness` lo ejecuta. Ningún
agente edita `harness/featureslist.json` ni `harness/progress/` a mano.

## Las tres reglas

1. **Nada se cierra sin `./init.sh` en verde.** Es la única definición de «hecho»
   — y la aplica `harness finish` en código, no un prompt.
2. **Evidencia, no afirmaciones.** Cada criterio se cierra con la salida real del
   comando que lo prueba. `finish` sin `--evidence` devuelve `needs`.
3. **Todo subagente registra con `harness record` antes de devolver el control.**
   Lo que solo vive en la ventana de contexto se pierde.

## El cierre (README + versión + commit)

Sin `.geas.yml`, `harness finish` marca `done`; `git commit_feature` cierra el ciclo:

- `--dry-run true` devuelve la propuesta (siguiente versión patch, mensaje
  `feat(<id>): <título>`, ficheros que entrarían) **sin escribir nada**.
- Solo tras la confirmación del usuario se ejecuta sin `--dry-run`: bump de
  versión, entrada en CHANGELOG y commit. Sin tag, sin push.

### Modo GEAS remoto

Exporta `GEAS_ACTOR_ID=<UUID-personal>` (alias `GEAS_ACTOR`), sin versionar un
actor administrador. `.geas.yml` declara `mcp_url`, `organization_id` y
`repository_id` en YAML plano. Antes de leer progreso/decidir: `init.sh`
sincroniza API HTTP + Git local. También `--quick`; no sustituye la puerta completa.
`harness status/next/start/finish/block/add/record/link/sync` sincronizan antes
de operar; `gate → init → sync` usa la misma hoja, sin recursión.

Asocia explícitamente con `harness link --id <FEATURE> --ticket-id <UUID>` o
`start --ticket-id <UUID>`. Se valida repositorio, no se buscan títulos ni se
crean tickets. Históricos cerrados pueden no tener asociación. `start` reclama
por API y verifica mediante read-back estado, actor y `commit_before` antes
de modificar local. Retomar un ticket propio conserva el informe. El CAS
upstream y las lecturas no equivalen a una transacción distribuida perfecta:
el MCP puede ignorar un fallo CAS y complete no comprueba propietario por CAS.

1. Revisión, evidencia y puerta completa (`tests/` + `agents/tests/`) en verde.
2. Proponer README/versión/CHANGELOG y **commit de entregables**, pedir OK y
   ejecutar el commit autorizado antes del cierre.
3. `harness finish --id <FEATURE> --evidence "<salida real>" --yes`: propiedad,
   árbol limpio, puerta completa, re-sync sin mover HEAD, push por `git publish`,
   SHA publicado verificado con `ls-remote`, complete GEAS con read-back y **al
   final** done local. `--yes` autoriza push; no crea commits ni fuerza push.
4. Backlog/current/history de cierre quedan para otro commit explícito posterior.

`fetch`/`pull --ff-only --no-rebase --no-autostash` nunca pisan trabajo local.
Árbol sucio solo si no entran commits. Divergencia, conflictos, sin upstream,
detached, actor/config inválidos, permisos/red/timeout y push/pull fallidos
bloquean sin done falso. Corrige la causa y repite. Respuestas perdidas se
reconcilian por actor/SHA; DONE coincidente permite reintentar las escrituras
locales sin repetir complete ni duplicar histórico (solo suciedad de los tres
metadatos de cierre). Sin config se mantiene modo local; config rota no lo activa.
`start.sh`, `finish.sh`, `sync.sh`, `status.sh` son wrappers root-relative de
este flujo y usan API remota, nunca CLI GEAS/SQLite/sync del cwd del servidor.

## Contexto: qué NO hacer

- No heredes el contexto del líder a los subagentes. Pásales el ID de la
  feature, sus criterios y las rutas. Nada más.
- No releas el repositorio en cada subagente. `harness/progress/` existe justo para eso.
- No pases el contenido de un informe de subagente a otro: pasa la **ruta**.

## Cómo engancha con los agentes Python

El arnés decide y verifica; el trabajo determinista lo hacen los agentes:

| Necesidad del arnés | Agente | Acción |
|---------------------|--------|--------|
| Backlog y progreso (todo cambio de estado) | `harness` | `status`, `next`, `start`, `finish`, `block`, `record`, `add`, `gate`, `sync`, `link` |
| Descomponer una feature en pasos | `plan` | `brief`, `answer`, `execute` |
| Comprobar que la suite pasa | `test` | `run_tests`, `coverage_summary` |
| Revisar el código de una feature | `review` | `review_package` |
| Diagnóstico antes de abrir trabajo | `doctor` | `python -m agents doctor` |
| Saber si el equipo va bien | `audit` | `suggest` |
| Contexto de sesiones anteriores | `memory` | `status`, `search` |
| Buscar dónde está algo | `doc` | `search` |
| Cerrar la feature (versión + changelog + commit) | `git` | `commit_feature` |

```bash
uv run python -m agents --json run plan brief --text "<descripción de la feature>"
uv run python -m agents --json run test run_tests
uv run python -m agents --json run review review_package
```

## Ficheros

| Fichero | Dueño | Qué es |
|---------|-------|--------|
| `AGENTS.md` | humano | Protocolo y reglas del juego |
| `init.sh` | humano + `reviewer` | La puerta. El reviewer puede endurecerla |
| `harness/featureslist.json` | `harness` | Backlog con criterios de aceptación |
| `harness/progress/current.md` | `harness` | Feature en curso |
| `harness/progress/history.md` | `harness` | Append-only de lo cerrado |
| `harness/progress/<agente>-<ID>.md` | `harness` (vía `record`) | Resultado de una ejecución |
| `.opencode/agents/*.md` | cada agente | Su propia definición (automejorable) |

## Automejora

Si el mismo fallo se cuela dos veces: si es automatizable va a `init.sh`; si es
regla del proyecto va a `AGENTS.md`; si es criterio de revisión va a
`.opencode/agents/reviewer.md`. Deja constancia en `harness/progress/history.md`.

## Comandos

```bash
make init            # ./init.sh — verificación completa
make harness-check   # ./init.sh --quick — sin tests
make backlog         # estado de harness/featureslist.json
./init.sh --json     # salida estructurada para agentes
uv run python -m agents.evals.runner --harness   # valida las piezas del arnés
make index-rag       # mete harness/progress/ e histórico en el índice semántico
```
