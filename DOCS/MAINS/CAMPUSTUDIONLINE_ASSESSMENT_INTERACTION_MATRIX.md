# MATRIZ DE INTERACCIÓN DE EVALUACIONES (UI/UX REGISTRY)
# Este documento define la relación Source -> Question -> Response para "Templates Tontas".

## 1. PRINCIPIO DE DISEÑO
El Backend determina el `render_mode`. El Frontend solo obedece y pinta el widget correspondiente. No hay lógica de negocio en el HTML.

## 2. CATÁLOGO DE VARIABLES

### A. SOURCE (El Estímulo)
| ID | Descripción | Ejemplo |
| :--- | :--- | :--- |
| **SRC_TXT** | Texto plano o Markdown | Reading Comprehension |
| **SRC_AUD** | Archivo de Audio (MP3) | Listening Comprehension |
| **SRC_IMG** | Imagen estática | Descripción de foto (Speaking) |
| **SRC_HYB** | Texto + Audio | Listening con soporte textual |
| **SRC_DIR** | Directo (Sin estímulo) | Preguntas de gramática aislada |

### B. QUESTION TYPE (La Tarea)
| ID | Descripción | Lógica de Validación |
| :--- | :--- | :--- |
| **QT_SEL** | Selección Simple | Match exacto de ID opción |
| **QT_CLZ_OPT** | Cloze con Opciones | Match exacto en cada hueco |
| **QT_CLZ_OPN** | Cloze Abierto | Match semántico/exacto de string |
| **QT_TRF** | Transformación | Match de estructura clave (Keyword Transformation) |
| **QT_PROD** | Producción Libre | Evaluación por IA (Rubric) |

### C. REQUEST MODE (El Widget de Usuario)
| ID | Descripción | Componentes UI |
| :--- | :--- | :--- |
| **REQ_RADIO** | Radio Buttons | Lista vertical de opciones |
| **REQ_DROP** | Dropdowns Inline | Selectores insertados en el texto |
| **REQ_INPUT** | Inputs Inline | Cajas de texto cortas insertadas en texto |
| **REQ_DUAL** | Escritura Dual | Textarea + File Upload (Dashed) |
| **REQ_REC** | Grabadora | Botones: Record/Stop/Play/Reset |

## 3. MATRIZ DE RENDERIZADO (COMBINACIONES VÁLIDAS)

### GRUPO 1: COMPRENSIÓN LECTORA (READING)
1. **R_TXT_SEL** (Source: TXT -> Task: SEL -> Req: RADIO)
   - *Uso:* Reading estándar.
2. **R_TXT_CLZ** (Source: TXT -> Task: CLZ_OPN -> Req: DROP/INPUT)
   - *Uso:* Gapped Text (frases eliminadas).

### GRUPO 2: USO DE LA LENGUA (USE OF ENGLISH)
3. **R_DIR_CLZ_OPT** (Source: DIR -> Task: CLZ_OPT -> Req: DROP)
   - *Uso:* Multiple Choice Cloze.
4. **R_DIR_CLZ_OPN** (Source: DIR -> Task: CLZ_OPN -> Req: INPUT)
   - *Uso:* Open Cloze.
5. **R_DIR_TRF** (Source: DIR -> Task: TRF -> Req: INPUT)
   - *Uso:* Key Word Transformation.

### GRUPO 3: COMPRENSIÓN AUDITIVA (LISTENING)
6. **R_AUD_SEL** (Source: AUD -> Task: SEL -> Req: RADIO)
   - *Uso:* Listening estándar.
7. **R_AUD_CLZ** (Source: AUD -> Task: CLZ_OPN -> Req: INPUT)
   - *Uso:* Sentence Completion (rellenar huecos escuchando).

### GRUPO 4: EXPRESIÓN ESCRITA (WRITING)
8. **R_TXT_PROD** (Source: TXT -> Task: PROD -> Req: DUAL)
   - *Uso:* Essay, Email, Report (Respuesta al prompt).

### GRUPO 5: EXPRESIÓN ORAL (SPEAKING)
9. **R_AUD_REC** (Source: AUD -> Task: PROD -> Req: REC)
   - *Uso:* Respuesta a pregunta oral.
10. **R_IMG_REC** (Source: IMG -> Task: PROD -> Req: REC)
    - *Uso:* Descripción de imagen.

