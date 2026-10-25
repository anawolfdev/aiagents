# implementer · CORE-001

- **Fecha:** 2026-10-25
- **Veredicto:** ok

Primera pieza funcional de punta a punta: 'meshharmes status' lee harness/featureslist.json y resume estados + siguiente feature elegible (deps cerradas), sin escribir nada. Nuevo meshharmes/backlog.py (load_features/summarize/read_summary, BacklogError con mensajes concretos) y CLI con subcomando status + --backlog. Sustituye el 'hello' de plantilla en Makefile (run/profile) y README ('## Uso' con salida esperada). Tests: camino feliz contra el backlog real y contra uno temporal con dependencias, sin pendientes, backlog inexistente (exit 1), JSON invalido, sin lista features y error de uso de argparse -> 11 passed en tests/. Real: make check -> 'check pasado: lint + typecheck + test + arnes OK'.
