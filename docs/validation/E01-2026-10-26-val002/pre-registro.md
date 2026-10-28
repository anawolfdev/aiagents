# Pre-registro — E01 / VAL-002

- **Feature:** VAL-002 — Piloto E01 (repetición observacional con flujo real)
- **Fecha de congelación:** 2026-10-26T11:54:24Z (UTC), antes del primer `opencode run`
- **Sustituye a:** VAL-001 (`docs/validation/E01-2026-10-26/`, conservado como histórico)
- **Estado del piloto en este documento:** pre-registrado, no ejecutado todavía

## 1. Autorización del propietario

Cita literal registrada, tal como la transmitió el líder de VAL-002:

> «haz el a»

- **Fecha:** 2026-10-26
- **Opción elegida:** A — repetición observacional con flujo real, repositorio
  temporal y criterios observacionales.
- **Alcance autorizado:** repetir el piloto E01 de VAL-001 con el flujo actual
  (`lider → explorer → implementer → reviewer`) y con un flujo simplificado de
  un solo agente, misma entrada y mismo modelo, n=1.
- **Transmisión:** la cita fue aportada por el líder en la instrucción de
  ejecución de VAL-002. Durante el piloto no se contacta al propietario ni se
  simula ninguna respuesta suya.

## 2. Parámetros fijados por el líder

Estos parámetros son los de la instrucción de ejecución de VAL-002. Se aceptan
tal cual; no se suben. Los topes son inferiores a la propuesta del explorer
(10.000.000 / 90 min y 500.000 / 20 min), por lo que no se amplía nada.

| Parámetro | Valor congelado |
|---|---|
| Ruta de evidencia | `docs/validation/E01-2026-10-26-val002/` |
| Ruta histórica que no se reutiliza | `docs/validation/E01-2026-10-26/` (no se sobrescribe) |
| Orden de flujos | `actual` → `simplificado` |
| Modelo | `opencode/big-pickle` |
| OpenCode | `1.18.32` |
| Base del sandbox | `0d38c72` (`0d38c728ac9303c0fb3d588501303770df8f9e6b`) |
| Sandbox actual | `/tmp/opencode/val002/actual` |
| Sandbox simplificado | `/tmp/opencode/val002/simplificado` |
| Tope actual | 2.000.000 tokens / 60 min (3.600 s) |
| Tope simplificado | 300.000 tokens / 15 min (900 s) |
| Tope global | 2.300.000 tokens / 75 min (4.500 s) |
| Aviso al 80 % | actual 1.600.000 tokens / 48 min; simplificado 240.000 / 12 min; global 1.840.000 / 60 min. Se registra el aviso. |
| Corte al 100 % | `timeout --signal=INT --kill-after=60`; exportar lo disponible, escribir `ABORTADO_POR_TOPE` y no estimar ni relanzar en silencio. |

### 2.1 Sanitización del sandbox

El clon temporal se prepara sin remoto y sin los elementos que filtrarían el
resultado o tocarían GEAS:

- sin `.geas.yml`;
- sin `config/geas.yml`;
- sin `docs/design/16-validacion.md` (rúbrica E01);
- sin `docs/validation/` (incluida la evidencia de VAL-001);
- sin informes ni progreso de VAL-001;
- sin remoto Git;
- una sola feature neutra, `VAL-E01-NEUTRAL`, con la descripción igual a la
  entrada exacta y criterios `por definir con el propietario`.

Las sesiones capturadas deben tener `directory` del sandbox correspondiente.
El repositorio principal no recibe código de producto durante la ejecución.

## 3. Entrada exacta

Cadena única, sin comillas angulares en el prompt real:

```text
Quiero una herramienta para gestionar las inscripciones de un evento y avisar a la gente
```

- `input_sha256 = 5f35bc01439230eb2579082bdf2ed3efef28f4aa80960fcf343b2c70c8e92582`
- La misma cadena para los dos flujos.
- En el flujo actual, la primera entrada es exactamente esa cadena. Si el líder
  no delega, se permite **como máximo una** continuación operativa
  pre-registrada que solo ordene delegar en `explorer`, `implementer` y
  `reviewer` y registrar con `harness record`. Esa continuación no es una
  respuesta del propietario ni una entrada de producto.
- Si el flujo pregunta, las preguntas se registran; no se contestan.

## 4. Protocolo de ejecución

### 4.1 Flujo actual

1. `opencode run --agent lider --model opencode/big-pickle --format json` con la
   entrada exacta como primer y único mensaje del turno 1.
2. Se consulta la tabla `session` de OpenCode para obtener el árbol real
   (`parent_id`) y se comprueba que haya sesiones hijas `explorer`,
   `implementer` y `reviewer`, todas bajo el `lider` y con `directory` del
   sandbox.
3. Si no hay delegación, se envía una única continuación operativa en la misma
   sesión. No se simula al propietario, no se responde al requisito y no se
   inventan decisiones.
4. El caso debe quedar pendiente de aclarar. No se ejecuta `harness finish` ni
   se marca la feature `done`.

### 4.2 Flujo simplificado

Un único agente primario `a1`, con el prompt de
`docs/design/roles/A1-analista.md`, mismo modelo, misma entrada exacta y sin
subagentes ni `bash`/`task`. No lleva continuación. Si no pregunta, se registra
el resultado observado; no se fuerza la pregunta.

### 4.3 Condición de parada

Se para cuando:

- los dos flujos han terminado y sus sesiones están exportadas;
- se alcanza un tope de tokens o de tiempo → `ABORTADO_POR_TOPE` con evidencia
  parcial y contadores reales;
- el flujo pide una decisión del propietario → se registra y no se simula;
- falta la cadena completa tras la única continuación permitida → run inválido
  y se registra como tal (no se rellena con ejecuciones manuales).

## 5. Observación de las cuatro dimensiones

Se comprobará, con cita literal, si el flujo pregunta antes de decidir por:

1. avisos;
2. canal;
3. destinatarios;
4. cuándo/momento.

`NO APARECE` y `DECIDIDO_EN_SILENCIO` son resultados válidos y se registran con
cita. No se añaden preguntas sintéticas ni se modifican los prompts para
introducir esas dimensiones. Un resultado negativo no se convierte en positivo.

## 6. Medición

- Fuente primaria: tabla `session` de
  `/home/cacelas/.local/share/opencode/opencode.db` (solo lectura) y
  `opencode export <session-id>`.
- Campos: `tokens_input`, `tokens_output`, `tokens_reasoning`,
  `tokens_cache_read`, `tokens_cache_write`, `cost`, `model`, `directory`,
  `time_created`, `time_updated`.
- `measured_at` se escribe después de todos los exports y debe ser posterior al
  máximo `time_updated`.
- Si una sesión no se puede medir, se escribe `no medible` y la limitación; no
  se estima ni se multiplica por una tarifa inventada.
- `invoice_verified = false`: OpenCode reporta coste, no es una factura
  independiente.

## 7. Límites del alcance

- n=1. No se declara superioridad general de un flujo sobre otro.
- No se declara la fábrica PROBADA ni se autoriza eliminar agentes.
- No se ejecutan A2–A5 ni se activa nada.
- No se actualiza `docs/design/16-validacion.md`: la fila E01 y la firma del
  propietario quedan pendientes. E02–E17 siguen `NO EJECUTADO`.
- No se commitea en el repositorio principal.

## 8. Congelación

El SHA-256 de este fichero, calculado antes del primer `opencode run`, se
registra en `manifest.json` (`pre_registro_sha256`). Cualquier cambio posterior
del pre-registro invalida el run.
