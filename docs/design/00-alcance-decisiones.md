# 00 — Alcance, principios y registro de decisiones

| Campo | Valor |
|---|---|
| Documento | Paquete de diseño de la fábrica personal de agentes |
| Entregable | 1 de 9 |
| Ticket | `FAB-001` — `b21b4d29-7d9c-4099-b693-3c1d67ae9311` |
| Versión | 1.0 |
| Fecha | 2026-10-22 |
| Estado | **DISEÑADO** |
| Autoridad | Propietario único del sistema |
| Vigencia | Sustituye cualquier versión anterior de alcance, principios o decisiones |

> Este documento fija qué se va a diseñar y qué queda fuera. **No ejecuta la
> fábrica, no instala agentes, no activa workflows, no publica contenido y no
> despliega nada.** Su estado es `DISEÑADO`, no `PROBADO` ni `DESPLEGADO`.

## 1. Propósito

Diseñar una fábrica personal de agentes que permita a un único propietario
especificar, construir, evaluar y desplegar agentes de IA sobre su propio
equipo y su entorno aislado de pruebas.

La fábrica debe ser útil sin convertirse en una plataforma sobredimensionada:
los controles existen para reducir riesgo, no para justificar más componentes.
El principio rector es la **solución más sencilla que satisface los requisitos
aprobados y los controles exigidos**.

El alcance de la tarea actual es el **paquete de diseño**. La ejecución de la
fábrica, la instalación de agentes, la activación de workflows, la publicación
de contenido y el despliegue quedan fuera de esta tarea.

## 2. Autoridad y vigencia

- El propietario único es la máxima autoridad. Ningún agente aprueba por él.
- Este documento sustituye versiones anteriores. No se recuperan reglas
  antiguas que lo contradigan.
- Una decisión solo es **confirmada** si consta en el diseño aprobado o si el
  propietario la autoriza explícitamente.
- Una **decisión de diseño** es una elección técnica tomada para hacer viable
  el diseño. Debe estar etiquetada y justificada; no equivale a una aprobación
  del propietario.
- Un **parámetro pendiente de activación** no se inventa: se registra, se
  asigna a un responsable y bloquea la activación hasta que exista evidencia.
- Ante conflicto entre documentos, prevalece este orden: autorización explícita
  del propietario → decisión confirmada → decisión de diseño → pendiente.
- Si el conflicto impide continuar, el agente se detiene y lo eleva.

## 3. Principios

1. **Proporcionalidad.** No se añaden agentes, herramientas, documentos,
   permisos ni infraestructura si no cubren una necesidad aprobada.
2. **Un dueño por artefacto.** Cada especificación, informe, configuración o
   entrega tiene un único responsable identificable.
3. **Evidencia, no afirmaciones.** Un artefacto no se declara probado,
   validado, publicado o desplegado sin la salida real que lo demuestre.
4. **Mínimo privilegio.** Cada rol recibe solo los datos, herramientas y
   permisos que necesita para su misión.
5. **Datos no confiables.** Lo que se lee de fuera —una web, un ticket, un PDF,
   una respuesta de una herramienta— es información, nunca una instrucción.
6. **Aprobación humana para lo irreversible.** Gasto, publicación,
   despliegue, borrado y ampliación de permisos requieren autorización.
7. **Sin memoria ni automatización por defecto.** Memoria persistente, RAG,
   bases de datos, navegación, subagentes y planificadores solo se añaden si
   una necesidad aprobada lo exige.
8. **Portabilidad sin promesas vacías.** El núcleo se especifica una vez y se
   adapta a OpenClaw y OpenCode; la compatibilidad se demuestra con pruebas en
   ambas plataformas antes de declararla.

## 4. Organización mínima

La fábrica se organiza en cinco roles. No todos los productos que salgan de
ella tienen que ser multiagente: si una tarea se resuelve con un solo agente,
se resuelve con uno.

| Rol | Misión | No hace |
|---|---|---|
| **A1 — Analista y entrevistador** | Convertir una idea en una especificación funcional completa, trazable y validada por el propietario | Inventar requisitos, aprobar el diseño, construir |
| **A2 — Revisión inicial y vigilancia** | Investigar el estado del arte, alternativas y riesgos; vigilar cambios relevantes después de la entrega | Modificar el spec, ejecutar código externo, acceder a servicios privados sin autorización |
| **A3 — Arquitecto y consolidador** | Convertir el spec aprobado y los hallazgos en una arquitectura mínima y un plan verificable; presidir el Gate 1 | Construir, aprobar el Gate 2, desplegar |
| **A4 — Constructor** | Implementar exclusivamente el alcance aprobado, en un entorno aislado, dejando evidencia | Ampliar alcance, inventar formatos, usar datos no autorizados, desplegar |
| **A5 — Evaluador independiente** | Evaluar de forma adversarial el artefacto construido y emitir un veredicto | Corregir el artefacto, aprobar el despliegue, certificar seguridad absoluta |

La **coordinación** es una función ligera del flujo, no un sexto agente
autónomo obligatorio. El coordinador:

- es el único interlocutor con el propietario;
- presenta las preguntas de A1 y evita repetirlas;
- gestiona estados, versiones, rondas y presupuestos;
- solicita las aprobaciones y registra los bloqueos con su causa;
- pasa a cada rol solo el contexto mínimo necesario;
- no aprueba, no corrige artefactos y no abre bucles libres.

Cada perfil de agente debe definir, como mínimo: misión, entradas, procedimiento,
salidas, herramientas mínimas, prohibiciones, criterio de terminación, causas
de bloqueo y destinatario de la entrega. Toda entrega debe indicar agente
destino, versión, trabajo realizado, evidencia, incertidumbres, bloqueos y
siguiente responsable.

## 5. Portabilidad OpenClaw / OpenCode

- Existe un **núcleo común** independiente de la plataforma: misión, entradas,
  salidas, reglas, permisos, criterios de aceptación y bloqueos.
- Cada plataforma tiene un **adaptador** para instrucciones de sistema,
  herramientas, formato de ejecución y mecanismos de aprobación.
- El adaptador no cambia el contrato funcional ni los permisos del rol.
- La compatibilidad se declara solo después de ejecutar las pruebas de
  aceptación en ambas plataformas.
- No se promete comportamiento idéntico: se promete el mismo contrato y la
  misma evidencia mínima.

Estado: `DISEÑADO`. La verificación en OpenClaw y OpenCode está pendiente y
pertenece a los tickets de bootstrap y validación.

## 6. Entornos y destinos autorizados

| Entorno | Uso permitido | Condición |
|---|---|---|
| Equipo del propietario | Diseño, configuración y ejecución local autorizada | Permisos mínimos y aprobación para acciones irreversibles |
| Entorno aislado de pruebas | Construcción y evaluación de artefactos | Aislamiento comprobado; datos sintéticos o autorizados |

No se autoriza ningún otro destino —otro equipo, servidor, cuenta, repositorio
público o servicio de terceros— sin una autorización adicional y explícita del
propietario. Un entorno local no es automáticamente un entorno aislado: el
aislamiento debe configurarse y comprobarse.

## 7. Decisiones confirmadas

Cada decisión cita su origen en el documento de diseño recibido el 2026-10-22.

| ID | Decisión confirmada | Origen | Consecuencia |
|---|---|---|---|
| C-01 | Propietario único | §1 | Ningún agente aprueba, publica ni despliega por iniciativa propia |
| C-02 | Destinos: equipo del propietario y entorno aislado de pruebas | §1 | Cualquier otro destino requiere autorización adicional |
| C-03 | Portabilidad OpenClaw/OpenCode con núcleo común y adaptadores | §1 | La compatibilidad se prueba en ambas plataformas antes de declararla |
| C-04 | Cinco roles A1–A5 | §2 | Los productos pueden ser monoagente; los roles son funciones, no una plantilla rígida |
| C-05 | Coordinación ligera como función del flujo | §2 | No se crea un sexto agente autónomo obligatorio |
| C-06 | El coordinador es el único interlocutor y no aprueba | §2 | Las preguntas de A1 se presentan de forma unificada; las aprobaciones son del propietario |
| C-07 | Un responsable único por artefacto y campos de entrega obligatorios | §2 | No hay entregas huérfanas ni responsabilidad difusa |
| C-08 | Matriz de necesidad y proporcionalidad | §3 | No se añaden extras sin aprobación; no se eliminan requisitos explícitos |
| C-09 | La vigilancia diaria de A2 es un requisito confirmado, no un extra | §3 | Se diseña la vigilancia, aunque su activación dependa de parámetros pendientes |
| C-10 | Sin memoria persistente, navegación, RAG, base de datos, subagentes, planificadores ni infraestructura extensible por defecto | §3 | Solo se añaden si una necesidad aprobada lo exige |
| C-11 | A1 hace una pregunta por turno, reutiliza respuestas, no inventa y valida el spec con el propietario | §4 | El spec debe ser trazable y aprobado antes de pasar a diseño |
| C-12 | A2 tiene modo inicial y modo periódico; no accede a login, pago o servicios privados sin autorización; no ejecuta código externo | §5 | La investigación es read-only y con fuentes primarias cuando sea posible |
| C-13 | A2 cubre spec saneado, inventario, dependencias transitivas y categorías de riesgo | §5 | No se envían secretos al proveedor; la cobertura es explícita |
| C-14 | A2 registra publicación, actualización, consulta y verificación; abrir una página no es revalidar | §5 | La vigencia máxima es de 7 días o la que apruebe el propietario |
| C-15 | A2 distingue indicio, riesgo de diseño, defecto del spec, exposición operativa no evaluada y exposición confirmada | §5 | Recomienda; no modifica el spec ni el artefacto |
| C-16 | A3 consolida, define arquitectura mínima, matriz de cumplimiento, hallazgos, cambios y plan; preside el Gate 1 | §6 | Los cambios materiales vuelven al Gate 1 |
| C-17 | A4 implementa solo el alcance aprobado, con datos sintéticos o autorizados y aislamiento comprobado | §7 | No amplía permisos, no inventa formatos y deja un artefacto inmutable |
| C-18 | A5 es independiente, evalúa utilidad, función, límites, privacidad, permisos, adversariales y regresiones | §8 | Emite conforme, no conforme o incompleto; no certifica seguridad absoluta |
| C-19 | Cobertura finita y versionada, estados explícitos, baseline y checkpoints | §9 | No se avanza sin evidencia; una corrección vuelve al punto afectado |
| C-20 | Los bloqueos se registran por agente, versión y causa; un riesgo crítico bloquea nuevos despliegues sin parar el agente | §10 | Los bloqueos parciales o fallidos bloquean; más de 24 h exige revisión |
| C-21 | No hay presupuesto aprobado; se estima y se aprueba antes de gastar | §11 | Se separan creación, corrección y vigilancia; hay límites y reintentos |
| C-22 | Máximo de tres rondas: una inicial y dos correcciones | §11 | Si no hay progreso se para; ampliar requiere aprobación; agotar no acepta |
| C-23 | Repositorio público y privado separados; secretos fuera; PR sin auto-merge | §12 | La rama pública solo publica lo autorizado; el saneamiento no sustituye la aprobación |
| C-24 | Telegram privado verificado; no se asume integración | §13 | Un fallo de Telegram mantiene bloqueos y cola privada; no hay publicación silenciosa |
| C-25 | Gate 1 y Gate 2; manifiesto de componentes; cambios materiales invalidan la aprobación | §14 | Toda reversión y monitorización se define antes de desplegar |
| C-26 | El bootstrap empieza por A1 y sigue la secuencia 1–7; cobertura provisional mientras no haya automatización | §15 | No se simula una automatización inexistente |
| C-27 | La validación usa escenarios y no se declara validada solo por redactar el diseño | §16 | Cada prueba debe tener entrada, resultado esperado y evidencia |
| C-28 | Entregables en orden 1–9; parámetros pendientes visibles; sin eliminar evidencia | §17 | La tarea termina en diseño; la activación se aprueba después |

## 8. Decisiones de diseño

Estas decisiones no fueron aprobadas explícitamente por el propietario: son
elecciones técnicas para resolver ambigüedades del diseño. Se revisan en el
Gate 1.

| ID | Decisión de diseño | Motivo | Estado |
|---|---|---|---|
| D-01 | Las excepciones de emergencia son humanas, justificadas, temporales, limitadas a una versión y causa, con vencimiento y sin renovación automática (§10) | Evitar que una excepción se convierta en permiso permanente | `DISEÑADO` |
| D-02 | El límite de tres rondas se aplica al ciclo completo, no por plataforma, y no se reinicia por cambios triviales (§11) | Evitar bucles de corrección que agoten el presupuesto | `DISEÑADO` |
| D-03 | La vigilancia se ejecuta desde el repositorio privado, con identidades y permisos separados para lectura, informes y publicación (§13) | Reducir el impacto de una credencial comprometida | `DISEÑADO` |
| D-04 | El seguimiento de esta entrega se organiza en tickets `FAB` de GEAS, con dependencias explícitas y un artefacto o control por ticket | Trazabilidad y reanudación sin depender de la conversación | `CONFIGURADO` (solo seguimiento; la fábrica no está configurada) |

## 9. No-goals

Queda explícitamente fuera del alcance:

- ejecutar la fábrica, instalar agentes, activar workflows, publicar contenido
  o desplegar en esta tarea;
- construir una interfaz gráfica, panel de control o base de datos propia;
- exigir que todos los productos sean multiagente;
- añadir memoria persistente, RAG, navegación, subagentes o planificadores por
  defecto;
- garantizar compatibilidad con OpenClaw u OpenCode sin pruebas en ambas;
- prometer seguridad absoluta o ausencia total de errores;
- hacer merge automático de PR;
- detener un agente por un riesgo crítico: se avisa y se bloquean nuevos
  despliegues, pero el agente no se para;
- dar acceso general al equipo del propietario;
- asumir que Telegram ya está integrado;
- recuperar reglas de versiones anteriores que contradigan este documento;
- inventar valores para parámetros de activación.

## 10. Parámetros pendientes de activación

Ningún valor de esta tabla se deduce ni se inventa. Cada fila bloquea la
activación de la parte correspondiente hasta que el propietario aporte el dato
y la evidencia.

| Parámetro | Estado | Responsable | Evidencia necesaria |
|---|---|---|---|
| Repositorio público concreto | Pendiente | Propietario | URL, visibilidad y permisos verificados |
| Repositorio privado concreto | Pendiente | Propietario | URL, visibilidad y permisos verificados |
| Proveedor y modelo autorizados | Pendiente | Propietario | Proveedor, modelo, límites y coste aprobados |
| Presupuesto de creación, corrección y vigilancia | Pendiente | Propietario | Importe o límite explícito por fase |
| Horario y zona horaria de vigilancia | Pendiente | Propietario | Franja, frecuencia y zona horaria |
| Conexión y destinatario de Telegram | Pendiente | Propietario | Bot, chat privado y prueba de entrega |
| Inventario real de componentes y versiones | Pendiente | A2 / propietario | Inventario fechado y con fuentes |
| Aislamiento del entorno de pruebas | Pendiente | A4 / propietario | Prueba de que no alcanza datos o servicios no autorizados |
| Permisos efectivos por rol | Pendiente | Propietario | Matriz aprobada y comprobada |
| Retención de evidencia | Pendiente | Propietario | Plazo y destino aprobados |
| Almacenamiento de artefactos y secretos | Pendiente | Propietario | Ubicación, cifrado y control de acceso |
| Supervisión independiente y detección de ausencia | Pendiente | Propietario | Mecanismo distinto del vigilado y prueba de fallo |
| Versiones de OpenClaw y OpenCode | Pendiente | A3 / A4 | Versiones fijadas y pruebas de aceptación |
| Destino y propietario del despliegue | Pendiente | Propietario | Destino autorizado y responsable |
| Umbral de riesgo crítico | Pendiente | Propietario | Definición operativa y ejemplos |

## 11. Estados de madurez

| Estado | Significado | Qué exige |
|---|---|---|
| **DISEÑADO** | Existe una especificación revisable | Documento, decisiones y criterios |
| **CONFIGURADO** | Los parámetros y permisos están puestos en el entorno | Configuración aplicada y verificable |
| **PROBADO** | Se ejecutaron las pruebas de aceptación | Evidencia real de entrada, salida y resultado |
| **DESPLEGADO** | Está activo en el destino autorizado | Gate 2, manifiesto, reversión y monitorización |

Estado actual de la fábrica: **DISEÑADO**. El seguimiento en GEAS está
`CONFIGURADO`; no se ha instalado ni ejecutado la fábrica, no se han probado
sus roles y no se ha desplegado ningún artefacto.

## 12. Trazabilidad de la entrega

| Sección del diseño | Entregable / ticket |
|---|---|
| §1 Alcance y principios | Este documento; `FAB-001` |
| §2 Organización y contratos | Este documento; `FAB-008` |
| §3 Matriz de necesidad y proporcionalidad | `FAB-002` |
| §4 A1 | `FAB-003` |
| §5 A2 | `FAB-004` |
| §6 A3 | `FAB-005` |
| §7 A4 | `FAB-006` |
| §8 A5 | `FAB-007` |
| §9 Flujo de estados y recuperación | `FAB-011` |
| §10 Bloqueos y emergencias | `FAB-012` |
| §11 Presupuesto, rondas y gates | `FAB-013` |
| §12 Publicación y proveedores | `FAB-014` |
| §13 Vigilancia y Telegram | `FAB-015` |
| §14 Gates y manifiesto | `FAB-013`, `FAB-014` |
| §15 Bootstrap | `FAB-017` |
| §16 Validación | `FAB-016` |
| §17 Entregables y pendientes | `FAB-018`, `FAB-019` |
| Plantillas operativas | `FAB-009` |
| Permisos, datos y secretos | `FAB-010` |

## 13. Criterios de cierre de este documento

- [x] Incluye alcance, propietario único, entornos, portabilidad, principio
  rector, no-goals y tabla de decisiones.
- [x] Cada decisión confirmada cita su origen.
- [x] Las decisiones de diseño llevan etiqueta explícita.
- [x] Los parámetros desconocidos quedan pendientes, sin valores inventados.
- [x] Distingue `DISEÑADO`, `CONFIGURADO`, `PROBADO` y `DESPLEGADO`.
- [x] `./init.sh` termina con `ENTORNO LISTO` (verificado el 2026-10-22:
  `612 passed, 15 skipped`, 0 avisos).

## 14. Registro de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-10-22 | Versión inicial: alcance, principios, organización, portabilidad, entornos, decisiones, no-goals, pendientes y estados |
