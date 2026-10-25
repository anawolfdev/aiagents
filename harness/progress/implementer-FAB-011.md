# implementer · FAB-011

- **Fecha:** 2026-10-25
- **Veredicto:** ok

Entregable: docs/design/11-estados-cobertura-recuperacion.md (110 líneas). Siete estados y grafo de transiciones con EN CURSO, INTERRUMPIDA RECUPERABLE y salida de AUSENTE (L11-38). Manifiesto finito y versionado MAN-<n> v<k>, con campos obligatorios cerrados y nueva versión ante cambio de alcance (L44-60). Recuperación desde el primer checkpoint no completado sin repetir trabajo válido (L74). Regla avance = checkpoint.hecho AND informe.persistido, con escritura atómica (L77-83). Parcial o fallida bloquea nuevos despliegues del agente afectado y retira solo esa causa (L41, L97-100). Cuatro fechas distintas: publicación, actualización, consulta y verificación sustantiva (L89-90).
