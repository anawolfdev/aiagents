# Objetivo — MeshHarmes

## Problema

Una sola persona que quiere construir agentes de IA para su propio equipo no
tiene dónde apoyarse: el trabajo acaba en prompts sueltos, sin especificación,
sin criterios de aceptación, sin evidencia y sin una puerta que decida qué
puede hacer cada agente. El resultado es que no se sabe cuándo un agente está
terminado, ni qué se le permite tocar, ni por qué se eligió un diseño y no
otro. Este repositorio resuelve eso: escribe primero el diseño de una fábrica
personal de agentes y lo acompaña de un arnés que convierte esas reglas en
código ejecutable.

## Usuario / consumidor

- **Propietario único** (la persona que encarga y aprueba): consume el paquete
  de diseño de `docs/design/` para decidir qué se construye y qué no.
- **El asistente de IA** que trabaja en el repositorio: consume el arnés
  (`init.sh`, `harness/featureslist.json`, `harness/progress/`) para saber qué
  toca hacer y con qué evidencia se cierra.
- **Los agentes Python** del arnés: consumen `agents/contracts.py` y la puerta
  de permisos para saber qué pueden hacer sin autorización humana.

## Criterio de hecho

El proyecto está hecho cuando estas cuatro comprobaciones se pueden ejecutar y
salen como se describe:

1. `./init.sh` termina con `ENTORNO LISTO — se puede trabajar.`
2. `uv run python -m agents --json run harness status` devuelve
   `0 pending · 0 blocked` en `data.counts`.
3. `docs/design/README.md` indexa los nueve entregables y su matriz de
   trazabilidad cubre los tickets `FAB-001`…`FAB-019`.
4. `git ls-files docs/design vault/01_PROYECTO` lista el paquete de diseño y
   los documentos de objetivo y arquitectura.

El estado que se declara es **DISEÑADO**. No es `PROBADO` ni `DESPLEGADO`: la
fábrica no se ha ejecutado.

## Fuera de alcance

- **Ejecutar la fábrica**: no se instalan agentes reales, no se activan
  workflows y no se despliega nada. El entregable es el diseño.
- **Publicar o desplegar**: nada de repositorios públicos, credenciales,
  proveedores de modelos ni PRs automáticos.
- **Plataforma multiusuario**: no hay cuentas, permisos por inquilino,
  marketplace ni SaaS; el propietario es único.
- **Entrenar modelos o añadir memoria/RAG por defecto**: solo si una necesidad
  aprobada lo exige, y entonces se diseña, no se improvisa.
- **Sustituir la aprobación humana**: gasto, publicación, despliegue, borrado
  y ampliación de permisos siguen necesitando autorización explícita.
