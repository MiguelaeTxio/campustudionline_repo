# Resumen de Sesión: Fallo de Visualización Post-Migración M2M

## 1. Diagnóstico del Incidente
- Tras la exitosa migración de `ContentMaterial.subject` a una relación `ManyToManyField` y la posterior estabilización del motor de automatización, se ha detectado una nueva anomalía.
- Las vistas públicas del frontend (principalmente `academic_directory` y `search`) no muestran el contenido académico generado, a pesar de que la evidencia del backend (panel de administración y flags `has_public_content` en la BBDD) confirma que los datos y los indicadores jerárquicos son correctos.

## 2. Hipótesis
- La causa raíz del fallo no reside en el modelo de datos ni en las señales (que han sido validadas), sino en la capa de lógica de las vistas.
- Las consultas del ORM de Django dentro de los archivos `views.py` de las aplicaciones afectadas (`academic_directory`, `search`, etc.) no fueron refactorizadas durante la migración. Siguen operando bajo la suposición de una relación `ForeignKey` directa, lo que resulta en consultas que no devuelven resultados con la nueva estructura `ManyToManyField`.

## 3. Hoja de Ruta para la Próxima Sesión
1.  **Análisis de Vistas:** Iniciar un `PVR` para solicitar los archivos `views.py` de las aplicaciones `academic_directory` y `search`.
2.  **Localización de Consultas Obsoletas:** Realizar un `TLA` para identificar todas las consultas que acceden al contenido a través de la jerarquía académica y que necesitan ser adaptadas a la relación M2M.
3.  **Refactorización Auditada:** Ejecutar un `PMA` para cada archivo afectado, modificando las consultas para utilizar la sintaxis correcta de M2M (ej. `__in` o `Exists`).
4.  **Verificación Empírica:** Validar la corrección navegando a las vistas públicas afectadas y confirmando que el contenido ahora se muestra correctamente.
