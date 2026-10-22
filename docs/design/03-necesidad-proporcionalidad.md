# 03 — Matriz de necesidad y proporcionalidad

| Campo | Valor |
|---|---|
| Documento | Paquete de diseño de la fábrica personal de agentes |
| Entregable | 2 de 9 |
| Ticket | `FAB-002` — `9880bc7b-24c0-4d27-82b3-b49e480c4550` |
| Versión | 1.0 |
| Fecha | 2026-10-22 |
| Estado | **DISEÑADO** |
| Depende de | `FAB-001` — `docs/design/00-alcance-decisiones.md` |

> Esta matriz decide qué capacidades se mantienen, simplifican, excluyen,
> posponen o deben aclararse. **No implementa ni activa ninguna capacidad.**
> Un `mantener` significa que la capacidad está justificada para el diseño;
> no significa que esté configurada, probada o desplegada.

## 1. Regla de proporcionalidad

Una capacidad solo entra si cubre una necesidad aprobada y su beneficio es
mayor que su coste y su riesgo. El principio rector es la solución más
sencilla que satisface los requisitos y controles aprobados.

Nada extra se implementa sin aprobación del propietario. Ningún requisito
explícito se elimina en silencio: si una decisión implica quitarlo, se para y
se eleva. A2 recomienda; A3 consolida; el propietario aprueba.

## 2. Vocabulario

### Origen

| Origen | Significado |
|---|---|
| **Explícito** | Está en el diseño aprobado o lo pidió el propietario |
| **Derivado justificado** | Se deduce de un requisito o control explícito; la deducción se explica |
| **Control obligatorio** | Reduce un riesgo que no se puede aceptar sin control: gasto, permisos, excepciones, evidencia |
| **Extra opcional** | No hay requisito aprobado; solo entra con autorización adicional |

### Decisión

| Decisión | Significado |
|---|---|
| **Mantener** | Cubre una necesidad aprobada; tiene prueba o argumento de proporcionalidad |
| **Simplificar** | Se conserva una versión mínima que cubre la necesidad |
| **Proponer exclusión** | No hay necesidad aprobada; se propone no implementarlo |
| **Posponer** | Puede tener valor futuro, pero no ahora; queda fuera hasta aprobación |
| **Aclarar** | Falta información o hay contradicción; no se decide por intuición |

### Coste y riesgo

El coste y el riesgo se expresan como `bajo`, `medio` o `alto`, con la causa.
Si falta un dato económico, operativo o de seguridad, se marca **pendiente** y
se remite al registro de parámetros de activación de `00-alcance-decisiones.md`.
No se inventan importes, plazos ni caudales.

## 3. Matriz rellenada

| # | Requisito / capacidad | Origen | Capacidad concreta | Beneficio observable | Qué falla si se elimina | Alternativa más sencilla | Coste y riesgo | Prueba | Decisión |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Vigilancia diaria de A2 | **Explícito** (§3; C-09) | A2 revisa a diario cambios relevantes del artefacto, sus dependencias y fuentes | El propietario se entera de un cambio o riesgo sin preguntar | Se incumple un requisito confirmado; el artefacto puede quedar obsoleto sin aviso | Revisión manual periódica, menos fiable y no equivale a vigilancia | **Medio**: tokens, tiempo y ruido de falsos positivos; presupuesto y horario pendientes | Escenario con cambio simulado: A2 lo detecta, registra fecha y fuente, y avisa por el canal aprobado | **Mantener** |
| 2 | Portabilidad OpenClaw / OpenCode | **Explícito** (§1; C-03) | Núcleo común de contrato y adaptadores por plataforma | El mismo rol se ejecuta en ambas plataformas sin reescribir el diseño | Dependencia de una sola plataforma y pérdida de la portabilidad aprobada | Diseñar solo para una plataforma y declarar la otra fuera de alcance | **Medio**: dos adaptadores y pruebas duplicadas; riesgo de deriva entre plataformas | Ejecutar la misma suite de aceptación en OpenClaw y OpenCode y comparar contrato y evidencia | **Mantener** |
| 3 | Telegram | **Explícito** (§13; C-24) | Canal privado para avisos, bloqueos y resultados | El propietario recibe avisos en un canal que ya usa | Los bloqueos y riesgos pueden quedar sin atención inmediata | Solo registro local y consulta manual | **Medio**: token, privacidad y dependencia de un tercero; conexión y destinatario pendientes | Mensaje de prueba en chat privado y prueba de caída con cola local que no pierde el aviso | **Mantener** |
| 4 | GitHub Actions | **Extra opcional** | Automatización de CI en GitHub | Detección temprana de fallos en cada push | No se pierde ningún requisito confirmado: la puerta local sigue existiendo | `./init.sh` local antes de publicar | **Bajo/medio**: mantenimiento de workflows y secretos; valor no demostrado para el diseño actual | No aplica hasta aprobación; si se activa, debe probar el mismo gate que `./init.sh` | **Posponer** |
| 5 | Memoria persistente | **Extra opcional** (§3; C-10) | Memoria entre sesiones para agentes | Continuidad entre ejecuciones | No se pierde ningún requisito confirmado; cada sesión parte de sus entradas | Ficheros de estado y documentos versionados | **Medio/alto**: privacidad, datos obsoletos y fuga de contexto; sin parámetros aprobados | No aplica hasta aprobación; si se activa, prueba de retención, borrado y aislamiento | **Proponer exclusión** |
| 6 | Navegación | **Derivado justificado** (§5; C-12) | A2 lee fuentes públicas en modo solo lectura | A2 puede contrastar el estado del arte y las dependencias | A2 pierde una vía necesaria para investigar y vigilar | Consulta manual de fuentes por el propietario | **Medio**: ruido, fuentes no fiables y prompt injection; sin acceso a login, pago o servicios privados | Caso público permitido y caso privado bloqueado; registrar fuente, fecha y consulta | **Simplificar** (solo A2, solo lectura) |
| 7 | Recuperación documental | **Extra opcional** (§3; C-10) | Búsqueda semántica o RAG sobre documentación | Recuperar contexto sin releer todo | No se pierde ningún requisito confirmado; la documentación sigue siendo la fuente | `rg` y búsqueda por rutas en `docs/` y `vault/` | **Bajo/medio**: índice desactualizado y resultados no auditables; sin corpus aprobado | No aplica hasta aprobación; si se activa, consulta conocida que devuelva el documento y la línea esperados | **Proponer exclusión** (se mantiene `rg` como alternativa) |
| 8 | Bases de datos | **Extra opcional** (§3; C-10) | Persistencia relacional o documental propia | Consultas y estado transaccional | No se pierde ningún requisito confirmado; el estado cabe en ficheros | JSON/Markdown versionados y validados por el arnés | **Medio**: migraciones, copias y superficie de ataque; sin necesidad aprobada | No aplica hasta aprobación; si se activa, prueba de migración, copia y restauración | **Proponer exclusión** |
| 9 | Subagentes | **Extra opcional** (§3; C-10) | Agentes que delegan en otros agentes | Paralelismo o especialización | No se pierde ningún requisito confirmado; los roles A1–A5 ya separan responsabilidades | Ejecución secuencial de roles y un único responsable por artefacto | **Medio/alto**: permisos, contexto y coste de coordinación; sin necesidad aprobada | No aplica hasta aprobación; si se activa, prueba de límites de permisos y presupuesto | **Proponer exclusión** |
| 10 | Planificadores | **Extra opcional** (§3; C-10) | Planificación autónoma de tareas | Descomposición automática de trabajo | No se pierde ningún requisito confirmado; el plan puede ser explícito | Checklist y estado en `harness/progress/` | **Medio**: bucles, planes divergentes y coste; sin necesidad aprobada | No aplica hasta aprobación; si se activa, prueba de límite de rondas y parada | **Proponer exclusión** |
| 11 | Infraestructura extensible | **Extra opcional** (§3; C-10) | Plugins, servidores o servicios adicionales | Extensión futura | No se pierde ningún requisito confirmado; la fábrica funciona en el equipo del propietario | Ejecución local mínima y adaptadores concretos | **Alto**: superficie de ataque, mantenimiento y coste; sin necesidad aprobada | No aplica hasta aprobación; si se activa, prueba de aislamiento y permisos mínimos | **Proponer exclusión** |
| 12 | Presupuesto | **Control obligatorio** (§11; C-21) | Estimar, aprobar y registrar gasto antes de consumirlo | Evita gasto no autorizado y permite comparar coste real con estimación | Se puede gastar sin límite ni aprobación | Aprobación manual por acción, sin estimación previa | **Bajo/medio**: fricción operativa; importes y límites pendientes | Simulación de consumo por encima del límite: la acción se bloquea y pide aprobación | **Mantener** |
| 13 | Excepciones | **Control obligatorio** (§10; C-20 y D-01) | Excepción humana, justificada, temporal, ligada a versión y causa, con vencimiento | Permite una salida segura sin convertirla en permiso permanente | Los bloqueos se saltan de forma ad hoc y sin trazabilidad | Bloqueo duro hasta corregir la causa | **Medio**: riesgo de abuso y de olvidar el vencimiento; requiere registro y revisión | Excepción con vencimiento: antes permite la acción, después la bloquea y deja evidencia | **Mantener** |

## 4. Resumen de decisiones

| Decisión | Filas | Total |
|---|---|---|
| Mantener | 1, 2, 3, 12, 13 | 5 |
| Simplificar | 6 | 1 |
| Proponer exclusión | 5, 7, 8, 9, 10, 11 | 6 |
| Posponer | 4 | 1 |
| Aclarar | — | 0 |

Las cinco capacidades que se mantienen tienen una prueba o un argumento de
proporcionalidad explícito. La que se simplifica conserva la necesidad mínima
y elimina la parte no aprobada. Las seis exclusiones y la capacidad pospuesta
no se implementan ni se activan en este paquete de diseño.

## 5. Política de extras

1. Un extra opcional no se implementa por defecto, aunque sea popular o barato.
2. Para activarlo hace falta una necesidad aprobada, un responsable, un coste
   estimado y una prueba de aceptación.
3. Si el extra puede resolverse con una alternativa más simple, se elige la
   alternativa y se registra la decisión.
4. Si un requisito explícito depende del extra, el extra deja de ser opcional:
   se reclasifica y se justifica.
5. Si el propietario pide un extra, se añade al registro de decisiones y se
   somete a la misma matriz; no se hereda como permiso permanente.
6. Un extra excluido o pospuesto no se introduce por la puerta de atrás en un
   adaptador, una plantilla o una configuración por defecto.

## 6. Plantilla para nuevas capacidades

Copiar esta fila y rellenar todas las columnas. Si falta un dato, escribir
`Pendiente` y explicar qué evidencia lo desbloquea; no inventar el valor.

| # | Requisito / capacidad | Origen | Capacidad concreta | Beneficio observable | Qué falla si se elimina | Alternativa más sencilla | Coste y riesgo | Prueba | Decisión |
|---|---|---|---|---|---|---|---|---|---|
| N | _(nombre)_ | _(explícito / derivado justificado / control obligatorio / extra opcional)_ | _(qué hace)_ | _(qué mejora observable)_ | _(qué requisito o control se pierde)_ | _(opción mínima)_ | _(bajo/medio/alto + causa; pendiente si falta)_ | _(cómo se demuestra)_ | _(mantener / simplificar / proponer exclusión / posponer / aclarar)_ |

## 7. Trazabilidad

| Decisión de `00-alcance-decisiones.md` | Dónde se aplica |
|---|---|
| C-03 Portabilidad | Fila 2 |
| C-08 Matriz de necesidad y proporcionalidad | Todo el documento |
| C-09 Vigilancia diaria | Fila 1 |
| C-10 Sin extras por defecto | Filas 5–11 |
| C-12 A2 solo lectura | Fila 6 |
| C-20 Bloqueos y excepciones | Fila 13 |
| C-21 Presupuesto | Fila 12 |
| C-23 Repositorio y PR | Fila 4 (GitHub Actions pospuesto) |
| C-24 Telegram | Fila 3 |
| D-01 Excepciones temporales | Fila 13 |

## 8. Criterios de cierre

- [x] Cada fila tiene origen y decisión.
- [x] La vigilancia diaria de A2 queda justificada como requisito confirmado.
- [x] Los extras no aprobados quedan excluidos o pospuestos.
- [x] Toda decisión de mantener tiene prueba o argumento de proporcionalidad.
- [x] No hay filas sin coste y riesgo estimados o marcados como pendientes.
- [x] `./init.sh` termina con `ENTORNO LISTO` (verificado el 2026-10-22:
  `612 passed, 15 skipped`, 0 avisos).

## 9. Registro de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-10-22 | Matriz inicial con 13 filas, plantilla y política de extras |
