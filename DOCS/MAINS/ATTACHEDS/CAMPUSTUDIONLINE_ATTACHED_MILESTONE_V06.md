# Hito 6: Sistema de Autoevaluaciones con IA (Depuración de Interfaz v6)

**Estado:** 🚧 EN DESARROLLO (Fase de Pulido UI/UX)
**Modelo:** `gemini-2.5-flash-lite`

## RESUMEN DE LA SESIÓN
- **Blindaje del Clasificador:** Implementado rol de "Rector" para distinguir entre Filología e Idiomas con éxito empírico.
- **Red de Seguridad:** Implementada lógica de rectificación de arquetipo (rejected_archetypes) y botón "Formato Incorrecto".
- **Integración Feedback:** Redirección automática a la app de feedback tras agotar intentos de clasificación.

## HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)

### PASO 1: DEPURACIÓN DE UI POR ARQUETIPO
1.  **Limpieza Global:** Eliminar los badges de "Arquetipo: X" de todas las plantillas (`humanities`, `languages`, `sciences`).
2.  **Reparación LANGUAGES:**
    *   Auditar por qué no se muestran los botones de `Play Audio` y `Record`. Verificar que el `prompt_data` contiene los campos `listening_script`.
    *   Sincronizar `take_assessment_languages.html` con las propiedades del modelo `Question`.
3.  **Mejora SCIENCES:**
    *   Implementar el widget de subida de archivos (imagen) en cada pregunta para permitir el envío de resoluciones manuscritas.

### PASO 2: VERIFICACIÓN DE FLUJO
1.  Testar el ciclo completo: Rectificación -> Nueva Generación -> Visualización correcta de Widgets específicos.

### PASO 3: ESTABILIZACIÓN
1.  Eliminar trazas de logs experimentales y archivos temporales residuales.
