# FAB-014: Publicación, proveedores de modelos y flujo de PR seguro

**Versión:** 1.0 · **Estado:** DISEÑADO  
**Ámbito:** Sección 12  
**Dueño:** A3 consolida · propietario aprueba · identidad de publicación ejecuta

---

## 1. Repositorios

| Repositorio | Contenido | Acceso |
|---|---|---|
| **Público** | Perfiles, código, plantillas y contenido autorizado | Lectura pública; escritura solo vía PR |
| **Privado** (separado) | Specs no publicados, inventarios, informes sensibles | Solo identidad autorizada |
| **Ninguno** | Secretos | Gestor de secretos del entorno |

- Los **specs reales** se publican **solo** tras revisión y **aprobación específica de su versión**.
- Una **rama pública también constituye publicación**.

## 2. Flujo de PR

Autorizado: **abrir PR y registrar hallazgos saneados sin aprobación individual**, dentro del alcance previamente autorizado.

Prohibido: **fusión automática**. Nunca se auto-fusiona.

### Checklist obligatorio de cada PR
- [ ] Clase de dato declarada por fichero (PÚBLICO / PRIVADO / SENSIBLE).
- [ ] Ningún `SECRETO`.
- [ ] Ninguna parte de un spec real sin aprobación de esa versión.
- [ ] Saneamiento aplicado — y se reconoce que **el saneamiento no sustituye la aprobación**.
- [ ] Sin detalles que faciliten explotar fallos **no corregidos**.
- [ ] Sin nombres internos, rutas, identificadores personales ni tokens.
- [ ] Destino correcto (público vs privado).
- [ ] Revisor humano asignado.

## 3. Distinciones que no se confunden

| Concepto | Significado |
|---|---|
| **Procesar** | Enviar material privado a un proveedor de modelos **autorizado**, con datos mínimos y sin secretos |
| **Publicar** | Hacer visible el contenido en un repositorio público o rama pública |
| **Buscar externamente** | Enviar términos a un buscador público (solo términos saneados) |

**Autorización para procesar ≠ autorización para publicar ≠ autorización para consultar en buscadores.**

## 4. Proveedores de modelos

- Material `PRIVADO`/`SENSIBLE` **solo** con proveedores **previamente autorizados**.
- Datos **mínimos**: lo necesario para la tarea, nada más.
- **Sin secretos**, en ningún caso.
- El proveedor/modelo autorizado es un parámetro **PENDIENTE**: sin él, no se procesa material privado.
- Si un componente no puede fijarse (modelo servido por API), se declara la limitación y la condición de reevaluación (FAB-013 §5).

## 5. Saneamiento

- El saneamiento reduce la exposición, **no** concede permiso.
- Qué se sanea: nombres internos, rutas, identificadores, versiones exactas de componentes sensibles, detalles explotables.
- Qué **no** se publica nunca: secretos, inventarios sin sanear, informes con detalles explotables de fallos abiertos.
- Un spec real saneado **sigue** necesitando la aprobación de publicación de su versión.

## 6. Retención

- **PENDIENTE de aprobación** antes de activar.
- **No** se elimina automáticamente evidencia de casos abiertos.
- La retención aplica igual a repositorio público, privado y colas de avisos.

## 7. Verificación FAB-014
- [x] Clases de repositorio y de dato separadas
- [x] El PR tiene checklist de publicación
- [x] No hay auto-merge
- [x] Los proveedores están sujetos a autorización previa
- [x] Los secretos quedan fuera
- [x] Se distingue procesamiento, publicación y búsqueda externa
