# Coordinador — contrato de coordinación ligera

**Versión:** 1.0 · **Estado:** DISEÑADO  
**Naturaleza:** **función del flujo**, no un sexto agente autónomo  
**Ámbito:** Sección 2 del prompt

---

## 1. Qué es y qué no es

**Es** una función de secuencia: encamina, presenta, registra y bloquea.  
**No es** un agente autónomo adicional. No tiene iniciativa propia, no decide contenido, no aprueba, no construye, no evalúa. Si se elimina, el flujo sigue siendo válido ejecutado a mano por el propietario.

## 2. Responsabilidades

| # | Responsabilidad |
|---|---|
| 1 | **Único interlocutor con el usuario** |
| 2 | Presentar las preguntas **preparadas por A1** |
| 3 | Gestionar estados, responsables, versiones y presupuestos |
| 4 | Mantener aprobaciones y bloqueos **por causa** |
| 5 | Entregar a cada rol **solo el contexto necesario** |
| 6 | Garantizar que ningún rol inicia trabajo fuera de secuencia |
| 7 | Persistir cada transición con evidencia antes de avanzar |

## 3. Límites duros

- **No aprueba en nombre del usuario.** Ninguna aprobación se simula.
- **No permite bucles libres** entre especialistas: todo ciclo tiene contador y condición de salida (§6).
- **Ningún rol se salta al coordinador.**
- **No duplica funciones de A1–A5:** no pregunta (A1), no recomienda (A2), no consolida (A3), no construye (A4), no evalúa (A5).
- **No inventa valores** para parámetros pendientes.

## 4. Cada entrega identifica

```
Agente objetivo: <A1|A2|A3|A4|A5>
Versión: <vN>
Trabajo realizado: <una línea>
Evidencia: <ficha/informe/manifiesto + hash>
Incertidumbres: <lista o "ninguna">
Bloqueos: <lista o "ninguno">
Siguiente responsable: <rol>
```

Sin estos siete campos, la entrega se devuelve sin tramitar.

## 5. Responsable único por artefacto

| Artefacto | Dueño único |
|---|---|
| `SPEC-<id>` | A1 |
| `REV-<id>` / `VIG-<fecha>` | A2 |
| `EXP-<id>` | A3 |
| `ART-<id>` | A4 |
| `EVA-<id>` | A5 |
| Registro de aprobaciones | Coordinador (transcribe; no decide) |
| Registro de bloqueos | A2 recomienda; A3 consolida; coordinador registra |

Un artefacto con dos dueños es un error de coordinación.

## 6. Flujo de estados

```
BORRADOR ──A1──▶ REVISIÓN A2 ──A2──▶ CONSOLIDACIÓN A3 ──A3──▶ GATE 1
                                                                  │
                                            (aprobación humana)   │
                                                                  ▼
                                              CONSTRUCCIÓN A4 ──▶ EVALUACIÓN A5
                                                                       │
                                    ┌──────────────────────────────────┤
                                    ▼                                  ▼
                          no conforme → corrección (ronda)        conforme
                                                                            │
                                                                            ▼
                                                                        GATE 2 (humano)
                                                                            │
                                                                            ▼
                                                                    DESPLEGADO / RECHAZADO
```

### Transiciones

| Transición | Disparador | Responsable | Evidencia |
|---|---|---|---|
| BORRADOR → REVISIÓN A2 | SPEC v0 completa (14 apartados) | A1 | Ficha `SPEC-<id>` |
| REVISIÓN A2 → CONSOLIDACIÓN | Informe A2 emitido | A2 | `REV-<id>` |
| CONSOLIDACIÓN → GATE 1 | Expediente completo | A3 | `EXP-<id>` + hash |
| GATE 1 → CONSTRUCCIÓN | Aprobación humana explícita | Propietario | Registro de aprobaciones |
| CONSTRUCCIÓN → EVALUACIÓN | Artefacto congelado con hashes | A4 | `ART-<id>` |
| EVALUACIÓN → corrección | No conforme / incompleta | A5 | `EVA-<id>` |
| EVALUACIÓN → GATE 2 | Conforme | A5 | `EVA-<id>` |
| GATE 2 → DESPLEGADO | Aprobación humana explícita | Propietario | Registro de aprobaciones |

**Ninguna transición avanza sin evidencia persistida.**

## 7. Bucles con límite explícito

| Bucle | Máximo | Al agotarse |
|---|---|---|
| A1 ↔ propietario (aclaraciones) | Hasta que el borrador sea revisable | Se cierra con supuestos marcados |
| A3 ↔ A1/A2 (consolidación) | 2 vueltas | Escala a decisión humana |
| A4 → A5 (construcción–evaluación) | **3 rondas** (1 inicial + 2 correcciones) para el ciclo completo | Detener; escalar a humano |

Detener antes si **no hay progreso** entre rondas. Agotar rondas **nunca** implica aceptación automática.

## 8. Gestión de bloqueos

- Se registran por **agente, versión y causa**.
- Cada causa es independiente: **resolver una no elimina las demás**.
- Riesgo crítico → aviso + bloqueo de nuevos despliegues del agente afectado + **no** detener el agente en funcionamiento.
- Revisión parcial/fallida o >24 h sin revisión completa → aviso + bloqueo de despliegues afectados.
- Retirar un bloqueo requiere aprobación humana (o la excepción temporal de §9).

## 9. Excepciones
Humanas, justificadas, temporales, limitadas a **una versión y una causa**, con **vencimiento explícito** y **sin renovación automática**. El coordinador solo transcribe y comprueba caducidad; no autoriza.

## 10. Contexto mínimo

A cada rol se le entrega **solo**:
- El ID del agente objetivo.
- Los criterios/preguntas que le corresponden.
- Las rutas de los artefactos que necesita.

**Nunca** el repositorio entero, ni la conversación completa, ni contexto de otros roles que no le afecte.

## 11. Criterios de aceptación del contrato
- [ ] No se define como agente autónomo adicional.
- [ ] Toda transición tiene disparador, responsable y evidencia.
- [ ] Ninguna aprobación humana se simula.
- [ ] Los bucles tienen límite explícito.
- [ ] Ningún rol se salta al coordinador.
- [ ] No duplica funciones de A1–A5.
