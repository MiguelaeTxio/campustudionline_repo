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

**ESTADO DEL HITO:** EN PROGRESO — Fase de Implementación ACTIVA. Incidencia SUB-LIN-TRA-LIT resuelta (v5.9). Implementación S020/S021 en curso: 14/17 archivos completados.
**FECHA DE ÚLTIMA ACTUALIZACIÓN:** 2026-05-24
**OBJETIVO DE LA PRÓXIMA SESIÓN:** Completar los 3 archivos pendientes de la Fase de Implementación y ejecutar el primer despliegue real.

---

### FASE DE IMPLEMENTACIÓN — ESTADO ACTUAL (S020/S021 — 2026-05-24)

**ARCHIVOS COMPLETADOS (PEA/PMA — SYNTAX OK verificado):**
1. `assessment_v2/models/main.py` ✅ — Migración `0020_hito6_v59_full_taxonomy` aplicada. Enums completos: 87 subarquetipos, ~130 subdivisiones, 23 widgets, 22 motores.
2. `core/services/gemini_schemas.py` ✅ — Schemas Pydantic alineados con v5.9: `AcademicClassificationSchema` (87 IDs), `ContentSchema` (source_text, targets, initial_scenario, cloze_options), `GradingLogicSchema` (gap_solutions como Dict, rubric_axes, kill_switch).
3. `core/services/gemini_service.py` ✅ — PMA quirúrgico: modelo corregido a `gemini-2.5-flash`, delay proactivo eliminado (0s), `classify_subject_identity` system_instruction actualizada con árbol de decisión completo de los 87 IDs certificados.
4. `assessment_v2/services/engine/strategies/base.py` ✅ — PEA completo: 11 motores implementados (PRM-STRIKE con NO_NEGATIVE_MARKING, RBT-CANON, RBT-SHORT-LANG, CLO-OPEN, CLO-MULTI, MAT-LINK, CDS-KILL, DRA-HOLO, DRA-HOLO-LIT, BMT-SHIFT, ILC-CONTEXT, EV-PALE, RPP-TRAZA con planteamiento-primo-50%, DIA-INTERACT). Rigor matrix LVL×ITIN completa.
5. `assessment_v2/services/engine/logic.py` ✅ — PEA completo: `AcademicDeductor` (Fases 1+2 híbridas, barrera de fuego ARCH_LANG), `GradingOrchestrator` (kill-switches ARCH_HEALTH/ARCH_HUM/ARCH_SOC, gating ARCH_LANG por puntos de corte variables, voz del catedrático por nivel/itinerario).
6. `assessment_v2/services/engine/factory.py` ✅ — PEA completo: mapeo explícito de los 6 arquetipos, fallback SocialStrategy documentado.
7. `assessment_v2/services/engine/strategies/languages.py` ✅ — PEA completo: 7 subarquetipos certificados con esqueletos específicos, motores EV-DIAC-VAL, EV-NORM-ANALYSIS, EV-TRA-PRECISION-TECH, rigor override NORM×1.7/PHILO×1.8, inmersión VEHICULAR/BILINGUAL/TOTAL.
8. `assessment_v2/services/engine/strategies/health.py` ✅ — PEA completo: 18 subarquetipos certificados, protocolo ECOE (ITIN_ROT, 5 estaciones), CDS-KILL con kill_switch, rigor override FISIO-NEURO y VET-CIR.
9. `assessment_v2/services/engine/strategies/humanities.py` ✅ — PEA completo: 6 subarquetipos certificados, motores EV-ICON-ART (Panofsky) y EV-MUS-ANAL, esqueletos bipartitos no compensables (ART-HIST).
10. `assessment_v2/services/engine/strategies/science.py` ✅ — PEA completo: 15 subarquetipos certificados, esqueletos TEORÍA+CALC por subarquetipo.
11. `assessment_v2/services/engine/strategies/social.py` ✅ — PEA completo: 19 subarquetipos certificados, FATAL VG (LO 1/2004 art. 44.5), bonus fuentes reales +20%, `_grade_dra_holo_social` con detección normativa.
12. `assessment_v2/services/engine/strategies/tech.py` ✅ — PEA completo: 17 subarquetipos certificados, `_validate_technical_value` con tolerancia 1% y variantes pipe, ITIN_PROF normativo.
13. `orchestrator/tasks.py` ✅ — PMA: sections_map indexado por orden (elimina colisiones), skeleton_json inyectado en prompt, TrackingService corregido a `gemini-2.5-flash`, quota exclusión estado ERROR.
14. `assessment_v2/views.py` ✅ — PMA: clasificación síncrona eliminada de `ExamCreateView.post()` (única clasificación en `generate_exam_task`), `AcademicDeductor` eliminado de imports de views.
15. `assessment_v2/services/quotas.py` ✅ — PMA: exámenes en estado ERROR excluidos del cómputo de cuota diaria y semanal.

**ARCHIVOS PENDIENTES (próxima sesión S022):**
- `assessment_v2/templates/assessment_v2/exam_take.html` — PEA: implementar los 12 widgets faltantes (W-MUS-SCORE, W-ART-IDENT, W-CALLI-PAD, W-PORTFOLIO, W-PHILO-IPA, W-PHILO-ECDO, W-PHILO-OCR-PALE, W-DOC-RESOURCES, W-CASE-ECOE, W-MEDI-LAYOUT, W-OCR-PRO, W-INSTR-SELECTOR), corregir W-AUDIO-INSTR (bloqueo hermético 2ª reproducción), W-TXT-CLOZE (marcadores [HUECO_ID_N]), W-OBJ-STRIKE (radio desactivado al tachar), Non-Scrubbing en reproductores.
- `assessment_v2/templates/assessment_v2/exam_report.html` — PEA: corregir acceso `item_score` (no `score`), `justification` directa (no `feedback.justification`).
- `assessment_v2/management/commands/validate_v06_engines.py` — PEA: actualizar tabla TARGETS con los 87 IDs certificados.

**ACCIÓN INMEDIATA SESIÓN S022:** Arrancar directamente con el PEA de `exam_take.html`. Es el archivo más extenso y crítico para la experiencia del alumno.

---

### CONSTELACIÓN DOCUMENTAL ACTIVA (v5.4)

Los archivos satélite de la constelación V06 son:
`V06DOC_ARCHETYPES.md`, `V06DOC_SUBARCHETYPES.md`, `V06DOC_BLOCKS.md`, `V06DOC_WIDGETS.md`, `V06DOC_LEVELS.md`, `V06DOC_SUBDIVISIONS.md`, `V06DOC_METADATA.md`, `V06DOC_STRUCTURE.md`, `V06DOC_BINDING_GUIDELINE.md`, `V06DOC_TEMPLATES.md`, `V06DOC_LOGIC_MAPPING.md`.

Ruta base de la constelación:
`/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/`

**IMPORTANTE:** La investigación online en tiempo real contra las fuentes primarias UGR es la única fuente de verdad para la certificación de cada subarquetipo.

---

### PROTOCOLO DE EJECUCIÓN OBLIGATORIO (PRÓXIMA SESIÓN)

**NORTE INAMOVIBLE:** CampuStudiOnline es un emulador de pruebas evaluativas universitarias. El alumno solicita ser evaluado de una asignatura y recibe una prueba que replica fielmente los criterios, estructura y baremos del examen oficial de esa asignatura en la UGR. Todo lo que no figure en la evaluación ordinaria o extraordinaria de la Guía Docente oficial **no se evalúa y no tiene cabida en la constelación.**

**NORMA PERMANENTE — INAMOVIBLE — NO SE VUELVE A CONSULTAR:**
*   Ante cualquier disyuntiva de aglutinar vs. segregar → **SIEMPRE SEGREGAR**.
*   Nunca se aglutina bajo ningún argumento, en ninguna sesión, sin excepción.

**PROHIBICIONES ABSOLUTAS HEREDADAS:**
*   El modelo de la próxima sesión **NO PODRÁ INVENTAR NI SUPONER NADA** que no esté escrito en esta hoja de ruta o en la documentación satélite auditada.
*   **NO** se permite el salto a otras ramas hasta que todos los subarquetipos de la Rama en curso alcancen Fidelidad 100% certificada por el usuario.
*   **NO** se modificará ningún subarquetipo ya certificado salvo indicación explícita del usuario con el nombre exacto del subarquetipo a revisar.
*   **NO** se crearán widgets ni motores adicionales sin investigación online previa contra las fuentes primarias UGR de la rama en curso.

---

#### RAMA CIENCIAS SOCIALES Y JURÍDICAS — ✅ COMPLETAMENTE CERTIFICADA (v5.5 — 2026-04-27)

Todos los pasos S1-S10 certificados y consolidados en  (secciones ## 2. RAMA: CIENCIAS SOCIALES Y JURÍDICAS) y  (secciones 5.1 a 5.26). Consultar el registro completo en el transcript de sesión 2026-04-26/27.

---

#### RAMA CIENCIAS TÉCNICAS E INGENIERÍA — ✅ COMPLETAMENTE CERTIFICADA (v5.6 — 2026-04-28)

Todos los pasos T1-T7 certificados y consolidados en `V06DOC_SUBARCHETYPES.md` (sección ## 4. RAMA: INGENIERÍA Y ARQUITECTURA) y `V06DOC_SUBDIVISIONS.md` (secciones 6.1 a 6.20).

**Resultado final de segregación (7 originales → 16 certificados):**
*   T1 — `SUB-TEC-SOFT` → `SUB-TEC-SOFT-ALG` + `SUB-TEC-SOFT-DS` + `SUB-TEC-SOFT-SE` (ETSIIT-UGR, aprobadas 30/06/2025)
*   T2 — `SUB-TEC-CIVIL` → `SUB-TEC-CIVIL-STRUCT` + `SUB-TEC-CIVIL-CONC` + `SUB-TEC-CIVIL-STEEL` (ETSICCP-UGR, aprobadas 23/06/2025)
*   T3 — `SUB-TEC-INDUS` → `SUB-TEC-INDUS-THERMO` + `SUB-TEC-INDUS-TMM` + `SUB-TEC-INDUS-DEM` (EPSC-UCO — nota vinculante: UGR no imparte Grado en Ingeniería Mecánica)
*   T4 — `SUB-TEC-CHEM` → `SUB-TEC-CHEM-BAL` + `SUB-TEC-CHEM-REACT` (Grado Ingeniería Química UGR, aprobadas 2025-2026)
*   T5 — `SUB-TEC-PROJ` → `SUB-TEC-PROJ-ARCH` + `SUB-TEC-PROJ-URB` (ETSAG-UGR, aprobadas 2025-2026)
*   T6 — `SUB-TEC-CONS` → `SUB-TEC-CONS-TECH` + `SUB-TEC-CONS-MAN` (ETSIE-UGR, aprobadas 24/06/2025)
*   T7 — `SUB-TEC-PURE` → `SUB-TEC-PURE-ANAL` + `SUB-TEC-PURE-ALGSTR` (Grado Matemáticas UGR, aprobadas 2025-2026)

**FLUJO DE TRABAJO ACTIVO (consolidado 2026-04-27/28):** Investigación → Segregación → Bloques → PMA directo. Sin presentación intermedia en chat. Solo se detiene para la autorización del diff.

---

#### RAMA CIENCIAS — ✅ COMPLETAMENTE CERTIFICADA (v5.7 — 2026-05-02)

Todos los pasos C1-C6 certificados y consolidados en `V06DOC_SUBARCHETYPES.md` (sección ## 5. RAMA: CIENCIAS) y `V06DOC_SUBDIVISIONS.md` (secciones 7.1 a 7.15).

**Resultado final de segregación (6 originales → 14 certificados):**
*   C1 — `SUB-SCI-BIO` → `SUB-SCI-BIO-GEN` + `SUB-SCI-BIO-ZOO` + `SUB-SCI-BIO-ECO` (UGR Biología, aprobadas 24-25/06/2025)
*   C2 — `SUB-SCI-CHEM` → `SUB-SCI-CHEM-ORG` + `SUB-SCI-CHEM-INORG` (UGR Química, aprobadas 24-26/06/2025)
*   C3 — `SUB-SCI-PHYS` → `SUB-SCI-PHYS-EM` + `SUB-SCI-PHYS-QM` (UGR Física, aprobada 24/06/2025)
*   C4 — `SUB-SCI-GEOL` → `SUB-SCI-GEOL-MIN` + `SUB-SCI-GEOL-STRAT` + `SUB-SCI-GEOL-MAP` (UGR Geología, aprobadas 18-30/06/2025)
*   C5 — `SUB-SCI-ENV` → `SUB-SCI-ENV-RES` + `SUB-SCI-ENV-CONT` (UGR Ciencias Ambientales, aprobadas 23-27/06/2025)
*   C6 — `SUB-SCI-DATA` → `SUB-SCI-DATA-STAT` + `SUB-SCI-DATA-ML` + `SUB-SCI-DATA-BIG` (UCM GIDIA — nota vinculante: UGR no dispone de guías docentes activas para el Grado en Ciencias de Datos e IA en 2025-2026; fuente primaria: Grado en Ingeniería de Datos e Inteligencia Artificial, Facultad de Informática, UCM — fichas docentes aprobadas 27/06/2025)

**SIGUIENTE FASE: Rama Ciencias Sociales y Jurídicas — pasos S5 a S10 pendientes.**

---

#### RAMA CIENCIAS SOCIALES Y JURÍDICAS — CERTIFICACIÓN S5-S10

**OBJETIVO DE LA PRÓXIMA SESIÓN:** Certificar los pasos S5 a S10 en orden estricto e inamovible.

**NORMAS PERMANENTES INAMOVIBLES:**
*   Ante cualquier disyuntiva aglutinar vs. segregar → **SIEMPRE SEGREGAR**. Sin excepción. Sin consulta.
*   **FLUJO DE TRABAJO:** Investigación → Segregación → Bloques → PMA directo. Sin presentación intermedia en chat. Solo se detiene para la autorización del diff.
*   **NO** se permite el salto a otras ramas hasta que todos los subarquetipos de la Rama Ciencias alcancen Fidelidad 100%.
*   **NO** se modifica ningún subarquetipo ya certificado salvo indicación explícita del usuario.
*   Si la UGR no imparte el Grado prototipo para un subarquetipo → buscar en otras universidades andaluzas (UCO, UMA, US, UJA, UAL) comenzando por la más próxima al dominio.

**PASOS DE CERTIFICACIÓN — RAMA CIENCIAS:**

**PASO C1 — SUB-SCI-BIO (Biología — Taxonomía, ecología y genética)**
*   **Fuentes a contrastar:** Guías Docentes del Grado en Biología UGR (Facultad de Ciencias). Asignaturas de Botánica, Zoología, Ecología, Genética. Identificar asignaturas troncales con evaluación certificada 2025-2026.
*   **Segregación previsible:** Biología Celular/Genética vs. Ecología vs. Zoología/Botánica (norma permanente: segregar).
*   **Documentos a actualizar:** `V06DOC_SUBARCHETYPES.md`, `V06DOC_SUBDIVISIONS.md`.

**PASO C2 — SUB-SCI-CHEM (Química — Síntesis, inorgánica y orgánica pura)**
*   **Fuentes a contrastar:** Guías Docentes del Grado en Química UGR (Facultad de Ciencias). Asignaturas de Química Orgánica, Química Inorgánica, Síntesis. Distinguir del SUB-TEC-CHEM (Ingeniería Química) ya certificado — este subarquetipo es Química pura.
*   **Segregación previsible:** Química Orgánica vs. Química Inorgánica vs. Síntesis/Técnicas (norma permanente: segregar).
*   **Nota vinculante:** No confundir con SUB-TEC-CHEM-BAL ni SUB-TEC-CHEM-REACT — esos son ingeniería de procesos. Este subarquetipo es Química básica/pura.
*   **Documentos a actualizar:** `V06DOC_SUBARCHETYPES.md`, `V06DOC_SUBDIVISIONS.md`.

**PASO C3 — SUB-SCI-PHYS (Física — Mecánica cuántica y electromagnetismo)**
*   **Fuentes a contrastar:** Guías Docentes del Grado en Física UGR (Facultad de Ciencias). Asignaturas de Mecánica Cuántica, Electromagnetismo, Mecánica Clásica. Distinguir del SUB-TEC-PURE-ANAL (Análisis Matemático) ya certificado — este subarquetipo es Física pura.
*   **Segregación previsible:** Mecánica Cuántica vs. Electromagnetismo vs. Mecánica Clásica/Estadística (norma permanente: segregar).
*   **Documentos a actualizar:** `V06DOC_SUBARCHETYPES.md`, `V06DOC_SUBDIVISIONS.md`.

**PASO C4 — SUB-SCI-GEOL (Geología — Mineralogía, estratigrafía y cartografía)**
*   **Fuentes a contrastar:** Guías Docentes del Grado en Geología UGR (Facultad de Ciencias). Asignaturas de Mineralogía, Estratigrafía, Cartografía Geológica, Petrología.
*   **Segregación previsible:** Mineralogía/Petrología vs. Estratigrafía vs. Cartografía Geológica (norma permanente: segregar).
*   **Documentos a actualizar:** `V06DOC_SUBARCHETYPES.md`, `V06DOC_SUBDIVISIONS.md`.

**PASO C5 — SUB-SCI-ENV (Ciencias Ambientales — Gestión de residuos y contaminación)**
*   **Fuentes a contrastar:** Guías Docentes del Grado en Ciencias Ambientales UGR (Facultad de Ciencias). Asignaturas de Contaminación, Gestión de Residuos, Evaluación de Impacto Ambiental.
*   **Segregación previsible:** Contaminación/Toxicología vs. Gestión de Residuos vs. EIA/Legislación ambiental (norma permanente: segregar).
*   **Documentos a actualizar:** `V06DOC_SUBARCHETYPES.md`, `V06DOC_SUBDIVISIONS.md`.

**PASO C6 — SUB-SCI-DATA (Ciencia de Datos — IA, Big Data y estadística computacional)**
*   **Fuentes a contrastar:** Guías Docentes del Grado en Estadística UGR o Doble Grado Informática+Matemáticas UGR (Facultad de Ciencias). Verificar si la UGR imparte un Grado específico de Ciencia de Datos o si el prototipo más adecuado es el Grado en Estadística. Asignaturas de Aprendizaje Automático, Big Data, Estadística Computacional.
*   **Nota vinculante:** Verificar la existencia del Grado en Ciencia de Datos en la UGR antes de buscar en otras universidades andaluzas.
*   **Segregación previsible:** Aprendizaje Automático/IA vs. Big Data/Ingeniería de Datos vs. Estadística Computacional (norma permanente: segregar).
*   **Documentos a actualizar:** `V06DOC_SUBARCHETYPES.md`, `V06DOC_SUBDIVISIONS.md`.

**PASO S1 — SUB-SOC-LAW-PROC → ✅ CERTIFICADO (v5.5 — 2026-04-26)**
*   Segregado en: `SUB-SOC-LAW-PROC-CIV` (Derecho Procesal Civil, Guías Docentes 2421121 y 2421137 Bloque Civil, UGR, aprobadas 17/06/2025) y `SUB-SOC-LAW-PROC-PEN` (Derecho Procesal Penal, Guía Docente 2421137 Bloque Penal, UGR, aprobada 17/06/2025).
*   Documentos actualizados: `V06DOC_SUBARCHETYPES.md` (sección ## 2. RAMA: CIENCIAS SOCIALES Y JURÍDICAS) y `V06DOC_SUBDIVISIONS.md` (secciones 5.1 y 5.2).

**PASO S2 — SUB-SOC-LAW-DICT → ✅ CERTIFICADO (v5.5 — 2026-04-26)**
*   Segregado en: `SUB-SOC-LAW-DICT-CIV` (Derecho Civil I-IV, Guías Docentes 2421116/2421124/2421128/2421143, UGR, aprobadas 27/06/2025) y `SUB-SOC-LAW-DICT-PEN` (Derecho Penal I y II, Guías Docentes 242111A/2421122, UGR, aprobadas 26/06/2025). Sistema de evaluación certificado Derecho Penal II: examen final 70% (mínimo 3,5/7) + actividades 30% (mínimo 1,5/3).
*   Documentos actualizados: `V06DOC_SUBARCHETYPES.md` y `V06DOC_SUBDIVISIONS.md` (secciones 5.3 y 5.4).

**PASO S3 — SUB-SOC-ECON-QUAN → ✅ CERTIFICADO (v5.5 — 2026-04-26)**
*   Segregado en: `SUB-SOC-ECON-QUAN-STAT` (Estadística y Técnicas Cuantitativas, Departamento de Métodos Cuantitativos UGR, aprobadas 25/06/2025) y `SUB-SOC-ECON-QUAN-ECON` (Econometría I-III: 2391131/2391136/2391141, Grado en Economía UGR, aprobadas 25/06/2025). Sistema de evaluación certificado Econometría I: prueba escrita 70% (mínimo 5/10) + evaluación continua 30%; extraordinaria: examen único 5T+5P.
*   Documentos actualizados: `V06DOC_SUBARCHETYPES.md` y `V06DOC_SUBDIVISIONS.md` (secciones 5.5 y 5.6).

**PASO S4 — SUB-SOC-ECON-MGMT → ✅ CERTIFICADO (v5.5 — 2026-04-26)**
*   Segregado en tres subarquetipos: `SUB-SOC-ECON-MGMT-ACC` (Contabilidad Financiera I/II y de Gestión I, Guías Docentes 2351131/2351137, UGR, aprobadas 24/06/2025), `SUB-SOC-ECON-MGMT-STR` (Dirección Estratégica I/II: 2351135/2351139, Grado ADE UGR, aprobadas 23/06/2025; bibliografía certificada: Guerras y Navas 2022) y `SUB-SOC-ECON-MGMT-ECO` (Microeconomía I/II y Macroeconomía I/II, Grado en Economía/ADE UGR, aprobadas 2025).
*   Sistema de evaluación certificado Contabilidad: evaluación continua con pruebas obligatorias; umbral mínimo 5/10 en parte teórica y 5/10 en parte teórico-práctica; extraordinaria: examen único con ambas partes.
*   Documentos actualizados: `V06DOC_SUBARCHETYPES.md` y `V06DOC_SUBDIVISIONS.md` (secciones 5.7, 5.8 y 5.9).

**PASO S5 — SUB-SOC-EDU-KIDS (Magisterio — Diseño de situaciones de aprendizaje y DUA)**
*   **Fuentes a contrastar:** Guías Docentes del Grado en Educación Primaria e Infantil UGR (Facultad de Ciencias de la Educación). Asignaturas de Didáctica General, Diseño Curricular, Atención a la Diversidad (DUA).
*   **Segregación previsible:** Educación Infantil vs. Educación Primaria, o Didáctica General vs. Atención a la Diversidad (norma permanente: segregar).
*   **Documentos a actualizar:** `V06DOC_SUBARCHETYPES.md`, `V06DOC_SUBDIVISIONS.md`.

**PASO S6 — SUB-SOC-EDU-SEC (Profesorado — Didáctica específica y normativa educativa)**
*   **Fuentes a contrastar:** Guías Docentes del Máster en Profesorado de Educación Secundaria UGR. Asignaturas de Aprendizaje y Desarrollo de la Personalidad, Procesos y Contextos Educativos y las didácticas específicas por especialidad.
*   **Nota:** Verificar si el scope es el Máster de Profesorado (MAES) o el Grado en Pedagogía — la diferencia es determinante para la fuente primaria.
*   **Documentos a actualizar:** `V06DOC_SUBARCHETYPES.md`, `V06DOC_SUBDIVISIONS.md`.

**PASO S7 — SUB-SOC-COMM-JOUR (Periodismo — Redacción, ética y análisis de medios)**
*   **Fuentes a contrastar:** Guías Docentes del Grado en Periodismo UGR (Facultad de Comunicación y Documentación). Asignaturas de Redacción Periodística, Ética y Deontología, Teoría de la Comunicación.
*   **Segregación previsible:** Redacción/Géneros periodísticos vs. Ética/Teoría vs. Análisis de medios (norma permanente: segregar).
*   **Documentos a actualizar:** `V06DOC_SUBARCHETYPES.md`, `V06DOC_SUBDIVISIONS.md`.

**PASO S8 — SUB-SOC-COMM-AV (Audiovisual — Guion, técnica de cámara y postproducción)**
*   **Fuentes a contrastar:** Guías Docentes del Grado en Comunicación Audiovisual UGR. Asignaturas de Guion Audiovisual, Realización y Técnica de Cámara, Postproducción y Edición.
*   **Segregación previsible:** Guion vs. Técnica/Realización vs. Postproducción (norma permanente: segregar).
*   **Emulación parcial previsible:** Prácticas de rodaje y grabación presencial no emulables — declarar Emulación Parcial Certificada si se confirma en las guías.
*   **Documentos a actualizar:** `V06DOC_SUBARCHETYPES.md`, `V06DOC_SUBDIVISIONS.md`.

**PASO S9 — SUB-SOC-GEOG (Geografía — Análisis territorial, SIG y climatología)**
*   **Fuentes a contrastar:** Guías Docentes del Grado en Geografía y Gestión del Territorio UGR (Facultad de Filosofía y Letras). Asignaturas de Geografía Física, Climatología, Análisis Territorial y Sistemas de Información Geográfica (SIG).
*   **Segregación previsible:** Geografía Física/Climatología vs. Geografía Humana/Territorial vs. SIG/Cartografía (norma permanente: segregar).
*   **Documentos a actualizar:** `V06DOC_SUBARCHETYPES.md`, `V06DOC_SUBDIVISIONS.md`.

**PASO S10 — SUB-SOC-WORK (Trabajo Social — Intervención social, políticas y mediación comunitaria)**
*   **Fuentes a contrastar:** Guías Docentes del Grado en Trabajo Social UGR (Facultad de Trabajo Social). Asignaturas de Métodos y Técnicas de Intervención Social, Política Social, Mediación Comunitaria.
*   **Segregación previsible:** Intervención individual/familiar vs. Intervención comunitaria vs. Políticas sociales (norma permanente: segregar).
*   **Documentos a actualizar:** `V06DOC_SUBARCHETYPES.md`, `V06DOC_SUBDIVISIONS.md`.

---

### 3. CONTROL DE INTEGRIDAD — ESTADO DE LAS RAMAS

**RAMA LENGUAS — CERRADA (v5.1/v5.2 — 2026-04-20/21):**
*   `SUB-LIN-INSTR` — [CERTIFICADO v5.0 — 2026-04-19]
*   `SUB-LIN-MINOR` — [CERTIFICADO v5.1 — 2026-04-20]
*   `SUB-LIN-PHILO` — [CERTIFICADO v5.1 — 2026-04-20]
*   `SUB-LIN-ECDO` — [CERTIFICADO v5.1 — 2026-04-20]
*   `SUB-LIN-NORM` — [CERTIFICADO v5.1 — 2026-04-20]
*   `SUB-LIN-TRA-TECH` — [CERTIFICADO v5.1 — 2026-04-20 / SINCRONIZADO v5.2 — 2026-04-21]
*   `SUB-LIN-TRA-LIT` — [CERTIFICADO v5.1 — 2026-04-20 / SINCRONIZADO v5.2 — 2026-04-21]

**RAMA HUMANIDADES — CERRADA (v5.3 — 2026-04-22):**
*   `SUB-HUM-HIST` — [CERTIFICADO v5.3 — 2026-04-22]
*   `SUB-HUM-PHIL` — [CERTIFICADO v5.3 — 2026-04-22]
*   `SUB-HUM-ART-HIST` — [CERTIFICADO v5.3 — 2026-04-22]
*   `SUB-HUM-ART-CREA` — [CERTIFICADO v5.3 — 2026-04-22] — Emulación Parcial Certificada
*   `SUB-HUM-MUS` — [CERTIFICADO v5.3 — 2026-04-22]
*   `SUB-HUM-ANTH` — [CERTIFICADO v5.3 — 2026-04-22] — Subarquetipo Transversal

**RAMA CIENCIAS DE LA SALUD — CERRADA (v5.4 — 2026-04-25):**
*   `SUB-SAN-MED-CLIN` — [CERTIFICADO v5.4 — 2026-04-25] — UGR Medicina
*   `SUB-SAN-MED-BASIC` — [CERTIFICADO v5.4 — 2026-04-25] — UGR Medicina
*   `SUB-SAN-MED-FISIO-GEN` — [CERTIFICADO v5.4 — 2026-04-25] — UGR Medicina
*   `SUB-SAN-MED-FISIO-NEURO` — [CERTIFICADO v5.4 — 2026-04-25] — UGR Medicina
*   `SUB-SAN-CUID` — [CERTIFICADO v5.4 — 2026-04-25] — UGR Enfermería
*   `SUB-SAN-ODON` — [CERTIFICADO v5.4 — 2026-04-25] — UGR Odontología — Emulación Parcial Certificada
*   `SUB-SAN-FISIO` — [CERTIFICADO v5.4 — 2026-04-25] — UGR Fisioterapia — Emulación Parcial Certificada
*   `SUB-SAN-BIOQUIM` — [CERTIFICADO v5.4 — 2026-04-25] — UGR Farmacia — Emulación Parcial Certificada
*   `SUB-SAN-FARM` — [CERTIFICADO v5.4 — 2026-04-25] — UGR Farmacia
*   `SUB-SAN-PSY-DIAG` — [CERTIFICADO v5.4 — 2026-04-25] — UGR Psicología
*   `SUB-SAN-PSY-EVAL` — [CERTIFICADO v5.4 — 2026-04-25] — UGR Psicología
*   `SUB-SAN-PSY-MET` — [CERTIFICADO v5.4 — 2026-04-25] — UGR Psicología
*   `SUB-SAN-PSY-STAT` — [CERTIFICADO v5.4 — 2026-04-25] — UGR Psicología
*   `SUB-SAN-VET-CLIN` — [CERTIFICADO v5.4 — 2026-04-25] — UCO Veterinaria — Emulación Parcial Certificada
*   `SUB-SAN-VET-CIR` — [CERTIFICADO v5.4 — 2026-04-25] — UCO Veterinaria — Emulación Parcial Certificada
*   `SUB-SAN-NUT-DIET` — [CERTIFICADO v5.4 — 2026-04-25] — UGR Nutrición
*   `SUB-SAN-NUT-BROM` — [CERTIFICADO v5.4 — 2026-04-25] — UGR Nutrición — Emulación Parcial Certificada
*   `SUB-SAN-NUT-SPUB` — [CERTIFICADO v5.4 — 2026-04-25] — UGR Nutrición — Doble umbral vinculante (40% por bloque)

**SINCRONIZACIÓN CONSTELACIÓN (v5.4 — 2026-04-25):**
*   `V06DOC_SUBARCHETYPES.md` — [SINCRONIZADO v5.4 — 2026-04-25]: 18 bloques de la Rama Ciencias de la Salud completos.
*   `V06DOC_SUBDIVISIONS.md` — [SINCRONIZADO v5.4 — 2026-04-25]: Secciones 4.1 a 4.18 añadidas con desglose competencial completo de todos los subarquetipos de la rama.

**RAMA CIENCIAS SOCIALES Y JURÍDICAS — ✅ CERRADA (v5.5 — 2026-04-27):**
*   S1-S10: todos los subarquetipos certificados y consolidados (secciones 5.1 a 5.26 de ).

**RAMA CIENCIAS TÉCNICAS E INGENIERÍA — ✅ CERRADA (v5.6 — 2026-04-28):**
*   `SUB-TEC-SOFT` → `SUB-TEC-SOFT-ALG` + `SUB-TEC-SOFT-DS` + `SUB-TEC-SOFT-SE` — [CERTIFICADO v5.6 — 2026-04-28] — ETSIIT-UGR
*   `SUB-TEC-CIVIL` → `SUB-TEC-CIVIL-STRUCT` + `SUB-TEC-CIVIL-CONC` + `SUB-TEC-CIVIL-STEEL` — [CERTIFICADO v5.6 — 2026-04-28] — ETSICCP-UGR
*   `SUB-TEC-INDUS` → `SUB-TEC-INDUS-THERMO` + `SUB-TEC-INDUS-TMM` + `SUB-TEC-INDUS-DEM` — [CERTIFICADO v5.6 — 2026-04-28] — EPSC-UCO
*   `SUB-TEC-CHEM` → `SUB-TEC-CHEM-BAL` + `SUB-TEC-CHEM-REACT` — [CERTIFICADO v5.6 — 2026-04-28] — UGR Ingeniería Química
*   `SUB-TEC-PROJ` → `SUB-TEC-PROJ-ARCH` + `SUB-TEC-PROJ-URB` — [CERTIFICADO v5.6 — 2026-04-28] — ETSAG-UGR
*   `SUB-TEC-CONS` → `SUB-TEC-CONS-TECH` + `SUB-TEC-CONS-MAN` — [CERTIFICADO v5.6 — 2026-04-28] — ETSIE-UGR
*   `SUB-TEC-PURE` → `SUB-TEC-PURE-ANAL` + `SUB-TEC-PURE-ALGSTR` — [CERTIFICADO v5.6 — 2026-04-28] — Grado Matemáticas UGR

**SINCRONIZACIÓN CONSTELACIÓN (v5.6 — 2026-04-28):**
*   `V06DOC_SUBARCHETYPES.md` — [SINCRONIZADO v5.6 — 2026-04-28]: Sección ## 4. RAMA: INGENIERÍA Y ARQUITECTURA añadida con 16 subarquetipos certificados (secciones 6.1 a 6.20).
*   `V06DOC_SUBDIVISIONS.md` — [SINCRONIZADO v5.6 — 2026-04-28]: Secciones 6.1 a 6.20 añadidas con desglose competencial completo de todos los subarquetipos de la rama.

**RAMA CIENCIAS — ✅ CERRADA (v5.7 — 2026-05-02):**
*   `SUB-SCI-BIO` → `SUB-SCI-BIO-GEN` + `SUB-SCI-BIO-ZOO` + `SUB-SCI-BIO-ECO` — [CERTIFICADO v5.7 — 2026-04-28] — UGR Biología
*   `SUB-SCI-CHEM` → `SUB-SCI-CHEM-ORG` + `SUB-SCI-CHEM-INORG` — [CERTIFICADO v5.7 — 2026-04-28] — UGR Química
*   `SUB-SCI-PHYS` → `SUB-SCI-PHYS-EM` + `SUB-SCI-PHYS-QM` — [CERTIFICADO v5.7 — 2026-04-28] — UGR Física
*   `SUB-SCI-GEOL` → `SUB-SCI-GEOL-MIN` + `SUB-SCI-GEOL-STRAT` + `SUB-SCI-GEOL-MAP` — [CERTIFICADO v5.7 — 2026-04-28] — UGR Geología
*   `SUB-SCI-ENV` → `SUB-SCI-ENV-RES` + `SUB-SCI-ENV-CONT` — [CERTIFICADO v5.7 — 2026-04-28] — UGR Ciencias Ambientales
*   `SUB-SCI-DATA` → `SUB-SCI-DATA-STAT` + `SUB-SCI-DATA-ML` + `SUB-SCI-DATA-BIG` — [CERTIFICADO v5.7 — 2026-05-02] — UCM GIDIA (nota vinculante: UGR no dispone de guías docentes activas para el Grado en Ciencias de Datos e IA en 2025-2026)

**SINCRONIZACIÓN CONSTELACIÓN (v5.7 — 2026-05-02):**
*   `V06DOC_SUBARCHETYPES.md` — [SINCRONIZADO v5.7 — 2026-05-02]: Sección ## 5. RAMA: CIENCIAS completa con 14 subarquetipos certificados.
*   `V06DOC_SUBDIVISIONS.md` — [SINCRONIZADO v5.7 — 2026-05-02]: Secciones 7.1 a 7.15 añadidas con desglose competencial completo de todos los subarquetipos de la rama.

---

**PROHIBICIONES ABSOLUTAS:**
*   El modelo de la próxima sesión **NO PODRÁ INVENTAR NI SUPONER NADA** que no esté escrito en esta hoja de ruta o en la documentación satélite auditada.
*   **NO** se permite el salto a otras ramas hasta que todos los subarquetipos de la Rama Ciencias alcancen Fidelidad 100% certificada por el usuario.
*   **NO** se modificará ningún subarquetipo ya certificado salvo indicación explícita del usuario con el nombre exacto del subarquetipo a revisar.
*   **NORMA PERMANENTE INAMOVIBLE:** Ante cualquier disyuntiva de aglutinar vs. segregar → SIEMPRE SEGREGAR. Sin excepción. Sin consulta.
*   **FLUJO DE TRABAJO ACTIVO (consolidado 2026-04-27/28):** Investigación → Segregación → Bloques → PMA directo. Sin presentación intermedia en chat. Solo se detiene para la autorización del diff.
