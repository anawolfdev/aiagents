# Tarea actual

**Feature:** GEAS-001
**Estado:** in_progress
**Iniciada:** 2026-10-22
**Responsable:** implementer

## Objetivo

Petición del usuario: sincronizar antes de trabajar y al reclamar/cerrar tickets, con pull y push. Usar la API HTTP de la instancia GEAS compartida, no acceso directo a SQLite. Las fallas de red, permisos, Git o cierre deben bloquear el avance y conservar estado recuperable.

## Criterios de aceptación

- [ ] init.sh sincroniza Git y GEAS antes de permitir trabajar con configuración remota válida
- [ ] harness sincroniza antes de leer o mutar trabajo operativo y reclama tickets atómicamente mediante API con identidad del actor
- [ ] Al reclamar se hace fetch y pull ff-only sin sobrescribir cambios locales y no se permite reclamar si sync falla
- [ ] Al cerrar se ejecuta la puerta con evidencia y se verifica pull y push de commits antes de completar ticket remoto o marcar done local
- [ ] El flujo respeta autorización de push y no crea commits ni fuerza push silenciosamente
- [ ] Errores HTTP, autorización, actor ausente, timeout, conflictos y fallos Git dejan estados recuperables sin falsos éxitos
- [ ] Hay tests deterministas de API y repos Git temporales y documentación de configuración, sync, start y finish
- [ ] ./init.sh termina con ENTORNO LISTO y las suites pertinentes pasan

## Bitácora

_(pendiente)_

## Bloqueos

_(ninguno)_
