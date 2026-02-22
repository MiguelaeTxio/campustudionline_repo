{# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md #}
### PARTE INMUTABLE (MANDATORIA EN TODOS LOS PCS)

**DIRECTRIZ DE CARGA OBLIGATORIA (LEY DE CONTINUIDAD):**
La próxima sesión debe cargarse OBLIGATORIAMENTE con la siguiente constelación documental:
*   V06DOC_ARCHETYPES.md
*   V06DOC_SUBARCHETYPES.md
*   V06DOC_SUBDIVISIONS.md
*   V06DOC_BLOCKS.md
*   V06DOC_WIDGETS.md
*   V06DOC_METADATA.md
*   V06DOC_LEVELS.md
*   V06DOC_TEMPLATES.md
*   V06DOC_STRUCTURE.md
*   V06DOC_LOGIC_MAPPING.md
*   V06DOC_ROADMAP.md

**PROTOCOLO DEL MANIFIESTO (FUENTE DE LA VERDAD):**
El archivo V06DOC_ROADMAP.md es la ÚNICA fuente de verdad para el progreso. 
1. Es OBLIGATORIO auditar este archivo al inicio de cada sesión.
2. Es MANDATORIO actualizar su estado atómico (Checklist) al cierre de cada sesión.

---

# ANEXO: HITO 06 - SISTEMA DE AUTOEVALUACIONES CON IA
# ESTADO: EN PROGRESO (FASE DE PRUEBAS DE ESTRÉS)

### PARTE MUTABLE (RESUMEN Y HOJA DE RUTA)

## 1. RESUMEN TÉCNICO DE LA SESIÓN (CYC)
*   **Blindaje Anti-Abuso:** Implementada la regla de caducidad de 24h y el campo `expiration_date`.
*   **Tolerancia Cero en Cuotas:** Implementado el bloqueo total de cuota semanal para usuarios FREE ante evaluaciones caducadas no realizadas.
*   **Navegación Dinámica:** Ajustado el builder de navegación para filtrar y ocultar exámenes caducados automáticamente.
*   **Sincronización de Verdad:** Actualizado `V06DOC_ROADMAP.md` y `V06DOC_TEMPLATES.md` reflejando el 100% de la implementación técnica y normativa.
*   **Auditoría Final:** Certificada la integridad atómica entre el código fuente y la documentación satelital.

## 2. HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)
**VALIDACIÓN MASIVA DE SUBARQUETIPOS (HITO 06):**

1.  **CONSTRUCCIÓN DE TEST DE ESTRÉS:** Crear script en `/home/MiguelAeTxio/SWAP/` que cargue el entorno Django de CSO.
2.  **EJECUCIÓN ATÓMICA CON ROLLBACK:** El script debe operar bajo `transaction.atomic()` con un rollback forzado final para no alterar la base de datos de producción.
3.  **MUESTREO DE LOS 22 SUBARQUETIPOS:**
    *   Seleccionar 22 asignaturas reales al azar, una por cada subarquetipo definido en `V06DOC_SUBARCHETYPES`.
    *   Para cada una: Crear `ContentCopy` -> Solicitar Examen -> Ejecutar `generate_exam_task`.
4.  **AUDITORÍA DE DEDUCCIÓN:** Verificar que el `AcademicDeductor` asigna correctamente la identidad (Arquetipo/Subarquetipo) y que los logs de eventos registran la generación sin errores.

---
