# Sumario de Sesión Temporal: CAMPUSTUDIONLINE_UI_BADGE_ERRORS_FIX

## Objetivo de la Sesión

Diagnosticar y corregir la lógica de visualización de los indicadores (badges) de estado de las autoevaluaciones en la vista raíz de la Sala de Estudio (`study_room:copy_directory_root`).

## Contexto y Síntomas

Durante la sesión del 13/11/2025, se observó que los badges de estado de las autoevaluaciones (ej. "Ver Resultados") no se alinean correctamente con la jerarquía académica a la que pertenecen, mostrando información potencialmente incorrecta o en lugares inesperados.

## Plan de Acción Empírico

1.  **Análisis de la Vista:** Revisar la lógica de la vista `user_copies_list` en `contents/study_room_views.py`, específicamente cómo se calculan y se pasan al contexto las anotaciones de estado de `Assessment` para los niveles jerárquicos superiores (`KnowledgeArea`, `FreeContentMasterCategory`).
2.  **Revisión de la Plantilla:** Inspeccionar la plantilla `contents/study_room/copy_list.html` para verificar cómo se renderizan estos indicadores y asegurar que la lógica de presentación es correcta.
3.  **Corrección:** Implementar las modificaciones necesarias en la vista y/o la plantilla para asegurar que los indicadores reflejen con precisión el estado de las autoevaluaciones dentro de su contexto jerárquico correcto.
