# FAB-018: Checklist de activación y registro de parámetros pendientes

**Versión:** 1.0 · **Estado:** DISEÑADO — **nada activado**  
**Ámbito:** Sección 17  
**Dueño:** propietario

---

## 1. Regla

> **Ningún punto se declara resuelto sin prueba.** No se inventan valores. No se atribuyen instalaciones, pruebas o despliegues inexistentes.

La **política de retención se aprueba antes de activar**. **No** se elimina automáticamente evidencia de casos abiertos.

## 2. Checklist de activación

| # | Parámetro | Responsable | Evidencia requerida | Condición bloqueante | Aprobación | Reversión | Estado |
|---|---|---|---|---|---|---|---|
| 1 | Repositorio público concreto | Propietario | URL + permisos verificados | Sin repo no hay publicación | GATE 1 | Archivar repo | DISEÑADO |
| 2 | Repositorio privado separado | Propietario | URL + permisos verificados | Sin él no se guardan specs/informes | GATE 1 | Archivar repo | DISEÑADO |
| 3 | Proveedor y modelo autorizado | Propietario | Lista de proveedores aprobados + modelo | Sin él no se procesa material privado | GATE 1 | Revocar acceso | DISEÑADO |
| 4 | Presupuesto (estimación + límites) | Propietario | Estimación por bolsa (creación/corrección/vigilancia) | Sin aprobación no se activa gasto | GATE 1 | Detener ejecuciones | DISEÑADO |
| 5 | Horario de vigilancia | Propietario | Cron declarado | Sin horario no hay revisión diaria | GATE 1 | Desactivar schedule | DISEÑADO |
| 6 | Zona horaria | Propietario | Zona IANA declarada | Afecta a >24 h y a frescura | GATE 1 | — | DISEÑADO |
| 7 | Conexión y destinatario Telegram | Propietario | Chat privado **verificado** (prueba de entrega) | Sin él no hay aviso; el bloqueo no depende de él | GATE 1 | Desconectar bot | DISEÑADO |
| 8 | Inventario (instantánea saneada) | Propietario | Snapshot con marca de frescura | Sin inventario la revisión es `PARCIAL` | GATE 1 | Descartar snapshot | DISEÑADO |
| 9 | Aislamiento comprobado | Propietario | Prueba de que el entorno está aislado | «Local» ≠ «aislado» | GATE 1 | Destruir entorno | DISEÑADO |
| 10 | Permisos | Propietario | Matriz FAB-010 aprobada | Sin permisos nada corre | GATE 1 | Revocar | DISEÑADO |
| 11 | Retención | Propietario | Política escrita y aprobada | **Bloquea toda activación** | Aprobación explícita | Ajustar política | DISEÑADO |
| 12 | Almacenamiento | Propietario | Ubicación + backup | Sin almacén no hay informes | GATE 1 | Migrar | DISEÑADO |
| 13 | Mecanismo independiente de supervisión | Propietario | Job de frescura probado | Sin él no hay detección de ausencia | GATE 1 + prueba | Desactivar | DISEÑADO |

## 3. Checklist de activación por fase (bootstrap FAB-017)

| Fase | Requisito previo | Estado |
|---|---|---|
| 2 · Recursos mínimos | #1, #2, #10, #12 | NO CUMPLIDO |
| 3 · Construcción A1 | Fase 2 + documento de decisiones | NO CUMPLIDO |
| 4 · Pruebas y validación humana | Fase 3 + revisor distinto | NO CUMPLIDO |
| 5 · Construcción A2–A5 | Fase 4 aprobada | NO CUMPLIDO |
| 6 · Ensayo integral | Fase 5 | NO CUMPLIDO |
| 7 · Activación | #3–#9, #11, #13 + GATE 2 por destino | NO CUMPLIDO |

## 4. Lo que este documento NO afirma

- No hay ningún repositorio creado.
- No hay proveedor autorizado.
- No hay presupuesto aprobado.
- No hay bot de Telegram conectado.
- No hay workflow de GitHub Actions activo.
- No hay inventario tomado.
- No hay aislamiento comprobado.
- No hay retención aprobada.
- No hay despliegue de ningún tipo.

## 5. Secretos

Este documento **no contiene secretos** y **no debe contenerlos**. Los tokens viven en el gestor de secretos del entorno; aquí solo se declara **dónde** están y **quién** los rota (PENDIENTE).

## 6. Verificación FAB-018
- [x] Están todos los parámetros pendientes
- [x] Cada uno tiene dueño y evidencia
- [x] Ninguno se declara resuelto sin prueba
- [x] La retención está marcada como bloqueante antes de la activación
- [x] No hay secretos en el documento
- [x] El checklist puede bloquear la activación
