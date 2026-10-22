# FAB-015: Vigilancia programada, Telegram y detección independiente de ausencia

**Versión:** 1.0 · **Estado:** DISEÑADO — **la vigilancia NO está activa**  
**Ámbito:** Sección 13  
**Dueño:** A2 ejecuta · A3 consolida · propietario autoriza la activación

---

## 1. Estado declarado

> **La vigilancia programada no está activa.** Este documento la **diseña**. Ninguna afirmación aquí implica una instalación, prueba o despliegue existente.

Pendientes de activación: repositorio privado, identidades, secrets, destinatario Telegram verificado, horario y zona horaria.

## 2. GitHub Actions

**Ubicación:** se ejecuta desde el **repositorio privado** (los informes sensibles no pueden vivir en el público).

### Diseño del workflow

| Requisito | Implementación |
|---|---|
| Permisos mínimos | `permissions:` explícito; por defecto `contents: read`; sin `write-all` |
| Dependencias verificadas y fijadas | Acciones por **SHA** (`uses: owner/action@<sha>`), no por tag móvil |
| Credenciales | Solo desde secrets; nunca impresas; rotables |
| Concurrencia controlada | `concurrency:` con grupo único y `cancel-in-progress: false` |
| Límites de consumo | `timeout-minutes`; máximo de reintentos declarado |
| Recuperación de interrupciones | Checkpoints persistidos (FAB-011 §5); reanudar sin repetir |
| Detección externa de ausencia | Job **separado** que comprueba la frescura del último informe |
| Disparo | `schedule:` diario + `workflow_dispatch` manual |

### Identidades separadas
| Identidad | Permiso |
|---|---|
| **Lectura** | Leer inventario saneado (solo lectura) |
| **Informes** | Escribir informes en el repositorio privado |
| **Publicación** | Abrir PR en el repositorio público |

No se comparten tokens entre identidades.

## 3. Inventario

- **No se abre acceso general al equipo del usuario** para obtener inventarios.
- Se diseña un **suministro mínimo y autorizado de instantáneas saneadas**: el propietario (u operador) entrega una instantánea concreta.
- Cada instantánea lleva **marca de frescura** (fecha de captura y antigüedad).
- Sin secretos, sin configuración sensible innecesaria.

## 4. Telegram

- Destino: **chat privado previamente verificado** con el propietario.
- **No se asume que la integración existe.**
- **No se solicitan secretos por ningún canal público.**
- El canal transporta avisos, no aprobaciones.

### Fallo de Telegram
| Acción | Detalle |
|---|---|
| Mantener bloqueos | El bloqueo **no** depende del aviso |
| Registrar entrega pendiente | Con marca temporal |
| Cola privada | Reintentos **limitados** |
| Nunca desviar | Prohibido enviar información sensible a destino público |
| Entrega tardía | **No** elimina bloqueos |

## 5. Detección independiente de ausencia

```
job: freshness-check
  comprueba: última revisión completa del agente X
  contra: intervalo declarado en el manifiesto
  si supera el intervalo: estado=AUSENTE → aviso + bloqueo de despliegues
```

- **Independiente** del job de vigilancia: si la vigilancia no corre, este job **sí** corre.
- **Independiente** de Telegram: el bloqueo se aplica aunque el aviso no llegue.
- El **gate de despliegue** vuelve a comprobar evidencia y vigencia por sí mismo (FAB-013 §4.5).

## 6. Verificación FAB-015
- [x] El workflow tiene permisos mínimos
- [x] Existe detección independiente de ausencia
- [x] El fallo de Telegram no borra bloqueos
- [x] No se piden secretos por canal público
- [x] El inventario no requiere acceso general
- [x] El documento **no** afirma que la vigilancia ya está activa
