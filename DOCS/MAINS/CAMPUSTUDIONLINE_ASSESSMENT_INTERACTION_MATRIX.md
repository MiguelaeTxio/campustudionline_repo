# MATRIZ DE INTERACCIÓN DE EVALUACIONES (ESTÁNDAR UGR / ACLES)
# Versión: 2.0 (Alineación Total con CLM-UGR)

## 1. PRINCIPIO DE DISEÑO
El sistema es una "Template Tonta". El Backend define el `render_mode`. Si el documento no lo contempla, el sistema no existe.

## 2. CATÁLOGO AMPLIADO DE VARIABLES (EMULADOR UGR)

### A. SOURCE (El Estímulo)
| ID | Descripción | Ejemplo UGR |
| :--- | :--- | :--- |
| **SRC_TXT** | Texto / Reading | Artículo de prensa, fragmento literario |
| **SRC_AUD** | Audio MP3 / Listening | Monólogo, diálogo, noticia radiofónica |
| **SRC_IMG** | Imagen / Gráfico | Fotografía para descripción (Speaking) |
| **SRC_HYB** | Híbrido | Vídeo con subtítulos o texto con apoyo audio |
| **SRC_DIR** | Directo | Gramática aislada (Use of English) |

### B. QUESTION TYPE (La Tarea Cognitiva)
| ID | Descripción | Lógica UGR |
| :--- | :--- | :--- |
| **QT_SEL** | Selección Múltiple | Elegir A, B, C o D |
| **QT_MATCH** | Emparejamiento | Unir Títulos (1-5) con Párrafos (A-E) |
| **QT_ORDER** | Ordenación | Secuenciar eventos (1º, 2º, 3º...) |
| **QT_CLZ_OPT** | Multiple Choice Cloze | Huecos con opciones desplegables |
| **QT_CLZ_OPN** | Open Cloze | Rellenar hueco con palabra exacta |
| **QT_TRF** | Transformación | Keyword Transformation (Re-writing) |
| **QT_PROD** | Producción Libre | Writing (Ensayo) o Speaking (Grabación) |

### C. REQUEST MODE (El Widget de Interfaz)
| ID | Descripción | Implementación UI |
| :--- | :--- | :--- |
| **REQ_RADIO** | Radio Buttons | Lista vertical única |
| **REQ_DROP** | Dropdowns Inline | Selectores dentro del flujo del texto |
| **REQ_INPUT** | Inputs Inline | Cajas de texto cortas dentro del texto |
| **REQ_MATCH** | Matriz de Emparejamiento | Tabla de premisas con selectores de respuesta |
| **REQ_ORDER** | Lista de Ordenación | Inputs numéricos junto a cada ítem de la lista |
| **REQ_DUAL** | Escritura Dual | Textarea + File Upload (Dashed) |
| **REQ_REC** | Grabadora Cassette | Botones 45px: Play, Stop, Rec, Save |

## 3. COMBINACIONES VÁLIDAS (MAPEO DE EXAMEN REAL)

### BLOQUE 1: READING (Comprensión Lectora)
- **R_TXT_SEL:** Reading estándar (Multiple Choice).
- **R_TXT_MATCH:** Heading to Paragraph (Emparejar títulos).
- **R_TXT_CLZ:** Gapped Text (Huecos en texto).

### BLOQUE 2: LISTENING (Comprensión Auditiva)
- **R_AUD_SEL:** Listening estándar.
- **R_AUD_ORDER:** Event Sequencing (Ordenar lo escuchado).
- **R_AUD_CLZ:** Sentence Completion (Rellenar escuchando).

### BLOQUE 3: USE OF ENGLISH (Gramática/Vocabulario)
- **R_DIR_CLZ_OPT:** Multiple Choice Cloze.
- **R_DIR_CLZ_OPN:** Open Cloze.
- **R_DIR_TRF:** Key Word Transformations.

### BLOQUE 4: WRITING / SPEAKING (Producción)
- **R_TXT_PROD:** Writing con prompt textual (REQ_DUAL).
- **R_IMG_REC:** Speaking basado en imagen (REQ_REC).
- **R_AUD_REC:** Speaking basado en pregunta oral (REQ_REC).

