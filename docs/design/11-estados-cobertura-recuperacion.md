# FAB-011: Flujo de estados, cobertura, checkpoints y recuperación

**Versión:** 1.0 · **Estado:** DISEÑADO  
**Ámbito:** Sección 9 y parte de la 11  
**Dueño único:** A2 (cobertura y ejecución); A3 consolida

---

## 1. Estados de revisión

| Estado | Definición |
|---|---|
| `COMPLETA SIN NUEVOS HALLAZGOS` | Todas las comprobaciones obligatorias cubiertas; nada nuevo |
| `COMPLETA CON HALLAZGOS` | Cobertura obligatoria completa; hay ≥1 hallazgo |
| `PARCIAL` | Faltan comprobaciones obligatorias por causa justificada |
| `FALLIDA` | La revisión no pudo ejecutarse o terminó sin resultados utilizables |
| `AUSENTE (DETECTADA EXTERNamente)` | La revisión debía existir y no existe; detectada por control independiente |

**«Completa» significa dentro del alcance declarado**, no ausencia universal de riesgos.

## 2. Transiciones

```
(nueva revisión) ──▶ EN CURSO
EN CURSO ──todas las obligatorias cubiertas──▶ COMPLETA (con/sin hallazgos)
EN CURSO ──obligatoria no cubierta + evidencia alternativa válida──▶ PARCIAL
EN CURSO ──error/interrupción sin recuperación──▶ FALLIDA
(sin ejecución en el intervalo) ──control independiente──▶ AUSENTE
PARCIAL/FALLIDA ──nueva corrida que cubre lo que faltaba──▶ COMPLETA
```

Reglas:
- `PARCIAL` y `FALLIDA` **bloquean** nuevos despliegues del agente afectado.
- Una fuente **opcional** inaccesible **no** convierte toda la revisión en incompleta si la obligación se satisface con **evidencia alternativa válida**.
- **No reclasificar** una obligación como opcional durante la ejecución para conseguir un resultado completo.

## 3. Manifiesto de cobertura (antes de cada revisión)

Finito y versionado. Campos: componentes, riesgos cubiertos, **comprobaciones obligatorias**, evidencia y fuentes necesarias, intervalos temporales, criterios de finalización, **lagunas admisibles y no admisibles**.

```
MAN-<n> v<k>
componentes: [...]
riesgos: [...]
obligatorias: [C1..Cn]        # no reclasificables en ejecución
fuentes: [{id, tipo: primaria|alternativa, necesaria: sí|no}]
intervalo: revalidación ≤ 7 días
finalización: todas las obligatorias con evidencia o incertidumbre declarada
lagunas admisibles: [...]
lagunas no admisibles: [...]
```

## 4. Baseline histórica inicial

- Primera corrida = **baseline**. Registra el estado conocido en esa fecha.
- Desde ahí, **recuperar novedades desde la cobertura anterior**, sin limitar la investigación a los últimos 7 días.
- La ventana de 7 días es de **revalidación de evidencia**, no de búsqueda de publicaciones.

## 5. Checkpoints y recuperación

- Un checkpoint por **unidad de cobertura** (una comprobación obligatoria).
- Cada checkpoint registra: `id`, estado (`pendiente`/`hecho`/`hueco`), evidencia, deduplicación aplicada.
- **Huecos** se registran explícitamente; no se cuentan como cubiertos.
- Tras interrupción: reanudar desde el primer checkpoint no completado, **sin repetir** trabajo válido.

### Vinculación atómica
- Un avance solo cuenta si su informe está **persistido** (escritura atómica: fichero temporal + rename, o equivalente recuperable).
- **Sin evidencia guardada no se avanza.**
- **No repetir indefinidamente** trabajo válido: el checkpoint persistido lo marca como hecho.

```
avance = checkpoint.hecho AND informe.persistido
```

## 6. Vigencia

- Búsqueda de novedades: **diaria**.
- Revalidación de evidencia usada: **≤7 días** desde la última verificación sustantiva, o antes si aparece un cambio invalidante.
- Registrar **cuatro fechas separadas**: `publicación`, `actualización`, `consulta`, `verificación sustantiva`.
- Abrir una página **no** equivale a revalidar.
- Si no puede verificarse: registrar incertidumbre + efecto sobre cobertura. No inventar confirmación.

## 7. Interacción con bloqueos

| Situación | Efecto |
|---|---|
| `PARCIAL` o `FALLIDA` | Aviso + bloqueo de **nuevos despliegues** afectados |
| >24 h desde la última revisión completa | Aviso + bloqueo de despliegues afectados |
| Sin revisión completa inicial | **No** se autoriza despliegue operativo |
| Cobertura válida completada | Se retira **esa** causa; las demás permanecen |

El **gate de despliegue** comprueba evidencia y vigencia **directamente**, sin depender de que llegue una notificación.

## 8. Verificación FAB-011
- [x] Todos los estados y transiciones definidos
- [x] Manifiesto finito y versionado
- [x] Recuperación tras interrupción
- [x] No se avanza sin evidencia persistida
- [x] Parcial o fallida bloquea despliegues afectados
- [x] Se distinguen publicación, actualización, consulta y verificación sustantiva
