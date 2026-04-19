<!-- /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_ARCHETYPES.md -->
# V06DOC_ARCHETYPES - PLANO MAESTRO DE ACREDITACIÓN UGR (V2.0 - ENFOQUE SUBATÓMICO)

## 1. ARQUETIPO: LENGUAS EXTRANJERAS (MODELO INSTRUMENTAL Y CERTIFICACIÓN OFICIAL UGR/CERTACLES)
*   **Denominación Oficial:** Arquetipo de Evaluación de Lenguas Extranjeras (Acreditación Oficial CertAcles / Centro de Lenguas Modernas UGR).
*   **Mecánica de Ejecución y Flujo:** 
    *   **Secuencialidad Estricta:** Navegación unidireccional forzada.
    *   **Time-Boxing:** Sistema de bloqueo temporal hermético por cada destreza evaluada.
    *   **Non-Backtracking:** Prohibición absoluta de retroceso a secciones anteriores una vez completadas, garantizando la validez de la prueba de dominio y evitando la corrección a posteriori basada en el input de destrezas posteriores.
    *   **Formato Binivel (Adaptativo):** Capacidad arquitectónica para evaluar dos niveles del MCERL simultáneamente (ej. B1/B2 o B2/C1) mediante escalada de dificultad adaptativa en los ítems y rúbricas dinámicas.
*   **Objetivo de Acreditación (Fin):** Certificación oficial, legal y vinculante de la competencia comunicativa y operativa integral bajo los descriptores del Marco Común Europeo de Referencia para las Lenguas (MCERL).
*   **Itinerarios Pedagógicos (Ejes UGR):**
    *   **Eje I (Funcional/Instrumental - CertAcles):** Competencia operativa para estudiantes no especialistas (Requisito de Grado).
    *   **Eje II (Científico-Filológico - MAIOR):** Grados en Filología y Traducción. Foco en el metalenguaje, la diacronía, la fonética histórica y el análisis científico de la lengua.
    *   **Eje III (Instrumental-Transversal - MINOR):** Competencia bilingüe añadida para otras ramas de conocimiento. Exigencia ineludible de dominio caligráfico explícito (trazos) en lenguas no occidentales (Árabe, Chino, Japonés, Ruso, Hebreo).
*   **Niveles de Acreditación (MCERL):** A1 (Acceso), A2 (Plataforma), B1 (Umbral), B2 (Avanzado), C1 (Dominio Operativo Eficaz), C2 (Maestría).
*   **Desglose Integral de Destrezas (Estructura Cuadri-Dimensional Oficial CLM-UGR — v5.0):**
    1.  **Comprensión de Lectura (Reading — 75 min):** 5 textos binivel (2×B1 + 1 bisagra + 2×B2), aproximadamente 40 ítems. Tipos: respuesta múltiple, reintegración de fragmento, emparejamiento y respuesta corta (máx. 4 palabras). Sin penalización por respuesta incorrecta.
    2.  **Comprensión Auditiva (Listening — aprox. 45 min):** 5 grabaciones binivel (2×B1 + 1 bisagra + 2×B2), aproximadamente 40 ítems. Tipos: respuesta múltiple, emparejamiento y respuesta corta (máx. 4 palabras). Límite estricto de 2 reproducciones por pista. Sin penalización por respuesta incorrecta.
    3.  **Expresión e Interacción Escritas (Writing — 60 min):** 2 tareas de distinta tipología. Tarea B1: 200-250 palabras (carta, email informal/neutro, narración, artículo, blog, informe). Tarea B2: 250-300 palabras (carta, email formal, artículo, informe, ensayo, narración, reseña). Rúbrica DRA-HOLO: cumplimiento de la tarea, coherencia y cohesión, competencia lingüística general, corrección gramatical, dominio y riqueza de vocabulario.
    4.  **Expresión e Interacción Orales (Speaking — 10 min):** Entrevista individual con examinador nativo del CLM. Tres fases: (A) preguntas sobre vida cotidiana (B1), (B) descripción y análisis de fotografía (B1/B2), (C) opinión argumentada sobre tema propuesto (B1/B2). Rúbrica: alcance y corrección gramatical y léxica, fluidez, coherencia y cohesión.
    *   **NOTA CRÍTICA (v5.0):** La Mediación Lingüística NO constituye una destreza independiente en el examen oficial CertAcles del CLM-UGR. Queda eliminada como quinta destreza de este arquetipo.
*   **Bloques de Evaluación Atómicos (Widgets y Motores — SUB-LIN-INSTR):**
    *   Respuesta Múltiple sin penalización (W-OBJ-STRIKE / Motor: MAT-LINK — NO_NEGATIVE_MARKING activo).
    *   Rellenado de Huecos Abierto (CLO-OPEN) y Selectivo (CLO-MULTI) — Widget: W-TXT-CLOZE.
    *   Emparejamiento (MAT-LINK) — Widget: W-MIX-MATCH.
    *   Respuesta Corta hasta 4 palabras (RBT-SHORT-LANG) con Fuzzy Matching de tolerancia mínima.
    *   Producción Escrita con Rúbrica Analítica Holística (DRA-HOLO) — Widget: W-HUM-TEXT / W-OCR-PRO.
    *   Interacción Oral con UniversIA (DIA-INTERACT) — Widget: W-COMM-DIALOG.
*   **Criterio de Éxito y Superación (Sistema Oficial CLM-UGR 2026 — v5.0):**
    *   **Mecanismo de Puntos de Corte Binivel:** La acreditación del nivel B1 o B2 en cada destreza se determina mediante puntos de corte variables fijados por convocatoria siguiendo las pautas del Consejo de Europa. No existe un umbral fijo del 60%: los puntos de corte se establecen mediante análisis estadístico de la distribución de respuestas de cada convocatoria.
    *   **Obligatoriedad de Superación por Destreza:** El alumno debe alcanzar el nivel objetivo en las CUATRO destrezas de forma independiente. La compensación entre destrezas no está permitida.
    *   **Gestión del Fallo Parcial:** Si el alumno no supera una única destreza, puede repetirla en convocatoria posterior en un plazo máximo de un año (FAIL_LOGIC: PARTIAL_RETRY). Si son dos o más destrezas, debe repetir el examen completo.

## 2. ARQUETIPO: CIENCIAS DE LA SALUD (ECOE)
*   **Mecánica:** Rotación por estaciones cronometradas e independientes.
*   **Fin:** Validación de competencia clínica y seguridad del paciente.
*   **Itinerarios:** Medicina, Enfermería, Farmacia, Odontología.
*   **Niveles:** Básico (Fundamentos), Intermedio, Avanzado (Rotatorio).
*   **Destrezas:** Anamnesis, Exploración, Juicio Diagnóstico, Comunicación, Técnica.
*   **Bloques:** Entrevista, Interpretación de Pruebas, Checklist Procedimental, Ética.
*   **Criterio de Éxito:** Checklist Dicotómico + Escala Likert. Errores fatales invalidantes.

## 3. ARQUETIPO: CIENCIAS TÉCNICAS E INGENIERÍA (RESOLUTIVO)
*   **Mecánica:** Desarrollo de larga duración con validación de procesos.
*   **Fin:** Acreditación de capacidad de diseño y resolución bajo normativa.
*   **Itinerarios:** Ingeniería (Software/Civil/Industrial), Arquitectura, Ciencias Puras.
*   **Niveles:** Teórico-Práctico (Grado), Profesional (Máster), Investigador.
*   **Destrezas:** Modelado, Precisión, Algoritmia, Diseño Estructural, Análisis de Error.
*   **Bloques:** Resolución de Ecuaciones, Debugging, Diseño de Planos, Demostración.
*   **Criterio de Éxito:** Ponderación por fases. El planteamiento lógico prima (50%).

## 4. ARQUETIPO: CIENCIAS SOCIALES Y JURÍDICAS (CASUÍSTICO)
*   **Mecánica:** Análisis de supuestos de hecho y aplicación de normativa.
*   **Fin:** Capacidad de dictaminar y resolver conflictos institucionales/económicos.
*   **Itinerarios:** Derecho, Economía/ADE, Sociología, Políticas.
*   **Niveles:** Introductorio, Especialización, Profesional (Dictamen).
*   **Destrezas:** Encuadre Normativo, Argumentación, Interpretación de Datos, Síntesis.
*   **Bloques:** Caso Práctico, Auditoría Financiera, Análisis Estadístico, Simulación de Juicio.
*   **Criterio de Éxito:** Suficiencia de Fundamentación. Uso de fuentes reales como multiplicador.

## 5. ARQUETIPO: ARTES Y HUMANIDADES (HERMENÉUTICO)
*   **Mecánica:** Disertación dialéctica y análisis de fuentes primarias.
*   **Fin:** Acreditación de madurez intelectual y capacidad crítica.
*   **Itinerarios:** Filología, Historia, Filosofía, Arte, Educación.
*   **Niveles:** Descriptivo, Analítico, Crítico-Sintético.
*   **Destrezas:** Crítica de Fuentes, Contextualización, Calidad Discursiva, Paleografía.
*   **Bloques:** Comentario de Texto, Comparativa de Fuentes, Ensayo, Diseño Didáctico.
*   **Criterio de Éxito:** Rúbrica Holística. La corrección formal es eliminatoria (-2 puntos).

## 6. ARQUETIPO: CIENCIAS PURAS Y EXPERIMENTALES (METODOLÓGICO/EMPÍRICO)
*   **Mecánica:** Rigor deductivo formal, validación de hipótesis y experimentación analítica.
*   **Fin:** Acreditación de capacidad analítica, formulación de modelos y trabajo de campo/laboratorio.
*   **Itinerarios:** Biología, Química, Física, Geología, Ambientales, Ciencia de Datos.
*   **Niveles:** Introductorio, Aplicado, Investigador.
*   **Destrezas:** Modelado formal, Precisión algorítmica, Análisis de datos, Método científico.
*   **Bloques Típicos:** Resolución algorítmica, Demostración matemática, Análisis de laboratorio.
*   **Criterio de Éxito:** Exactitud analítica y rigor absoluto en el método científico.
