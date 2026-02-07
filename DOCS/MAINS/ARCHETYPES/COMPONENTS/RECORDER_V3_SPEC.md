# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ARCHETYPES/COMPONENTS/RECORDER_V3_SPEC.md
# ESPECIFICACIÓN TÉCNICA: WIDGET GRABADORA DE VOZ (RECORDER V3)
# Componente de Interfaz para Competencia Oral Productiva ("The Cassette")

## 1. DEFINICIÓN DEL COMPONENTE
El Recorder V3 es una interfaz de captura de audio diseñada para emular el flujo de una grabadora física, garantizando que el alumno pueda revisar su producción antes de la entrega definitiva y que el sistema no reciba archivos vacíos.

## 2. INTERFAZ FÍSICA Y CONTROLES
- **Botón REC (Grabar):**
  - Función: Inicia la captura de audio desde el micrófono del dispositivo.
  - Comportamiento: Cambia a un icono de "Grabando" parpadeante.
- **Botón STOP (Detener):**
  - Función: Finaliza la captura de audio.
  - Comportamiento: Habilita los botones PLAY y SAVE.
- **Botón PLAY (Revisar):**
  - Función: Reproduce la grabación recién capturada.
- **Botón SAVE (Guardar/Entregar):**
  - Función: Envía el archivo de audio al servidor para su persistencia.
  - Comportamiento: Una vez pulsado, todos los botones se deshabilitan y el widget muestra un estado de "Entregado".

## 3. MÁQUINA DE ESTADOS Y LÓGICA DE NEGOCIO
El widget debe seguir este flujo no alterable:
1.  **READY (Listo):** Solo el botón REC está habilitado.
2.  **RECORDING (Grabando):** El botón REC está deshabilitado, STOP está habilitado. El sistema monitoriza el nivel de audio.
3.  **REVIEW (Revisión):** Tras pulsar STOP. Los botones PLAY y REC están habilitados (para volver a grabar), STOP está deshabilitado. SAVE está habilitado si la grabación tiene una duración mínima.
4.  **SAVING (Guardando):** Estado transitorio mientras se sube el archivo.
5.  **SUBMITTED (Entregado):** Todos los controles están deshabilitados.

## 4. ESPECIFICACIONES TÉCNICAS (BACKEND/FRONTEND)
- **Formato de Salida:** MP3 (128kbps) o WAV. El formato debe ser consistente en toda la plataforma.
- **Seguridad (Prevención de Archivos Nulos):**
  - El botón SAVE solo se habilita si la grabación supera una duración mínima (configurable, default: 3 segundos).
  - El sistema debe mostrar un **indicador de nivel de audio (vu-meter/waveform)** durante la grabación para que el alumno tenga feedback visual de que su micrófono funciona.
- **Persistencia:** Al pulsar SAVE, el frontend debe enviar el archivo de audio (Blob) al backend, que lo asociará al objeto `UserAnswer` correspondiente.
- **Permisos:** El componente debe gestionar la solicitud de permisos de micrófono al navegador/sistema operativo.

## 5. FOCO PEDAGÓGICO
El flujo REC -> STOP -> PLAY imita el proceso de reflexión y autocorrección, un pilar de la evaluación de la producción oral en la UGR. El sistema no permite la edición del audio, solo la regrabación completa.
