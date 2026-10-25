# Estado del arte — MeshHarmes

> Qué se ha publicado ya sobre el problema de este proyecto y qué se toma y qué
> se descarta de cada fuente. Fecha de la búsqueda: 2026-10-25.
>
> Método: `research find_papers` (OpenAlex/arXiv) sobre el objetivo de
> `vault/01_PROYECTO/objetivo.md`; las fuentes abiertas se indexaron con
> `rag index_urls` para poder consultarlas después sin volver a la web.

## Fuentes

### 1. Shadows in the Code: Risks and Defenses of LLM-based Multi-Agent Software Development — Wang et al., AAAI 2026 (arXiv:2511.18467)

Identifica dos escenarios de riesgo (usuario malicioso con agentes benignos y
usuario benigno con agentes comprometidos) y demuestra que los agentes de
código y de pruebas son los más peligrosos cuando se comprometen.

- **Se toma:** la separación entre dato externo e instrucción, el mínimo
  privilegio por rol y la prioridad de proteger las fases de código y test.
  Es la base de `agents/policy_guard.py` y de la puerta de permisos.
- **Se descarta:** implementar su defensa adversarial (Adv-IMBIA). No es un
  sandbox y aquí no hay modelo propio que atacar; añadirla sería teatro.

### 2. Optimizing LLM-Based Multi-Agent System with Textual Feedback — Shen et al., 2025 (arXiv:2505.16086)

Optimiza prompts de sistemas multiagente en dos pasos: detectar el agente que
rinde peor a partir de explicaciones de fallo y reescribir su prompt; compara
optimización individual contra grupal y online contra offline.

- **Se toma:** registrar el fallo con su explicación y usarlo para mejorar el
  prompt, midiendo antes y después. El histórico del arnés y `agents/evals/`
  existen para eso.
- **Se descarta:** la mutación automática de prompts en caliente. Sin un
  conjunto de evaluación estable y presupuesto aprobado, optimizar prompts es
  ruido; la reescritura la propone una persona y la valida la puerta.

### 3. Agentless: Demystifying LLM-based Software Engineering Agents — Xia et al., 2024 (arXiv:2407.01489)

Un proceso simple de tres fases (localizar, reparar, validar el parche) supera
en SWE-bench Lite a agentes autónomos más complejos y cuesta menos.

- **Se toma:** la carga de la prueba cae sobre la complejidad. Un pipeline
  interpretable es el punto de partida, y un agente solo se añade cuando una
  necesidad aprobada lo exige (principio de proporcionalidad del diseño).
- **Se descarta:** su pipeline específico de SWE-bench y sus cifras. Nuestro
  problema no es reparar issues ajenos, sino mantener un arnés propio honesto.

### 4. Do Multi-agent Systems Make Better Software? — Mitrović et al., 2026 (DOI 10.1007/978-3-032-39395-1_23)

Evaluación empírica de frameworks multiagente de desarrollo frente a
alternativas más simples, con la pregunta de si el multiagente mejora el
resultado.

- **Se toma:** la pregunta como criterio de diseño. Cada feature declara su
  criterio de aceptación verificable y no se asume que más agentes es mejor.
- **Se descarta:** trasladar sus conclusiones de benchmark sin replicarlas. El
  texto completo no está en abierto y no se ha reproducido aquí.

### 5. A Validation and Governance Framework for Multi-Agent LLM Scientific Software Development — Bass, 2026 (DOI 10.1145/3816713.3818807)

Propone un marco de validación y gobierno para software científico construido
por agentes: gates, evidencia y responsabilidad explícita.

- **Se toma:** el gobierno como código, no como prompt. `harness finish` no
  cierra una feature sin puerta en verde y evidencia real; el propietario
  autoriza lo irreversible.
- **Se descarta:** el aparato documental orientado a software científico y a
  equipos. Aquí hay un propietario único y el coste de cumplir debe ser menor
  que el riesgo que evita.

### 6. LLM-Based MaSE: A Software Development Framework for Developing Multi-agent Systems — 2025 (DOI 10.1007/978-981-96-8889-0_37)

Framework que aplica LLMs al ciclo de vida de desarrollo de sistemas
multiagente.

- **Se toma:** el ciclo spec → diseño → construcción → evaluación con entregas
  trazables, que es la estructura de `docs/design/` y del backlog.
- **Se descarta:** su notación y sus artefactos de proceso. El arnés ya tiene
  un formato mínimo (backlog + progreso + evidencia) y añadir otro sería
  duplicar la fuente de verdad.

### 7. Multi-Agent LLM Workflow for Regulatory-Driven Requirement Generation — Abdalla et al., 2026 (DOI 10.4271/2026-01-0787)

Workflow multiagente que extrae requisitos de especificaciones y normativa y
hace que los agentes validen sus salidas entre sí.

- **Se toma:** la validación cruzada y la trazabilidad de cada requisito a su
  fuente. Se refleja en los criterios de aceptación y en la evidencia por
  criterio.
- **Se descarta:** el dominio automoción/Euro 7 y la revisión por expertos
  sectoriales, que no existen en este proyecto.

## Capacidades sin agente: qué se acepta y qué no

`bootstrap suggest_agents` devuelve 21 términos del objetivo que ningún
contrato cubre **literalmente**. El cruce es léxico, no semántico: la mayoría
ya tiene dueño. Revisados uno a uno:

| Términos | Dueño real | Decisión |
|---|---|---|
| especificar, diseñar, diseño, alcance, entregable | `plan` (orden de trabajo), `documentation`, `docs/design/` | Cubierto |
| construir, ejecutar, fábrica, paquete | `installer scaffold`, `harness` (puerta), `git`/`documentation` | Cubierto |
| pruebas, evaluar | `test`, `review`, `rag evaluate`, `agents.evals.runner` | Cubierto |
| aislado | `env`, `docker`, worktrees de git | Cubierto |
| activar, desplegar, publicar | `cicd` valida workflows, `git publish` publica con autorización; el resto es aprobación humana (GATE 2) | Cubierto por diseño: lo irreversible no lo decide un agente |
| propietario, personal, único, queda, fuera, permita | No son capacidades: adjetivos, preposiciones y verbos del texto | No aplica |

**Huecos aceptados: ninguno.** Crear un agente para un término que ya tiene
dueño viola la proporcionalidad del diseño (`00-alcance-decisiones.md`) y la
regla de no añadir funcionalidad no pedida. Se vuelve a ejecutar
`suggest_agents` cuando cambie el objetivo; un hueco solo se acepta si nombra
una acción repetible, con evidencia que la pruebe, y sin dueño actual.
