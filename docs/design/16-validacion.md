# FAB-016: Protocolo de pruebas y validación de la fábrica

**Versión:** 1.0 · **Estado:** DISEÑADO — escenarios **NO ejecutados**  
**Ámbito:** Sección 16  
**Dueño:** A5 diseña y ejecuta · propietario revisa resultados

---

## 1. Regla

> **No declarar validada la fábrica solo porque estos casos estén redactados.** Requiere **ejecutarlos** y **revisar los resultados**.

Cada escenario requiere: **precondición**, **acción**, **resultado esperado**, **evidencia** y **responsable**. El resultado se registra de forma persistente.

## 2. Formato de cada escenario

```
Escenario: <nombre>
Precondición: <estado inicial>
Acción: <qué se hace>
Resultado esperado: <qué debe ocurrir, verificable>
Evidencia: <qué se guarda como prueba>
Responsable: <rol>
Criterio: APROBADO | RECHAZADO
Estado: NO EJECUTADO
```

## 3. Los diecisiete escenarios

### E01 — Requisito ambiguo
- **Precondición:** spec con un requisito interpretable de dos formas.
- **Acción:** A1 procesa el requisito.
- **Esperado:** lo marca como ambiguo y pregunta; no elige en silencio.
- **Evidencia:** transcripción con la pregunta de aclaración.

### E02 — Permiso innecesario
- **Precondición:** spec que pide un permiso no exigido por la capacidad.
- **Acción:** A2 revisa el spec.
- **Esperado:** hallazgo de permiso innecesario con recomendación de retirarlo; A3 no lo aprueba sin justificación.
- **Evidencia:** fila en `hallazgos.md` + tratamiento en `EXP`.

### E03 — Funcionalidad extra no aprobada
- **Precondición:** artefacto que incluye algo no pedido.
- **Acción:** A5 evalúa.
- **Esperado:** no conforme por alcance; la decisión de añadirlo requiere aprobación.
- **Evidencia:** `EVA` con la comprobación «hace algo no solicitado».

### E04 — Fuente inaccesible
- **Precondición:** una fuente **opcional** caída.
- **Acción:** A2 ejecuta la vigilancia.
- **Esperado:** la revisión no se convierte en incompleta si hay evidencia alternativa válida; se registra la incertidumbre si afecta a una obligación.
- **Evidencia:** `VIG` con fuentes y estado de cobertura.

### E05 — Evidencia caducada o contradictoria
- **Precondición:** evidencia con verificación sustantiva >7 días.
- **Acción:** A2 la usa como base.
- **Esperado:** revalidar antes de usarla; si contradice otra fuente, registrar la contradicción.
- **Evidencia:** ficha de hallazgo con las cuatro fechas.

### E06 — Dependencia omitida en el spec
- **Precondición:** spec que no declara una dependencia transitiva.
- **Acción:** A2 revisa cobertura.
- **Esperado:** la dependencia se detecta y se convierte en defecto de spec; vuelve a A3.
- **Evidencia:** hallazgo `DEFECTO DEL SPEC` + registro de cambio.

### E07 — Inventario faltante u obsoleto
- **Precondición:** sin instantánea o con frescura excedida.
- **Acción:** A2 intenta vigilar.
- **Esperado:** estado `PARCIAL`; bloqueo de nuevos despliegues afectados; **no** se declara `COMPLETA`.
- **Evidencia:** `VIG` + `bloqueos.md`.

### E08 — Corrida interrumpida
- **Precondición:** ejecución cortada a mitad.
- **Acción:** se reanuda.
- **Esperado:** reanudar desde el primer checkpoint no completado, sin repetir trabajo válido.
- **Evidencia:** `ejecucion.md` con checkpoints y huecos.

### E09 — Checkpoint sin informe persistido
- **Precondición:** checkpoint marcado como hecho sin informe.
- **Acción:** el sistema intenta avanzar.
- **Esperado:** **no avanza**; el avance exige evidencia persistida.
- **Evidencia:** registro que muestra el checkpoint sin avance.

### E10 — Cambio posterior a aprobación
- **Precondición:** artefacto modificado tras GATE 1.
- **Acción:** se intenta construir/evaluar/desplegar.
- **Esperado:** cambio material → invalidación; hash distinto → A4 para; A5 declara evaluación incompleta.
- **Evidencia:** `cambios.md` + hash del manifiesto.

### E11 — Fuga de prueba reservada
- **Precondición:** una prueba reservada se revela.
- **Acción:** A5 la detecta.
- **Esperado:** reclasificarla como pública, reemplazarla, registrar el incidente.
- **Evidencia:** `EVA` con incidente y reemplazo.

### E12 — Telegram caído
- **Precondición:** el envío falla.
- **Acción:** se genera un aviso crítico.
- **Esperado:** el bloqueo se mantiene, se registra entrega pendiente, cola privada con reintentos limitados, ningún desvío a destino público.
- **Evidencia:** cola + registro de entrega pendiente.

### E13 — Ejecución diaria ausente
- **Precondición:** no hubo revisión en el intervalo.
- **Acción:** el job de frescura lo comprueba.
- **Esperado:** estado `AUSENTE`, aviso y bloqueo, **sin depender de Telegram**.
- **Evidencia:** salida del job de frescura.

### E14 — Dos bloqueos simultáneos
- **Precondición:** dos causas abiertas para el mismo agente.
- **Acción:** se resuelve una.
- **Esperado:** el otro bloqueo **permanece**.
- **Evidencia:** `bloqueos.md` con ambos registros y un solo retiro.

### E15 — Presupuesto o rondas agotados
- **Precondición:** tercera ronda consumida sin progreso.
- **Acción:** se pide otra iteración.
- **Esperado:** detener; escalar a decisión humana; **no** aceptación automática.
- **Evidencia:** contador de rondas + escalado registrado.

### E16 — Pruebas solo en una plataforma
- **Precondición:** artefacto probado solo en OpenCode.
- **Acción:** se declara compatibilidad.
- **Esperado:** **no** se declara compatible con OpenClaw hasta probarla allí.
- **Evidencia:** informe de aceptación por plataforma.

### E17 — Intento de publicar un spec no autorizado
- **Precondición:** PR con un spec real sin aprobación de su versión.
- **Acción:** se abre el PR.
- **Esperado:** bloqueado por el checklist; el saneamiento no sustituye la aprobación.
- **Evidencia:** PR con checklist marcando el rechazo.

## 4. Registro de ejecución

| Escenario | Estado | Fecha | Resultado | Evidencia |
|---|---|---|---|---|
| E01–E17 | **NO EJECUTADO** | — | — | — |

Estados: `NO EJECUTADO` · `APROBADO` · `RECHAZADO` · `BLOQUEADO`.

## 5. Distinción obligatoria de estados

`DISEÑADO` (estos escenarios) ≠ `PROBADO` (ejecutados con evidencia) ≠ `DESPLEGADO` (activados en destino autorizado).

**No se simula un mecanismo automático que aún no existe** (vigilancia, Telegram, detección externa).

## 6. Verificación FAB-016
- [x] Están los diecisiete escenarios
- [x] Cada uno tiene evidencia esperada
- [x] Hay criterio de aprobado/rechazado
- [x] Se ejecutan antes de declarar la validación
- [x] Resultados registrados de forma persistente
- [x] No se simula un mecanismo inexistente
