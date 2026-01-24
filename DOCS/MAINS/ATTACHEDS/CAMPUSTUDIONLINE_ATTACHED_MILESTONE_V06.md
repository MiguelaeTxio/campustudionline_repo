# ANEXO HITO 6: SISTEMA DE EVALUACIONES (ESTABILIZACIÓN ARQUITECTÓNICA)

DIRECTRIZ OBLIGATORIA: Al iniciar sesión con este hito, es **MANDATORIO** cargar los archivos:
1. `DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_MASTER_PLAN.md` (Lógica de Motor)
2. `DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_ARCHETYPES_SPEC.md` (Esqueleto y Granularidad)

## ESTADO DE LA HOJA DE RUTA
1. [X] **Restauración de Sistema.** (Sintaxis corregida y servidor WSGI operativo).
2. [X] **Implementación de Atomic Flow (Fase A).** (Esqueletos deterministas delegados a estrategias).
3. [X] **Sincronización PAIR de Rotación.** (Blindaje ante errores 429 y rotación proactiva).
4. [X] **Implementación de INPUT_DUALITY.** (Modelos híbridos Texto/Archivo operativos).
5. [X] **Inyección de STIMULUS_STICKY.** (Botón flotante de referencia funcional en todos los arquetipos).
6. [X] **Refactorización de Fase B (Audio).** (Orquestador Celery reparado y forzado de MP3 activo).
7. [X] **Validación de Esqueleto Minor.** (Chino B1 validado con 5 destrezas UGR).

## HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)
1. **Iconografía de Control (UI Refactor):** En `take_assessment_languages.html`, sustituir los botones `<button>` de texto por iconos FontAwesome:
   - Reproductor: `fa-play-circle` (Play), `fa-pause-circle` (Pause), `fa-stop-circle` (Stop).
   - Grabador: `fa-microphone` (Grabar), `fa-stop` (Parar).
   - Eliminar todo texto interior de los botones para un acabado minimalista.
2. **Rediseño del Componente de Carga (Input File):** Sustituir el `input type="file"` estándar por un contenedor visual con el icono `fa-cloud-upload-alt`. El área debe ser estética y centrar la atención en la acción de "Subir Foto/Archivo".
3. **Purga de Duality:** Eliminar definitivamente el `textarea` de "Notas Adicionales" en el bloque `if question.requires_upload` de la plantilla de idiomas.
4. **Sincronización de Botón Flotante:** Ajustar el CSS del botón `#offcanvasReference` para que su tamaño, sombra y radio de borde coincidan exactamente con los botones de la sidebar de navegación.

## LOG DE CAMBIOS (NRA)
- Corregido SyntaxError crítico en tasks.py (paréntesis huérfano).
- Unificado contrato de anotación de indicadores (assessment_status -> assessment_state).
- Reparada sintaxis de templates de idiomas (etiquetas Django desbalanceadas).
- Restaurada la 5ª destreza (Expresión Oral) en el arquetipo Minor.
