# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ARCHETYPES/COMPONENTS/PLAYER_V3_SPEC.md
# ESPECIFICACIÓN TÉCNICA: WIDGET REPRODUCTOR DE AUDIO (PLAYER V3)
# Componente de Interfaz para Competencia Oral Receptiva

## 1. DEFINICIÓN DEL COMPONENTE
El Player V3 es un reproductor de audio de estado controlado, diseñado para cumplir con la normativa de exámenes oficiales (UGR/CLM), donde el acceso al estímulo sonoro es limitado y supervisado por el sistema.

## 2. INTERFAZ FÍSICA Y CONTROLES
- **Botón PLAY/PAUSE:** 
  - Función: Inicia o reanuda la reproducción.
  - Comportamiento: Cambia de icono dinámicamente.
- **Botón STOP:** 
  - Función: Detiene la reproducción y resetea el cursor de tiempo a 00:00.
  - Relevancia: En modo Acreditación, pulsar Stop NO recupera el intento gastado.
- **Barra de Progreso (SeekBar):**
  - Restricción: Deshabilitada (ReadOnly) durante la primera escucha para evitar el "skipping". Habilitada solo en la segunda escucha (si el nivel lo permite).
- **Contador de Intentos:**
  - Visualización: Texto tipo "Escuchas restantes: 1/2".

## 3. MÁQUINA DE ESTADOS Y LÓGICA DE NEGOCIO
El widget debe gestionar los siguientes estados:
1.  **IDLE (Inactivo):** Esperando interacción inicial.
2.  **PLAYING (Reproduciendo):** Audio en curso. El sistema bloquea la navegación fuera de la pregunta.
3.  **PAUSED (Pausado):** Reproducción detenida temporalmente.
4.  **DEPLETED (Agotado):** El contador de intentos llega a 0. El botón PLAY se oculta o se deshabilita permanentemente mediante `disabled="true"`.

## 4. ESPECIFICACIONES TÉCNICAS (BACKEND/FRONTEND)
- **Formatos Soportados:** MP3 (VBR/CBR), AAC, OGG.
- **Bitrate Mínimo:** 128 kbps (Garantía de nitidez para discriminación fonética).
- **Persistencia:** El número de reproducciones debe guardarse en la sesión del usuario o en el objeto `UserAnswer` para evitar que un refresco de página (F5) reinicie los intentos.
- **Evento de Finalización:** Al terminar el archivo de audio, el sistema debe disparar un evento `audio_finished` que descuenta automáticamente el intento en la base de datos.

## 5. CONFIGURACIÓN SEGÚN MODALIDAD
- **Modo PRÁCTICA:** Intentos ilimitados. Barra de progreso libre.
- **Modo EXAMEN/ACREDITACIÓN:** Límite estricto de 2 escuchas. Barra de progreso bloqueada en la primera escucha.
