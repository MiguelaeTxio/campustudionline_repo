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
# ESTADO: EN PROGRESO (RESOLUCIÓN DE ERRORES DE IMPLEMENTACIÓN)

### PARTE MUTABLE (RESUMEN Y HOJA DE RUTA)

## 1. RESUMEN TÉCNICO DE LA SESIÓN (MAMC)
*   **Certificación de Motores:** Éxito total en la validación de los 22 subarquetipos académicos tras corregir los nominales de las asignaturas.
*   **Saneamiento de Base de Datos:** Se ha detectado y corregido un error de integridad (1451) en MySQL. Se aplicó una reparación física de la restricción `FOREIGN KEY` en la tabla `contents_userstudynavigation` para habilitar el `ON DELETE CASCADE` real.
*   **Verificación:** Borrado de usuarios de prueba realizado con éxito desde el panel de administración.

## 2. HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)
**DEPURACIÓN DE ERRORES DE GENERACIÓN:**

1.  **CORRECCIÓN DE TYPEERROR:** Investigar y corregir el fallo en `orchestrator/tasks.py` (línea 441) donde `LanguagesStrategy.get_system_prompt()` falla por argumentos inesperados.
2.  **AUDITORÍA DE FIRMAS:** Revisar el contrato de métodos entre la `BaseStrategy` y sus implementaciones concretas en `assessment_v2/services/engine/strategies/`.
3.  **TEST DE GENERACIÓN REAL:** Realizar una prueba de generación de examen completa desde la interfaz de usuario para confirmar la estabilidad del flujo Skeleton-First.
4.  **REVISIÓN DE LOGS DE BLEACH:** Atender el aviso `NoCssSanitizerWarning` en el procesamiento de HTML con la librería `bleach`.

