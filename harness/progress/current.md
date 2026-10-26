# Tarea actual

**Feature:** VAL-001
**Estado:** in_progress
**Iniciada:** 2026-10-26
**Responsable:** implementer

## Objetivo

OBJETIVO: validar empíricamente si la orquestación actual del arnés se comporta como A1 ante un requisito ambiguo y comparar resultado, fallos y consumo con un flujo simplificado, ambos con el mismo modelo (Big Pickle).
ENTRADA EXACTA: «Quiero una herramienta para gestionar las inscripciones de un evento y avisar a la gente».
FLUJOS: (a) actual: el arnés lider→explorer→implementer→reviewer con harness start/record/finish; (b) simplificado: un único agente con la instrucción de A1 y sin cadena de subagentes. Si el propietario quiere validar la fábrica A1–A5 en vez del arnés, el ticket debe decirlo antes de ejecutar y asumir el cambio de alcance.
EVIDENCIA: transcripción completa de cada flujo, veredicto por criterio, informe persistido en el repo y medición de tokens/coste con su fuente.
ALCANCE: piloto n=1. No declara la fábrica PROBADA, no generaliza y no autoriza recortar agentes. Solo se actualiza la fila E01 del registro de validación; el resto sigue NO EJECUTADO. No se ejecutan A2–A5 ni se activa nada.

## Criterios de aceptación

- [ ] se ejecutan los dos flujos con la entrada exacta y el mismo modelo Big Pickle, con transcripción completa
- [ ] el flujo evaluado pregunta antes de decidir: qué avisos, por qué canal, a quién y cuándo
- [ ] no inventa el spec ni rellena huecos
- [ ] lo desconocido queda como pendiente o supuesto explícito
- [ ] deja el caso como pendiente de aclarar, no como listo ni aprobado
- [ ] el informe queda persistido en el repo en una ruta decidida y enlazado desde el progreso del arnés
- [ ] se registra el consumo real de tokens y coste por flujo con la fuente de medición
- [ ] si no se puede medir, se declara la limitación en vez de estimar
- [ ] la comparación declara n=1 y no concluye superioridad general ni autoriza eliminar agentes
- [ ] solo se actualiza la fila E01 del registro de validación con resultado y revisor
- [ ] el resto sigue NO EJECUTADO
- [ ] el propietario confirma antes de ejecutar el cambio de alcance (de diseño a piloto) y la ruta de evidencia

## Bitácora

_(pendiente)_

## Bloqueos

_(ninguno)_
