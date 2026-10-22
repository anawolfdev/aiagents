# reviewer · GEAS-001

- **Fecha:** 2026-10-22
- **Veredicto:** rechazado

## Veredicto independiente

RECHAZADO. La puerta real y los 69 tests nuevos pasan, pero cuatro reproducciones deterministas muestran fallos de concurrencia, recuperación y publicación. No se requiere corregir las limitaciones CAS de upstream fuera de este repositorio.

## Alcance y método

Leídos backlog/current e informes explorer/implementer-GEAS-001; revisados cliente HTTP, hoja de sync, GitTool/GitAgent, HarnessAgent, permisos/CLI, init, wrappers y documentación. Contrastadas en solo lectura las implementaciones upstream de /home/cancelas/geas/geas/mcp.py:265-310,332-361 y storage.py:881-919. Las reproducciones usan las fixtures HTTP local y remotos bare temporales de agents/tests/test_geas_integration.py. El cierre de las fixtures usa su puerta simulada; la puerta completa real del clon se ejecutó por separado. Ninguna reproducción opera sobre GEAS ni origin de producción.

## Hallazgos concretos

### R1 — P1: el lock termina antes de las decisiones/escrituras y se pierden mutaciones confirmadas

Rutas: agents/agents/harness_agent.py:46-55,169-189,720-758; agents/tools/git_tool.py:60-82.

El decorador sincroniza, pero no mantiene exclusión durante la carga, decisión y escritura. Reproducción: dos instancias HarnessAgent sobre el mismo clon; pausar FIRST.add después de _load; ejecutar SECOND.add completamente; reanudar FIRST. Ambos devuelven success=True, pero FIRST guarda un documento anterior y elimina SECOND. No es una limitación CAS de GEAS: es pérdida de estado local bajo dos entradas públicas del propio arnés. El nombre .tmp compartido tampoco proporciona exclusión entre escritores. Debe protegerse el ciclo operativo completo sin provocar recursión/deadlock cuando gate llama init.

Salida real:
CONCURRENT: first.success=True, second.success=True, final_ids=[F-001, FIRST]

### R2 — P1: cambiar la URL de origin durante gate no se detecta y se completa contra otro destino

Rutas: agents/tools/git_tool.py:51-58,112-126; agents/agents/harness_agent.py:542-556.

El snapshot comparado después de gate solo guarda branch, nombre del remoto, ref, upstream, HEAD y ahead; no la URL resuelta. Reproducción: partir de origin=A; ejecutar gate; cambiar remote.origin.url a un segundo bare B, sin cambiar HEAD, branch ni nombre origin; continuar finish(confirm=True). Devuelve éxito, publica en B y completa el ticket, mientras A conserva el commit antiguo. Comparar push/fetch URL solo dentro de publish no fija el destino aprobado al comenzar el cierre. Debe conservarse y contrastarse la identidad del destino de publicación, además del SHA.

Salida real:
DESTINATION_CHANGE: success=True, original_destination_unchanged=True, other_destination_published=True, ticket=DONE

### R3 — P2: una recuperación de claim puede destruir progreso existente

Ruta: agents/agents/harness_agent.py:411-445.

Reproducción: start reclama y escribe current.md; hacer fallar _save con OSError, dejando backlog pending y remoto IN_PROGRESS propio; añadir notas de recuperación a current.md y repetir start. Reutiliza correctamente el claim remoto, pero como el backlog sigue pending, regenera current.md y borra las notas. El test existente test_claim_local_write_failure_can_be_retried_without_second_claim solo cuenta claims, no comprueba preservación de progreso.

Salida real:
CLAIM_RETRY: first.success=False, retry.success=True, start_ticket_calls=1, recovery_notes_preserved=False

### R4 — P2: segundo fetch implícito en pull evita la protección dirty-behind

Ruta: agents/tools/git_tool.py:94-105.

Reproducción: árbol sucio con cambios no conflictivos y primer fetch sin commits entrantes; publicar un commit desde peer inmediatamente antes de ejecutar el pull real. pull vuelve a hacer fetch, integra ese commit y start reclama el ticket con success=True. El árbol sucio deja de ser un no-op. La comprobación behind/dirty corresponde al primer fetch, no al commit que se integra. Debe evitarse integrar una revisión distinta de la validada sin volver a aplicar la protección del árbol sucio. En esta reproducción las notas locales permanecen, pero se incumple el bloqueo documentado cuando entran commits.

Salida real:
DIRTY_PULL_RACE: success=True, dirty_tree_HEAD_changed=True, remote_ticket=IN_PROGRESS

### R5 — P3: sintaxis inválida en wrapper

Ruta: status.sh:6. Sobra un fi sin if. bash -n status.sh devuelve exit 2:
status.sh: línea 6: error de sintaxis cerca del elemento inesperado `fi\x27
status.sh: línea 6: `fi\x27

La ejecución habitual puede no alcanzar esa línea por el exec precedente; no se presenta como un fallo universal de ./status.sh, pero el script no supera validación sintáctica.

## Criterios uno por uno

1. init sincroniza antes del trabajo: VERIFICADO. Puerta completa real con actor indicado: sync success=true, mode=remote, HEAD 6c8b3352abe844ad9073c5893031f2311197ff1a, ticket real IN_PROGRESS. init --quick --json real también devuelve ready=true y checks[0]=sync; únicamente omite pytest con aviso.
2. Preflight y claim con identidad/API: PARCIAL. status/next/start/finish/block/add/record/link/sync tienen decorador, gate pasa por init y no hay recursión init/harness. Tests verifican headers personales, pertenencia de ticket al repositorio, dueño, read-back y claim perdido. R1 demuestra que decisiones y escrituras operativas quedan fuera de exclusión y pierden cambios confirmados. La API upstream usa CAS en storage, pero su MCP ignora el booleano; documentación reconoce el límite y no promete transacción distribuida perfecta.
3. Fetch/pull seguro antes de reclamar: PARCIAL. Tests existentes cubren dirty-current, dirty-behind estático, divergencia, conflictos, detached, operación Git pendiente, sin upstream y fallos/timeout de fetch/pull. Flags ff-only/no-rebase/no-autostash presentes; los fallos impiden claim. R4 reproduce la carrera no cubierta entre fetch y el segundo fetch de pull.
4. Cierre con evidencia, gate y publicación verificada antes de DONE: PARCIAL. Se exige evidencia y entregables commiteados; pruebas cubren puerta roja, cambios de HEAD por gate/pull, SHA incorrecto, push rechazado y cierre tras publicación. R2 permite completar publicando en otro destino tras cambiar su URL sin mover HEAD. No se ejecutó finish sobre el ticket real.
5. Autorización y ausencia de commits/push forzados automáticos: VERIFICADO. BaseAgent y GitAgent exigen booleano True; CLI traduce --yes de forma estricta. Tests rechazan False, cadenas false/true y entero 1 como confirmación directa; comprueban --yes y --confirm false. publish pertenece a Git, es destructive, no hace commit/stash/reset/force y no sigue tags implícitamente. El contador de commits permanece estable en el cierre de fixtures.
6. Fallos recuperables sin falsos éxitos: PARCIAL. Tests verifican HTTP 401/403/500, JSON/formas inválidas, red/timeout, actor ausente, permisos/repositorio, propiedad, respuestas perdidas de claim/complete y reintentos de cierre sin histórico duplicado. R1 pierde una mutación que devuelve éxito y R3 destruye notas al reconciliar un claim tras fallo local.
7. Tests deterministas y documentación: EXISTEN Y PASAN, con lagunas funcionales R1-R4 y defecto menor R5. README/AGENTS/prompts documentan configuración, identidad personal, sync/start/finish, metadatos posteriores al push y limitaciones upstream. Wrappers operan desde la raíz, sin CLI GEAS local, SQLite ni sync del servidor.
8. Puerta completa y suites pertinentes: VERIFICADO en ejecución propia, pero insuficiente para aprobar ante las reproducciones adicionales.

## Comandos y salida real

GEAS_ACTOR_ID=f2e9c3af-7a61-42b5-bc7a-385a0a88ef86 ./init.sh
sync: success=true, mode=remote
pytest: 607 passed, 15 skipped in 42.82s
ENTORNO LISTO — 0 aviso(s)

uv run pytest agents/tests/test_geas_integration.py -q
..................................................................... [100%]
69 passed in 25.41s

git diff --check
exit 0, sin salida

GEAS_ACTOR_ID=f2e9c3af-7a61-42b5-bc7a-385a0a88ef86 ./init.sh --quick --json
ready=true, errors=0, warnings=1; primer check sync=ok, mode=remote; pytest omitido por --quick

make lint typecheck prompts-check opencode-check
All checks passed!
7 files already formatted
Success: no issues found in 7 source files
Prompts y subagentes sincronizados con el código y con los contratos.
Definiciones y referencias de prompts OpenCode válidas.
33 prompts fuente disponibles.

PYTHONPATH=/home/cancelas/aiagents uv run pytest -q -s /tmp/opencode/review_geas001_repros.py --basetemp=/tmp/opencode/geas001-review-fixtures
CONCURRENT: first.success=True, second.success=True, final_ids=[F-001, FIRST]
CLAIM_RETRY: first.success=False, retry.success=True, start_ticket_calls=1, recovery_notes_preserved=False
DIRTY_PULL_RACE: success=True, dirty_tree_HEAD_changed=True, remote_ticket=IN_PROGRESS
DESTINATION_CHANGE: success=True, original_destination_unchanged=True, other_destination_published=True, ticket=DONE
4 passed in 1.82s

Estos cuatro passed confirman explícitamente los cuatro comportamientos defectuosos observados; no significan que se satisfagan las invariantes deseadas. Snippets completos disponibles en /tmp/opencode/review_geas001_repros.py. Sustituir las aserciones por preservación de ambas features/notas, bloqueo de dirty-pull y rechazo de cambio de destino debe fallar con el código actual.

## Entrega

Requiere corrección y pruebas de regresión de R1-R4 antes de aprobar. GEAS-001 debe continuar in_progress hasta revisión satisfactoria y posterior commit/push autorizados. Esta revisión no edita fuente ni realiza commit/push al origin real ni completa/bloquea tickets de producción; las únicas escrituras operativas solicitadas son las de harness record.
