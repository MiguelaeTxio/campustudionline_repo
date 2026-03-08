# PLAN MAESTRO DE AUDITORÍA DE ESPECTRO COMPLETO (V4.0)
# ESTE DOCUMENTO ES LA ÚNICA FUENTE DE VERDAD PARA LA VALIDACIÓN DEL HITO 6.
# EXIGE LA COMPROBACIÓN LITERAL DE CADA PUNTO. NO SE ADMITEN SUPOSICIONES.

## 1. AUDITORÍA DE INTEGRIDAD DOCUMENTAL (10 ARCHIVOS VS CÓDIGO)
El modelo debe verificar que la lógica del código respeta las definiciones canónicas:

1.  **V06DOC_ARCHETYPES.md:** Verificar en `models.py` que existen `ARCH_LANG`, `ARCH_HEALTH`, `ARCH_TECH`, `ARCH_SOC`, `ARCH_HUM`, `ARCH_SCI`.
2.  **V06DOC_SUBARCHETYPES.md:** Verificar en `models.py` (Enum `SubArchetype`) la existencia literal de los 45 IDs.
3.  **V06DOC_LEVELS.md:** Verificar en `base.py` la lógica de `rigor_factor` (0.8, 1.0, 1.3, 1.6).
4.  **V06DOC_WIDGETS.md:** Verificar en `exam_take.html` (o `_exam_widgets.html`) la existencia de HTML para los 7 widgets.
5.  **V06DOC_BLOCKS.md:** Verificar en las estrategias (`strategies/*.py`) la lógica de calificación (`grade_item`) para cada bloque.
6.  **V06DOC_METADATA.md:** Verificar en `models.py` los Enums de `FeedbackTaxonomy` y `CompetencyDomain`.
7.  **V06DOC_TEMPLATES.md:** Verificar en `gemini_schemas.py` que el JSON coincide con el contrato de plantilla.
8.  **V06DOC_STRUCTURE.md:** Verificar en `base.py` la firma `get_exam_skeleton`.
9.  **V06DOC_LOGIC_MAPPING.md:** Verificar en `logic.py` la deducción de Itinerarios (`ITIN_MAI`, `ITIN_MIN`, etc.).
10. **V06DOC_URGENCY_ROADMAP.md:** Confirmar que el parche de emergencia (firmas y adjuntos) está aplicado en todos los archivos.

---

## 2. MATRIZ DE AUDITORÍA DE FLUJO (45 SUBARQUETIPOS)
Para CADA subarquetipo, se debe verificar el TRIÁNGULO DE FLUJO:
*   (A) **Python Skeleton:** `if sid == 'ID': ...` (Definición correcta de widgets y layout).
*   (B) **Prompt Binding:** `get_user_prompt` inyecta instrucciones específicas y JSON.
*   (C) **Renderizado:** El HTML final muestra los controles correctos.

### GRUPO 1: ARTES Y HUMANIDADES (STRATEGY: `humanities.py`)
1.  **SUB-LIN-INSTR (Lenguas):** (A) Destrezas 5-skills. (B) Prompt: Bilingüe/Objetivo. (C) Widget: `W-TXT-CLOZE` (Inputs).
2.  **SUB-LIN-MINOR (Lenguas):** (A) Nivel bajo. (B) Prompt: Apoyo/Tutor. (C) Widget: `W-MIX-MATCH`.
3.  **SUB-LIN-PHILO (Filología):** (A) Fonética/Historia. (B) Prompt: Rigor filológico. (C) Widget: `W-HUM-TEXT`.
4.  **SUB-LIN-NORM (Normativa):** (A) Corrección. (B) Prompt: Análisis de error. (C) Widget: `W-TXT-CLOZE`.
5.  **SUB-LIN-TRA-TECH (Traducción):** (A) Glosarios. (B) Prompt: Terminología técnica. (C) Widget: `W-HUM-TEXT` (Split).
6.  **SUB-LIN-TRA-LIT (Literaria):** (A) Estilística. (B) Prompt: Matices. (C) Widget: `W-HUM-TEXT` (Split).
7.  **SUB-HUM-HIST (Historia):** (A) Fuentes. (B) Prompt: Cronología/Fuentes. (C) Widget: `W-HUM-TEXT` (Split).
8.  **SUB-HUM-PHIL (Filosofía):** (A) Dialéctica. (B) Prompt: Lógica argumental. (C) Widget: `W-HUM-TEXT` (Split).
9.  **SUB-HUM-ART-HIST (H. Arte):** (A) Iconografía. (B) Prompt: Descripción formal. (C) Widget: `W-HUM-TEXT` (Split + Imagen).
10. **SUB-HUM-ART-CREA (Bellas Artes):** (A) Técnica. (B) Prompt: Proceso matérico. (C) Widget: `W-HUM-TEXT` (Split + Imagen).
11. **SUB-HUM-MUS (Música):** (A) Partitura. (B) Prompt: Armonía. (C) Widget: `W-HUM-TEXT` (Split + Audio/Img).
12. **SUB-HUM-ANTH (Antropología):** (A) Etnografía. (B) Prompt: Estructuras culturales. (C) Widget: `W-HUM-TEXT` (Split).

### GRUPO 2: CIENCIAS DE LA SALUD (STRATEGY: `health.py`)
13. **SUB-SAN-MED-CLIN (Medicina):** (A) Diagnóstico. (B) Prompt: Diferencial. (C) Widget: `W-OBJ-STRIKE`.
14. **SUB-SAN-MED-BASIC (Básicas):** (A) Anatomía. (B) Prompt: Identificación. (C) Widget: `W-CLIN-SCAN` (Zoom).
15. **SUB-SAN-ODON (Odonto):** (A) Dental. (B) Prompt: Radiología. (C) Widget: `W-CLIN-SCAN`.
16. **SUB-SAN-FISIO (Fisio):** (A) Función. (B) Prompt: Palpación. (C) Widget: `W-CLIN-SCAN`.
17. **SUB-SAN-CUID (Enfermería):** (A) NANDA. (B) Prompt: Protocolos. (C) Widget: `W-PROC-ACTION` (Checklist).
18. **SUB-SAN-LAB (Laboratorio):** (A) Analítica. (B) Prompt: Valores ref. (C) Widget: `W-OBJ-STRIKE`.
19. **SUB-SAN-PSY-CLIN (Psico Clín):** (A) DSM-5. (B) Prompt: Criterios. (C) Widget: `W-HUM-TEXT` (Caso).
20. **SUB-SAN-PSY-EXP (Psico Exp):** (A) Metodología. (B) Prompt: Diseño exp. (C) Widget: `W-OBJ-STRIKE`.
21. **SUB-SAN-VET (Veterinaria):** (A) Zoonosis. (B) Prompt: Clínica animal. (C) Widget: `W-CLIN-SCAN`.
22. **SUB-SAN-NUT (Nutrición):** (A) Dietética. (B) Prompt: Bromatología. (C) Widget: `W-OBJ-STRIKE`.

### GRUPO 3: SOCIALES Y JURÍDICAS (STRATEGY: `social.py`)
23. **SUB-SOC-LAW-PROC (Procesal):** (A) Plazos. (B) Prompt: Ley Enjuiciamiento. (C) Widget: `W-LAW-NAV` (Simulador).
24. **SUB-SOC-LAW-DICT (Dictamen):** (A) Jurisprudencia. (B) Prompt: Resolución. (C) Widget: `W-HUM-TEXT` (Split).
25. **SUB-SOC-ECON-QUAN (Cuantitativa):** (A) Econometría. (B) Prompt: Modelos. (C) Widget: `W-OBJ-STRIKE`.
26. **SUB-SOC-ECON-MGMT (Empresa):** (A) Estrategia. (B) Prompt: Casos negocio. (C) Widget: `W-HUM-TEXT`.
27. **SUB-SOC-EDU-KIDS (Magisterio):** (A) DUA/LOMLOE. (B) Prompt: Sit. Aprendizaje. (C) Widget: `W-HUM-TEXT`.
28. **SUB-SOC-EDU-SEC (Secundaria):** (A) Didáctica. (B) Prompt: Unidades didácticas. (C) Widget: `W-HUM-TEXT`.
29. **SUB-SOC-COMM-JOUR (Periodismo):** (A) Redacción. (B) Prompt: Ética/Estilo. (C) Widget: `W-HUM-TEXT`.
30. **SUB-SOC-COMM-AV (Audiovisual):** (A) Guion. (B) Prompt: Escaleta. (C) Widget: `W-HUM-TEXT` (Split).
31. **SUB-SOC-GEOG (Geografía):** (A) SIG/Mapas. (B) Prompt: Territorio. (C) Widget: `W-CLIN-SCAN` (Mapas).
32. **SUB-SOC-WORK (Trabajo Soc):** (A) Intervención. (B) Prompt: Mediación. (C) Widget: `W-HUM-TEXT`.

### GRUPO 4: INGENIERÍA Y ARQUITECTURA (STRATEGY: `tech.py`)
33. **SUB-TEC-SOFT (Software):** (A) Código. (B) Prompt: Algoritmia. (C) Widget: `W-TECH-CALC` (Traza).
34. **SUB-TEC-CIVIL (Civil):** (A) Estructuras. (B) Prompt: CTE/EHE. (C) Widget: `W-TECH-CALC`.
35. **SUB-TEC-INDUS (Industrial):** (A) Termo. (B) Prompt: Ciclos. (C) Widget: `W-TECH-CALC`.
36. **SUB-TEC-CHEM (Ing. Quím):** (A) Reactores. (B) Prompt: Balances. (C) Widget: `W-TECH-CALC`.
37. **SUB-TEC-PROJ (Arquitectura):** (A) Proyecto. (B) Prompt: Composición. (C) Widget: `W-HUM-TEXT` (Planos).
38. **SUB-TEC-CONS (Edificación):** (A) Obra. (B) Prompt: Seguridad/Materiales. (C) Widget: `W-OBJ-STRIKE`.
39. **SUB-TEC-PURE (Física/Mat):** (A) Demostración. (B) Prompt: Rigor formal. (C) Widget: `W-TECH-CALC` (LaTeX).

### GRUPO 5: CIENCIAS PURAS (STRATEGY: `science.py`)
40. **SUB-SCI-BIO (Biología):** (A) Genética. (B) Prompt: Taxonomía. (C) Widget: `W-OBJ-STRIKE` / `W-TECH-CALC`.
41. **SUB-SCI-CHEM (Química):** (A) Síntesis. (B) Prompt: Orgánica/Inorg. (C) Widget: `W-TECH-CALC`.
42. **SUB-SCI-PHYS (Física):** (A) Teórica. (B) Prompt: Leyes conservación. (C) Widget: `W-TECH-CALC`.
43. **SUB-SCI-GEOL (Geología):** (A) Cortes. (B) Prompt: Estratigrafía. (C) Widget: `ILC-CONTEXT` (Imagen).
44. **SUB-SCI-ENV (Ambientales):** (A) Impacto. (B) Prompt: Gestión residuos. (C) Widget: `ILC-CONTEXT`.
45. **SUB-SCI-DATA (Datos):** (A) Estadística. (B) Prompt: ML/Probabilidad. (C) Widget: `W-TECH-CALC`.

---

## 3. AUDITORÍA DE RENDERIZADO HTML (WIDGETS)
Verificar en `_exam_widgets.html` o `exam_take.html` la existencia de bloques condicionales para:
1.  **W-OBJ-STRIKE:** Loop sobre `item.content.options`. Inputs Radio/Checkbox. Feedback oculto hasta respuesta.
2.  **W-TXT-CLOZE:** Parseo de `[gap]`. Generación de inputs `name="gap_{{forloop.counter}}"`.
3.  **W-MIX-MATCH:** Contenedores Flex/Grid `.left-col`, `.right-col`. JS de conexión (LeaderLine o similar).
4.  **W-HUM-TEXT:** Editor TinyMCE/Quill o Textarea. Contenedor Split si `layout_mode='SPLIT_TEXT'`.
5.  **W-LAW-NAV:** Iframe o simulador de búsqueda. Input de selección de artículos.
6.  **W-TECH-CALC:** Librería MathJax cargada. Input multilínea o estructurado para pasos (`RPP-TRAZA`).
7.  **W-CLIN-SCAN:** Visor OpenSeadragon o similar (Zoom). Botones de herramientas (Regla, ROI).
8.  **W-PROC-ACTION:** Tabla de Checklist (`CDS-KILL`). Inputs Checkbox.

## 4. INSTRUCCIONES DE EJECUCIÓN OBLIGATORIA
El modelo debe iterar la lista del 1 al 45. Si encuentra un fallo (ej: `SUB-HUM-ANTH` no tiene rama `if` en `humanities.py`), debe **DETENERSE Y CORREGIRLO** antes de continuar.
No se admite "el resto está bien". Se debe imprimir el estado de cada uno: [OK] o [FIXED].

