# Sumario de Sesión Temporal: Bug en la Generación de Contenido Libre (SOLUCIONADO)

## 1. Resumen de la Solución
La sesión de depuración ha concluido con éxito, identificando y resolviendo una compleja cascada de errores cuya causa raíz era la **lógica de las señales de Django**, que no discriminaban entre contenido académico y libre.

### Diagnóstico Final
El problema se manifestaba como la aparición de jerarquías académicas en el "Directorio de Contenidos Libres". La investigación empírica, guiada por el usuario, demostró que:
1.  La tarea de creación de contenido (`tasks.py`) fue corregida para no vincular erróneamente contenido libre a asignaturas académicas, mediante la introducción de un campo booleano `is_free_content` en el modelo `ContentMaterial`.
2.  La causa raíz de la corrupción de los flags `has_free_content` residía en las señales (`signals.py`), cuya lógica de recálculo se activaba con cualquier tipo de contenido.

### Pasos de la Solución Implementada
1.  **Migración de Modelo:** Se añadió el campo `is_free_content` a `ContentMaterial` para una distinción explícita.
2.  **Corrección de Errores de Sistema:** Se solucionaron múltiples errores tipográficos (`subjects` vs `subject`) en `admin.py` y `models.py` que impedían las migraciones.
3.  **Refactorización de Tareas:** Se modificó `content_automation/tasks.py` para usar el nuevo flag `is_free_content` y prevenir la vinculación incorrecta.
4.  **Refactorización de Señales:** Se corrigió `contents/signals.py` para que la lógica que actualiza los flags del directorio libre (`has_free_content`) ignore por completo el contenido académico, y viceversa.
5.  **Saneamiento de Datos:** Se creó y ejecutó un comando de gestión (`resync_free_content_flags`) para recalcular y corregir todos los flags en la base de datos.
6.  **Estabilización del Entorno:** Se identificó y solucionó el problema de los "workers zombies" de Celery que operaban con código obsoleto, forzando su reinicio con `pkill` para que cargaran la lógica corregida.

El resultado es un sistema robusto, con una clara separación entre los flujos de contenido libre y académico, y una base de datos íntegra.
