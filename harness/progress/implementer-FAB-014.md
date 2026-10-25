# implementer · FAB-014

- **Fecha:** 2026-10-25
- **Veredicto:** ok

Entregable: docs/design/14-publicacion-proveedores.md. Clases de repositorio (público/privado/ninguno-para-secretos, L11-15) y clase de dato por fichero (L27). Checklist de publicación de ocho puntos obligatorios por PR (L26-34). Prohibición explícita de fusión automática (L24). Proveedores externos sujetos a autorización previa; privado/sensible solo con proveedor autorizado y parámetro declarado PENDIENTE (L48, L51). Secretos nunca en repositorio ni enviados al proveedor (L15, L28, L50). Separación procesar ≠ publicar ≠ búsqueda externa con autorizaciones independientes (L38-44).
