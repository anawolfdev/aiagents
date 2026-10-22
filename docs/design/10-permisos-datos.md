# FAB-010: Matriz de permisos, separación de datos y secretos

**Versión:** 1.0 · **Estado:** DISEÑADO  
**Ámbito:** Secciones 12, 13 y 14  
**Dueño único:** A3 (consolida); el propietario aprueba

---

## 1. Principio

**Mínimo privilegio**: cada rol recibe solo el permiso que su misión exige, para el recurso concreto, durante el tiempo necesario, con el control declarado.

## 2. Clases de dato

| Clase | Ejemplos | Repositorio | Proveedor externo | Buscador público |
|---|---|---|---|---|
| `PÚBLICO` | plantillas, perfiles, código autorizado | Público | Permitido | Permitido |
| `PRIVADO` | specs no publicados, expedientes | Privado | Solo proveedor autorizado | **PROHIBIDO** |
| `SENSIBLE` | inventarios, informes de vulnerabilidades, hallazgos | Privado | Solo proveedor autorizado, datos mínimos | **PROHIBIDO** |
| `SECRETO` | tokens, claves, credenciales | **NINGUNO** | Nunca al modelo | **PROHIBIDO** |

**Regla dura:** los secretos **no** están en el repositorio público **ni** en el privado. Viven en el gestor de secretos del entorno de ejecución.

## 3. Recursos y accesos

| Recurso | Acceso | Identidad | Notas |
|---|---|---|---|
| Repositorio público | Lectura A1–A5; escritura solo vía PR | Identidad de publicación | — |
| Repositorio privado | Lectura A1, A2, A3, A5; escritura A2/A3/A4 | Identidad de informes | Separada de la de publicación |
| Inventario saneado | **Solo lectura** | Identidad de lectura | Sin secretos; con marca de frescura |
| Pruebas públicas | Libre | — | — |
| Pruebas reservadas | Control real de acceso | Identidad de evaluación | No por instrucción |
| Producción | **Sin acceso** para A1–A5 | — | — |
| Chat Telegram | Escritura de avisos | Identidad de avisos | Chat privado verificado |
| Gestor de secretos | Lectura solo en ejecución | Identidad de CI | Nunca al modelo |

## 4. Matriz rol × acción × recurso × dato × aprobación

| Rol | Acción | Recurso | Clase de dato | Aprobación requerida |
|---|---|---|---|---|
| A1 | Preguntar al propietario | Conversación | PRIVADO | — |
| A1 | Escribir spec | Repo privado | PRIVADO | — |
| A2 | Leer inventario | Snapshot saneado | SENSIBLE | Autorización de lectura (GATE 1) |
| A2 | Buscar en web | Fuentes públicas | Términos saneados | — |
| A2 | Escribir informe | Repo privado | SENSIBLE | — |
| A2 | Enviar aviso | Telegram privado | SENSIBLE | Verificación de destinatario |
| A2 | Modificar agentes | — | — | **PROHIBIDO** |
| A2 | Pruebas ofensivas en producción | — | — | **PROHIBIDO** |
| A3 | Leer specs/informes | Repo privado | PRIVADO/SENSIBLE | — |
| A3 | Escribir expediente | Repo privado | PRIVADO | — |
| A3 | Preparar GATE 1 | — | — | Presenta; **no** aprueba |
| A4 | Construir | Entorno delimitado | Sintético/autorizado | GATE 1 |
| A4 | Ejecutar pruebas públicas | Entorno delimitado | Sintético | GATE 1 |
| A4 | Acceder a pruebas reservadas | — | — | **PROHIBIDO** |
| A4 | Ampliar permisos | — | — | **PROHIBIDO** (solicitar) |
| A5 | Evaluar | Artefacto congelado | Sintético + reservado | — |
| A5 | Escribir evaluación | Repo privado | SENSIBLE | — |
| A5 | Construir/corregir | — | — | **PROHIBIDO** |
| Coordinador | Presentar preguntas | Conversación | PRIVADO | — |
| Coordinador | Transcribir aprobaciones | Registro | PRIVADO | La decide el propietario |
| Coordinador | Aprobar | — | — | **PROHIBIDO** |

### Casos obligatorios verificados
| Caso | Cumple |
|---|---|
| A2 no modifica agentes | Sí (§4, PROHIBIDO) |
| A4 no aprueba | Sí (no tiene acción de aprobación) |
| A5 no construye | Sí (PROHIBIDO) |
| Ningún rol acumula publicar y aprobar | Sí: identidad de publicación ≠ propietario |
| El coordinador no sustituye al usuario | Sí (solo transcribe) |
| Los datos privados no van a buscadores | Sí (clase PRIVADO/SENSIBLE bloqueada) |

## 5. Separación de identidades

Tres identidades **distintas**, con permisos no intercambiables:

| Identidad | Puede | No puede |
|---|---|---|
| **Lectura** | Leer inventario y repositorio privado | Escribir, publicar |
| **Informes** | Escribir informes en repositorio privado | Publicar, leer secretos |
| **Publicación** | Abrir PR en repositorio público | Leer repositorio privado, fusionar |

## 6. Flujo de PR seguro

1. Rama en el repositorio público (una **rama pública también constituye publicación**).
2. Solo contenido `PÚBLICO` o `PRIVADO` con aprobación específica de esa versión.
3. PR con **checklist de publicación** (ver §7).
4. **Nunca auto-merge**; la fusión es decisión humana.
5. No incluir contenido privado aún no aprobado.
6. No publicar detalles que faciliten explotar fallos sin corregir.

## 7. Checklist de publicación (obligatorio en cada PR)

- [ ] Clase de dato de cada fichero declarada.
- [ ] Ningún `SECRETO`.
- [ ] Specs reales: solo si esa **versión** tiene aprobación de publicación específica.
- [ ] Saneamiento aplicado (el saneamiento **no sustituye** la aprobación).
- [ ] Sin detalles explotables de fallos no corregidos.
- [ ] Sin nombres internos, rutas ni identificadores del propietario.
- [ ] Destino de publicación correcto (público vs privado).

## 8. Proveedores de modelos

- Material `PRIVADO`/`SENSIBLE` solo con proveedores **previamente autorizados**.
- Datos **mínimos** y **sin secretos**.
- **Autorización para procesar ≠ autorización para publicar ≠ autorización para consultar en buscadores.**
- Los proveedores autorizados quedan como parámetro **PENDIENTE** (§9).

## 9. Parámetros pendientes
| Parámetro | Estado |
|---|---|
| Repositorio público concreto | PENDIENTE |
| Repositorio privado concreto | PENDIENTE |
| Proveedor/modelo autorizado | PENDIENTE |
| Destinatario Telegram verificado | PENDIENTE |
| Política de retención | **PENDIENTE — se aprueba antes de activar** |
| Almacenamiento | PENDIENTE |
| Mecanismo independiente de supervisión | PENDIENTE |

## 10. Verificación FAB-010
- [x] Cada permiso tiene justificación y control
- [x] Clases de dato definidas
- [x] Secretos en ningún repositorio
- [x] PR seguro, sin auto-fusión
- [x] Retención pendiente de aprobación
- [x] Se distingue procesar de publicar
