# implementer · FAB-015

- **Fecha:** 2026-10-25
- **Veredicto:** ok

Entregable: docs/design/15-vigilancia-telegram.md. Workflow con permissions explícitos, contents: read, sin write-all y acciones fijadas por SHA (L23-24). Job separado de frescura que detecta ausencia aunque no corra la vigilancia (L29, L66-75). El bloqueo no depende del aviso y una entrega tardía no elimina bloqueos (L58, L62). Prohibido pedir o desviar secretos por canal público (L52, L61). Inventario como instantánea saneada entregada por el propietario, con marca de frescura y sin acceso general (L43-45). Estado DISEÑADO declarado; la vigilancia programada no está activa (L3, L11).
