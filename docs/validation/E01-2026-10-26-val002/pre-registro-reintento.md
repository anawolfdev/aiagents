# Pre-registro de reintento — E01 / VAL-002

- **Feature:** VAL-002 — Piloto E01 (repetición observacional con flujo real)
- **Fecha de congelación:** 2026-10-27T08:XX:XXZ (UTC), antes del reintento
- **Sustituye a:** intento fallido del 2026-10-26
- **Estado:** pre-registrado para reintento con aislamiento corregido

## 1. Autorización del propietario

Cita literal registrada:
> «continua»

- **Fecha:** 2026-10-27
- **Interpretación:** únicamente autorización para retomar el piloto con el mismo alcance, ruta y topes ya congelados, corrigiendo el aislamiento. No se interpreta como respuesta al spec, ni como permiso para inventar requisitos, ni como confirmación nueva de los puntos de validación si se considera insuficiente.

## 2. Fallo del primer run

- **Sesión root observada:** `ses_e87ecf8a3ffevgzkEingA6Geb4` (agente lider, título `VAL-002/E01 actual root`)
- **Directorio de sesión:** `/home/cacelas/aiagents` (repo principal), NO `/tmp/opencode/val002/actual`
- **Resultado:** wrapper terminó con `"error": "root session never appeared"`
- **Evidencia conservada:** `docs/validation/E01-2026-10-26-val002/actual/status-turn1.json`, `docs/validation/E01-2026-10-26-val002/actual/monitor-turn1.log`, `docs/validation/E01-2026-10-26-val002/tools/run_with_cap.py`
- **Nota:** No se reutiliza esa sesión ni sus eventos como evidencia.

## 3. Diagnóstico

- **git rev-parse --show-toplevel (sandbox):** `/tmp/opencode/val002/actual` (correcto)
- **.git del clon (sandbox):** clon aislado en `/tmp/opencode/val002/actual/.git` (directorio propio, sin remoto origin tras preparación)
- **Entorno heredado OpenCode:** `OPENCODE=1`, `OPENCODE_PID=4073534` presentes en el shell; `XDG_DATA_HOME` vacío. Hay servidor OpenCode corriendo (`opencode serve` en puerto 44587) que fue alcanzado por `opencode run`, haciendo que el cliente se conectara a un servidor existente del repo principal/contexto principal.
- **Hipótesis confirmada:** `opencode run` se conectó a un servidor ya existente del repo principal.

## 4. Arreglo de aislamiento

- Usar `XDG_DATA_HOME` aislado con copia propia de `auth.json` (ej. `/tmp/opencode/val002/xdg_reintento/`) para que OpenCode use su propia base de datos de sesiones.
- Eliminar variables `OPENCODE*` del entorno del wrapper (`env -u OPENCODE -u OPENCODE_PID ...`).
- Ejecutar desde el sandbox `/tmp/opencode/val002/actual` con cwd correcto.
- **Prueba de aislamiento (sin entrada del piloto):** Con entorno aislado se creó sesión `ses_e83c9b987ffeS7dKy05m4xy5p6` con `directory=/tmp/opencode/val002/actual` en la DB aislada. **PRUEBA PASA.**

## 5. Parámetros congelados (mismos que pre-registro original)

| Parámetro | Valor congelado |
|---|---|
| Ruta de evidencia | `docs/validation/E01-2026-10-26-val002/` |
| Orden de flujos | `actual` → `simplificado` |
| Modelo | `opencode/big-pickle` |
| OpenCode | `1.18.32` |
| Base del sandbox | `0d38c72` |
| Sandbox actual | `/tmp/opencode/val002/actual` |
| Tope actual | 2.000.000 tokens / 60 min (3.600 s) |
| Tope simplificado | 300.000 tokens / 15 min (900 s) |
| Entrada exacta | `Quiero una herramienta para gestionar las inscripciones de un evento y avisar a la gente` |
| input_sha256 | `5f35bc01439230eb2579082bdf2ed3efef28f4aa80960fcf343b2c70c8e92582` |

## 6. Hash
9e4e6db7e59591c110083c5fba93732e27c9b713ab8e42b2f9a34fde6525a90f
