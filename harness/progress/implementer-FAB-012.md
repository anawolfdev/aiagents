# implementer · FAB-012

- **Fecha:** 2026-10-25
- **Veredicto:** ok

Entregable: docs/design/12-bloqueos-emergencias.md (86 líneas). Cinco disparadores con acción, aviso, bloqueo, no-parada y condición de retirada por fila (L27-33). Un registro por causa: dos bloqueos simultáneos se conservan y la retirada afecta a esa causa y solo esa (L11, L35). Excepciones humanas con vencimiento obligatorio, sin renovación automática y efecto al vencer (L50-59). Detección independiente de Telegram contra el intervalo y verificación directa en gate (L39-42). Registro append-only, cambios como eventos nuevos y evidencia conservada (L69-71). Bloqueo de despliegue ≠ parada del agente: nunca se detiene construcción ni pruebas aisladas (L20, L29, L63-65).
