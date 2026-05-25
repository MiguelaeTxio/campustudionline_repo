# ANEXO: HITO 06 - SISTEMA DE AUTOEVALUACIONES CON IA
# ESTADO: EN PROGRESO - FASE DE IMPLEMENTACIÓN ACTIVA (S020/S021)
# FECHA DE ACTUALIZACIÓN: 2026-05-24

## 1. RESUMEN DE LA SITUACIÓN ACTUAL (EDC)

La **Rama Ciencias de la Salud** queda **COMPLETAMENTE CERTIFICADA Y SINCRONIZADA (v5.4, 2026-04-25)**. Los 18 subarquetipos han alcanzado Fidelidad 100% UGR/UCO en sesión única. La constelación documental ha sido actualizada íntegramente:

*   `V06DOC_SUBARCHETYPES.md` — Bloques SUB-SAN-MED-CLIN, SUB-SAN-MED-BASIC, SUB-SAN-MED-FISIO-GEN, SUB-SAN-MED-FISIO-NEURO, SUB-SAN-CUID, SUB-SAN-ODON, SUB-SAN-FISIO, SUB-SAN-BIOQUIM, SUB-SAN-FARM, SUB-SAN-PSY-DIAG, SUB-SAN-PSY-EVAL, SUB-SAN-PSY-MET, SUB-SAN-PSY-STAT, SUB-SAN-VET-CLIN, SUB-SAN-VET-CIR, SUB-SAN-NUT-DIET, SUB-SAN-NUT-BROM y SUB-SAN-NUT-SPUB completos con perfiles institucionales, secuencias genéticas, protocolos de superación y rigor certificados contra Guías Docentes UGR/UCO 2025-2026.
*   `V06DOC_SUBDIVISIONS.md` — Secciones 4.1 a 4.18 añadidas con desglose competencial completo de todas las destrezas de los 18 subarquetipos.

**Decisiones arquitectónicas vinculantes de la sesión 2026-04-25:**
*   **NORMA PERMANENTE DE SESIÓN — INAMOVIBLE:** Ante cualquier disyuntiva de aglutinar vs. segregar, la respuesta es **SIEMPRE SEGREGAR**. Esta norma no se vuelve a consultar en ninguna sesión futura.
*   SUB-SAN-MED-BASIC segregado en SUB-SAN-MED-FISIO-GEN y SUB-SAN-MED-FISIO-NEURO (Fisiología General y Médica I, UGR).
*   SUB-SAN-LAB segregado en SUB-SAN-BIOQUIM (Bioquímica Metabólica, UGR Farmacia) y SUB-SAN-FARM (Farmacología I+II, UGR Farmacia).
*   SUB-SAN-PSY-CLIN segregado en SUB-SAN-PSY-DIAG (Psicopatología del Adulto) y SUB-SAN-PSY-EVAL (Evaluación Psicológica: Técnicas y Aplicaciones).
*   SUB-SAN-PSY-EXP segregado en SUB-SAN-PSY-MET (Métodos y Diseños) y SUB-SAN-PSY-STAT (Descripción y Exploración de Datos).
*   SUB-SAN-VET segregado en SUB-SAN-VET-CLIN y SUB-SAN-VET-CIR. **Nota institucional vinculante:** La UGR no imparte Grado en Veterinaria. Fuente primaria: UCO (única Facultad de Veterinaria en Andalucía). Esta nota se aplica a todas las sesiones futuras que involucren subarquetipos veterinarios.
*   SUB-SAN-NUT segregado en SUB-SAN-NUT-DIET, SUB-SAN-NUT-BROM y SUB-SAN-NUT-SPUB.
*   Emulación Parcial Certificada aplicada a: SUB-SAN-FISIO (prácticas de exploración manual sobre paciente), SUB-SAN-ODON (prácticas en maniquí y laboratorio dental), SUB-SAN-BIOQUIM (prácticas de laboratorio húmedo), SUB-SAN-VET-CLIN (prácticas en HCV-UCO), SUB-SAN-VET-CIR (prácticas procedimentales quirúrgicas), SUB-SAN-NUT-BROM (prácticas analíticas de laboratorio bromatológico).

**La siguiente fase es la Rama Ciencias Sociales y Jurídicas** — siguiente rama pendiente de certificación.

---


---

## 4. Registro de Sesiones

> **NOTA DE AUDITORÍA (PAA — 2026-05-09):** Esta tabla fue reconstruida mediante el
> Protocolo de Auditoría de Anexos (PAA) a partir del historial real de commits Git
> del repositorio `campustudionline_repo`. Las sesiones de la Etapa Pre-v5.0 (S001–S008)
> corresponden a refactorizaciones documentales sin investigación certificada contra
> fuentes primarias UGR — el trabajo de esas sesiones fue subsanado íntegramente en
> la Etapa de Certificación v5.0+ (S009 en adelante), que es la única con Fidelidad
> 100% UGR garantizada.

| Sesión | Fecha      | Alcance                          | Resumen |
|--------|------------|----------------------------------|---------|
| S001   | 2026-03-18 | Pre-v5.0 — SUB-LIN-INSTR/MINOR  | Refactorización subatómica inicial de SUB-LIN-INSTR y SUB-LIN-MINOR. Inyección de la Regla de Oro ACLES (60% por destreza), motor RBT-SHORT-LANG con validación de ductus para lenguas no latinas, mandato de bloqueo caligráfico en W-TXT-CLOZE. Sin investigación certificada contra fuentes primarias UGR — trabajo de baja fidelidad subsanado en S009. |
| S002   | 2026-03-19 | Pre-v5.0 — SUB-LIN-PHILO        | Refactorización SUB-LIN-PHILO: cuatro fases (Fonética, Morfología, Lexicología, Crítica Textual). Motores EV-DIAC-VAL y EV-PALE. Widgets IPA y ecdótica. Rigor Engine x1.8. Error de truncamiento detectado y restaurado. Sin contraste certificado con fuentes primarias UGR. |
| S003   | 2026-03-19 | Pre-v5.0 — SUB-LIN-NORM         | Refactorización SUB-LIN-NORM: secuencia CORPES XXI, queísmo/leísmo, OLE 2010, DPD. Motor EV-NORM-ANALYSIS. Adaptación W-LAW-NAV-LING. Fallo crítico de exhaustividad detectado en sesión: eliminación accidental de material de PHILO — restaurado letra por letra. Sin contraste certificado con fuentes primarias UGR. |
| S004   | 2026-03-19 | Pre-v5.0 — Blindaje documental   | Reescritura íntegra del anexo V06 para blindaje documental. Hoja de ruta centrada en auditoría subarquetipo por subarquetipo. Instauración de V06DOC_WORD_OF_GOD.md como Mandato Supremo (decisión revertida posteriormente en S009). |
| S005   | 2026-03-19 | Pre-v5.0 — SUB-LIN-TRA-TECH     | Refactorización quirúrgica SUB-LIN-TRA-TECH: secuencia genética Análisis Skopos, Diario de Traducción, TAPE. Saneamiento jerarquía de errores FTI. Actualización CAT Emulator y Navegador IATE/UNTERM. Sobrescritura accidental previa resuelta con reconstrucción quirúrgica por scripts Python. |
| S006   | 2026-03-22 | Pre-v5.0 — SUB-LIN-NORM (bis)   | Nueva sesión NRA sobre SUB-LIN-NORM. Restauración de material de PHILO truncado. Calibración Rigor Engine x1.7. Sin contraste certificado con Guía Docente 2831111 real — el trabajo de esta sesión fue auditado y corregido en S012. |
| S007   | 2026-03-23 | Pre-v5.0 — TRA-TECH quirúrgico   | Reconstrucción quirúrgica post-sobrescritura accidental sobre V06DOC_SUBARCHETYPES.md, BLOCKS.md, WIDGETS.md y LEVELS.md. Hoja de ruta reescrita para auditoría metódica subarquetipo por subarquetipo en sesiones futuras. |
| S008   | 2026-03-25 | Pre-v5.0 — Infraestructura       | Corrección AttributeError en users/views.py (campo is_used → pending_referral_code). Resolución OSError NFS. Optimización register.html con reCAPTCHA dinámico. Actualización menor de documentación V06. No es sesión de certificación pedagógica. |
| S009   | 2026-04-19 | v5.0 — SUB-LIN-INSTR (cert.)    | **INICIO DE LA FASE DE CERTIFICACIÓN REAL.** Auditoría subatómica completa de SUB-LIN-INSTR contra fuentes primarias oficiales UGR: Guía Oficial CLM-UGR CertAcles + Guías Docentes FTI y FiloLetras 2025-2026. 12 errores detectados y corregidos: estructura 5→4 destrezas (Mediación no existe en examen oficial), rangos escritura corregidos (120-150 → 200-250 palabras), mecanismo superación corregido (umbral fijo 60% → puntos de corte variables por convocatoria con PARTIAL_RETRY), PRM-STRIKE desactivado para INSTR (NO_NEGATIVE_MARKING), estructura Reading/Listening corregida (3+2 → 5+5 textos binivel), fases orales corregidas. V06DOC_WORD_OF_GOD.md eliminado definitivamente. Constelación pasa a v5.0. DECISIÓN VINCULANTE: investigación online contra fuentes primarias UGR es la única fuente de verdad para toda certificación futura. |
| S010   | 2026-04-20 | v5.1 — SUB-LIN-MINOR/PHILO/ECDO | Certificación SUB-LIN-MINOR contra oferta real CLM-UGR (9 lenguas certificadas, marco académico reglado ≠ CertAcles). Corrección protocolo superación (60% CertAcles → nota académica 5/10). Ficha técnica completa W-CALLI-PAD. SUB-LIN-PHILO certificado: 3 asignaturas fuente reales (2831113, 2831141, 2831145), refactorización de Cuatri-Destreza a Tri-Destreza Científica (SD_PHONO + SD_MORPH_DIAC + SD_LEX_SEM), SD_TEXT_CRIT desmembrada. Nuevo subarquetipo SUB-LIN-ECDO creado por desmembramiento — asignatura fuente 28311A9. VBO del usuario emitido en los 3 casos. V06DOC_WIDGETS.md, BLOCKS.md y SUBDIVISIONS.md actualizados. |
| S011   | 2026-04-20 | v5.1 — SUB-LIN-NORM/TRA-TECH/TRA-LIT | Certificación SUB-LIN-NORM contra Guía Docente 2831111 (aprobada 18/06/2025). SUB-LIN-TRA-TECH certificado contra Guía 252113T: extensión textos corregida (350 → 200-250 palabras), SD_TRA_REVIEW eliminada como destreza autónoma. SUB-LIN-TRA-LIT certificado contra Guía 25211NJ (asignatura optativa — nota institucional vinculante). Actualización SDK google-genai 1.55.0 → 1.73.1 (18 versiones de retraso detectadas). DECISIÓN VINCULANTE: CampuStudiOnline es un emulador de pruebas evaluativas, no plataforma formativa. ERROR PMP detectado y corregido: sed sustituyó TRA-LIT por TRA-TECH — corregido con sed quirúrgico en línea exacta. Rama Lenguas COMPLETAMENTE CERTIFICADA (7 subarquetipos, Fidelidad 100% UGR). |
| S012   | 2026-04-21 | v5.2 — Sincronización Lenguas + Fase A Humanidades | Sincronización completa constelación Rama Lenguas: W-TRA-CAT-EMULATOR reconvertido a W-DOC-RESOURCES (herramienta TAO incorrecta para contexto universitario), W-TRA-LIT-CREA eliminado como widget fantasma y mapeado a W-HUM-TEXT modo TRA-LIT, restricción NORM en W-HUM-TEXT, nota certificación EV-TRA-PRECISION-TECH, DRA-HOLO-LIT definido, SD_TRA_REVIEW eliminado de BLOCKS.md, contratos 6.2/6.3/6.4 añadidos a TEMPLATES.md. Arranque Rama Humanidades Fase A: investigación online 6 subarquetipos, mapa widgets necesarios — lagunas identificadas: W-ART-IDENT y W-MUS-SCORE. DECISIÓN VINCULANTE: SUB-HUM-ART-CREA como Emulación Parcial Certificada, SUB-HUM-ANTH como subarquetipo transversal. Nuevos widgets y motores V06DOC_WIDGETS.md Sección 8 y V06DOC_BLOCKS.md Sección 6. |
| S013   | 2026-04-22 | v5.3 — Rama Humanidades (cert.)  | Certificación completa 6 subarquetipos Humanidades en orden B1-B6: SUB-HUM-HIST (guías 2921128/2921126), SUB-HUM-PHIL (guías 26311M3/2631111/26311M5 — patrón cuatripartito), SUB-HUM-ART-HIST (guías 26511M2/2931114 — bipartito Panofsky no compensable), SUB-HUM-ART-CREA (guías 26011D1/2601114 — Emulación Parcial Certificada declarada vinculante), SUB-HUM-MUS (guías 2991132/2991114 — bipartito SD_MUS_LIST 50% + SD_MUS_SCORE 50%), SUB-HUM-ANTH (transversal, sin asignatura monográfica UGR). V06DOC_SUBDIVISIONS.md secciones 4-9 añadidas. V06DOC_TEMPLATES.md contratos 6.5/6.6/6.7 añadidos. INCIDENCIA: comando rm -f * en PLD no eliminaba ocultos — corregido a find -mindepth 1 -delete, skill PCS actualizada. Rama Humanidades CERRADA (v5.3). |
| S014   | 2026-04-25 | v5.4 — Rama Ciencias de la Salud (cert.) | Certificación completa 18 subarquetipos Ciencias de la Salud en sesión única. DECISIÓN VINCULANTE PERMANENTE: ante disyuntiva aglutinar vs. segregar → SIEMPRE SEGREGAR (inamovible, no se vuelve a consultar). Segregaciones: SUB-SAN-MED-BASIC→FISIO-GEN+FISIO-NEURO (baremos diferenciados), SUB-SAN-LAB→BIOQUIM+FARM (naturaleza evaluativa distinta), SUB-SAN-PSY-CLIN→DIAG+EVAL, SUB-SAN-PSY-EXP→MET+STAT, SUB-SAN-VET→CLIN+CIR (nota vinculante: UGR no imparte Veterinaria — fuente UCO), SUB-SAN-NUT→DIET+BROM+SPUB. Emulación Parcial Certificada declarada en 6 subarquetipos. Baremos no estándar certificados: FISIO-NEURO (-0,033), FISIO (proporcional), FARM y VET-CIR (-0,33 explícito), NUT-SPUB (doble umbral 40% por bloque independiente). V06DOC_SUBARCHETYPES.md 18 bloques, V06DOC_SUBDIVISIONS.md secciones 4.1-4.18, V06DOC_WIDGETS.md actualizado. Rama Ciencias de la Salud CERRADA (v5.4). |
| S015   | 2026-04-26 | v5.5 — Rama CSJ pasos S1-S4     | Inicio certificación Rama Ciencias Sociales y Jurídicas. S1: SUB-SOC-LAW-PROC→PROC-CIV+PROC-PEN (guías 2421121/2421137, aprobadas 17/06/2025, rigor x1.6, FAIL_LOGIC FATAL vulneraciones constitucionales). S2: SUB-SOC-LAW-DICT→DICT-CIV+DICT-PEN (guías civiles y penales, rigor x1.6/x1.7). S3: SUB-SOC-ECON-QUAN→QUAN-STAT+QUAN-ECON (Econometría I-III, sistema evaluación certificado: 70%+30%, extraordinaria examen único 5T+5P, FAIL_LOGIC FATAL endogeneidad con MCO). S4: SUB-SOC-ECON-MGMT→MGMT-ACC+MGMT-STR+MGMT-ECO (3 segregaciones, bibliografía Guerras y Navas 2022 certificada). INCIDENCIAS: archivo truncado en descarga concatenada — anclas PMA construidas sobre archivo incorrecto, requirió verificación previa con python3; anclas incorrectas en S3/S4 por asunción sin verificar — protocolo de verificación previa obligatoria establecido. 9 subarquetipos definitivos, secciones 5.1-5.9 en SUBDIVISIONS.md. |
| S016   | 2026-04-27 | v5.5 — Rama CSJ pasos S5-S10    | Certificación pasos S5-S10 Rama CSJ. S5: SUB-SOC-EDU-KIDS. S6: SUB-SOC-EDU-SEC. S7: SUB-SOC-COMM-JOUR. S8: SUB-SOC-COMM-AV. S9: SUB-SOC-GEOG→GEOG-SIG+GEOG-TER+GEOG-FIS (guías 2081127/20811X3/2081119, asistencia ≥75%, FAIL_LOGIC FATAL confusión vectorial/ráster). S10: SUB-SOC-WORK→WORK-INT+WORK-POL+WORK-MED (guías aprobadas 16/06/2025, asistencia ≥80%, FAIL_LOGIC FATAL mediación en violencia de género — prohibición legal art. 44.5 LO 1/2004). DECISIÓN VINCULANTE: flujo Investigación→Segregación→Bloques→PMA directo sin presentación intermedia en chat. Lección técnica: verificar stub exacto en disco con grep -n antes de construir OLD_BLOCK en cualquier PMA. Secciones 5.21-5.26 en SUBDIVISIONS.md. Rama CSJ CERRADA (v5.5). |
| S017   | 2026-04-28 | v5.6 — Rama Ingeniería (cert.)   | Certificación completa Rama Ciencias Técnicas e Ingeniería: 7 subarquetipos originales → 16 certificados. T1→SOFT-ALG+SOFT-DS+SOFT-SE (ETSIIT-UGR). T2→CIVIL-STRUCT+CIVIL-CONC+CIVIL-STEEL (ETSICCP-UGR). T3→INDUS-THERMO+INDUS-TMM+INDUS-DEM (EPSC-UCO — nota vinculante: UGR no imparte Ingeniería Industrial). T4→CHEM-BAL+CHEM-REACT (IQ-UGR). T5→PROJ-ARCH+PROJ-URB (ETSAG-UGR). T6→CONS-TECH+CONS-MAN (ETSIE-UGR). T7→PURE-ANAL+PURE-ALGSTR (Matemáticas UGR). INCIDENCIAS: PMA T1 consumió ancla de T2/T3 — PMAs abortaron silenciosamente; resuelto con PMA unificado atómico. Búsqueda errónea inicial en Ingeniería Electrónica para T3 — corregido a UCO. Presentación de bloques en chat en T1 (incumplimiento flujo) consumió 30% cuota de sesión innecesariamente. Secciones 6.1-6.20 en SUBDIVISIONS.md. Rama Ingeniería CERRADA (v5.6). |
| S018   | 2026-05-02 | v5.7 — Rama Ciencias (cert.)     | Certificación completa Rama Ciencias (C1-C5 ya certificados en S017; esta sesión certifica C6). INCIDENCIA CRÍTICA: al inicio de sesión se generó contenido nuevo sin haber leído la constelación — bloque duplicado en V06DOC_SUBARCHETYPES.md. Detectado mediante auditoría y resuelto con git checkout HEAD sobre el archivo afectado. C6 SUB-SCI-DATA: UGR no dispone de guías docentes activas para Grado en Ciencias de Datos e IA 2025-2026 — fuente primaria: Grado en Ingeniería de Datos e IA, Facultad de Informática UCM (fichas aprobadas 27/06/2025). Nota vinculante registrada. Fallo patcher por carácter raya larga (—) en codificación del archivo servidor — resuelto cambiando estrategia a SEARCH_MARKER por substring corto. Subarquetipos DATA→DATA-STAT+DATA-ML+DATA-BIG, secciones 7.13-7.15 en SUBDIVISIONS.md. Rama Ciencias CERRADA (v5.7). |
| S019   | 2026-05-11 | v5.9 — Auditoría de Fidelidad Documental (87/87) | Auditoría de consistencia y fidelidad documental completa de la constelación V06: 87/87 subarquetipos verificados contra fuentes primarias UGR/UCO/UCM 2025-2026. Resultado: 86 CONFORMES + 1 INCIDENCIA LEVE (SUB-LIN-TRA-LIT: mecanismo Non-Backtracking entre fases no verificado en guía docente real — contenido conforme, estructura en duda). CERO incidencias moderadas. CERO incidencias graves. Constelación documental V06 declarada AUTORIZADA para la Fase de Implementación. La incidencia leve SUB-LIN-TRA-LIT queda como primer punto del orden del día de la S020. |
| S020   | 2026-05-16 | Resolución SUB-LIN-TRA-LIT + Apertura Implementación | Resolución incidencia SUB-LIN-TRA-LIT: verificación online guía 25211NJ (aprobada 23/06/2025) — sistema evaluación real: trabajos escritos 30% + presentaciones 40% + participación 30%. Sin Non-Backtracking entre destrezas. Opción B aplicada: refactorización quirúrgica PMA sobre V06DOC_SUBARCHETYPES, V06DOC_SUBDIVISIONS y V06DOC_TEMPLATES (3 destrezas independientes evaluadas holísticamente: SD_TRA_STYLE, SD_TRA_CREATIVE, SD_TRA_CRIT con DRA-HOLO-LIT). Auditoría completa de implementación: 42 errores identificados en 9 bloques. Inicio PEAs Fase de Implementación: models/main.py (migración 0020 aplicada) y core/services/gemini_schemas.py completados. |
| S021   | 2026-05-24 | Implementación Hito 6 — PEAs core (12/17 archivos) | Continuación Fase de Implementación. PMA quirúrgico gemini_service.py (modelo gemini-2.5-flash, delay 0s, system_instruction 87 IDs). PEAs: base.py (11 motores completos, rigor matrix), logic.py (AcademicDeductor híbrido, GradingOrchestrator con kill-switches y gating variable), factory.py (6 arquetipos explícitos). PEAs strategies: languages.py (7 sub., rigor override), health.py (18 sub., ECOE ITIN_ROT), humanities.py (6 sub., Panofsky), science.py (15 sub.), social.py (19 sub., FATAL VG), tech.py (17 sub., tolerancia 1%). PMAs tasks.py (sections_map por orden, skeleton_json en prompt, tracking corregido), views.py (clasificación síncrona eliminada), quotas.py (ERROR excluido de cuota). Skills actualizadas (ped v2, pisa v2, pee v2, pcs v2, pcva v2). 15/17 archivos completados. Pendiente: exam_take.html, exam_report.html, validate_v06_engines.py.

## 2. HOJA DE RUTA PARA LA PRÓXIMA SESIÓN (LEY SUPREMA - INELUDIBLE)

**ESTADO DEL HITO:** EN PROGRESO — Fase de Implementación COMPLETADA S022. Pendiente certificación de fidelidad documental antes del primer despliegue.
**FECHA DE ÚLTIMA ACTUALIZACIÓN:** 2026-05-25
**OBJETIVO DE LA PRÓXIMA SESIÓN (S023):** TLA — Auditoría de fidelidad documental completa. Certificar que los 21 widgets de `exam_take.html` implementados en S020/S021/S022 coinciden fielmente con los 11 satélites de la constelación. Corregir cualquier desviación detectada. Solo tras la certificación se puede declarar el hito listo para primer despliegue real.

---

### FASE DE IMPLEMENTACIÓN — ESTADO ACTUAL (S022 — 2026-05-25)

**17/17 ARCHIVOS COMPLETADOS (SYNTAX OK verificado):**
1. `assessment_v2/models/main.py` ✅
2. `core/services/gemini_schemas.py` ✅
3. `core/services/gemini_service.py` ✅
4. `assessment_v2/services/engine/strategies/base.py` ✅
5. `assessment_v2/services/engine/logic.py` ✅
6. `assessment_v2/services/engine/factory.py` ✅
7. `assessment_v2/services/engine/strategies/languages.py` ✅
8. `assessment_v2/services/engine/strategies/health.py` ✅
9. `assessment_v2/services/engine/strategies/humanities.py` ✅
10. `assessment_v2/services/engine/strategies/science.py` ✅
11. `assessment_v2/services/engine/strategies/social.py` ✅
12. `assessment_v2/services/engine/strategies/tech.py` ✅
13. `orchestrator/tasks.py` ✅
14. `assessment_v2/views.py` ✅
15. `assessment_v2/services/quotas.py` ✅
16. `assessment_v2/templates/assessment_v2/exam_take.html` ✅ — S022: 12 widgets nuevos implementados (W-AUDIO-INSTR, W-MUS-SCORE, W-ART-IDENT, W-CALLI-PAD, W-PORTFOLIO, W-PHILO-IPA, W-PHILO-ECDO, W-PHILO-OCR-PALE, W-DOC-RESOURCES, W-CASE-ECOE, W-MEDI-LAYOUT, W-OCR-PRO, W-INSTR-SELECTOR). Correcciones: W-OBJ-STRIKE (radio desactivado al tachar), W-AUDIO-INSTR (bloqueo hermético + Non-Scrubbing), submission controller completo (20 widgets). 0 errores djlint.
17. `assessment_v2/templates/assessment_v2/exam_report.html` ✅ — S022: `item_score` y `justification` directa corregidos. 0 errores djlint.
18. `assessment_v2/management/commands/validate_v06_engines.py` ✅ — S022: rediseñado para búsqueda dinámica en BD (~2.500 asignaturas). Usa `get_exam_skeleton()` (API real). Resultado: 47/82 ÉXITO, 35/82 SKIP (datos pendientes), 0 FALLOS de código.

**MASTER DOCUMENT:** Sección 2.1.1 Logs del Servidor añadida con rutas PythonAnywhere.

---

### S023 — AUDITORÍA TLA: FIDELIDAD DOCUMENTAL COMPLETA

**CONTEXTO OBLIGATORIO:**
La implementación de los 12 widgets nuevos en `exam_take.html` se realizó
en S022 desde memoria de sesión sin contrastar sistemáticamente la totalidad
de los 11 satélites. La auditoría es OBLIGATORIA antes de declarar el hito
listo para despliegue. El modelo de S023 NO puede saltarse este paso bajo
ningún argumento.

**CRITERIO DE ÉXITO:** Cada uno de los 21 widgets de `exam_take.html` queda
auditado y certificado contra su especificación en los satélites. Las
desviaciones quedan documentadas y corregidas. Al cierre de S023 se declara
formalmente la Fase de Implementación como CERTIFICADA.

---

#### PASO 0 — Carga obligatoria ANTES de auditar (NO NEGOCIABLE)

Solicitar y leer íntegramente, en este orden:
1. `exam_take.html` actual del servidor.
2. Los 11 satélites completos (todos, sin excepción):
   - `V06DOC_WIDGETS.md`
   - `V06DOC_STRUCTURE.md`
   - `V06DOC_TEMPLATES.md`
   - `V06DOC_BINDING_GUIDELINE.md`
   - `V06DOC_METADATA.md`
   - `V06DOC_SUBARCHETYPES.md`
   - `V06DOC_BLOCKS.md`
   - `V06DOC_SUBDIVISIONS.md`
   - `V06DOC_LOGIC_MAPPING.md`
   - `V06DOC_LEVELS.md`
   - `V06DOC_ARCHETYPES.md`

**PROHIBIDO** comenzar la auditoría sin haber leído la totalidad de estos
12 documentos. Trabajar desde memoria de sesión anterior es un ERROR CRÍTICO.

---

#### PASO 1 — Auditoría widget por widget (21 widgets)

Para cada `widget_id` presente en `exam_take.html`, contrastar:

**A. HTML (estructura visual)**
- ¿Los campos, controles y layout coinciden con la especificación de
  `V06DOC_WIDGETS` para ese `widget_id`?
- ¿Los `data-*` attributes están presentes según `V06DOC_BINDING_GUIDELINE`?
- ¿Las clases CSS son coherentes con `V06DOC_TEMPLATES`?

**B. JavaScript (comportamiento)**
- ¿El método de init/control en `AssessmentWidgets` implementa el
  comportamiento de `V06DOC_WIDGETS`?
- ¿El submission controller recoge la respuesta en el formato exacto de
  `V06DOC_BLOCKS` para el motor correspondiente?
- ¿`widgetState` almacena la estructura correcta según `V06DOC_METADATA`?

**C. Binding**
- ¿El `widget_id` HTML coincide exactamente con `V06DOC_BINDING_GUIDELINE`?
- ¿El `block_type` asociado es coherente con `V06DOC_BLOCKS`?

---

#### PASO 2 — Registro de desviaciones

Por cada desviación detectada, registrar:
- `widget_id` afectado.
- Satélite de referencia y sección exacta.
- Descripción de la desviación.
- Corrección a aplicar.

---

#### PASO 3 — Correcciones

Aplicar todas las correcciones del PASO 2 mediante PMA/PMP según alcance.
Relanzar `djlint --lint` al finalizar. 0 errores como condición de salida.

---

#### PASO 4 — Certificación

Una vez auditados los 21 widgets y aplicadas todas las correcciones:
- Actualizar este anexo marcando la Fase de Implementación como CERTIFICADA.
- Declarar el hito listo para primer despliegue real.
- Programar en el MASTER DOCUMENT el cambio de fase del Hito 6 a
  Fase de Despliegue.

---

### CONSTELACIÓN DOCUMENTAL ACTIVA (v5.9)

Los archivos satélite de la constelación V06 son:
`V06DOC_ARCHETYPES.md`, `V06DOC_SUBARCHETYPES.md`, `V06DOC_BLOCKS.md`,
`V06DOC_WIDGETS.md`, `V06DOC_LEVELS.md`, `V06DOC_SUBDIVISIONS.md`,
`V06DOC_METADATA.md`, `V06DOC_STRUCTURE.md`, `V06DOC_BINDING_GUIDELINE.md`,
`V06DOC_TEMPLATES.md`, `V06DOC_LOGIC_MAPPING.md`.

Ruta base:
`/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/`

---

### NORMAS PERMANENTES — INAMOVIBLES

**NORTE INAMOVIBLE:** CampuStudiOnline es un emulador de pruebas evaluativas
universitarias. El alumno solicita ser evaluado de una asignatura y recibe
una prueba que replica fielmente los criterios, estructura y baremos del
examen oficial de esa asignatura en la UGR. Todo lo que no figure en la
evaluación ordinaria o extraordinaria de la Guía Docente oficial no se
evalúa y no tiene cabida en la constelación.

- Ante cualquier disyuntiva de aglutinar vs. segregar → SIEMPRE SEGREGAR.
- El modelo NO PODRÁ INVENTAR NI SUPONER NADA que no esté en la hoja de
  ruta o en la documentación satélite auditada.
- NO se modificará ningún subarquetipo ya certificado salvo indicación
  explícita del usuario con el nombre exacto del subarquetipo a revisar.
- NO se crearán widgets ni motores adicionales sin investigación online
  previa contra las fuentes primarias UGR.
