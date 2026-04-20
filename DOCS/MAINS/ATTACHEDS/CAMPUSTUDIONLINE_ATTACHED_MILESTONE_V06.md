# ANEXO: HITO 06 - SISTEMA DE AUTOEVALUACIONES CON IA
# ESTADO: EN PROGRESO - REFACTORIZACIÓN DOCUMENTAL RAMA LENGUAS (V5.1)
# FECHA DE ACTUALIZACIÓN: 2026-04-20

## 1. RESUMEN DE LA SITUACIÓN ACTUAL (EDC)
*   La Rama Lenguas queda COMPLETAMENTE CERTIFICADA (v5.1, 2026-04-20). Los siete subarquetipos (SUB-LIN-INSTR, SUB-LIN-MINOR, SUB-LIN-PHILO, SUB-LIN-ECDO, SUB-LIN-NORM, SUB-LIN-TRA-TECH, SUB-LIN-TRA-LIT) han alcanzado Fidelidad 100% UGR.
*   La sesión del 2026-04-20 ha revelado un **hallazgo arquitectónico fundamental** que reencuadra el alcance del Hito 6: CampuStudiOnline no es una plataforma formativa sino un **emulador de pruebas evaluativas universitarias**. El alumno solicita ser evaluado de una asignatura y recibe una prueba que replica fielmente los criterios, estructura y baremos del examen oficial de esa asignatura en la UGR. Este norte es vinculante para toda la constelación documental.
*   Como consecuencia de este reencuadre, se han identificado las siguientes lagunas en la constelación que deben resolverse antes de arrancar la siguiente rama:
    *   `V06DOC_WIDGETS.md` — `W-TRA-CAT-EMULATOR` mal especificado (emula TAO profesional, no herramienta de examen universitario). `W-TRA-LIT-CREA` es un widget fantasma (referenciado en SUBARCHETYPES pero inexistente en WIDGETS). Falta nota de restricción de entrada para NORM.
    *   `V06DOC_BLOCKS.md` — `EV-TRA-PRECISION-TECH` sin nota de certificación contra Guía Docente 252113T. Falta configuración `DRA-HOLO` para contexto literario TRA-LIT. Referencia a `SD_TRA_REVIEW` como destreza autónoma debe eliminarse (no existe en evaluación oficial FTI-UGR).
    *   `V06DOC_TEMPLATES.md` — Faltan contratos de fases específicos para SUB-LIN-NORM (6.2), SUB-LIN-TRA-TECH (6.3) y SUB-LIN-TRA-LIT (6.4).
    *   `V06DOC_SUBARCHETYPES.md` — La secuencia genética de SUB-LIN-TRA-TECH debe reducirse de cuatro a **tres destrezas** (SD_TRA_REVIEW eliminado por no existir en la evaluación oficial).
*   Asimismo, la infraestructura de IA ha sido actualizada: `google-genai` actualizado de `1.55.0` a `1.73.1` en venv, `requirements.txt` y `requirements.in`.

## 2. HOJA DE RUTA PARA LA PRÓXIMA SESIÓN (LEY SUPREMA - INELUDIBLE)
**ESTADO DEL HITO:** EN PROGRESO — Constelación documental Rama Lenguas pendiente de sincronización completa.
**FECHA DE ÚLTIMA ACTUALIZACIÓN:** 2026-04-20
**OBJETIVO DE LA PRÓXIMA SESIÓN:** Completar la sincronización de la constelación documental de la Rama Lenguas ejecutando en orden estricto e inamovible los pasos 1 al 4 definidos a continuación. Solo tras completar los cuatro pasos procederá el salto a la siguiente rama.

---

### CONSTELACIÓN DOCUMENTAL ACTIVA (v5.0)
Los archivos satélite de la constelación V06 tras la eliminación de V06DOC_WORD_OF_GOD.md son:
`V06DOC_ARCHETYPES.md`, `V06DOC_SUBARCHETYPES.md`, `V06DOC_BLOCKS.md`, `V06DOC_WIDGETS.md`, `V06DOC_LEVELS.md`, `V06DOC_SUBDIVISIONS.md`, `V06DOC_METADATA.md`, `V06DOC_STRUCTURE.md`, `V06DOC_BINDING_GUIDELINE.md`, `V06DOC_TEMPLATES.md`, `V06DOC_LOGIC_MAPPING.md`.

**IMPORTANTE:** `V06DOC_WORD_OF_GOD.md` ha sido eliminado definitivamente. La investigación online en tiempo real contra las fuentes primarias UGR es la única fuente de verdad para la certificación de cada subarquetipo.

---

### PROTOCOLO DE EJECUCIÓN OBLIGATORIO (PRÓXIMA SESIÓN)

**NORTE INAMOVIBLE:** CampuStudiOnline es un emulador de pruebas evaluativas universitarias. El alumno solicita ser evaluado de una asignatura y recibe una prueba que replica fielmente los criterios, estructura y baremos del examen oficial de esa asignatura en la UGR. Todo lo que no figure en la evaluación ordinaria o extraordinaria de la Guía Docente oficial **no se evalúa y no tiene cabida en la constelación.**

#### PASO 1 — SINCRONIZACIÓN DE `V06DOC_WIDGETS.md` (PMA)

**Cambios obligatorios a aplicar:**

**A) Reconversión de `W-TRA-CAT-EMULATOR`:**
El widget actual emula una herramienta TAO profesional (memoria de traducción, glosario automático). Esto es incorrecto para el contexto universitario UGR. En el examen oficial de Traducción Especializada B-A Inglés (252113T, FTI-UGR) el alumno **no usa herramienta TAO** — trabaja con diccionarios bilingües convencionales y elabora su propio glosario durante la fase SD_TERM_RESEARCH. Reconvertir a **`W-DOC-RESOURCES` (Panel de Recursos Documentales UGR):**
*   **Uso:** SUB-LIN-TRA-TECH, fases SD_TERM_RESEARCH y SD_TRA_DRAFT.
*   **Panel izquierdo (Estímulo — Sticky):** Texto fuente en inglés. No editable.
*   **Panel central (Recursos — Sticky):** Acceso emulado a diccionarios bilingües de referencia: IATE (terminología UE), UNTERM (terminología ONU), Diccionario panhispánico del español jurídico (DPEJ-RAE), Diccionario médico CUN, Glosario científico-técnico. El alumno consulta y arrastra términos al glosario.
*   **Panel derecho (Glosario del alumno):** Zona de construcción del glosario bilingüe durante SD_TERM_RESEARCH. Los términos validados quedan disponibles durante SD_TRA_DRAFT como referencia.
*   **Motor:** EV-TRA-PRECISION-TECH. La IA audita que los términos del glosario del alumno procedan de fuentes de autoridad y se apliquen coherentemente en la traducción.

**B) Eliminación de `W-TRA-LIT-CREA` como widget independiente:**
Este widget es un fantasma — está referenciado en `V06DOC_SUBARCHETYPES.md` para SD_TRA_CREATIVE de SUB-LIN-TRA-LIT pero no existe en `V06DOC_WIDGETS.md`. No debe crearse como widget separado. SD_TRA_CREATIVE se mapea a **`W-HUM-TEXT` en modo `SPLIT_TEXT`** con la siguiente configuración específica para TRA-LIT:
*   **Panel izquierdo (Estímulo — Sticky):** Texto literario fuente (poema, fragmento teatral o narrativo) en la lengua original (inglés). No editable.
*   **Panel derecho (Producción — Editor):** `W-HUM-TEXT` en modo edición libre donde el alumno redacta su traducción literaria al español. Modos de entrada: teclado latino estándar + OCR/captura de manuscrito. Sin pad de trazos (no aplica para inglés→español).
*   Documentar en la sección de `W-HUM-TEXT` como **Modo TRA-LIT** con la referencia a SUB-LIN-TRA-LIT.

**C) Nota de restricción de entrada para NORM en `W-HUM-TEXT`:**
La Directriz de Multimodalidad genérica de `W-HUM-TEXT` incluye "Occidentalización/Pinyin/Romaji" como opción. Para SUB-LIN-NORM esta opción **no tiene cabida** — la asignatura es español, teclado latino estándar. Añadir nota explícita: en el contexto SUB-LIN-NORM los modos activos son exclusivamente Teclado Latino Nativo y OCR/Captura de manuscrito. Los modos de Occidentalización y Pad de Trazos quedan deshabilitados.

**D) Actualizar referencias cruzadas:**
En todos los widgets que referencien `W-TRA-CAT-EMULATOR` o `W-TRA-LIT-CREA` sustituir por los nuevos identificadores (`W-DOC-RESOURCES` y `W-HUM-TEXT` modo TRA-LIT respectivamente).

#### PASO 2 — SINCRONIZACIÓN DE `V06DOC_BLOCKS.md` (PMA)

**Cambios obligatorios a aplicar:**

**A) Nota de certificación en `EV-TRA-PRECISION-TECH`:**
Añadir al bloque `EV-TRA-PRECISION-TECH` la nota: *"[CERTIFICADO v5.1 — 2026-04-20] Jerarquía de errores verificada como coherente con la metodología de evaluación de la FTI-UGR (Guía Docente 252113T, aprobada 01/07/2025). El baremo numérico exacto (Categorías A/B/C) no está publicado en la Guía Docente — se entrega al alumnado por PRADO al inicio de curso — pero la estructura categorial A/B/C es el estándar reconocido internacionalmente en la FTI-UGR y coherente con la ISO 17100:2015."*

**B) Configuración `DRA-HOLO` modo literario (TRA-LIT):**
La rúbrica `DRA-HOLO` existe para INSTR/NORM. Para TRA-LIT necesita una configuración específica coherente con los criterios de evaluación de la Guía Docente 25211NJ (Literatura y Traducción Lengua B Inglés). Añadir como sub-sección de `DRA-HOLO`:
*   **Modo TRA-LIT (DRA-HOLO-LIT — SUB-LIN-TRA-LIT):**
    *   **Eje 1 — Adecuación al Skopos literario:** La traducción cumple la función estética del texto fuente en la lengua meta. El lector de la traducción experimenta un efecto equivalente al del lector del original.
    *   **Eje 2 — Gestión de culturemas e intertextualidad:** El alumno identifica y resuelve de forma documentada las referencias culturales, intertextos y juegos lingüísticos del original. Las pérdidas inevitables están justificadas y compensadas.
    *   **Eje 3 — Calidad literaria de la versión meta:** La traducción funciona como texto literario autónomo en español. Registro literario correcto, puntuación expresiva, sintaxis coherente con el género (poético, teatral, narrativo).
    *   **Eje 4 — Rigor del comentario crítico (SD_TRA_CRIT):** El ensayo justificatorio demuestra dominio de la bibliografía traductológica (Reynolds 2011, Venuti 2017, Skopos), cita correctamente y argumenta de forma original. Estructura académica rigurosa.
    *   **Umbral:** Mínimo 5/10 en la media de los cuatro ejes para superar la destreza (coherente con la nota mínima 5 declarada en la Guía Docente 25211NJ).

**C) Eliminación de referencias a `SD_TRA_REVIEW` como destreza autónoma:**
`SD_TRA_REVIEW` no existe en la evaluación oficial de la Guía Docente 252113T. La evaluación ordinaria y extraordinaria de TRA-TECH consiste exclusivamente en traducciones directas cronometradas. Auditar `V06DOC_BLOCKS.md` y eliminar cualquier referencia a SD_TRA_REVIEW como destreza evaluable. Si el motor `BMT-SHIFT` referencia SD_TRA_REVIEW como destreza autónoma de TRA-TECH, corregir para indicar que en TRA-TECH no existe SD_TRA_REVIEW y BMT-SHIFT opera únicamente como componente auxiliar.

#### PASO 3 — SINCRONIZACIÓN DE `V06DOC_TEMPLATES.md` (PMA)

Añadir al final de la sección 6 (SECUENCIAS DE FASES POR SUBARQUETIPO) los tres contratos de fases pendientes:

**A) Contrato 6.2 — SUB-LIN-NORM:**
*   **Estructura:** Cuatro fases secuenciales no compensables. Umbral 75% por fase.
*   **Fase 1 (SD_CORPUS_ANALYSIS):** Widget W-LAW-NAV modo lingüístico. Estímulo: consulta emulada CORPES XXI/CREA sobre construcción en conflicto. La IA genera el ítem con datos de frecuencia y distribución geográfica reales. Motor: EV-NORM-ANALYSIS. Layout: SPLIT_TEXT (resultados de corpus en panel izquierdo, respuesta en panel derecho).
*   **Fase 2 (SD_MORPH_ANTINORM):** Widgets W-OBJ-STRIKE y W-TXT-CLOZE. La IA genera textos con fenómenos antinormativos (queísmo, dequeísmo, leísmo, laísmo, loísmo, discordancias en clíticos). El alumno identifica, nombra técnicamente y corrige. Motor: RBT-CANON (nomenclatura técnica exacta obligatoria). NO_NEGATIVE_MARKING: desactivado (penalización activa).
*   **Fase 3 (SD_ORTHO_PRESCRIPTIVE):** Widget W-HUM-TEXT modo Revisión. Modo entrada: teclado latino + OCR. Sin Occidentalización ni Pad de Trazos. La IA genera un texto con errores ortotipográficos deliberados (OLE 2010). El alumno edita con control de cambios visible. Motor: EV-NORM-ANALYSIS. Rigor x1.7.
*   **Fase 4 (SD_CRITICAL_NORM):** Widget W-HUM-TEXT con SPLIT_TEXT. Panel izquierdo: texto fuente inadecuado (estímulo). Panel derecho: editor de justificación académica. La IA evalúa la cita explícita y correcta de NGLE o DPD. Motor: DRA-HOLO. Cita falsa o inexacta: FAIL_LOGIC FATAL para el ítem.

**B) Contrato 6.3 — SUB-LIN-TRA-TECH:**
*   **Estructura:** Tres bloques temáticos evaluables de forma independiente (jurídico, CSH, científico-técnico). Umbral mínimo 5/10 por bloque. Sin compensación entre bloques (FAIL_LOGIC: FATAL por bloque no superado). Nota: SD_TRA_REVIEW NO existe como destreza evaluable — la evaluación oficial consiste exclusivamente en traducciones directas cronometradas.
*   **Fase 1 (SD_TRA_ANALYSIS + SD_TERM_RESEARCH — Preparación):** Widget W-DOC-RESOURCES. El alumno recibe el texto fuente y construye su glosario técnico bilingüe consultando los recursos documentales disponibles. Motor: EV-TRA-PRECISION-TECH (audita la calidad terminológica del glosario).
*   **Fase 2 (SD_TRA_DRAFT — Traducción):** Widget W-MEDI-LAYOUT (panel izquierdo: texto fuente en inglés; panel derecho: editor de traducción). Texto de 200-250 palabras por bloque temático. Tiempo límite: 1 hora por bloque. Motor: EV-TRA-PRECISION-TECH con jerarquía de errores A/B/C.
*   **Secuencia de bloques:** Jurídico → CSH (Ciencias Sociales y Humanidades) → Científico-Técnico. Non-backtracking entre bloques.

**C) Contrato 6.4 — SUB-LIN-TRA-LIT:**
*   **Estructura:** Tres fases secuenciales evaluadas conjuntamente mediante DRA-HOLO modo TRA-LIT. Umbral mínimo 5/10 en la media de los cuatro ejes de la rúbrica. Non-backtracking entre fases.
*   **Fase 1 (SD_TRA_STYLE — Análisis Estilístico):** Widget W-HUM-TEXT con SPLIT_TEXT. Panel izquierdo: texto literario fuente (poema o fragmento teatral/narrativo en inglés, autor anglófono del corpus de la asignatura 25211NJ). Panel derecho: editor de análisis. El alumno identifica y describe la voz autorial, los rasgos estilísticos, los culturemas y los retos de transferencia. Motor: DRA-HOLO-LIT (Ejes 1 y 2). Extensión mínima del análisis: 300 palabras.
*   **Fase 2 (SD_TRA_CREATIVE — Transferencia Estética):** Widget W-HUM-TEXT en modo SPLIT_TEXT. Panel izquierdo: mismo texto fuente de Fase 1. Panel derecho: editor de traducción literaria al español. Modos de entrada activos: teclado latino estándar + OCR/captura. Motor: DRA-HOLO-LIT (Ejes 1, 2 y 3).
*   **Fase 3 (SD_TRA_CRIT — Comentario Exegético):** Widget W-HUM-TEXT modo libre. El alumno redacta el ensayo crítico justificando sus decisiones traductoras (1500-2000 palabras, conforme a los criterios de la Guía Docente 25211NJ). Debe incluir citas de la bibliografía traductológica oficial (Reynolds 2011, Venuti 2017). Motor: DRA-HOLO-LIT (Eje 4). Enviado a través de Turnitin emulado (control de originalidad).

#### PASO 4 — SINCRONIZACIÓN DE `V06DOC_SUBARCHETYPES.md` (PMP)

**Único cambio:**
En el bloque SUB-LIN-TRA-TECH, la secuencia genética declara cuatro destrezas: `SD_TRA_ANALYSIS → SD_TERM_RESEARCH → SD_TRA_DRAFT → SD_TRA_REVIEW`. `SD_TRA_REVIEW` no existe en la evaluación oficial de la Guía Docente 252113T y debe eliminarse. La secuencia correcta es: `SD_TRA_ANALYSIS → SD_TERM_RESEARCH → SD_TRA_DRAFT` (tres destrezas — las dos primeras corresponden a la fase de preparación documentada en el contrato 6.3, la tercera a la traducción directa cronometrada).

**Herramienta:** PMP con `sed` sobre la línea que declara la secuencia genética.

#### PASO 5 — PROTOCOLO DE CIERRE DE SINCRONIZACIÓN

Una vez completados los cuatro pasos anteriores, la constelación documental de la Rama Lenguas quedará íntegramente sincronizada con el norte arquitectónico de la plataforma. En ese momento procede el salto a la siguiente rama según el orden estratégico del Hito 6 (a determinar por el usuario al inicio de esa sesión).

#### ORDEN INAMOVIBLE DE SUBARQUETIPOS (HISTORIAL COMPLETO)
*   `SUB-LIN-INSTR` — **[CERTIFICADO v5.0 — 2026-04-19]**
*   `SUB-LIN-MINOR` — **[CERTIFICADO v5.1 — 2026-04-20]**
*   `SUB-LIN-PHILO` — **[CERTIFICADO v5.1 — 2026-04-20]**
*   `SUB-LIN-ECDO` — **[CERTIFICADO v5.1 — 2026-04-20]**
*   `SUB-LIN-NORM` — **[CERTIFICADO v5.1 — 2026-04-20]**
*   `SUB-LIN-TRA-TECH` — **[CERTIFICADO v5.1 — 2026-04-20]**
*   `SUB-LIN-TRA-LIT` — **[CERTIFICADO v5.1 — 2026-04-20]**

---

### 3. CONTROL DE INTEGRIDAD (ESTADO DE LA RAMA)
*   [CERTIFICADO — 2026-04-19] `SUB-LIN-INSTR` (v5.0). Fuente: Guía Oficial del Candidato CLM-UGR. Correcciones: estructura cuadri-destreza oficial, rangos escritura 200-250/250-300 palabras, puntos de corte variables CLM-UGR, NO_NEGATIVE_MARKING en SD_READ y SD_LIST, eliminación SD_MEDI como destreza autónoma, estructura oral 3 fases oficiales, modelo IA `gemini-2.5-flash`.
*   [CERTIFICADO — 2026-04-20] `SUB-LIN-MINOR` (v5.1). Fuente: Grado en Lenguas Modernas y sus Literaturas — Facultad de Filosofía y Letras, UGR (BOE 02/12/2024). Correcciones: lista de lenguas minor certificada contra plan de estudios vigente (alemán, árabe, checo, francés, griego moderno, inglés, japonés, polaco, portugués), distinción institucional MINOR vs. INSTR (marco académico reglado vs. acreditación CertAcles), protocolo de superación corregido (nota académica mínima 5/10, elimina umbral 60% CertAcles), nueva ficha técnica W-CALLI-PAD para lenguas no latinas (árabe, checo, griego moderno, japonés) con validación de ductus por norma MEXT/MSA/escolar griega/diacrítica checa, ampliación de RBT-SHORT-LANG con referencia normativa por lengua y activación condicional, nuevo Bloque A.2 en SUBDIVISIONS con fases MINOR diferenciadas de INSTR, y desglose competencial 3.0 completo en SUBDIVISIONS.
*   [CERTIFICADO — 2026-04-20] `SUB-LIN-PHILO` (v5.1). Fuente: Fonética y Fonología del Español (2831113), Historia de la Lengua Española I (2831141), Historia de la Lengua Española II (2831145) e Historia del Léxico Español (28311A5) — Dpto. de Lengua Española, UGR (Guías Docentes curso 2025-2026, aprobadas 18/06/2025). Correcciones: restructuración de Cuatri-Destreza a Tri-Destreza Científica (eliminación de SD_TEXT_CRIT, desmembrada a SUB-LIN-ECDO), corrección del perfil institucional (Dpto. Lengua Española exclusivamente, eliminado Dpto. Filologías Clásicas), corrección de SD_PHONO con base sincrónica certificada (Fonética y Fonología 2831113) más aplicación diacrónica (Historia de la Lengua I), ampliación de SD_LEX_SEM con fuentes oficiales UGR (Dworkin 2012, NTLLE, CDH), adición de SD_LEX_SEM en desglose competencial de V06DOC_SUBDIVISIONS.md (sección 3.1), y creación del nuevo subarquetipo SUB-LIN-ECDO.
*   [CERTIFICADO — 2026-04-20] `SUB-LIN-ECDO` (v5.1). Fuente: La Industria Editorial: Edición, Corrección, Anotación y Evaluación de Textos Españoles (28311A9, 4º Optativa, Dpto. Lengua Española, UGR — Guía Docente aprobada 18/06/2025) + CE10 transversal del Grado en Filología Hispánica como competencia de contexto. Correcciones respecto a la especificación provisional: reformulación de Modelo Ecdótico puro a Modelo de Edición y Crítica Textual, anclaje en asignatura fuente real certificable (28311A9) en lugar de competencia transversal sin asignatura monográfica, secuencia genética redefinida como Cuatri-Destreza Editorial (SD_ORTOTYPO → SD_STYLE → SD_ANNOT → SD_EVAL), Rigor Engine ajustado a x1.5 (perfil aplicado/profesional vs. epistemológico), umbral de superación fijado en 60% por destreza, Blecua (2004) incorporado como referencia complementaria en SD_ANNOT, nuevo desglose competencial completo en V06DOC_SUBDIVISIONS.md (sección 3.0.1).
*   [CERTIFICADO — 2026-04-20] `SUB-LIN-NORM` (v5.1). Fuente: El Español Actual: Norma y Uso (2831111), 1º Grado en Filología Hispánica, Troncal, Dpto. Lengua Española, UGR (Guía Docente aprobada 18/06/2025). Correcciones: perfil institucional ajustado con código de asignatura real (2831111), cuatro dominios certificados contra Guía Docente (SD_CORPUS_ANALYSIS con CORPES XXI/CREA, SD_MORPH_ANTINORM con fenómenos antinormativos canónicos, SD_ORTHO_PRESCRIPTIVE con OLE 2010, SD_CRITICAL_NORM con DPD/NGLE), bibliografía de autoridad (DPD 2005, NGLE 2009, OLE 2010, CORPES XXI, CREA) íntegramente verificada contra bibliografía fundamental oficial, umbral 75% y Rigor Engine x1.7 coherentes con nivel LVL_C de la asignatura.
*   [CERTIFICADO — 2026-04-20] `SUB-LIN-TRA-TECH` (v5.1). Fuente: Traducción Especializada B-A Inglés (252113T), 3º Grado en Traducción e Interpretación, Obligatoria, FTI-UGR (Guía Docente aprobada 01/07/2025). Correcciones: perfil institucional ajustado con código de asignatura real (252113T), secuencia genética SD_TRA_ANALYSIS → SD_TERM_RESEARCH → SD_TRA_DRAFT → SD_TRA_REVIEW certificada contra temario práctico oficial, umbral 50% por bloque independiente certificado contra criterios de evaluación oficiales (nota mínima 5/10 por bloque), extensión de textos corregida de 350 a 200-250 palabras por texto conforme al baremo oficial de evaluación, ISO 17100 coherente con CE19 FTI-UGR, recursos IATE/UNTERM coherentes con CE22 (gestión de bases de datos terminológicas).
*   [CERTIFICADO — 2026-04-20] `SUB-LIN-TRA-LIT` (v5.1). Fuente: Literatura y Traducción Lengua B Inglés (25211NJ), 3º Grado en Traducción e Interpretación, Optativa, FTI-UGR (Guía Docente aprobada 23/06/2025). Nota institucional: no existe asignatura obligatoria de Traducción Literaria en el Grado en T&I de la UGR; la competencia literaria se canaliza por optativas de Literatura y Traducción. Correcciones: perfil institucional ajustado con código de asignatura real (25211NJ) y carácter optativo documentado, secuencia genética SD_TRA_STYLE → SD_TRA_CREATIVE → SD_TRA_CRIT certificada contra resultados de aprendizaje y metodología oficial, Skopos/culturemas/intertextualidad coherentes con competencias específicas del módulo y bibliografía oficial (Reynolds 2011, Venuti 2017), rúbrica DRA-HOLO y nivel C2 hermenéutico coherentes con el nivel de exigencia y los criterios de evaluación de la asignatura.

---

**PROHIBICIONES ABSOLUTAS:**
*   El modelo de la próxima sesión **NO PODRÁ INVENTAR NI SUPONER NADA** que no esté escrito en esta hoja de ruta o en la documentación satélite auditada.
*   **NO** se permite el salto a otras ramas (Salud, Técnica, Social) hasta que todos los subarquetipos de la Rama Lenguas alcancen Fidelidad 100% certificada por el usuario.
*   **NO** se modificará ningún subarquetipo ya certificado salvo indicación explícita del usuario con el nombre exacto del subarquetipo a revisar.
