# Anexo del Hito 20: Ingesta UCO mediante Recopilación Manual de URLs

## 1. Estado Actual del Sistema
- **Base de Datos:** PURGADA. Se ha ejecutado con éxito el protocolo de borrado quirúrgico (Bottom-Up), eliminando la Universidad de Córdoba y todas sus dependencias (Asignaturas, Años, Grados, Tareas y Solicitudes) para asegurar una base limpia.
- **Harvester:** El método de descubrimiento automático mediante Selenium ha sido DESCARTADO debido a la inconsistencia extrema de los slugs y la estructura de navegación de la UCO.

## 2. Estrategia para la Próxima Sesión (LEY SUPREMA)
La sesión se iniciará con la carga de una lista hardcodeada de URLs de planificación que el usuario ha recopilado manualmente. 

### Lógica del Script (UCO_HARVESTER_V19):
1. **Entrada de Datos:** El script procesará una tupla de diccionarios con el formato `{"degree": "Nombre", "url": "URL_REAL_PLANIFICACION"}`.
2. **Motor de Extracción:** Se utilizará BeautifulSoup sobre las URLs directas.
3. **Reglas de Selección de Año:** El "Año Académico" se extraerá EXCLUSIVAMENTE del texto contenido en el `panel-title` del acordeón (Ej: "Primero", "1º", "Segundo"...).
4. **Tratamiento de Tablas:** 
   - Se extraerá la celda con el texto más largo como "Nombre de Asignatura".
   - En facultades multiversión (Veterinaria), se seleccionará el enlace de la columna que contenga el texto "25-26".
5. **Filtro Agresivo (Hito 20):** Aplicación estricta de la lista de exclusión (TFG, Prácticas, etc.), respetando la protección de "Trabajo Social" y "Derecho del Trabajo".

## 3. Hoja de Ruta Inmediata
1. Recibir la lista de URLs manuales.
2. Generar y ejecutar el script V19 en entorno local (PCv).
3. Validar el JSON resultante (`uco_master_map.json`).
4. Subir al servidor y ejecutar el comando de ingesta.

