# Paquete de diseño — Fábrica de agentes de IA (uso personal)

**Estado global:** **DISEÑADO** — la fábrica no está configurada, probada ni desplegada. El único elemento `CONFIGURADO` es el seguimiento de la entrega en GEAS; nada más.
**Versión del paquete:** 1.0 · **Fecha:** 2026-10-22  
**Alcance:** paquete de diseño completo. La tarea **termina aquí**: no se ejecuta la fábrica, no se instalan agentes, no se activan workflows, no se publican contenidos, no se despliega.

Este paquete sustituye versiones anteriores. No recuperar reglas que lo contradigan.

---

## Índice — orden de entrega (sección 17)

| # | Entregable | Artefacto | Estado |
|---|---|---|---|
| 1 | Resumen de decisiones confirmadas y de diseño | [`00-alcance-decisiones.md`](00-alcance-decisiones.md) | DISEÑADO |
| 2 | Cinco instrucciones de sistema completas | [`roles/A1`](roles/A1-analista.md) · [`A2`](roles/A2-riesgos-vigilancia.md) · [`A3`](roles/A3-arquitecto.md) · [`A4`](roles/A4-constructor.md) · [`A5`](roles/A5-evaluador.md) | DISEÑADO |
| 3 | Contrato del coordinador | [`02-coordinador.md`](02-coordinador.md) | DISEÑADO |
| 4 | Plantillas (spec, necesidad, hallazgos, cambios, evaluación, cobertura, ejecución, aprobaciones, bloqueos) | [`09-plantillas/`](09-plantillas/README.md) | DISEÑADO |
| 5 | Matriz de permisos y separación de datos | [`10-permisos-datos.md`](10-permisos-datos.md) | DISEÑADO |
| 6 | Flujo de estados, corrección, recuperación y despliegue | [`11-estados-cobertura-recuperacion.md`](11-estados-cobertura-recuperacion.md) · [`12-bloqueos-emergencias.md`](12-bloqueos-emergencias.md) · [`13-presupuesto-gates.md`](13-presupuesto-gates.md) | DISEÑADO |
| 7 | Protocolo de pruebas y validación | [`16-validacion.md`](16-validacion.md) | DISEÑADO (escenarios NO ejecutados) |
| 8 | Plan de bootstrap y portabilidad | [`17-bootstrap-portabilidad.md`](17-bootstrap-portabilidad.md) | DISEÑADO |
| 9 | Checklist de activación | [`18-activacion.md`](18-activacion.md) | DISEÑADO (nada activado) |

Documentos de apoyo: [`03-necesidad-proporcionalidad.md`](03-necesidad-proporcionalidad.md) · [`14-publicacion-proveedores.md`](14-publicacion-proveedores.md) · [`15-vigilancia-telegram.md`](15-vigilancia-telegram.md)

---

## Resumen de decisiones (entregable 1)

**Decisiones confirmadas** (origen: prompt; tabla completa en [`00-alcance-decisiones.md`](00-alcance-decisiones.md#7-decisiones-confirmadas) C-01…C-28): propietario único; solo equipo del propietario + entorno aislado de pruebas; ningún otro destino sin autorización; portabilidad OpenClaw/OpenCode con núcleo común y adaptadores; pruebas en ambas plataformas antes de declarar compatibilidad; sin prometer comportamiento idéntico; cinco roles cuyos productos no tienen que ser multiagente; coordinación ligera, no un sexto agente autónomo obligatorio; coordinador como único interlocutor; repositorios público y privado separados con secretos fuera y saneamiento que no sustituye la aprobación de publicación; GATE 1 y GATE 2 con manifiesto de componentes, y cambios materiales que invalidan la aprobación afectada; solución más sencilla que satisfaga requisitos y controles; no ejecutar/instalar/activar/publicar/desplegar en esta tarea; las recomendaciones de diseño no sustituyen aprobaciones de gasto, proveedores, permisos, publicación o despliegue.

**Decisiones de diseño** (etiquetadas, se revisan en Gate 1; tabla completa en [`00-alcance-decisiones.md`](00-alcance-decisiones.md#8-decisiones-de-diseño) D-01…D-04): D-01 excepciones humanas temporales con vencimiento y sin renovación automática; D-02 límite de 3 rondas para el ciclo completo; D-03 vigilancia desde el repositorio privado con identidades y permisos separados; D-04 seguimiento de la entrega en tickets `FAB` de GEAS. Ninguna sustituye aprobaciones.

---

## Matriz de trazabilidad (secciones 1–17 → artefactos)

| Sección | Contenido | Artefacto(s) |
|---|---|---|
| 1 | Alcance y principios | `00-alcance-decisiones.md`, `17-bootstrap-portabilidad.md` |
| 2 | Organización y contratos | `00-alcance-decisiones.md`, `02-coordinador.md`, `09-plantillas/` |
| 3 | Necesidad y proporcionalidad | `03-necesidad-proporcionalidad.md` |
| 4 | A1 — analista y entrevistador | `roles/A1-analista.md` |
| 5 | A2 — revisión y vigilancia | `roles/A2-riesgos-vigilancia.md`, `09-plantillas/` |
| 6 | A3 — arquitecto y consolidador | `roles/A3-arquitecto.md` |
| 7 | A4 — constructor | `roles/A4-constructor.md` |
| 8 | A5 — evaluador independiente | `roles/A5-evaluador.md` |
| 9 | Cobertura, estado y recuperación | `11-estados-cobertura-recuperacion.md`, `09-plantillas/` |
| 10 | Bloqueos y emergencias | `12-bloqueos-emergencias.md`, `09-plantillas/` |
| 11 | Presupuesto y rondas | `13-presupuesto-gates.md` |
| 12 | Publicación, datos y proveedores | `14-publicacion-proveedores.md`, `10-permisos-datos.md` |
| 13 | Telegram y ejecución programada | `15-vigilancia-telegram.md` |
| 14 | Aprobaciones y despliegue | `13-presupuesto-gates.md`, `14-publicacion-proveedores.md`, `10-permisos-datos.md`, `09-plantillas/` |
| 15 | Arranque sin circularidad | `17-bootstrap-portabilidad.md` |
| 16 | Validación de la fábrica | `16-validacion.md` |
| 17 | Entregables | Este documento, `18-activacion.md` |

Sin huecos: las 17 secciones están cubiertas.

---

## Estados: qué es verdad hoy

| Concepto | Estado real |
|---|---|
| Seguimiento de la entrega en GEAS | **CONFIGURADO** (solo el seguimiento; no la fábrica) |
| Perfiles A1–A5 | **DISEÑADO** |
| Contrato del coordinador | **DISEÑADO** |
| Plantillas | **DISEÑADO** |
| Permisos y clases de dato | **DISEÑADO** |
| Flujo de estados y bloqueos | **DISEÑADO** |
| Gates 1 y 2 | **DISEÑADO** |
| Escenarios de validación | **DISEÑADO** (no ejecutados) |
| Portabilidad OpenClaw/OpenCode | **NO PROBADO** en ninguna plataforma |
| Vigilancia diaria | **NO ACTIVA** |
| Telegram | **NO CONECTADO** |
| GitHub Actions | **NO CREADO** |
| Repositorios | **NO CREADOS** |
| Presupuesto | **NO APROBADO** |
| Retención | **NO APROBADA** |
| Despliegues | **NINGUNO** |

---

## Pendientes antes de activar

Repositorios concretos · proveedor y modelo autorizado · presupuesto · horario · zona horaria · conexión y destinatario Telegram · inventario · aislamiento · permisos · **retención (bloqueante)** · almacenamiento · mecanismo independiente de supervisión · versiones de OpenClaw y OpenCode · destino y propietario del despliegue · umbral de riesgo crítico.

Detalle y evidencia exigida: [`18-activacion.md`](18-activacion.md).

---

## Declaración final

- La tarea actual **termina con el paquete de diseño**.
- **No** se atribuye ninguna instalación, prueba o despliegue inexistente.
- Los escenarios de validación (FAB-016) están **redactados, no ejecutados**: la fábrica **no** está validada.
- La conformidad técnica de un artefacto, cuando exista, **no** autorizará desplegar: eso es GATE 2.

## Verificación FAB-019
- [x] Están los nueve entregables
- [x] La trazabilidad cubre las secciones 1–17
- [x] Sin contradicciones con `00-alcance-decisiones.md`
- [x] Pendientes listados
- [x] Se declara que la tarea termina en diseño
- [x] La revisión independiente se registra en `harness/progress/reviewer-FAB-019.md` antes de cerrar la puerta
- [x] No se atribuye instalación, prueba o despliegue inexistente

> Las casillas son cobertura del documento; no son evidencia de ejecución de la fábrica.
