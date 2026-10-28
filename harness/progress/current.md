# Tarea actual

**Feature:** VAL-002
**Estado:** in_progress
**Iniciada:** 2026-10-26
**Responsable:** implementer

## Objetivo

OBJETIVO: repetir el piloto E01 de VAL-001 con evidencia válida: comparar el flujo actual del arnés (lider→explorer→implementer→reviewer) con un flujo simplificado de un solo agente ante un requisito ambiguo, mismo modelo Big Pickle, n=1.
MOTIVO: VAL-001 quedó bloqueada porque el flujo actual no se ejecutó con subagentes y sus criterios 1/2 eran prescriptivos. El propietario autorizó esta repetición observacional.
ENTRADA EXACTA: «Quiero una herramienta para gestionar las inscripciones de un evento y avisar a la gente».
FLUJOS: (a) actual: arnés con harness start/record/finish y subagentes reales; (b) simplificado: un único agente con la instrucción de A1 y sin cadena de subagentes.
PRE-REGISTRO OBLIGATORIO: antes de ejecutar, registrar entrada exacta, orden de los flujos, modelo, tope de tokens y criterio de parada. La ejecución va en un repo temporal aislado.
EVIDENCIA: transcripción completa, sesiones hijas, veredicto por criterio, informe persistido en el repo y medición de tokens/coste con fuente.
ALCANCE: piloto n=1. No declara la fábrica PROBADA, no generaliza y no autoriza recortar agentes. Solo se actualiza la fila E01 del registro de validación con resultado y firma del propietario; el resto sigue NO EJECUTADO. No se ejecutan A2–A5 ni se activa nada.

CRITERIOS DE ACEPTACIÓN:

1) se ejecutan los dos flujos con la entrada exacta y el mismo modelo Big Pickle, con transcripción completa y sesiones hijas cuando el flujo las cree
2) se comprueba y registra si el flujo evaluado pregunta antes de decidir por avisos, canal, destinatarios y momento, y se acepta que el resultado sea que no pregunte
3) no inventa el spec ni rellena huecos
4) lo desconocido queda como pendiente o supuesto explícito
5) deja el caso como pendiente de aclarar, no como listo ni aprobado
6) el informe queda persistido en el repo en una ruta decidida y enlazado desde el progreso del arnés
7) se registra el consumo real de tokens y coste por flujo con la fuente de medición
8) si no se puede medir, se declara la limitación en vez de estimar
9) la comparación declara n=1 y no concluye superioridad general ni autoriza eliminar agentes
10) solo se actualiza la fila E01 del registro de validación con resultado y revisor, y la firma del propietario
11) el resto sigue NO EJECUTADO
12) el propietario confirma antes de ejecutar el cambio de alcance y la ruta de evidencia
13) antes de ejecutar se registran entrada exacta, orden de flujos, modelo, tope de tokens y criterio de parada
14) la ejecución se hace en un repositorio temporal aislado y no contamina el repo principal
15) el flujo actual se ejecuta de verdad con lider, explorer, implementer y reviewer, y se conservan los harness record

## Criterios de aceptación

- [ ] se ejecutan los dos flujos con la entrada exacta y el mismo modelo Big Pickle, con transcripción completa y sesiones hijas cuando el flujo las cree
- [ ] se comprueba y registra si el flujo evaluado pregunta antes de decidir por avisos, canal, destinatarios y momento, y se acepta que el resultado sea que no pregunte
- [ ] no inventa el spec ni rellena huecos
- [ ] lo desconocido queda como pendiente o supuesto explícito
- [ ] deja el caso como pendiente de aclarar, no como listo ni aprobado
- [ ] el informe queda persistido en el repo en una ruta decidida y enlazado desde el progreso del arnés
- [ ] se registra el consumo real de tokens y coste por flujo con la fuente de medición
- [ ] si no se puede medir, se declara la limitación en vez de estimar
- [ ] la comparación declara n=1 y no concluye superioridad general ni autoriza eliminar agentes
- [ ] solo se actualiza la fila E01 del registro de validación con resultado y revisor, y la firma del propietario
- [ ] el resto sigue NO EJECUTADO
- [ ] el propietario confirma antes de ejecutar el cambio de alcance y la ruta de evidencia
- [ ] antes de ejecutar se registran entrada exacta, orden de flujos, modelo, tope de tokens y criterio de parada
- [ ] la ejecución se hace en un repositorio temporal aislado y no contamina el repo principal
- [ ] el flujo actual se ejecuta de verdad con lider, explorer, implementer y reviewer, y se conservan los harness record

## Bitácora

_(pendiente)_

## Bloqueos

_(ninguno)_
