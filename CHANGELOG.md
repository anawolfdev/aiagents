# Changelog

Todos los cambios relevantes del proyecto se documentan aquí.
Formato basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/).

El dueño de este fichero es el agente `documentation`: `git commit_feature`
añade aquí una entrada por cada feature cerrada del arnés.

---

## [Unreleased] — 2026-10-25

### Añadido

- flujo de estados, cobertura y recuperación (FAB-011)

## [Unreleased] — 2026-10-25

### Añadido

- matriz de permisos, datos y secretos coherente (FAB-010)

## [Unreleased] — 2026-10-25

### Añadido

- plantillas operativas y trazabilidad campo a campo (FAB-009)

## [Unreleased] — 2026-10-25

### Añadido

- contrato del coordinador y límites de interlocución (FAB-008)

## [Unreleased] — 2026-10-25

### Añadido

- Qué se sabe ya y qué agentes hacen falta (ONBOARD-002)

## [Unreleased] — 2026-10-25

### Añadido

- Entender el proyecto (ONBOARD-001)

## [Unreleased] — 2026-10-25

### Añadido

- Primera pieza funcional de punta a punta (CORE-001)

## [Unreleased] — 2026-10-25

### Añadido

- Decidir cómo se va a resolver (DESIGN-001)

## [Unreleased] — 2026-10-25

### Añadido

- Definir qué se quiere resolver (SCOPE-001)

## [Unreleased] — 2026-10-25

### Añadido

- Batería de calidad en verde (QA-001)

## [Unreleased] — 2026-10-22

### Añadido

- docs(design): contrato del coordinador (FAB-008)

## [Unreleased] — 2026-10-22

### Añadido

- docs(design): perfil A5 evaluador independiente (FAB-007)

## [Unreleased] — 2026-10-22

### Añadido

- docs(design): perfil A4 constructor (FAB-006)

## [Unreleased] — 2026-10-22

### Añadido

- docs(design): perfil A3 arquitecto y consolidador (FAB-005)

## [Unreleased] — 2026-10-22

### Añadido

- docs(design): perfil A2 riesgos y vigilancia (FAB-004)

## [Unreleased] — 2026-10-22

### Añadido

- docs(design): perfil A1 analista y entrevistador (FAB-003)

## [Unreleased] — 2026-10-22

### Añadido

- docs(design): matriz de necesidad y proporcionalidad (FAB-002)

## [Unreleased] — 2026-10-22

### Añadido

- docs(design): fijar alcance y registro de decisiones (FAB-001)

## [Unreleased] — 2026-08-04

### Añadido

- protege app.__main__ para que importar el paquete no ejecute la CLI (FIX-001)

## [0.1.0] — 2026-08-04

### Añadido

- Arnés de trabajo: `AGENTS.md`, `init.sh`, `harness/` (backlog + progreso) y
  los cuatro subagentes (`lider`, `explorer`, `implementer`, `reviewer`).
- Sistema de 23 agentes Python en `agents/`, con contratos de rol y puerta de
  permisos (`agents/permissions.py`) para las acciones irreversibles.
- `agents/policy_guard.py` como política para las herramientas del asistente,
  sin cablear a ningún hook: se activa a mano (ver `AGENTS.md`).
- Vault de conocimiento en `vault/`, RAG local opcional y grafo con graphify.
- Paquete de ejemplo `app/` con su CLI y tests, `make check` en verde y CI.
