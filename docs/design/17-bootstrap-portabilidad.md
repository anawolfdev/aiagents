# FAB-017: Plan de bootstrap sin circularidad y portabilidad OpenClaw/OpenCode

**Versión:** 1.0 · **Estado:** DISEÑADO  
**Ámbito:** Secciones 15 y 1  
**Dueño:** coordinador orquesta · propietario autoriza cada fase

---

## 1. Secuencia (sin circularidad)

| # | Fase | Salida | Responsable | ¿Simula algo? |
|---|---|---|---|---|
| 1 | Diseño completo | Este paquete (`docs/design/`) | Agente diseñador | No |
| 2 | Preparación autorizada de recursos mínimos | Repos privado/público, ubicación de artefactos | Propietario | No |
| 3 | Construcción **provisional** de A1 | Perfil A1 v1 ejecutable en la plataforma 1 | Operador | No |
| 4 | Pruebas independientes y validación humana | Informe de pruebas de A1 + aprobación explícita | Revisor **distinto** del constructor | No |
| 5 | Construcción progresiva de los demás roles | A2 → A3 → A4 → A5 (uno a uno, mismo ciclo) | Operador | No |
| 6 | Ensayo integral | Recorrido completo con un agente de prueba | A1–A5 con el propietario | No |
| 7 | Activación autorizada | Vigilancia diaria + gates en operación | Propietario | No |

**Sin circularidad:** A1 no se crea ni se aprueba a sí mismo. La fase 4 la realiza alguien distinto del que construyó.

## 2. Cobertura provisional antes de la vigilancia automática

Antes de que exista A2 automatizado:
- El **propietario** (u operador designado) cubre explícitamente las funciones inexistentes: revisión de riesgos, cobertura y avisos.
- Cualquier despliegue operativo exige **evidencia equivalente** obtenida por el **procedimiento provisional autorizado** (revisión manual documentada con las mismas cuatro fechas y el mismo manifiesto de cobertura).
- Las pruebas aisladas de bootstrap **no** son aprobación operativa.
- **No** se simula que el mecanismo automático ya funciona.

### Responsabilidades provisionales
| Función aún inexistente | Quién la cubre | Cómo se evidencia |
|---|---|---|
| Vigilancia diaria | Propietario | Informe manual con fuentes y fechas |
| Detección de ausencia | Propietario (revisión de calendario) | Registro de la comprobación |
| Avisos | Propietario | Registro de la decisión tomada |
| Evaluación independiente | Persona distinta del constructor (o el propietario si no hay otra) | Informe `EVA` manual |

**No afirmar independencia** si la misma ejecución construye y certifica sin revisión separada. Si el propietario construye y evalúa, se declara **no independiente** y se compensa con pruebas deterministas adicionales.

## 3. Portabilidad OpenClaw / OpenCode

### Modelo
```
┌─────────────────────────────┐
│  Núcleo de especificación   │  común: misión, entradas, procedimiento,
│  (común, portable)          │  salidas, prohibiciones, criterios,
└──────────┬──────────────────┘  permisos, escalado
           │
    ┌──────┴──────┐
    ▼             ▼
┌────────┐   ┌─────────┐
│Adaptador│   │Adaptador│   separados: formato de instrucciones,
│OpenClaw │   │OpenCode │   configuración, herramientas, rutas
└────────┘   └─────────┘
```

### Reglas
- Un solo **núcleo** con la especificación; **nunca** duplicar el spec por plataforma.
- Adaptadores **separados** solo donde sea necesario; deben ser delgados y reversibles.
- **Pruebas de aceptación en ambas plataformas antes de declarar compatibilidad con ambas.**
- **No prometer comportamiento idéntico** ni configuraciones compatibles sin pruebas.
- Si una plataforma no pasa las pruebas: se declara **no compatible**, no se «ajusta» el criterio.

### Matriz de portabilidad
| Aspecto | Núcleo | Adaptador |
|---|---|---|
| Misión, procedimiento, prohibiciones | ✅ | — |
| Criterios de aceptación | ✅ | — |
| Formato de instrucciones | — | ✅ |
| Declaración de herramientas | — | ✅ |
| Rutas y nombres de fichero | — | ✅ |
| Mecanismo de aviso | — | ✅ |
| Modelo/proveedor | — | ✅ (PENDIENTE) |

### Prueba de portabilidad
1. Ejecutar la **misma** suite de aceptación en OpenClaw.
2. Ejecutarla en OpenCode.
3. Registrar resultado **por plataforma**.
4. Declarar: `compatible con X` · `no compatible con X` · `no probado en X`.

Sin el paso 2, la declaración es **«no probado»**, nunca «compatible».

## 4. Parámetros pendientes (no inventar)

| Parámetro | Estado | Quién lo resuelve |
|---|---|---|
| Repositorios concretos | PENDIENTE | Propietario |
| Proveedor/modelo autorizado | PENDIENTE | Propietario |
| Presupuesto | PENDIENTE | Propietario (estimación + aprobación) |
| Horario | PENDIENTE | Propietario |
| Zona horaria | PENDIENTE | Propietario |
| Conexión y destinatario Telegram | PENDIENTE | Propietario (chat privado verificado) |
| Inventario | PENDIENTE | Propietario (instantánea saneada) |
| Aislamiento | PENDIENTE | Propietario (comprobación) |
| Permisos | PENDIENTE | Propietario (GATE 1) |
| Retención | **PENDIENTE — se aprueba antes de activar** | Propietario |
| Almacenamiento | PENDIENTE | Propietario |
| Mecanismo independiente de supervisión | PENDIENTE | Propietario |

## 5. Verificación FAB-017
- [x] La secuencia no tiene circularidad
- [x] Cada fase tiene salida y responsable
- [x] Hay cobertura provisional antes de la vigilancia automática
- [x] La portabilidad se prueba en ambas plataformas o se declara no compatible
- [x] Los parámetros desconocidos quedan pendientes
- [x] No se simula ninguna activación
