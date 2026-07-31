# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ANNEX_ROUTER.md
# Enrutador de Anexos — Proyecto CampuStudiOnline

---

## 1. Función

Este archivo es la **única fuente de verdad** sobre qué hito está
`EN PROGRESO`. `CAMPUSTUDIONLINE_MASTER_DOCUMENT.md` es puramente
descriptivo e invariable (salvo adición de hito nuevo) y **nunca**
menciona estados de hito — esa responsabilidad es exclusiva de este
archivo.

**Creado 2026-07-24**, migrando el proyecto del sistema de tres
estados que tenía hasta ahora (`EN PROGRESO`/`PAUSADO`/`COMPLETADO`,
mencionados directamente en el master document) al mismo sistema
binario que usa EnterpriseBot: solo `EN PROGRESO` y `PAUSADO` son
estados reales de seguimiento. Los hitos ya terminados no llevan
ninguna marca de estado — su propia existencia en la tabla, con
anexo cerrado, basta; nunca se etiquetan como "COMPLETADO" en ningún
sitio del sistema.

Cumple dos funciones inseparables:

1. **Enrutamiento:** identifica qué anexo leer según el hito EN
   PROGRESO de la tabla de abajo.
2. **Cambio de hito:** al cambiar el hito EN PROGRESO, se edita este
   mismo archivo (mover el marcador) — ver `nfs-campustudionline-pch`.

---

## 2. Tabla de Enrutamiento

| Hito | Título resumido | Anexo |
|---|---|---|
| H01 | Migración del Sistema de Mensajería y Chat a WSGI | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V01.md` |
| H02 | Optimización para Motores de Búsqueda (SEO) | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V02.md` |
| H03 | Ecosistema de Salas de Chat Globales y Contextuales | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V03.md` |
| H04 | Gestión Avanzada de Cuentas de Usuario | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V04.md` |
| H05 | Mantenimiento y Mejoras Generales | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V05.md` |
| **H06** | **Sistema de Autoevaluaciones con IA** | **`CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md`** ← EN PROGRESO |
| H07 | Mejoras de Usabilidad y Feedback de Usuario | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V07.md` |
| H08 | Estandarización de Imagen Corporativa en Emails | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V08.md` |
| H10 | Depuración: Sistema de Notificaciones Push | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V10.md` |
| H11 | Estabilización: Generador de Contenido v5 | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V11.md` |
| H12 | Migración a Python 3.9+ y SDK de Google Gen AI | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V12.md` |
| H13 | Final 2: Documentación de Proyecto | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V13.md` |
| H14 | Final 1: Refinamiento y Coherencia del Código | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V14.md` |
| H18 | Re-arquitectura del Generador de Contenido | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V18.md` |
| H19 | Re-arquitectura de los Directorios de Navegación | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V19.md` |
| H20 | Refinamiento del Proceso de Scraping de Datos | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V20.md` |
| H21 | Refactorización del Orquestador de Tareas Asíncronas | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V21.md` |
| H22 | Refactorización de Navegación de Sala de Estudio | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V22.md` |
| H23 | Cumplimiento Normativo y Legal | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V23.md` |
| H24 | Sistema de Ruegos y Preguntas | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md` |
| H25 | Estrategia de Campaña Meta Ads | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V25.md` |
| H26 | Cumplimiento Regla de Oro del Idioma | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V26.md` |
| H27 | Optimización de UX y Onboarding para Evaluaciones | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V27.md` |
| H28 | Implementación de Asistente Contextual 'UniversIA' | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V28.md` |
| H29 | Extensión de UniversIA a la Plataforma | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V29.md` |
| H30 | Estrategia Comercial de Recomendación y Gestión de Afiliados | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V30.md` |
| H31 | Sistema de Agenda Académica Personal (Schedule) | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V31.md` |
| H32 | Sistema de Visitas Guiadas e Integración de Onboarding | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V32.md` |
| H33 | Optimización de Comunicaciones Administrativas | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V33.md` |
| H34 | Optimización de Redes Sociales y Metadatos de Compartición | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V34.md` |
| H35 | Optimización de Infraestructura Redis y Gestión de Tareas | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V35.md` |
| H36 | Implementación de la Sala de Traducción | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V36.md` |
| H37 | Migración a Gemini 3 Flash y Estandarización de SDK | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V37.md` |
| H38 | Adquisición y Licenciamiento de Imágenes para Evaluaciones | `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V38.md` |

Todos los anexos viven en `DOCS/MAINS/ATTACHEDS/`. Numeración con
huecos (H09, H15, H16, H17 no existen) heredada del proyecto
original — no se renumera, se respeta tal cual estaba.

---

## 3. Resultado Actual

**Hito EN PROGRESO:** H06 — Sistema de Autoevaluaciones con IA →
`CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md`. Reactivado en S028
(2026-07-31): H38 quedó cerrado en S027 con sus siete puntos
verificados en producción, el bloqueo sobre ARCH_HEALTH desapareció,
y Miguel Ángel confirmó explícitamente la reanudación. La hoja de
ruta de reanudación, redactada en S026, no se ha tocado — sigue siendo
la ley suprema tal cual quedó escrita.

H38 queda sin marca de estado: los siete puntos de su hoja de ruta
están cerrados y verificados con datos reales de producción, no hay
trabajo pendiente propio del hito. No se anota "COMPLETADO" (ver
directriz 6) — la ausencia de marca es la convención del sistema para
hitos terminados.

**Hitos PAUSADO** (heredados de la migración de sistema de estados,
2026-07-24 — no son un desvío de esta sesión, sino el estado real en
que estaban marcados en el master document antes de la migración):

- H20 — Refinamiento del Proceso de Scraping de Datos
- H24 — Sistema de Ruegos y Preguntas
- H29 — Extensión de UniversIA a la Plataforma
- H31 — Sistema de Agenda Académica Personal (Schedule) — nota
  heredada: funcionalidad técnica completa, pendiente integración
  futura con IA.
- H34 — Optimización de Redes Sociales y Metadatos de Compartición

El resto de hitos de la tabla no llevan marca de estado porque están
terminados — no se anota "COMPLETADO" en ningún sitio del sistema,
solo aquí en este resumen de migración, con carácter puramente
informativo y no repetible en futuras sesiones (ver directriz 6).

---

## 4. Protocolo de Enrutamiento Estándar

### Caso normal — Un único hito EN PROGRESO

1. Leer el hito EN PROGRESO de la tabla (marcador `← EN PROGRESO`).
2. Consultar `CAMPUSTUDIONLINE_MASTER_DOCUMENT.md` para el título y
   descripción completa de ese hito.
3. Leer el anexo indicado.
4. La hoja de ruta de ese anexo es la **LEY SUPREMA** de la sesión.

---

## 5. Casos Especiales

### Caso A — Desvío de sesión a otro hito

El trabajo se desvía de H_X (EN PROGRESO) a atender H_Y (PAUSADO).

**Al cierre de sesión se actualizan DOS anexos** (vía
`nfs-campustudionline-edit`):

1. Anexo de H_X → registrar únicamente la NOTA DE DESVÍO. La hoja
   de ruta no cambia porque el hito no avanzó.
2. Anexo de H_Y → registrar el trabajo realizado y actualizar su
   hoja de ruta.

El marcador `← EN PROGRESO` de esta tabla **NO cambia**. Un desvío de
sesión no implica cambio de hito EN PROGRESO.

### Caso B — Cambio de hito al cierre de sesión

El hito EN PROGRESO (H_X) se pausa y se abre H_Y (ya existente en la
tabla, o terminado y se reabre trabajo sobre él).

**Flujo obligatorio:**

**Paso 1 — Determinar el tipo de cambio:**

- Hito actual no terminado → continuar en el mismo hito. Actualizar
  solo la hoja de ruta del anexo actual. No hay cambio de hito.
- Trabajo para hito anterior pausado (o ya cerrado sin marca) →
  proponer REACTIVACIÓN. Mover el marcador `← EN PROGRESO` de H_X a
  H_Y en la tabla de este archivo.
- Hito completamente nuevo → ver Caso C.
- Incidencia fuera del hito actual → atenderla como Caso A (desvío).
  No alterar la hoja de ruta del hito en progreso.

**Paso 2 — Editar este archivo** (vía `nfs-campustudionline-edit`):
mover el marcador `← EN PROGRESO` de H_X a H_Y en la tabla, y
actualizar la sección "3. Resultado Actual". Solo puede haber UN
hito EN PROGRESO en todo momento.

**Paso 3 — Actualizar los DOS anexos afectados** (mismo commit o
inmediatamente después, vía `nfs-campustudionline-edit`):

1. Anexo de H_X → registrar el trabajo final. Hoja de ruta de cierre
   o vacía.
2. Anexo de H_Y → registrar el contexto inicial y la hoja de ruta de
   arranque.

### Caso C — Hito nuevo, sin anexo todavía

1. Editar `CAMPUSTUDIONLINE_MASTER_DOCUMENT.md`: añadir fila a la
   tabla de anexos y su descripción en la Hoja de Ruta Estratégica
   (vía `nfs-campustudionline-edit`).
2. Editar este archivo: añadir el hito nuevo a la tabla como PAUSADO
   (nunca EN PROGRESO directamente sin que Miguel Ángel lo confirme).
3. Crear el anexo nuevo en `DOCS/MAINS/ATTACHEDS/` (número
   correlativo siguiente al último existente, H38) con estructura
   base: objetivo del hito, contexto técnico, hoja de ruta ejecutable
   de forma autónoma.
4. **No modificar el anexo del hito que se pausa.**
5. Un solo commit `docs:` para los tres archivos, vía
   `nfs-campustudionline-edit`.

### Caso D — Tres o más hitos tocados en la misma sesión

Actualizar tantos anexos como hitos tocados, en este orden:

1. Hito EN PROGRESO (primero siempre).
2. Hitos atendidos por desvío, en orden cronológico.
3. Hito nuevo que abre, si lo hay (último).

---

## 6. Reglas de Obligado Cumplimiento

- Los estados de hito son responsabilidad **exclusiva** de este
  archivo. Ningún anexo ni `CAMPUSTUDIONLINE_MASTER_DOCUMENT.md`
  puede mencionar estados de hito.
- Solo un hito EN PROGRESO en todo momento, sin excepción.
- **QUEDA TERMINANTEMENTE PROHIBIDO** trabajar sobre un anexo que no
  figure en la tabla de este archivo.
- **QUEDA TERMINANTEMENTE PROHIBIDO** usar la palabra "COMPLETADO"
  (o cualquier otro estado que no sea `EN PROGRESO`/`PAUSADO`) como
  marca de estado en este archivo o en cualquier otro del sistema —
  ver origen de esta regla en `ENTERPRISEBOT_MASTER_DOCUMENT.md`
  §REGLA ABSOLUTA de hitos.
