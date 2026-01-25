# PLAN MAESTRO DEL SISTEMA DE EVALUACIONES (EL SANTO GRIAL)
# Versión: 1.0 (UGR/ACLES Emulator Standard)

## 1. FILOSOFÍA DE DISEÑO
El sistema opera bajo una "Plantilla Tonta" (Stateless UI). La inteligencia reside en el Backend, que calcula una Matriz de Interacción para cada pregunta. 

### 1.1. La Triada de Renderizado
Para cada pregunta, el sistema debe definir:
- **SOURCE (S):** El estímulo proporcionado al alumno.
- **QUESTION TYPE (Q):** La tarea cognitiva requerida.
- **REQUEST MODE (R):** El widget de entrada del usuario.

## 2. MATRIZ DE INTERACCIÓN (S-Q-R)

### A. SOURCE (Estímulo)
- **SRC_DIR:** Directo (Sin estímulo adicional).
- **SRC_TXT:** Texto / Reading.
- **SRC_AUD:** Audio MP3 / Listening.
- **SRC_IMG:** Imagen / Fotografía.
- **SRC_HYB:** Híbrido (Texto + Audio).

### B. QUESTION TYPE (Tarea)
- **QT_SEL:** Selección Simple (Test).
- **QT_MATCH:** Emparejamiento (A con B).
- **QT_CLZ_OPT:** Cloze con Opciones (Multiple Choice Cloze).
- **QT_CLZ_OPN:** Cloze Abierto (Open Cloze).
- **QT_TRF:** Transformación (Re-writing con keyword).
- **QT_PROD:** Producción Libre (Ensayo/Grabación).

### C. REQUEST MODE (Interfaz)
- **REQ_RADIO:** Radio Buttons (Vertical).
- **REQ_DROP:** Desplegables inline (para Cloze).
- **REQ_INPUT:** Caja de texto inline (para Cloze abierto).
- **REQ_DUAL:** Escritura Dual (Textarea + Upload simultáneo).
- **REQ_REC:** Grabadora Multimedia (Botones 45px).

## 3. ESPECIFICACIÓN DE ARQUETIPOS (ESTÁNDAR UGR)

### I. CEFR_LANGUAGES (Acreditación ACLES)
Estructura de 5 destrezas. Obligatorio soporte para alfabetos no latinos.
1. **Reading:** [SRC_TXT -> QT_SEL -> REQ_RADIO] y [SRC_TXT -> QT_CLZ_OPN -> REQ_DROP].
2. **Use of English:** 
   - [SRC_DIR -> QT_CLZ_OPT -> REQ_DROP] (Grammar Cloze).
   - [SRC_DIR -> QT_TRF -> REQ_INPUT] (Transformations).
3. **Listening:** [SRC_AUD -> QT_SEL -> REQ_RADIO] y [SRC_AUD -> QT_CLZ_OPN -> REQ_INPUT].
4. **Writing:** [SRC_TXT -> QT_PROD -> REQ_DUAL] (Soporte manuscrito vía JPG).
5. **Speaking:** [SRC_IMG/SRC_AUD -> QT_PROD -> REQ_REC].

### II. LOGIC_AND_TECH (Ingeniería ETSIIT)
1. **Theoretical:** [SRC_DIR -> QT_SEL -> REQ_RADIO].
2. **Problem Solving:** [SRC_DIR -> QT_PROD -> REQ_INPUT] con MathJax activado.

### III. SOCIO_LEGAL (Derecho UGR)
1. **Teoría Normativa:** [SRC_TXT -> QT_SEL -> REQ_RADIO].
2. **Dictamen Jurídico:** [SRC_TXT (Supuesto de Hecho) -> QT_PROD -> REQ_DUAL].

### IV. HEALTH_SCIENCES (Medicina ECOE)
1. **Diagnóstico:** [SRC_IMG (Placa/Síntoma) -> QT_SEL -> REQ_RADIO].
2. **Actuación Clínica:** [SRC_DIR -> QT_PROD -> REQ_DUAL].

### V. HUMANITIES_ARTS (Filosofía y Letras)
1. **Comentario de Fuente:** [SRC_TXT (Fragmento) -> QT_PROD -> REQ_DUAL].

## 4. ESTÁNDARES DE INTERFAZ (UI BINDINGS)
- **Botonera Cassette:** Botones redondos de 45px.
  - Reproductor: Play, Stop (obligatorio).
  - Grabadora: Record, Stop, Play, Save (confirmación visual).
- **Dual Writing:** El widget REQ_DUAL nunca es excluyente. Siempre muestra el Textarea y el área Dashed de subida juntos.
- **Cloze Engine:** Lógica de parseo de corchetes `[opcion1/opcion2]` para generar dropdowns dinámicos.

