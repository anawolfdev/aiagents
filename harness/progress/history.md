# Historial del arnés

Registro append-only de features completadas. Es el changelog del trabajo hecho
por agentes: qué se cerró, con qué evidencia y qué quedó pendiente.

Formato de cada entrada:

```
## <FEATURE-ID> — <título>

- **Cerrada:** YYYY-MM-DD
- **Verificación:** ./init.sh en verde · N tests pasando
- **Cambios:** rutas de los ficheros tocados
- **Decisiones:** lo que se eligió y por qué (solo si no es obvio desde el código)
- **Pendiente:** lo que se dejó fuera a propósito
```

---

_(sin features completadas todavía — el proyecto acaba de empezar)_

## BOOT-001 — Arranque en frio operativo: contratos inline + agente bootstrap

- **Cerrada:** 2026-08-04
- **Verificación:** ./init.sh en verde · 6 passed in 0.31s
- **Cambios:** agents/agents/bootstrap_agent.py; agents/prompts/bootstrap_agent.md (nuevo); agents/tests/test_bootstrap_agent.py (nuevo, 20 tests); agents/tests/test_contracts.py (+6 tests de contratos inline); conteo 23->24 y ficha de bootstrap en README.md, AGENTS.md, agents/README.md, agents/prompts/agents_reference.md, agents/prompts/orchestrator.md, .opencode/agents/orquestador.md, .opencode/agents/lider.md, .claude/agents/lider.md (regenerado)
- **Decisiones:** BootstrapAgent.describe() tapaba BaseAgent.describe() y reventaba 'python -m agents list' con TypeError. Arreglo: el metodo pasa a llamarse describe_project y la clave de accion sigue siendo 'describe', asi que la CLI no cambia. Queda un test de regresion generico sobre list_agents(). Pendientes reportados y NO tocados: (a) 'describe' esta en destructive, asi que el criterio de ONBOARD-001 tal como esta escrito en TICKETS_ARRANQUE es infalsable sin --yes; (b) status devuelve first_run=true en este repo pese a tener 7 features, relevante para BOOT-003; (c) el conteo de agentes en los docs se escapo dos veces: candidato a check en init.sh.
- **Pendiente:** _(nada)_

<details><summary>Evidencia</summary>

```
$ make check
uv run ruff check app/ tests/ agents/
All checks passed!
uv run ruff format --check app/ tests/
6 files already formatted
uv run mypy app/ tests/
Success: no issues found in 6 source files
  typecheck OK
uv run pytest
======================= 490 passed, 15 skipped in 16.99s =======================
  check pasado: lint + typecheck + test + arnes OK
EXIT=0

$ uv run python -m agents.prompts_sync
Prompts y subagentes sincronizados con el codigo y con los contratos.
PROMPTS_EXIT=0

$ uv run python -m agents list | wc -l
24
```

</details>

## BOOT-002 — installer scaffold: creador de agentes autocontenidos

- **Cerrada:** 2026-08-04
- **Verificación:** ./init.sh en verde · 6 passed in 0.35s
- **Cambios:** agents/tools/agent_scaffold_tool.py (nuevo: AgentSpec + AgentScaffoldTool); agents/agents/installer_agent.py (accion scaffold); agents/contracts.py (solo el contrato de installer: scaffold en destructive); agents/prompts/installer_agent.md (prosa sobre scaffold + AUTOGEN); agents/tests/test_installer_scaffold.py (nuevo, 22 tests)
- **Decisiones:** El generador no puede reproducir el bug de BOOT-001: si una ACCION colisiona con un metodo de BaseAgent renombra el METODO (describe -> describe_action) y conserva el nombre de la accion; si el NOMBRE DEL AGENTE colisiona, rechaza. Verificado generando un agente con acciones describe/run/actions/can_handle: 'python -m agents list' sigue en exit 0. La logica de renderizado va en agents/tools/agent_scaffold_tool.py y no dentro del agente, siguiendo la convencion que declara _template_agent.py. owns con recurso ya adueñado se rechaza en validar(), no solo en validate_contracts(). name y description tienen default '' en vez de ser obligatorios para devolver success=False + needs en vez de un TypeError en la CLI (patron de git.commit_feature). DEUDA ANOTADA, no tocada: agents/permissions.py:70 decide con 'not kwargs.get(dry_run)', mirando los kwargs recibidos y no el default de la firma, asi que scaffold sin --dry_run explicito queda bloqueado por la puerta aunque no fuera a escribir nada. Falla del lado seguro; arreglarlo cambia la puerta para los 24 agentes y es feature aparte.
- **Pendiente:** _(nada)_

<details><summary>Evidencia</summary>

```
$ make check
uv run ruff check app/ tests/ agents/
All checks passed!
uv run ruff format --check app/ tests/
6 files already formatted
uv run mypy app/ tests/
Success: no issues found in 6 source files
  typecheck OK
uv run pytest
======================= 512 passed, 15 skipped in 11.31s =======================
  check pasado: lint + typecheck + test + arnes OK
CHECK_EXIT=0

$ uv run python -m agents.prompts_sync
Prompts y subagentes sincronizados con el codigo y con los contratos.
P_EXIT=0

$ ls agents/external/   -> __init__.py  README.md  (ningun agente generado suelto)

Prueba de fuego del reviewer sobre una COPIA del repo, generando agentes reales con --dry_run false --yes:
  1 agente generado  -> make check: 517 passed, exit 0
  3 agentes generados -> make check: 535 passed, exit 0
  ./init.sh completo  -> ENTORNO LISTO, 0 avisos
  dry-run: md5 de todo el arbol identico antes/despues (solo cambia agents/workspace/audit/audit.jsonl, el log de BaseAgent.run)
  barrido AST: las 14 llamadas a AgentResult de los modulos generados tienen success=False, y las 14 acciones fallan con needs no vacio
```

</details>

## BOOT-004 — knowledge sync_agent_cards: las fichas del vault desde los contratos

- **Cerrada:** 2026-08-04
- **Verificación:** ./init.sh en verde · 6 passed in 0.34s
- **Cambios:** agents/agents/knowledge_agent.py (accion sync_agent_cards + helpers); agents/contracts.py (knowledge.destructive); agents/permissions.py (_es_dry_run resuelve el defecto de la firma); agents/core/base_agent.py (1 linea: pasa el metodo a la puerta); agents/prompts_sync.py (_splice acepta begin/end, reutilizado); agents/tests/test_knowledge_agent.py (+6 tests); agents/tests/test_permissions.py (+2 tests); agents/prompts/knowledge_agent.md; README.md; vault/05_AGENTES/ (24 fichas + fila de bootstrap en _index.md)
- **Decisiones:** El contrato de knowledge prometia desde el principio 'poblar vault/05_AGENTES/ con fichas desde contracts.py' y eso nunca estuvo implementado: un contrato que miente. Esta feature nace de ese hallazgo al bloquear BOOT-003. Las fichas se generan desde all_contracts() (no CONTRACTS) para que los agentes de contrato inline como bootstrap tengan ficha. El nombre de fichero sale de cls.__name__ y no del name del agente, para respetar la convencion existente (GitAgent.md, APIAgent.md). La prosa a mano de las fichas se conserva con el _splice de prompts_sync, reutilizado en vez de duplicado. _index.md NO se autogenera (agrupa por categorias humanas y lleva un mermaid que el contrato no contiene): la accion lo audita y avisa. Las fichas huerfanas se reportan, no se borran. EFECTO EN LA CAPA COMPARTIDA: marcar sync_agent_cards como destructive dejaba su propio dry-run pidiendo confirmacion, asi que se arreglo la puerta (agents/permissions.py) para que resuelva el defecto de la firma y no solo los kwargs recibidos. Acerca el codigo a lo que AGENTS.md ya documentaba ('un --dry-run nunca pregunta'). Auditadas las 14 acciones destructivas: ninguna irreversible perdio su confirmacion. AVISO: la revision del subagente reviewer se corto por limite de gasto de la API sin emitir veredicto; el bloque critico lo verifico el lider y lo que quedo sin revisar esta listado en harness/progress/reviewer-BOOT-004.md.
- **Pendiente:** _(nada)_

<details><summary>Evidencia</summary>

```
$ make check
All checks passed!
6 files already formatted
Success: no issues found in 6 source files
  typecheck OK
======================= 520 passed, 15 skipped in 51.35s =======================
  check pasado: lint + typecheck + test + arnes OK
CHECK_EXIT=0

$ uv run python -m agents.prompts_sync
Prompts y subagentes sincronizados con el codigo y con los contratos.  P_EXIT=0

$ ./init.sh
  pytest  6 passed in 0.55s
  ENTORNO LISTO  0 aviso(s)

$ run knowledge sync_agent_cards            (dry-run)  -> md5 del arbol de vault/ identico antes y despues
$ run knowledge sync_agent_cards --dry_run false --yes  -> 24 fichas sincronizadas
$ segunda pasada real -> 0 nuevas, 0 actualizadas, 24 sin cambios; md5 identico (idempotente)
$ md5 de vault/ identico antes y despues de make check -> la suite no toca el vault real
$ ls vault/05_AGENTES/*.md | wc -l -> 25 (24 fichas + _index.md); BootstrapAgent.md presente

Auditoria de la puerta de permisos (14 acciones destructivas, ejecutada):
  las 12 acciones irreversibles siguen pidiendo confirmacion sin argumentos;
  solo installer.scaffold y knowledge.sync_agent_cards (dry_run=True por defecto) no la piden,
  y ambas la piden con dry_run=False explicito. No se abrio agujero.
```

</details>

## BOOT-003 — Protocolo de arranque en frio en el lider + documentacion

- **Cerrada:** 2026-08-04
- **Verificación:** ./init.sh en verde · 6 passed in 0.41s
- **Cambios:** .opencode/agents/lider.md (paso 0 + seccion de arranque en frio); .claude/agents/lider.md (regenerado con assistants-sync, no a mano); agents/agents/bootstrap_agent.py (criterio de ONBOARD-001 en TICKETS_ARRANQUE: --yes); agents/README.md (seccion installer scaffold); AGENTS.md (paso 0 + seccion Arranque en frio); harness/featureslist.json via bootstrap seed --yes (ONBOARD-001 y ONBOARD-002)
- **Decisiones:** La feature estuvo BLOQUEADA: el criterio del vault no era alcanzable porque ninguna accion escribia vault/05_AGENTES/ pese a que el contrato de knowledge lo prometia. Se abrio BOOT-004 para implementarlo y se reabrio esta. Sobre la puerta: se decidio NO sacar 'describe' de destructive (escribir la identidad del proyecto merece confirmacion y la puerta falla del lado seguro); lo que se arreglo fue el criterio de ONBOARD-001, que sin --yes era infalsable. El ciclo de arranque en frio deja explicito en el prompt del lider que las preguntas de 'describe' son para el usuario y no se deducen del codigo, y que suggest_agents da candidatos lexicos y no un veredicto. PENDIENTE DE DECISION DEL USUARIO: SCOPE-001 se solapa con ONBOARD-001 (los dos producen el objetivo del proyecto en el vault); no se borro nada porque harness no tiene accion de borrado y la decision es del usuario.
- **Pendiente:** _(nada)_

<details><summary>Evidencia</summary>

```
$ make check
All checks passed!
6 files already formatted
Success: no issues found in 6 source files
  typecheck OK
================= 520 passed, 15 skipped in 188.32s (0:03:08) ==================
  check pasado: lint + typecheck + test + arnes OK
CHECK_EXIT=0

$ ./init.sh
  ENTORNO LISTO  0 aviso(s)

$ uv run python -m agents.prompts_sync
Prompts y subagentes sincronizados con el codigo y con los contratos.
(esto cubre tambien que .claude/agents/lider.md esta sincronizado con .opencode/agents/lider.md)

$ grep -n "Paso 0" .opencode/agents/lider.md
14: uv run python -m agents --json run bootstrap status
15: #   first_run=false -> sigue en el paso 1
16: #   first_run=true  -> arranque en frio antes de abrir ninguna feature
46: ## Paso 0 - arranque en frio
85: **Condicion de salida:** run bootstrap status devuelve description_pending: false

$ backlog
ONBOARD-001    pending      Entender el proyecto
ONBOARD-002    pending      Que se sabe ya y que agentes hacen falta

$ criterio de ONBOARD-001 corregido
uv run python -m agents run bootstrap describe --description \"<respuesta del usuario>\" --yes devuelve success=true

$ agents/README.md: linea 77 \"los 24 agentes\", linea 205 seccion \"installer scaffold\", linea 238 \"Los 24 agentes\"
$ AGENTS.md: linea 15 paso 0 en el bloque de protocolo, linea 26 seccion \"Arranque en frio\"
$ vault/05_AGENTES/BootstrapAgent.md presente con el contrato inline (generado por knowledge sync_agent_cards en BOOT-004)
```

</details>

## FIX-001 — app.__main__ rompe los imports: falta la guarda __name__

- **Cerrada:** 2026-08-04
- **Verificación:** ./init.sh en verde · 7 passed in 0.13s
- **Cambios:** app/__main__.py (guarda if __name__ == '__main__'); tests/test_main_import.py (nuevo: test de regresion que importa app.__main__ y barre el paquete)
- **Decisiones:** El test importa app.__main__ a nivel de modulo: si la guarda regresa, pytest muere en coleccion con SystemExit(2) y no solo falla un caso. Diagnosticado el alcance: pkgutil.walk_packages(app.__path__) importa app.__main__, por eso barrer el paquete mataba el proceso.
- **Pendiente:** _(nada)_

<details><summary>Evidencia</summary>

```
$ uv run python -c "import app.__main__; print('ok')"  ->  ok, EXIT=0 (sin usage)
$ uv run python -m pytest tests/ -q --no-header        ->  7 passed in 0.40s
$ uv run python -m app hello                           ->  Hola, mundo. EXIT=0
$ make check                                           ->  check pasado: lint + typecheck + test + arnes OK
$ ./init.sh                                            ->  ENTORNO LISTO  0 aviso(s)
```

</details>

## REPAIR-001 — Recuperar las definiciones y el entorno del arnés

- **Cerrada:** 2026-10-22
- **Verificación:** ./init.sh en verde · 7 passed in 0.18s
- **Cambios:** Restauradas seis definiciones OpenCode, espejos Claude, referencias prompt válidas y checker con 17 regresiones. Entorno Python 3.12 y extra dev instalados.
- **Decisiones:** Reparación explícitamente autorizada. Se conserva modelo y nombres de agentes y el cambio previo uv.lock. No se inventa objetivo SCOPE/ONBOARD.
- **Pendiente:** _(nada)_

<details><summary>Evidencia</summary>

```
Revisión independiente: uv run pytest -> 538 passed, 15 skipped (extras opcionales fastapi/chromadb). ./init.sh -> ENTORNO LISTO, 7 passed, 0 avisos. make opencode-check y uv run python -m agents.prompts_sync pasan. OpenCode carga los seis prompts con options={}. Ver harness/progress/implementer-REPAIR-001.md y reviewer-REPAIR-001.md para salida completa.
```

</details>

## GEAS-001 — Sincronización remota GEAS y Git obligatoria en init y arnés

- **Cerrada:** 2026-10-22
- **Verificación:** ./init.sh en verde · 612 passed, 15 skipped in 46.18s
- **Cambios:** Cliente HTTP GEAS, sync Git ff-only seguro, claim con read-back, push contra destino fijado y verificado, cierre remoto, lock de estado y regresiones.
- **Decisiones:** Configuración remota presente falla cerrada; repos sin .geas.yml conservan modo local. El push exige confirmación explícita. La revisión independiente de ronda 2 fue cancelada por el usuario para priorizar la publicación.
- **Pendiente:** Commit posterior de los metadatos de cierre.

<details><summary>Evidencia</summary>

```
Correcciones ronda 1 verificadas: add concurrente sin pérdida de escritura confirmada; reintento de claim conserva notas; árbol sucio no integra commits tardíos; cambio de destino Git durante la puerta bloquea publicación; status.sh válido con bash -n. Evidencia: agents/tests/test_geas_integration.py 74 passed; ./init.sh con actor real 612 passed, 15 skipped, ENTORNO LISTO 0 avisos; ruff check/format, prompts_sync, opencode_check y git diff --check OK. Push verificado: 5ab1a2568f7a0f9ed4ab3937155bd9e7fe4e4bb3 en origin/main.
```

</details>

## FAB-001 — Alcance, principios y registro de decisiones del paquete de diseño

- **Cerrada:** 2026-10-22
- **Verificación:** ./init.sh en verde · 612 passed, 15 skipped in 51.01s
- **Cambios:** _(no indicados)_
- **Decisiones:** _(ninguna reseñable)_
- **Pendiente:** _(nada)_

<details><summary>Evidencia</summary>

```
docs/design/00-alcance-decisiones.md (271 líneas) cubre alcance, propietario, entornos, portabilidad, principio rector, no-goals, 28 decisiones confirmadas con origen, 4 decisiones de diseño etiquetadas, 15 parámetros pendientes y estados DISEÑADO/CONFIGURADO/PROBADO/DESPLEGADO. Revisión independiente aprobada. ./init.sh: ENTORNO LISTO, 612 passed, 15 skipped, 0 avisos. git diff --check OK. uv.lock sincronizado a 0.1.2.
```

</details>

## FAB-002 — Matriz de necesidad y proporcionalidad; política de extras y exclusiones

- **Cerrada:** 2026-10-22
- **Verificación:** ./init.sh en verde · 612 passed, 15 skipped in 45.81s
- **Cambios:** docs/design/03-necesidad-proporcionalidad.md; política de extras y plantilla
- **Decisiones:** 5 mantener, 1 simplificar, 6 proponer exclusión, 1 posponer; vigilancia diaria de A2 confirmada
- **Pendiente:** Presupuesto, horario, Telegram, proveedor/modelo y corpus documental

<details><summary>Evidencia</summary>

```
docs/design/03-necesidad-proporcionalidad.md (140 líneas): matriz de 13 filas obligatorias, 10 columnas, plantilla y política de extras. Revisión ronda 1 rechazada por fila 7 y corregida a Proponer exclusión; ronda 2 aprobada. ./init.sh: ENTORNO LISTO, 612 passed, 15 skipped, 0 avisos. git diff --check OK. uv.lock sincronizado a 0.1.3.
```

</details>

## FAB-003 — Instrucción de sistema A1 — analista y entrevistador

- **Cerrada:** 2026-10-22
- **Verificación:** ./init.sh en verde · 612 passed, 15 skipped in 47.94s
- **Cambios:** docs/design/roles/A1-analista.md
- **Decisiones:** Una pregunta por turno; supuestos explícitos; requisitos y extras separados; validación humana del spec
- **Pendiente:** Herramientas y permisos concretos del propietario

<details><summary>Evidencia</summary>

```
docs/design/roles/A1-analista.md: perfil autosuficiente con misión, entradas, procedimiento de una pregunta por turno, spec de 16 apartados, pruebas mínimas, requisitos vs extras, prohibiciones, bloqueos, destinatario y validación humana. Revisión independiente aprobada (reviewer-FAB-003.md). ./init.sh: ENTORNO LISTO, 612 passed, 15 skipped, 0 avisos.
```

</details>

## FAB-004 — Instrucción de sistema A2 — revisión inicial y vigilancia

- **Cerrada:** 2026-10-22
- **Verificación:** ./init.sh en verde · 612 passed, 15 skipped in 45.01s
- **Cambios:** docs/design/roles/A2-riesgos-vigilancia.md
- **Decisiones:** Modo inicial y periódico separados; cobertura independiente del spec; regla de 7 días; vigilancia diaria pendiente de activación
- **Pendiente:** Activar GitHub Actions y definir fuentes autorizadas cuando el propietario lo autorice

<details><summary>Evidencia</summary>

```
docs/design/roles/A2-riesgos-vigilancia.md: modos inicial y periódico, cobertura independiente del spec, regla de siete días, fuentes inaccesibles/caducadas/contradictorias, defensa ante prompt injection y vigilancia diaria pendiente de activación. Revisión independiente aprobada (reviewer-FAB-004.md). ./init.sh: ENTORNO LISTO, 612 passed, 15 skipped, 0 avisos.
```

</details>

## FAB-005 — Instrucción de sistema A3 — arquitecto y consolidador

- **Cerrada:** 2026-10-22
- **Verificación:** ./init.sh en verde · 612 passed, 15 skipped in 48.08s
- **Cambios:** docs/design/roles/A3-arquitecto.md
- **Decisiones:** GATE 1 sobre spec consolidado; cambios materiales vuelven a evaluación; A3 no aprueba
- **Pendiente:** Umbrales concretos de riesgo y presupuesto

<details><summary>Evidencia</summary>

```
docs/design/roles/A3-arquitecto.md: consolidación con tratamiento por hallazgo, alternativas comparadas, arquitectura mínima, matriz requisito-capacidad-permiso-prueba, GATE 1, cambios materiales y separación consolidar/aprobar. Revisión independiente aprobada (reviewer-FAB-005.md). ./init.sh: ENTORNO LISTO, 612 passed, 15 skipped, 0 avisos.
```

</details>

## FAB-006 — Instrucción de sistema A4 — constructor

- **Cerrada:** 2026-10-22
- **Verificación:** ./init.sh en verde · 612 passed, 15 skipped in 47.10s
- **Cambios:** docs/design/roles/A4-constructor.md
- **Decisiones:** Entorno local no equivale a aislado; el artefacto se congela para A5; A4 no aprueba ni despliega
- **Pendiente:** Herramientas y límites concretos del entorno de construcción

<details><summary>Evidencia</summary>

```
docs/design/roles/A4-constructor.md: alcance aprobado, aislamiento y datos verificados, artefacto congelado con manifiesto, reversión documentada y separación construir/aprobar. Revisión independiente aprobada (reviewer-FAB-006.md). ./init.sh: ENTORNO LISTO, 612 passed, 15 skipped, 0 avisos.
```

</details>

## FAB-007 — Instrucción de sistema A5 — evaluador independiente

- **Cerrada:** 2026-10-22
- **Verificación:** ./init.sh en verde · 612 passed, 15 skipped in 45.77s
- **Cambios:** docs/design/roles/A5-evaluador.md
- **Decisiones:** Conformidad técnica no autoriza despliegue; independencia obligatoria; pruebas reservadas con control real
- **Pendiente:** Definir el conjunto reservado y su custodia

<details><summary>Evidencia</summary>

```
docs/design/roles/A5-evaluador.md: siete ejes, independencia real, pruebas públicas y reservadas con controles, veredicto con cobertura y límites, y prohibición de autorizar despliegue. Revisión independiente aprobada (reviewer-FAB-007.md). ./init.sh: ENTORNO LISTO, 612 passed, 15 skipped, 0 avisos.
```

</details>

## QA-001 — Batería de calidad en verde

- **Cerrada:** 2026-10-25
- **Verificación:** ./init.sh en verde · 612 passed, 15 skipped in 416.21s (0:06:56)
- **Cambios:** _(no indicados)_
- **Decisiones:** _(ninguna reseñable)_
- **Pendiente:** _(nada)_

<details><summary>Evidencia</summary>

```
Sobre origin/main (50c5c25): make lint -> 'ruff check app/ tests/ agents/' 'All checks passed!' + 'ruff format --check app/ tests/' '7 files already formatted'. make typecheck -> 'mypy app/ tests/' 'Success: no issues found in 7 source files'. make test -> '612 passed, 15 skipped in 413.92s (0:06:53)'. CI: .github/workflows/ci.yml ejecuta 'make check' (lint + typecheck + test + harness-check) con uv 0.13.5 y PYTHONUTF8=1. Puerta ./init.sh --json en verde con pytest verde.
```

</details>

## SCOPE-001 — Definir qué se quiere resolver

- **Cerrada:** 2026-10-25
- **Verificación:** ./init.sh en verde · 612 passed, 15 skipped in 433.98s (0:07:13)
- **Cambios:** _(no indicados)_
- **Decisiones:** _(ninguna reseñable)_
- **Pendiente:** _(nada)_

<details><summary>Evidencia</summary>

```
Criterio 1: grep '^## ' vault/01_PROYECTO/objetivo.md -> '## Problema', '## Usuario / consumidor', '## Criterio de hecho', '## Fuera de alcance'. Criterio 2: el criterio de hecho son comandos ejecutables (./init.sh, harness status, docs/design/README.md + git ls-files), no 'que funcione bien'. Criterio 3: el apartado Fuera de alcance tiene 5 entradas (ejecutar la fabrica, publicar/desplegar, multiusuario, entrenar modelos o memoria/RAG por defecto, sustituir la aprobacion humana). Criterio 4: README -> '> Diseno y arnes de una fabrica personal de agentes: un solo propietario especifica, construye y evalua agentes sobre su propio equipo...'. Criterio 5: puerta ./init.sh --json -> ready=true, errors=0.
```

</details>
