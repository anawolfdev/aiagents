# FAB-009: Paquete de plantillas operativas

**Versión:** 1.0 · **Estado:** DISEÑADO  
**Ámbito:** Secciones 2, 3, 5, 9, 14 y 17  
**Regla común:** cada plantilla tiene **dueño único**, versión, campos obligatorios, evidencia, estados, criterios de cierre y política de retención **pendiente de aprobación**. Ninguna plantilla solicita secretos.

Índice:
1. [spec.md](#1-specmd)
2. [necesidad.md](#2-necesidadmd)
3. [hallazgos.md](#3-hallazgosmd)
4. [cambios.md](#4-cambiosmd)
5. [evaluacion.md](#5-evaluacionmd)
6. [cobertura.md](#6-coberturamd)
7. [ejecucion.md](#7-ejecucionmd)
8. [aprobaciones.md](#8-aprobacionesmd)
9. [bloqueos.md](#9-bloqueosmd)

---

## 1. `spec.md`
**Dueño único:** A1 · **Fuente:** sección 4

| Campo | Obligatorio | Estado admitido |
|---|---|---|
| `spec_id`, `version`, `fecha` | Sí | — |
| Problema (con ejemplo concreto) | Sí | DEFINIDO/SUPUESTO/PENDIENTE |
| Usuario | Sí | idem |
| Resultado útil | Sí | idem |
| Alcance | Sí | idem |
| Exclusiones explícitas | Sí | idem |
| Requisitos (con origen) | Sí | EXPLÍCITO/DERIVADO/CONTROL/EXTRA |
| Extras propuestos (separados) | Sí (puede estar vacío) | — |
| Entradas / salidas / ejemplos | Sí | — |
| Herramientas y permisos | Sí | — |
| Datos y memoria (retención) | Sí | retención: PENDIENTE |
| Autonomía y escalado | Sí | — |
| Restricciones y costes | Sí | coste: PENDIENTE si no estimado |
| Criterios de aceptación | Sí | verificables uno a uno |
| Pruebas públicas | Sí | — |
| Riesgos / supuestos / decisiones pendientes | Sí (tres listas) | — |
| Matriz de necesidad aplicable | Sí | — |
| Trazabilidad requisito → origen | Sí | — |

**Evidencia:** transcripción saneada de la entrevista.  
**Criterio de cierre:** los 14 apartados con estado; supuestos marcados como supuestos.  
**Ejemplo mínimo:**
```
spec_id: SPEC-0001     version: v0     fecha: 2026-10-22
Problema: [DEFINIDO] el propietario revisa a mano 12 dependencias cada semana
Alcance: [DEFINIDO] informe semanal de vulnerabilidades de las dependencias
Exclusiones: [DEFINIDO] sin corrección automática, sin despliegue
Requisito R1 [EXPLÍCITO]: detectar avisos de las dependencias del inventario
Extra propuesto E1: [EXTRA] panel web — fuera de alcance sin aprobación
Coste: PENDIENTE (no estimado)
```
**Retención:** PENDIENTE de aprobación.

---

## 2. `necesidad.md`
**Dueño único:** A3 · **Fuente:** sección 3

Columnas: `Requisito | Origen | Capacidad | Beneficio observable | Qué falla si se elimina | Alternativa sencilla | Coste y riesgo | Prueba | Decisión`.

**Decisiones admitidas:** mantener · simplificar · proponer exclusión · posponer · aclarar.  
**Orígenes admitidos:** EXPLÍCITO · DERIVADO · CONTROL · EXTRA.  
**Criterio de cierre:** ninguna fila sin origen, sin decisión, ni sin coste/riesgo (o marcados PENDIENTE).  
**Ejemplo mínimo:**
```
R1 | EXPLÍCITO | vigilancia diaria | aviso en ≤24h | despliegue con CVE conocida
   | revisión manual (no cumple) | 1 CI/día; riesgo falsos positivos
   | escenario-13 | MANTENER
```
**Retención:** PENDIENTE de aprobación.

---

## 3. `hallazgos.md`
**Dueño único:** A2 · **Fuentes:** secciones 5 y 6

| Campo | Obligatorio |
|---|---|
| `hallazgo_id`, informe, fecha | Sí |
| Componente y versión | Sí |
| Clase | INDICIO / RIESGO DE DISEÑO / DEFECTO DEL SPEC / EXPOSICIÓN OPERATIVA NO EVALUADA / EXPOSICIÓN CONFIRMADA |
| Fuente (primaria/secundaria, independiente sí/no) | Sí |
| Fecha de publicación | Sí |
| Fecha de consulta | Sí |
| Fecha de **verificación sustantiva** | Sí |
| Aplicabilidad al componente/versión | Sí |
| Severidad | Sí |
| Tratamiento propuesto | Sí |
| Tratamiento final (A3) | Al consolidar |

**Criterio de cierre:** todo hallazgo con las cuatro fechas y aplicabilidad declarada.  
**Ejemplo mínimo:**
```
H-01 | libX 2.1.0 | EXPOSICIÓN CONFIRMADA | aviso oficial | pub 2026-10-01
consulta 2026-10-22 | verificación sustantiva 2026-10-22 | aplica: sí
severidad: alta | tratamiento: fijar 2.1.3 o justificar
```
**Retención:** PENDIENTE de aprobación. **No eliminar evidencia de casos abiertos.**

---

## 4. `cambios.md`
**Dueño único:** A3 · **Fuente:** secciones 6 y 14

| Campo | Obligatorio |
|---|---|
| `cambio_id`, versión origen, versión destino | Sí |
| Qué cambia | Sí |
| Motivo | Sí |
| ¿Material? | Sí/No |
| Aprobaciones invalidadas | Sí (puede ser «ninguna») |
| Pruebas invalidadas | Sí (puede ser «ninguna») |
| Hash antes / después | Sí |
| Requiere GATE | 1 / 2 / ninguno |

**Material** si afecta a intención, alcance, permisos, clases de dato, dependencias, modelo/proveedor, destino o criterios de aceptación.  
**Ejemplo mínimo:**
```
C-01 | v1 → v2 | se añade permiso de red | necesario para fuente oficial
material: sí | invalida: AP-0003 (GATE 1) | pruebas: P-04 caducada
hashes: a1b2… → c3d4… | requiere GATE: 1
```
**Retención:** PENDIENTE de aprobación.

---

## 5. `evaluacion.md`
**Dueño único:** A5 · **Fuente:** sección 8

| Campo | Obligatorio |
|---|---|
| `evaluacion_id`, artefacto, versión, hash | Sí |
| Criterios definidos antes de construir (fecha) | Sí |
| Siete ejes: utilidad, funcionalidad, límites, privacidad, permisos, adversarial, regresiones | Sí |
| Hace algo no solicitado | Sí |
| Usa capacidades innecesarias | Sí |
| Rechaza en exceso | Sí |
| Satisface la necesidad original | Sí |
| Cobertura y limitaciones | Sí |
| No conformidades (saneadas) | Sí |
| Veredicto | CONFORME / NO CONFORME / INCOMPLETA |

**Criterio de cierre:** veredicto + cobertura + limitaciones + declaración «no autoriza despliegue».  
**Ejemplo mínimo:**
```
EVA-01 | ART-01 v1 | hash 9f8e… | criterios fijados 2026-10-20
funcionalidad: 6/6 criterios OK | límites: entrada vacía → error claro
privacidad: no escribe fuera del directorio de trabajo
adversarial: ignora instrucciones embebidas en datos
veredicto: NO CONFORME (R4 sin prueba) | no autoriza despliegue
```
**Retención:** PENDIENTE de aprobación.

---

## 6. `cobertura.md`
**Dueño único:** A2 · **Fuente:** sección 9

| Campo | Obligatorio |
|---|---|
| `manifiesto_id`, versión, fecha | Sí |
| Componentes | Sí |
| Riesgos cubiertos | Sí |
| Comprobaciones obligatorias | Sí |
| Evidencia y fuentes necesarias | Sí |
| Intervalos temporales | Sí (revalidación ≤7 días) |
| Criterios de finalización | Sí |
| Lagunas admisibles / no admisibles | Sí |
| Estado final | completa sin hallazgos / completa con hallazgos / parcial / fallida / ausente |

**Criterio de cierre:** manifiesto finito y versionado; «completa» = dentro del alcance declarado.  
**Ejemplo mínimo:**
```
MAN-07 v3 | 2026-10-22 | componentes: libX 2.1.0, toolY 0.9
obligatorias: 5 | cubiertas: 5 | evidencia: fuentes primarias 4, alternativa 1
intervalo: 7 días | lagunas admisibles: foro sin API
estado: COMPLETA CON HALLAZGOS (H-01)
```
**Retención:** PENDIENTE de aprobación.

---

## 7. `ejecucion.md`
**Dueño único:** A2 (vigilancia programada) · **Fuentes:** secciones 9 y 13

| Campo | Obligatorio |
|---|---|
| `corrida_id`, fecha/hora, zona horaria | Sí (zona: PENDIENTE si no definida) |
| Disparador (programado/manual) | Sí |
| Checkpoints completados | Sí |
| Checkpoints con hueco | Sí |
| Deduplicación aplicada | Sí |
| Informe persistido (ruta) | Sí |
| Interrupción y recuperación | Si hubo |
| Progreso vinculado a informe | Sí (mecanismo atómico o recuperable) |
| Estado | igual que cobertura |

**Criterio de cierre:** **sin informe persistido no hay avance**.  
**Ejemplo mínimo:**
```
RUN-2026-10-22T06:00Z | programado | checkpoints 5/5 | huecos: 0
dedup: 3 duplicados descartados | informe: vig/2026-10-22.md
estado: completa con hallazgos
```
**Retención:** PENDIENTE de aprobación.

---

## 8. `aprobaciones.md`
**Dueño único:** propietario (el coordinador transcribe) · **Fuente:** sección 14

| Campo | Obligatorio |
|---|---|
| `aprobacion_id` | Sí |
| Gate | GATE 1 / GATE 2 |
| Artefacto y versión | Sí |
| Destino (solo GATE 2) | Sí |
| Manifiesto: spec, prompt, configuración, código, dependencias, adaptadores, modelo | Sí |
| Hashes | Sí, o declaración de limitación + condición de reevaluación |
| Evidencia de evaluación | Sí |
| Vigencia / caducidad | Sí |
| Cambio material que la invalida | Sí (puede ser «ninguno») |
| Decisión | APROBADO / RECHAZADO / APROBADO CON CONDICIONES |

**Regla:** una aprobación **no se hereda** a otro artefacto ni a otro destino.  
**Ejemplo mínimo:**
```
AP-0003 | GATE 1 | ART-01 v1 | manifiesto: spec 4f2a…, prompt 8b1c…, cfg 77de…
hashes: completos | evaluación: EVA-01 | vigencia: 2026-11-21
invalida si: cambia permiso de red | decisión: APROBADO CON CONDICIONES
```
**Retención:** PENDIENTE de aprobación.

---

## 9. `bloqueos.md`
**Dueño único:** A2 recomienda, A3 consolida, coordinador registra · **Fuente:** sección 10

| Campo | Obligatorio |
|---|---|
| `bloqueo_id` | Sí |
| Agente y versión | Sí |
| Causa (una por registro) | Sí |
| Disparador | crítico / parcial / fallida / >24h sin revisión / sin revisión inicial |
| Acción tomada | aviso + bloqueo de nuevos despliegues del afectado |
| ¿Detiene el agente en funcionamiento? | **No** |
| Aprobación requerida para retirarlo | Sí |
| Excepción (si existe) | causa, versión, vencimiento, sin renovación automática |
| Estado | ABIERTO / RETIRADO / CADUCADO |

**Reglas:** dos bloqueos simultáneos se conservan; resolver una causa no elimina las demás; la excepción caduca.  
**Ejemplo mínimo:**
```
BL-04 | A2 v1 | causa: revisión parcial (fuente obligatoria inaccesible)
disparador: parcial | acción: aviso + bloqueo de despliegues de A2
detiene agente: no | retirada: aprobación humana tras cobertura válida
estado: ABIERTO
```
**Retención:** PENDIENTE de aprobación. **No eliminar evidencia de casos abiertos.**

---

## Verificación FAB-009
- [x] Nueve plantillas presentes
- [x] Cada campo trazado a una sección del prompt
- [x] Ninguna plantilla pide secretos
- [x] Ejemplo mínimo por plantilla
- [x] Dueño único por plantilla
- [x] Retención marcada PENDIENTE, sin inventar valores
