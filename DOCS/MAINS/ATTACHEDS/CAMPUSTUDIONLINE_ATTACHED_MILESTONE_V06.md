# Hito 6: Sistema de Autoevaluaciones con IA (Acreditación Técnica v5)

**Estado:** 🚧 EN DESARROLLO (Ajuste de Reglas de Negocio / Clasificador)
**Modelo Vinculante:** `gemini-2.5-flash-lite`

## RESUMEN DE LA SESIÓN
- **Segregación de Estrategias:** Se ha implementado una arquitectura de servicios separados en `core/services/assessment_strategies/` para Humanidades, Idiomas y Ciencias.
- **Refactorización de `tasks.py`:** El orquestador ahora consume estos servicios de forma aislada.
- **Incidencia Detectada:** Error de clasificación en asignaturas de Filología Hispánica ("El Español Actual"). El sistema las etiqueta erróneamente como "Idiomas" (Foreign Language), activando la interfaz de Reading/Listening indebidamente.

## HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)

### PASO 1: BLINDAJE DEL CLASIFICADOR (REGLA DE NEGOCIO "ANDALUCÍA")
1.  **Modificar `classifier.py`:**
    *   **Contexto Geográfico:** Definir explícitamente que las universidades son andaluzas y no existen usuarios extranjeros.
    *   **Regla "Español":** Cualquier asignatura que contenga "Español", "Lengua", "Literatura" o "Filología" debe clasificarse OBLIGATORIAMENTE como `PHILOLOGY` (Humanidades), nunca como `LANGUAGES`.
    *   **Regla "Idiomas":** Restringir la categoría `LANGUAGES` exclusivamente a lenguas extranjeras (Inglés, Francés, Alemán, Italiano, Portugués, etc.).

### PASO 2: VERIFICACIÓN DE UI
1.  **Prueba de Campo:** Repetir la generación para "El Español Actual".
2.  **Criterio de Éxito:**
    *   Arquetipo detectado: `PHILOLOGY`.
    *   Interfaz: **Sin botón** "Leer Texto de Referencia".
    *   Contenido: Preguntas conceptuales sobre normativa y uso, no sobre un texto inventado.

### PASO 3: ESTABILIZACIÓN FINAL
1.  Revisión de logs para confirmar que no quedan trazas de lógica antigua.
