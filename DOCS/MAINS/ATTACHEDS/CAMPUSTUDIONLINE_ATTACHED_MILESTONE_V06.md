# Hito 6: Sistema de Autoevaluaciones con IA (Acreditación Técnica v5)

**Estado:** 🚧 EN DESARROLLO (Refactorización de Arquetipos Segregados)
**Modelo Vinculante:** `gemini-2.5-flash-lite`

## RESUMEN DE LA SESIÓN
- **Estabilización de Infraestructura:** Blindaje de las Always-on tasks con wrappers Bash inmortales (2026 Ready) y protección de memoria.
- **Blindaje Técnico:** Implementación del Escudo LaTeX y corrección de la visibilidad de evaluaciones (save() vs update()).
- **UI/UX:** Selector de rango corregido geométricamente (elementFromPoint) y exclusión de Bibliografía en el backend. Interfaz de examen ampliada y preparada para Markdown.
- **Redefinición Pedagógica:** Acordado el fin del "Texto de Apoyo" para Humanidades y Ciencias. El examen ahora debe ser una acreditación directa del rango seleccionado en los Sliders.

## HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)

### PASO 1: REFACTORIZACIÓN DEL ENRUTADOR (TASKS.PY)
1.  **Bifurcación Real:** Modificar `tasks.py` para que `HUMANITIES` y `EXACT_SCIENCES` salten directamente al Paso 2, usando como fuente el `filtered_content` de los Sliders.
2.  **Inyección de la Verdad:** Asegurar que el prompt reciba el fragmento del temario como la única fuente de información permitida.

### PASO 2: DESARROLLO DE TRIBUNALES ESPECIALIZADOS
1.  **Implementar los 5 Tribunales en `prompt_generators.py`:**
    *   Ciencias Jurídicas (Derecho/Normas).
    *   Artes y Patrimonio (Análisis formal/Contexto).
    *   Pensamiento y Sociedad (Filosofía/Sociología).
    *   Geografía e Historia (Causalidad/Cronología).
    *   Estudios Filológicos (Análisis lingüístico/Crítico).
2.  **Estructura Técnica:** Asegurar los 3 bloques (Test terminológico, Análisis práctico y Ensayo de síntesis).

### PASO 3: VALIDACIÓN DE IDIOMAS (RETOQUE FINAL)
1.  Verificar que el prompt de Idiomas incluya los encabezados Markdown en el idioma de destino (ej: `### LETTURA`) para el renderizado en el template.

### PASO 4: PRUEBA DE CAMPO
1.  Generar una evaluación de "El Español Actual" y confirmar que es un examen de Grado y no un comentario de texto genérico.
