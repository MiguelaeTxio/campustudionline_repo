# Hito 6: Sistema de Autoevaluaciones con IA (EN PROGRESO)

## Resumen de la Sesión del 16/11/2025 (PCS - FALLIDA)

**Objetivo:** Refactorizar la vista de la "Sala de Estudio" (`user_copies_list`) para implementar una navegación jerárquica que muestre correctamente las copias de contenido académico, basándose en su `subject_context` real.

**Desarrollo:**
Se ha completado la refactorización atómica de los tres archivos implicados:
1.  `contents/study_room_urls.py`: Se han añadido las nuevas rutas jerárquicas para la navegación académica.
2.  `contents/study_room_views.py`: Se ha reescrito la vista para que actúe como un despachador, distinguiendo entre la ruta académica y la de contenido libre, implementando las consultas correctas para la jerarquía académica y preservando la funcionalidad de los `assessment badges`.
3.  `contents/templates/contents/study_room/_copy_list_partial.html`: Se ha modificado la plantilla para que pueda renderizar la nueva estructura de datos de la jerarquía académica.

**Causa del Fallo y Bloqueo:**
La implementación no ha podido ser verificada empíricamente. Las pruebas han revelado un error bloqueante `django.template.base.VariableDoesNotExist: Failed lookup for key [HTTP_REFERER]` en la plantilla `contents/content_detail.html`. Este error es una regresión introducida en una sesión anterior y debe ser solucionado antes de poder validar la refactorización actual.

## Hoja de Ruta para la Próxima Sesión (Estabilización y Verificación)

**Objetivo Estratégico:** Estabilizar la plataforma solucionando el error bloqueante y verificar de forma exhaustiva la correcta implementación de la refactorización de la "Sala de Estudio". **QUEDA PROHIBIDO INTRODUCIR NUEVA FUNCIONALIDAD HASTA COMPLETAR ESTOS PUNTOS.**

**Plan de Acción Atómico y Secuencial (Orden Inviolable):**

**1. Fase de Estabilización (Prioridad Máxima):**
   -   **Acción:** Corregir el bug `VariableDoesNotExist` en `contents/templates/contents/content_detail.html`.
   -   **Solución Empírica:** La causa es el intento de acceder a `request.META.HTTP_REFERER` cuando no existe (ej. acceso por crawlers o directo). La solución consiste en envolver el botón "Volver" en una condición que verifique su existencia: `{% if request.META.HTTP_REFERER %}`.

**2. Fase de Verificación Exhaustiva:**
   -   **Acción:** Una vez estabilizada la plataforma, se debe verificar empíricamente que la nueva "Sala de Estudio" funciona como se espera y no ha introducido regresiones.
   -   **Puntos de Prueba Obligatorios:**
      -   **Navegación Raíz:** Verificar que la vista raíz (`/study-room/directory/`) muestra correctamente tanto las raíces académicas (Universidades) como las de contenido libre.
      -   **Navegación Académica Completa:** Navegar desde una Universidad hasta una lista de copias de una asignatura, verificando que cada nivel (`Rama`, `Titulación`, `Año`, `Asignatura`) se muestra correctamente y que las copias listadas corresponden inequívocamente al `subject_context` correcto.
      -   **Navegación Contenido Libre:** Verificar que la navegación por la jerarquía de contenido libre sigue funcionando sin cambios.
      -   **Verificación de Badges de Assessment:** Confirmar que los indicadores de autoevaluación se muestran correctamente en **todos los niveles** de **ambas** jerarquías (tanto en los elementos agregados como en las copias individuales).
