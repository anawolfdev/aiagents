# Arquitectura — MeshHarmes

> Diseño y arnés de una fábrica personal de agentes de IA. El diseño vive en
> `docs/design/`; el arnés que lo mantiene honesto vive en `agents/`,
> `harness/` e `init.sh`; la pieza ejecutable es el paquete `meshharmes/`.
>
> Estado: **DISEÑADO**. Nada PROBADO ni DESPLEGADO: la fábrica no se ejecuta.

## Stack

- **Lenguaje:** Python 3.12+ (el `.venv` de referencia es 3.12)
- **Entorno y dependencias:** uv (`uv.lock`)
- **Calidad:** ruff, mypy, pytest, bandit, pip-audit; CI con `make check`
- **Conocimiento:** vault Obsidian + graphify + RAG local opcional (chromadb)
- **Persistencia del trabajo:** ficheros versionados (`harness/`), no una base
  de datos

## Piezas y flujo

```
propietario
    │  encarga y aprueba (GATE 1 / GATE 2, gasto, publicación)
    ▼
docs/design/  ──────────────►  contrato de la fábrica (A1–A5 + coordinador)
    │                          estado: DISEÑADO, sin ejecutar
    │  se convierte en trabajo
    ▼
harness/featureslist.json ──►  harness (Python)  ──►  harness/progress/
    │  qué toca, con criterios      único que escribe        memoria fuera de
    │  de aceptación               backlog y progreso        la ventana
    ▼
agentes del asistente (razonan) ──► agents/ (Python, stdlib) ──► acciones
    explorer · implementer · reviewer      contratos + puerta de permisos
    │
    ▼
init.sh  ──►  ENTORNO LISTO / ENTORNO BLOQUEADO  ──►  cierre de feature
    │                                                   (solo con evidencia)
    ▼
meshharmes/ (CLI)  ·  tests/  ·  .github/workflows/ci.yml
```

Reglas del flujo que no se pueden saltar:

- **Un dueño por recurso.** El backlog y el progreso los escribe `harness`;
  el código de producto, el `implementer`; el veredicto, el `reviewer`.
- **La puerta es código, no una instrucción.** `harness finish` ejecuta
  `./init.sh` y devuelve `success=false` si está en rojo o falta evidencia.
- **El rumbo va primero.** `SCOPE-001` (objetivo) y `DESIGN-001`
  (arquitectura) preceden a cualquier feature: sin ellos no hay contra qué
  decidir.
- **Dos fronteras de seguridad.** Agentes Python: `run()` → puerta de
  permisos (siempre activa). Asistente: herramienta → `agents/policy_guard.py`
  (opcional, sin cablear a propósito). Ninguna es un sandbox.

## Estructura del repositorio

```
meshharmes/            — La CLI del arnés (`python -m meshharmes`)
tests/                 — Tests de la CLI

agents/                — Sistema multi-agente del arnés (stdlib pura)
├── contracts.py       — Contratos de rol: can / cannot / needs / owns
├── agents/            — Un módulo por agente
├── tools/             — Herramientas compartidas
├── prompts/           — Skills cargables por el asistente
├── evals/             — Ruteo, contratos y RAG, medidos
└── workspace/         — Lo que generan los agentes (git-ignored)

harness/               — Backlog, progreso e histórico (memoria del arnés)
vault/                 — Conocimiento estable (Obsidian): objetivo, arquitectura
docs/design/           — El paquete de diseño de la fábrica (9 entregables)
docs/                  — Sphinx
```

## Alternativas consideradas y descartadas

1. **Un sexto agente "coordinador" autónomo.** Descartada: la coordinación es
   una función del flujo (transportar, registrar, bloquear), no un rol con
   criterio propio. Un agente más añade una identidad que aprobar, permisos
   que revisar y una vía de interlocución paralela; el contrato de
   `02-coordinador.md` cubre lo mismo sin ese coste. Motivo: proporcionalidad.
2. **Orquestador de terceros con estado en base de datos** (LangGraph, CrewAI
   o similar). Descartada: mete una dependencia de proveedor en el núcleo,
   saca el estado del repositorio (deja de ser revisable y diffeable) y deja
   la puerta de permisos fuera de nuestro control. Motivo: portabilidad y
   auditabilidad; el arnés es stdlib pura a propósito.
3. **Layout `src/meshharmes/`.** Descartada: el arnés resuelve el paquete por
   `project_slug` en la raíz y así funciona en un repo recién clonado antes de
   instalar nada. Motivo: simplicidad; el layout plano no compra nada aquí.

## Riesgos conocidos

| Riesgo | Impacto | Mitigación actual |
|---|---|---|
| GEAS remoto inalcanzable | El sync bloquea y `init.sh` se detiene | Modo local documentado; el bloqueo es explícito, sin rodeos |
| Diferencias Windows/Linux (`bash`, CRLF, rutas) | La puerta falla por el entorno, no por el código | `.gitattributes` con LF, bash de Git for Windows, UTF-8 forzado |
| Deriva entre prompts y contratos | El asistente hace lo que el código no permite | `agents.prompts_sync` y `make prompts-check` |
| Índice RAG desfasado | La búsqueda devuelve la respuesta de ayer sin error | `rag status` + `make eval-rag` con `hit_rate`/MRR |
| Variabilidad del modelo | Dos ejecuciones del mismo ticket no son iguales | Criterios verificables y evidencia pegada, no "parece que funciona" |
| La puerta completa tarda ~7 min | Cerrar 18 features cuesta horas | Es el precio de que el cierre signifique algo; `--quick` solo para estructura |
| `policy_guard` no es un sandbox | Un comando creativo lo esquiva | Aislamiento real fuera del repo; la puerta de `run()` sigue activa |

## Decisiones aplazadas

- Retención de datos y almacenamiento (bloqueante para activar; ver
  `18-activacion.md`).
- Proveedor y modelo autorizado, y presupuesto por ejecución.
- Conexión y destinatario de Telegram; horario y zona horaria de la vigilancia.
- Repositorios concretos (público/privado) y despliegue: GATE 2, no esta tarea.
- Embedder definitivo del RAG y política de reconstrucción del índice.
- Mecanismo independiente de supervisión de la ausencia del propietario.
