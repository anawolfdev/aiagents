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
| Repositorio privado | Lectura A1–A5; escritura A1, A2, A3, A4 y A5, cada rol solo su propio entregable | Identidad de informes | Separada de la de publicación |
| Inventario saneado | **Solo lectura** | Identidad de lectura | Sin secretos; con marca de frescura |
| Pruebas públicas | Libre | — | — |
| Pruebas reservadas | Control real de acceso | Identidad de evaluación | No por instrucción |
| Producción | **Sin acceso** para A1–A5 | — | — |
| Chat Telegram | Escritura de avisos | Identidad de avisos | Chat privado verificado |
| Gestor de secretos | Lectura solo en ejecución | Identidad de CI | Nunca al modelo |

## 4. Matriz rol × acción × recurso × dato × aprobación

| Rol | Acción | Recurso | Clase de dato | Aprobación requerida | Justificación | Control |
|---|---|---|---|---|---|---|
| A1 | Preguntar al propietario | Conversación | PRIVADO | — | Necesita el requisito de primera mano | Conversación privada; contexto mínimo |
| A1 | Escribir spec | Repo privado | PRIVADO | — | Es su entregable | Identidad de informes; versión y GATE 1 posterior |
| A2 | Leer inventario | Snapshot saneado | SENSIBLE | Autorización de lectura (GATE 1) | La vigilancia exige el inventario | Solo lectura; snapshot saneado con frescura |
| A2 | Buscar en web | Fuentes públicas | Términos saneados | — | Necesita fuentes públicas | Nunca datos privados; términos saneados |
| A2 | Escribir informe | Repo privado | SENSIBLE | — | Entregable de vigilancia | Identidad de informes; repo privado |
| A2 | Enviar aviso | Telegram privado | SENSIBLE | Verificación de destinatario | El aviso es obligatorio | Chat privado verificado; sin secretos |
| A2 | Modificar agentes | — | — | **PROHIBIDO** | Separar vigilancia de construcción | Sin permiso de escritura en agentes |
| A2 | Pruebas ofensivas en producción | — | — | **PROHIBIDO** | Producción queda fuera del alcance | Sin acceso a producción |
| A3 | Leer specs/informes | Repo privado | PRIVADO/SENSIBLE | — | Consolidar exige ver los hallazgos | Solo el mínimo necesario |
| A3 | Escribir expediente | Repo privado | PRIVADO | — | Entregable de arquitectura | Identidad de informes; repo privado |
| A3 | Preparar GATE 1 | — | — | Presenta; **no** aprueba | Separar consolidar de aprobar | Firma del propietario |
| A4 | Construir | Entorno delimitado | Sintético/autorizado | GATE 1 | Ejecuta el alcance aprobado | Entorno aislado; alcance congelado |
| A4 | Escribir entregable y manifiesto | Repo privado | PRIVADO/SENSIBLE | GATE 1 | Deja evidencia del artefacto | Identidad de informes; sin fusionar |
| A4 | Ejecutar pruebas públicas | Entorno delimitado | Sintético | GATE 1 | Verificar sin datos reales | Entorno aislado |
| A4 | Acceder a pruebas reservadas | — | — | **PROHIBIDO** | Independencia de A5 | Sin credenciales de evaluación |
| A4 | Ampliar permisos | — | — | **PROHIBIDO** (solicitar) | Mínimo privilegio | Solicitud explícita al propietario |
| A4 | Aprobar | — | — | **PROHIBIDO** | Separar construir de aprobar | Sin acción de aprobación |
| A5 | Evaluar | Artefacto congelado | Sintético + reservado | — | Veredicto independiente | Acceso real controlado a pruebas reservadas |
| A5 | Escribir evaluación | Repo privado | SENSIBLE | — | Entregable de evaluación | Identidad de informes; repo privado |
| A5 | Construir/corregir | — | — | **PROHIBIDO** | Independencia del evaluador | Sin escritura en el artefacto |
| Coordinador | Presentar preguntas | Conversación | PRIVADO | — | Interlocutor único con el propietario | Solo preguntas preparadas por A1 |
| Coordinador | Transcribir aprobaciones | Registro | PRIVADO | La decide el propietario | Registro fiel de la decisión | Transcripción literal; no interpreta |
| Coordinador | Aprobar | — | — | **PROHIBIDO** | No sustituye al usuario | Sin acción de aprobación |
| Publicación | Abrir PR | Repo público | PÚBLICO | Checklist + revisor humano | Única vía de escritura pública | Identidad de publicación; no fusiona ni lee el repo privado |

### Casos obligatorios verificados
| Caso | Cumple |
|---|---|
| A2 no modifica agentes | Sí (§4, PROHIBIDO) |
| A4 no aprueba | Sí (§4, fila «A4 / Aprobar / PROHIBIDO») |
| A5 no construye | Sí (§4, PROHIBIDO) |
| Ningún rol acumula publicar y aprobar | Sí: identidad de publicación ≠ propietario; §5 |
| El coordinador no sustituye al usuario | Sí (§4, solo transcribe) |
| Los datos privados no van a buscadores | Sí (§2 y §6.2: `PRIVADO`/`SENSIBLE` no salen a un PR público sin aprobación de versión y reclasificación) |

## 5. Separación de identidades

Seis identidades **distintas**, con permisos no intercambiables (son las seis que aparecen en §3):

| Identidad | Puede | No puede |
|---|---|---|
| **Lectura** | Leer inventario saneado y repositorio privado | Escribir, publicar |
| **Informes** | Escribir spec, expediente, informes y evaluación en repositorio privado | Publicar, leer secretos |
| **Publicación** | Abrir PR en repositorio público | Leer repositorio privado, fusionar |
| **Evaluación** | Acceso real controlado a pruebas reservadas | Construir o corregir el artefacto |
| **Avisos** | Escribir avisos en el chat Telegram privado verificado | Publicar, leer repositorio privado |
| **CI** | Leer secretos solo en tiempo de ejecución | Exponer secretos al modelo, publicar |

## 6. Flujo de PR seguro

1. Rama en el repositorio público (una **rama pública también constituye publicación**).
2. Solo contenido `PÚBLICO`. Un contenido `PRIVADO`/`SENSIBLE` permanece en el repositorio privado; solo puede entrar en un PR público si esa **versión concreta** tiene aprobación de publicación y se **reclasifica explícitamente a `PÚBLICO`** para esa versión. Sin ambas cosas, no se abre el PR.
3. PR con **checklist de publicación** (ver §7).
4. **Nunca auto-merge**; la fusión es decisión humana.
5. No incluir contenido privado aún no aprobado.
6. No publicar detalles que faciliten explotar fallos sin corregir.

## 7. Checklist de publicación (obligatorio en cada PR)

- [ ] Clase de dato de cada fichero declarada.
- [ ] Si hay `PRIVADO`/`SENSIBLE`: no entra hasta aprobación de esa versión y reclasificación explícita a `PÚBLICO`.
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
