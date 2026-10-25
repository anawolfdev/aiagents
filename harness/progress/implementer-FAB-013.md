# implementer · FAB-013

- **Fecha:** 2026-10-25
- **Veredicto:** ok

Entregable: docs/design/13-presupuesto-gates.md (110 líneas). GATE 1 (spec/permisos/presupuesto) y GATE 2 (artefacto+destino) con quién aprueba y contenido obligatorio (L42-56, L58-70). Manifiesto identifica spec, prompt, configuración, código, dependencias, adaptadores y modelo con versión/hash o limitación declarada (L75-86). Límite de 3 rondas ejecutable (1 inicial + 2 correcciones), aplicado al ciclo completo, sin reinicio por cambios triviales y sin aceptar al agotar (L27-40). Sin presupuesto aprobado: estimación y aprobación antes de activar coste (L11-13, L50). Cambio material invalida la aprobación afectada y puede exigir GATE 1 (L90-94). La aprobación no se hereda a otro artefacto, versión ni destino (L96).
