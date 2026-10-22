# FAB-012: Registro de bloqueos, emergencias y excepciones temporales

**Versión:** 1.0 · **Estado:** DISEÑADO  
**Ámbito:** Sección 10  
**Dueño:** A2 detecta y recomienda · A3 consolida · coordinador registra · propietario aprueba retiradas

---

## 1. Registro

Todo bloqueo se registra **por agente, versión y causa**. Una causa por registro; nunca se agrupan causas distintas.

| Campo | Contenido |
|---|---|
| `bloqueo_id` | Identificador único |
| Agente + versión | A quién afecta |
| Causa | Una sola, concreta |
| Disparador | §2 |
| Acción tomada | Aviso y/o bloqueo de nuevos despliegues |
| ¿Detiene el agente en funcionamiento? | **No**, nunca |
| Retirada | Quién la aprueba y con qué evidencia |
| Excepción | §4, si existe |
| Estado | ABIERTO / RETIRADO / CADUCADO |

## 2. Disparadores y acciones

| Disparador | Aviso | Bloqueo de nuevos despliegues | Detener agente | Retirada |
|---|---|---|---|---|
| **Riesgo potencialmente crítico** | Telegram | Sí, del agente afectado | **No** | Aprobación **humana** |
| **Revisión parcial** | Sí | Sí, de los afectados | No | Al completar cobertura válida |
| **Revisión fallida** | Sí | Sí, de los afectados | No | Al completar cobertura válida |
| **>24 h sin revisión completa** | Sí | Sí, de los afectados | No | Al completar revisión válida |
| **Sin revisión completa inicial** | — | **No se autoriza despliegue operativo** | No | Tras la primera revisión completa |

**Regla de retirada:** completar una cobertura válida retira **esa causa** y **solo esa**. Las demás causas permanecen abiertas.

## 3. Detección independiente de ausencia

El mecanismo de detección **no** depende de que llegue una notificación ni de que Telegram funcione:
- Comprueba la existencia y vigencia de la última revisión contra el intervalo declarado.
- Si el intervalo se supera → estado `AUSENTE` + bloqueo.
- El **gate de despliegue** comprueba evidencia y vigencia **directamente**.

**Pendiente:** mecanismo independiente de supervisión (parámetro de activación).

## 4. Excepciones temporales (DECISIÓN DE DISEÑO)

Humanas, justificadas y acotadas:

| Requisito | Valor |
|---|---|
| Autor | El propietario (nunca un rol) |
| Justificación | Escrita, con el problema que se quiere corregir |
| Alcance | **Una versión** y **una causa** |
| Vencimiento | **Obligatorio** y explícito |
| Renovación automática | **Prohibida** |
| Efecto al vencer | El bloqueo sigue vigente |

Una excepción no desbloquea otras causas ni otros agentes.

## 5. Construcción y pruebas aisladas

- **No** se bloquean la construcción ni las pruebas aisladas necesarias para corregir un problema: eso no es un despliegue operativo.
- Si esas pruebas requieren permisos nuevos, **se piden** (GATE 1); no se asumen.
- Las pruebas aisladas de bootstrap **no** son aprobación operativa.

## 6. Auditoría

- El registro es **append-only**; los cambios de estado son eventos nuevos, no ediciones.
- Cada bloqueo conserva su evidencia de detección.
- **No se elimina automáticamente** evidencia de casos abiertos; la política de retención (PENDIENTE) se aprueba antes de activar.

## 7. Fallo de Telegram
- El bloqueo **se mantiene**.
- Se registra la **entrega pendiente**.
- Se conserva una **cola privada** con reintentos limitados.
- **No** se desvía información sensible a un destino público.
- La entrega tardía del aviso **no elimina** el bloqueo.

## 8. Verificación FAB-012
- [x] Cada disparador tiene acción asociada
- [x] Dos bloqueos simultáneos se conservan
- [x] La excepción caduca y no se renueva
- [x] La detección no depende de Telegram
- [x] El registro es auditable
- [x] No se confunde bloqueo de despliegue con parada del agente
