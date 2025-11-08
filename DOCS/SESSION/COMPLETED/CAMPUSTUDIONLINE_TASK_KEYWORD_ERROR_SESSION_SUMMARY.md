# Resumen de Sesión: `FieldError` en `_get_next_subject_queryset`

## Problema
Se detectó un error `FieldError` que impedía la generación de contenido. El log de la tarea mostraba el mensaje: `Cannot resolve keyword 'year' into field`.

## Diagnóstico Empírico
1.  **Identificación del Error:** El análisis del log de la tarea reveló que el error no era un `KeyError` como se sospechaba inicialmente, sino un `FieldError` de Django.
2.  **Localización de la Causa:** Se utilizó el comando `grep` para buscar el uso del parámetro `year=` dentro del archivo `content_automation/tasks.py`. La búsqueda confirmó que la función `_get_next_subject_queryset` estaba construyendo una consulta con el campo incorrecto.

## Solución Aplicada
Se corrigió la línea `query = query.filter(year=year_int)` sustituyéndola por `query = query.filter(academic_year=year_int)`. El cambio fue aplicado de forma segura mediante el protocolo `PMA`.

## Verificación
Tras aplicar el parche, se reinició el worker de Celery en PythonAnywhere. El worker recargó el código corregido y reanudó la tarea, que se completó exitosamente, confirmando la solución.
