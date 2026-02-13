### PARTE INMUTABLE (MANDATORIA EN TODOS LOS PCS)

**DIRECTRIZ DE CARGA OBLIGATORIA (LEY DE CONTINUIDAD):**
La próxima sesión debe cargarse con los siguientes documentos para garantizar el contexto completo del Estándar de Máxima Calidad:
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

### PARTE MUTABLE PERO MANDATORIA EN TODOS LOS PCS

---

# ANEXO: HITO 06 - SISTEMA DE AUTOEVALUACIONES CON IA
# ESTADO: EN PROGRESO (FASE 3: UX PENDIENTE DE REFINAMIENTO)

## 1. RESUMEN TÉCNICO
Se ha implementado el núcleo funcional del generador de exámenes (V2):
*   **Orquestación:** Tarea `generate_exam_task` funcional con inyección de contexto.
*   **Lógica de Negocio:** Algoritmo de deducción automática (`V06DOC_LOGIC_MAPPING`) implementado en backend.
*   **Frontend Básico:** Interfaz de selección de rango operativa pero **NO REFINADA**.

## 2. HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)
Finalizar la **Fase 3 (UX)** y pasar a **Validación**.

### TAREAS CRÍTICAS PENDIENTES (UX SELECTOR DE RANGO)
1.  **Limpieza de TOC (`contents/utils.py`):**
    *   Filtrar H1 (Título del documento).
    *   Excluir metadatos: "Tabla de Contenidos", "Bibliografía", "Fuentes".
2.  **Lógica de Selectores (`exam_create.html`):**
    *   **Selector INICIO:** Orden natural (1 -> N).
    *   **Selector FINAL:** Orden inverso (N -> 1).
    *   Implementar botón de "Reiniciar Selección".
3.  **Validación de Flujo:**
    *   Verificar que la deducción automática (Regex) funciona correctamente con asignaturas reales.

---
