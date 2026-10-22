# 02 — Contrato del coordinador

| Campo | Valor |
|---|---|
| Documento | Paquete de diseño de la fábrica personal de agentes |
| Entregable | Contrato de coordinación (§2) |
| Ticket | `FAB-008` — `decb9d40-3f37-46d4-bc0b-27ce599c4084` |
| Versión | 1.0 |
| Fecha | 2026-10-22 |
| Estado | **DISEÑADO** |
| Autoridad | Propietario único del sistema |

> La coordinación es una **función del flujo**, no un sexto agente autónomo
> obligatorio. Este documento define qué hace, qué no hace y cómo se demuestra
> cada transición.

## 1. Definición

El coordinador es la función que mantiene el flujo entre el propietario y los
roles A1–A5. Puede implementarse como una persona, un guion determinista o una
instrucción de sistema; no tiene identidad de agente independiente ni capacidad
de decisión sobre el contenido.

## 2. Responsabilidades

1. **Interlocución única.** Es el único canal con el propietario. Presenta las
   preguntas que prepara A1, agrupadas y sin repetir las ya respondidas.
2. **Estado y versión.** Mantiene el estado verificable de cada artefacto:
   `DISEÑADO`, `CONFIGURADO`, `PROBADO`, `DESPLEGADO`, además de los estados de
   revisión de §11.
3. **Responsables.** Garantiza un dueño único por artefacto y registra quién
   entrega, quién revisa y quién aprueba.
4. **Contexto mínimo.** Entrega a cada rol solo los datos, documentos y permisos
   necesarios para su tarea.
5. **Aprobaciones.** Solicita al propietario las aprobaciones de GATE 1, GATE 2,
   gasto, publicación, permisos y excepciones. No las sustituye.
6. **Bloqueos.** Registra cada bloqueo con agente, versión y causa, y lo eleva.
7. **Límites de bucle.** Aplica el máximo de tres rondas y detiene el flujo
   cuando no hay progreso.
8. **Trazabilidad.** Conserva la evidencia de cada transición y la versión a la
   que se refiere.

## 3. Lo que no hace

- No se define como agente autónomo adicional ni como sexto rol.
- No aprueba en nombre del propietario.
- No corrige artefactos ni reescribe el spec.
- No construye, evalúa ni despliega.
- No permite que un rol hable directamente con otro saltándose el flujo.
- No abre bucles libres entre especialistas.
- No inventa parámetros pendientes.
- No convierte una entrega en aprobación.

## 4. Transiciones

Toda transición tiene disparador, responsable, evidencia y estado de destino.

| De | A | Disparador | Responsable | Evidencia |
|---|---|---|---|---|
| Inicio | A1 | Idea del propietario | Coordinador | Idea registrada y versión 0.1 |
| A1 | Revisión del propietario | Spec completo | A1 | Spec, supuestos y preguntas cerradas |
| Revisión | A2 | Spec validado por el propietario | Coordinador | Aprobación humana registrada |
| A2 | A3 | Informe inicial de riesgos | A2 | Hallazgos, fuentes y vigencia |
| A3 | GATE 1 | Arquitectura y plan listos | A3 | Matriz y plan verificable |
| GATE 1 | A4 | Aprobación del propietario | Propietario | Aprobación con versión y alcance |
| A4 | A5 | Artefacto congelado | A4 | Manifiesto, pruebas públicas y reversión |
| A5 | GATE 2 | Veredicto conforme | A5 | Informe de evaluación y límites |
| GATE 2 | Despliegue | Aprobación del propietario | Propietario | Destino, manifiesto y reversión |
| Cualquiera | Bloqueo | Causa identificada | Rol que detecta | Registro de bloqueo |
| Bloqueo | Cualquiera | Causa resuelta y evidencia | Coordinador | Verificación de la causa |

## 5. Entrega obligatoria

Cada entrega incluye:

- agente objetivo;
- versión del artefacto;
- trabajo realizado;
- evidencia real;
- incertidumbres;
- bloqueos;
- siguiente responsable.

Una entrega sin estos campos se devuelve al emisor. No se interpreta como
aprobación.

## 6. Aprobaciones humanas

| Aprobación | Quién | Qué cubre | Caducidad |
|---|---|---|---|
| Spec | Propietario | Versión concreta de A1 | Cambio material |
| GATE 1 | Propietario | Alcance, arquitectura, permisos y presupuesto | Cambio material |
| GATE 2 | Propietario | Un artefacto en un destino concreto | Cambio material o de destino |
| Gasto | Propietario | Estimación y límite | Fin del ciclo o cambio de alcance |
| Publicación | Propietario | Versión concreta y destino | Cambio de versión |
| Excepción | Propietario | Una versión y una causa | Vencimiento explícito |

El coordinador puede preparar la solicitud, pero nunca marcar la aprobación.

## 7. Bucles y rondas

- El ciclo completo tiene una ronda inicial y como máximo dos correcciones.
- El límite no se multiplica por plataforma ni se reinicia por cambios
  triviales.
- Si no hay progreso, se detiene antes de agotar las rondas.
- Agotar las rondas no acepta el artefacto: se bloquea y se eleva.
- Una ampliación de rondas requiere aprobación humana.

## 8. Encaje con A1–A5

| Rol | El coordinador le entrega | El rol le devuelve |
|---|---|---|
| A1 | Idea, respuestas previas y límites | Spec, supuestos y preguntas |
| A2 | Spec saneado, inventario y alcance | Hallazgos, fuentes y vigencia |
| A3 | Spec validado y hallazgos | Arquitectura, matriz, plan y GATE 1 |
| A4 | Alcance aprobado y entorno | Artefacto, manifiesto y pruebas |
| A5 | Artefacto congelado y criterios | Veredicto, cobertura y límites |

El coordinador no duplica las funciones de ningún rol: solo transporta,
registra y bloquea.

## 9. Bloqueos de coordinación

| Código | Causa | Acción |
|---|---|---|
| `BLQ-CO-01` | Falta aprobación humana | Detener la transición |
| `BLQ-CO-02` | Entrega incompleta | Devolver al emisor |
| `BLQ-CO-03` | Dos responsables para un artefacto | Resolver antes de continuar |
| `BLQ-CO-04` | Bucle sin progreso | Bloquear y elevar |
| `BLQ-CO-05` | Rol intenta saltarse el flujo | Rechazar y registrar |
| `BLQ-CO-06` | Versión no identificada | No aceptar la entrega |

## 10. Criterios de cierre

- [x] No se define como agente autónomo adicional.
- [x] Toda transición tiene disparador, responsable y evidencia.
- [x] Ninguna aprobación humana se simula.
- [x] Los bucles tienen límite explícito.
- [x] Ningún rol se salta al coordinador.
- [x] El contrato encaja con A1–A5 y no duplica sus funciones.

## 11. Trazabilidad

- `docs/design/00-alcance-decisiones.md`: C-05, C-06, C-07, C-22.
- `docs/design/02-coordinador.md`: este contrato.
