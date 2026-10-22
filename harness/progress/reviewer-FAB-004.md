verdict: ok
evidence:
  - FAB-004 A2-riesgos-vigilancia.md: autosuficiente (secciones 1-15). Obligatorios presentes.
  - Específico A2: modos inicial (3) y periódico (4) separados y completos. Cobertura independiente del spec (5: términos saneados + inventario + transitivas + categorías independientes). Regla 7 días (4.6, 7). Fuentes inaccesibles/caducadas/contradictorias tratadas (7, bloqueos BLQ-A2-01/02/03). Prompt injection (7.8-7.10, 10.6, BLQ-A2-05). Vigilancia diaria marcada como pendiente de activación (4, 11.7, BLQ-A2-07). Pruebas mínimas cubiertas.
  - Gate: ./init.sh pasado (ENTORNO LISTO, pytest 612 passed, 15 skipped)
