# FAB-013: Presupuesto, rondas y gates de aprobación y despliegue

**Versión:** 1.0 · **Estado:** DISEÑADO  
**Ámbito:** Secciones 11 y 14  
**Dueño:** A3 prepara · propietario aprueba · coordinador registra

---

## 1. Presupuesto

- **No hay presupuesto monetario aprobado.** Estado: PENDIENTE.
- Antes de activar ejecuciones con coste: **estimación + aprobación** del propietario.
- **No** se autoriza gasto recurrente por defecto.
- El presupuesto se separa en tres bolsas independientes:

| Bolsa | Cubre |
|---|---|
| **Creación** | A1–A4 hasta el primer artefacto |
| **Corrección** | Rondas de corrección tras evaluación |
| **Vigilancia** | Ejecuciones programadas de A2 |

- Límites **ejecutables**: por corrida, duración máxima, número de reintentos.
- **El agotamiento del presupuesto no equivale a ausencia de riesgos**: se declara `PARCIAL`/`FALLIDA` y se bloquea lo afectado.

## 2. Rondas de construcción–evaluación

**DECISIÓN DE DISEÑO**

| Regla | Valor |
|---|---|
| Máximo de rondas | **3** |
| Composición | 1 inicial + 2 de corrección |
| Ámbito | El **ciclo completo** |
| ¿Se multiplica por plataforma? | **No** |
| ¿Se reinicia por cambios triviales? | **No** |
| ¿Agotar rondas acepta el artefacto? | **Nunca** |

- **Detener antes** si no hay progreso entre rondas.
- Ampliaciones requieren aprobación explícita.
- Al agotar rondas: escalar a decisión humana; el artefacto queda **no conforme** hasta que se apruebe otra cosa.

## 3. GATE 1 — spec, permisos y presupuesto

**Quién aprueba:** el propietario. **Quién prepara:** A3.

Contenido obligatorio:
1. Versión del spec + hash.
2. Matriz requisito–capacidad–permiso–prueba.
3. Permisos solicitados, cada uno justificado.
4. Estimación de coste (o `PENDIENTE`, sin inventar).
5. Hallazgos y su tratamiento.
6. Cambios materiales desde la aprobación anterior.
7. Riesgos residuales.
8. Recomendación de A2.

Sin GATE 1 aprobado, A4 **no construye**.

## 4. GATE 2 — despliegue de un artefacto concreto en un destino concreto

**Quién aprueba:** el propietario.

Contenido obligatorio:
1. Manifiesto del artefacto (spec, prompt, configuración, código, dependencias, adaptadores, modelo).
2. Hashes de cada componente **o** declaración de la limitación + condición de reevaluación.
3. Evidencia de evaluación (EVA) conforme.
4. Destino concreto (equipo del propietario o entorno aislado de pruebas).
5. Evidencia y **vigencia** del último informe de cobertura (comprobado directamente por el gate).
6. Procedimiento de reversión.
7. Monitorización proporcional.
8. Estado de bloqueos del agente afectado.

## 5. Manifiesto de artefacto

```
manifest:
  spec:         <id, versión, hash>
  prompt:       <versión, hash>
  configuracion:<versión, hash>
  codigo:       <versión, hash>
  dependencias: [{nombre, versión, hash si aplica}]
  adaptadores:  [{plataforma, versión, hash}]
  modelo:       <proveedor/modelo/versión o PENDIENTE>
```

- Usar identificadores o hashes cuando apliquen.
- Si un componente no puede fijarse (p. ej. modelo tras API), **declarar la limitación** y la **condición de reevaluación**.

## 6. Invalidación

| Cambio | Efecto |
|---|---|
| Material (intención, alcance, permisos, datos, dependencias, modelo, destino, criterios) | Invalida la aprobación afectada |
| Material que afecta al despliegue | Invalida GATE 2; puede requerir GATE 1 |
| No material (formato, comentarios) | No invalida, pero se registra |

Una aprobación **no se amplía automáticamente** a otro artefacto, versión o destino.

## 7. Reversión y monitorización

- Proporcionales al riesgo y al destino.
- Reversión **probada** al menos una vez antes de considerar el despliegue reversible.
- Monitorización declara qué se vigila, con qué umbral y quién actúa.

## 8. Verificación FAB-013
- [x] Ambos gates definidos
- [x] El manifiesto identifica el artefacto
- [x] El límite de rondas es ejecutable
- [x] Todo gasto exige aprobación
- [x] Un cambio material invalida la aprobación
- [x] Una aprobación no se hereda a otro artefacto o destino
