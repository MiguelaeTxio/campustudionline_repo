# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06 -- HITO 6: SISTEMA DE AUTOEVALUACIONES CON IA

## 1. Descripcion del Hito

Motor de autoevaluacion con IA basado en arquetipos y subarquetipos academicos.
82 subarquetipos certificados. 22 widgets de evaluacion. 20 motores de calificacion.

---

## 2. HOJA DE RUTA PARA LA PROXIMA SESION (LEY SUPREMA - INELUDIBLE)

**ESTADO DEL HITO:** EN PROGRESO - Pipeline VERIFICADO en produccion de extremo a extremo para ARCH_SCI (S024). Pendiente extension a los cinco arquetipos restantes.
**FECHA DE ULTIMA ACTUALIZACION:** 2026-07-27
**OBJETIVO S025:** Completar la prueba E2E para los cinco arquetipos que faltan y ejercitar los casos especiales que S024 no llego a tocar.

---

### RESULTADO DE S024 -- PRIMER PIPELINE COMPLETO DESDE EL 2026-03-17

Los seis puntos de verificacion que exigia la hoja de ruta anterior quedan
CERRADOS para ARCH_SCI / SUB-SCI-PHYS-EM, verificados EJECUTANDO, no leyendo:

| Punto | Verificacion | Evidencia |
|---|---|---|
| a | Clasificacion IA correcta | ARCH_SCI / SUB-SCI-PHYS-EM |
| b | Skeleton correcto del subarquetipo | 2 secciones (SD_PHYS_TEORIA, SD_PHYS_CALC) |
| c | Llenado completo de items | 2/2 con contenido real |
| d | Widgets renderizados | W-OBJ-STRIKE y W-TECH-CALC, vistos en navegador |
| e | Entrega y calificacion | nota -0.1667, section_scores por seccion |
| f | Informe con qualitative_summary | Valoracion del Catedratico renderizada |

Examen de referencia: `d53500e2-af55-499b-947f-fad85b1fcd48`, generado,
respondido, entregado y calificado desde el navegador por Miguel Angel.

---

### HALLAZGO CENTRAL DE S024 -- LA CERTIFICACION POR LECTURA NO DETECTA ESTOS FALLOS

S023 declaro CERTIFICADOS los 18 archivos de la Fase de Implementacion tras
una auditoria TLA bidireccional contra 11 satelites, con 0 fallos de codigo.
S024 encontro SIETE defectos que impedian por completo el funcionamiento del
motor, ninguno detectable leyendo el codigo, y todos en archivos que aquella
auditoria dio por buenos.

El patron es sistematico y conviene tenerlo presente: **cada defecto tapaba
al siguiente**. El schema invalido abortaba la generacion antes de alcanzar
dos NameError; corregidos esos, la plantilla no compilaba por un filtro
inexistente; compilada, su JavaScript entero estaba muerto por una cadena
mal cerrada; vivo el JavaScript, la URL de entrega apuntaba a un prefijo que
no existe; corregida, el informe reventaba por una clave fantasma. Ninguna
auditoria estatica encuentra el escalon N+1 mientras el escalon N siga en pie.

**Lo que se hizo el 2026-05-28 y nunca se registro:** existia ya un intento
de esta misma prueba E2E, dos dias despues de cerrar S023, con los seis
arquetipos lanzados en lote (17:27:59-17:28:00). Los seis fallaron identicamente
con `AIServiceCriticalError: ABORTO FATAL: La Seccion no pudo generarse tras
3 intentos`. Ese intento no quedo anotado en este anexo, cuya ultima
actualizacion seguia siendo del 2026-05-26, de modo que S024 arranco creyendo
que el sistema estaba sin estrenar. Los seis examenes siguen en la base de
datos en estado ERROR y son la evidencia que permitio el diagnostico.

---

### HOJA DE RUTA S025 -- EN ESTE ORDEN

PASO 1 -- Completar la prueba E2E de los cinco arquetipos restantes
- ARCH_TECH, ARCH_HEALTH, ARCH_SOC, ARCH_HUM, ARCH_LANG.
- Las copias de estudio ya existen (Fisica, Antropologia social, Economia
  Politica, Anatomia y las de idiomas), y arrastran el aviso rojo de
  `assessment_status == ERROR` del lote del 2026-05-28. El aviso desaparece
  al generar un examen nuevo que llegue a READY.
- Verificar los seis puntos (a-f) en cada uno, igual que en ARCH_SCI.

PASO 2 -- Ejercitar W-TXT-CLOZE (SIN PROBAR TODAVIA)
El normalizador `_normalize_gap_solutions` de `base.py` se escribio en S024
y NO se ha ejecutado nunca con datos reales de la IA: el examen de Fisica uso
W-OBJ-STRIKE y W-TECH-CALC, que no llevan `gap_solutions`. Hace falta un
examen con widget cloze para confirmar que la IA respeta el contrato NUEVO
(lista de objetos `{gap_id, accepted_answer}`) y que los motores CLO-OPEN y
CLO-MULTI lo normalizan bien. Es la unica pieza de S024 sin verificar.

PASO 3 -- Casos especiales que el anexo anterior ya pedia y siguen pendientes
- Asignatura de Magisterio: confirmar que AcademicDeductor le asigna ITIN_DOC.
- SUB-LIN-MINOR en japones: confirmar que `wanakana.bind()` se activa leyendo
  `data-target-lang` del div#exam-container (modo Occidentalizacion).
- Atencion especial a las secciones SD_LIST: el disparador de audio contenia
  un NameError corregido en S024 (7504fd9) que nunca llego a ejecutarse. El
  primer examen de idiomas con comprension oral es su estreno real.

PASO 4 -- Decidir apertura a usuarios reales
El panel de evaluacion de `edit_copy.html` esta condicionado a
`request.user.is_staff or request.user.id == 1`; el resto de usuarios ve la
pantalla "En Mantenimiento". Abrir implica relajar esa condicion.

---

### DEUDA TECNICA ABIERTA, DETECTADA EN S024

**1. Dos tareas periodicas fantasma (prioridad alta, afecta a reglas de negocio del hito).**
Beat dispara puntualmente `orchestrator.tasks.purge_and_penalize_corrections`
y `orchestrator.tasks.expire_untaken_assessments`. Ninguna de las dos existe
en el codigo -- cero coincidencias en todo el arbol. El worker Pesado las
recibe por la cola `default`, no las tiene registradas y las descarta con
`KeyError`, dejando un traceback en el log cada vez.

Esto no es solo ruido: `expire_untaken_assessments` es el mecanismo que
implementaria la regla anti-abuso que el propio modelo `Exam` documenta
(`expiration_date`, "24h tras el estado READY, penalizacion total si no se
realiza", estado `EXPIRED_UNTAKEN`). **Esa regla no se esta aplicando.**
Decidir si se implementan las dos tareas o se eliminan las filas huerfanas
de `PeriodicTask`.

**2. Cobertura de verificacion.** S024 improviso tres controles que
encontraron defectos reales y que convendria sistematizar antes de dar por
buena cualquier plantilla o modulo del motor:
- `node --check` sobre el JavaScript embebido, sustituyendo las etiquetas de
  Django por literales (encontro la cadena partida de `exam_take.html`).
- `pyflakes` sobre `orchestrator/tasks.py` y `assessment_v2/services/engine/`
  (encontro el NameError de SD_LIST antes de que se ejecutara).
- Render real de cada plantilla via `django.test.Client` con
  `SERVER_NAME='www.campustudionline.com'` y `force_login`, que es lo que
  destapo el filtro `split`, la clave fantasma del informe y las trazas
  completas que el log del servidor entrega truncadas a ~1000 caracteres.

**3. Pool de claves API.** ~100 claves, casi todas con
`consecutive_failures = 6` y ninguna en cuarentena. La clave activa (MAMC)
esta a 0 pese a acumular 18 fallos el 2026-05-28, porque la rama de error
no-cuota de `_safe_generate_content` no incrementa el contador. Residuo
antiguo, sin efecto operativo conocido, anotado por si aparece.

---

### FASE DE IMPLEMENTACION - ESTADO FINAL (S023 -- 2026-05-26)

**18/18 ARCHIVOS CERTIFICADOS (Auditoria TLA S023 -- 0 fallos de codigo):**
1. assessment_v2/models/main.py -- INC-01: comentario INGENIERIA (16)->(17)
2. core/services/gemini_schemas.py -- INC-04: SD_MEDI eliminado. INC-05: step_matrix. INC-06: gap_solutions dict
3. core/services/gemini_service.py -- Sin incidencias
4. assessment_v2/services/engine/strategies/base.py -- INC-07: _grade_ev_tra_precision
5. assessment_v2/services/engine/logic.py -- ITIN_DOC verificado y certificado
6. assessment_v2/services/engine/factory.py -- Sin incidencias
7. assessment_v2/services/engine/strategies/languages.py -- INC-07: EV-TRA-PRECISION en grade_item
8. assessment_v2/services/engine/strategies/health.py -- 18 subarquetipos conformes
9. assessment_v2/services/engine/strategies/humanities.py -- 6 subarquetipos conformes
10. assessment_v2/services/engine/strategies/science.py -- 15 subarquetipos conformes
11. assessment_v2/services/engine/strategies/social.py -- 19 subarquetipos conformes
12. assessment_v2/services/engine/strategies/tech.py -- 17 subarquetipos conformes
13. orchestrator/tasks.py -- Pipeline Skeleton-First verificado
14. assessment_v2/views.py -- Barrera de fuego Data Leak verificada
15. assessment_v2/services/quotas.py -- Ventana movil y penalizacion FREE verificadas
16. assessment_v2/templates/assessment_v2/exam_take.html -- 22/22 widgets. Occidentalizacion (ja/ar/el). data-target-lang
17. assessment_v2/templates/assessment_v2/exam_report.html -- INC-09: qualitative_summary. INC-10: rutas feedback
18. assessment_v2/management/commands/validate_v06_engines.py -- INC-11: docstring 87->82

**DOCUMENTACION SATELITE ACTUALIZADA:**
- V06DOC_LEVELS.md -- Seccion 5 ITIN_DOC certificado (5.1-5.6, base documental UGR 2024-2025)

---

### S024 -- PLAN PREVISIONAL (SUPERADO POR LOS HECHOS)

El plan que esta seccion contenia (verificacion de servidor, prueba E2E de los
seis arquetipos, resolucion de incidencias y decision de apertura) se ejecuto
realmente en S024. Su resultado, mucho mas extenso de lo previsto por los siete
defectos encontrados, esta recogido en la seccion 2 de este mismo anexo. Las dos
notas tecnicas que acompanaban al plan (ITIN_DOC en Magisterio y modo
Occidentalizacion en japones) siguen VIGENTES y se han trasladado al PASO 3 de la
hoja de ruta de S025, porque S024 no llego a tocar ningun examen de idiomas.

---

### NOTA DE DESVIO DE S024 -- INCIDENCIA DE PRODUCCION AJENA AL HITO

Trabajo realizado durante S024 que NO pertenece a H06 y se registra aqui por
no existir hito de infraestructura al que adscribirlo.

**Caida total de produccion (resuelta).** Al arrancar la sesion el sitio
devolvia 500 en TODAS las paginas -- portada, login, directorio academico y
contenidos -- de forma continua y desde antes de la sesion. Causa:
`staticfiles_production` contenia los 188 archivos pero NO `staticfiles.json`.
Con `ManifestStaticFilesStorage`, cada `{% static %}` de `templates/base.html`
lanza `ValueError: Missing staticfiles manifest entry for
'images/og_branded_default.png'` al renderizar, de ahi que cayeran todas las
vistas a la vez pese a estar en apps distintas. El estatico de origen existia
y siempre existio: faltaba el manifiesto entero. Resuelto ejecutando
`collectstatic --noinput` sin `--clear` (0 copiados, 188 sin cambios, 188
post-procesados, manifiesto de 14939 bytes).

**Queda sin explicar, y se deja constancia en vez de inventar una causa:** por
que el `collectstatic --noinput --clear` del despliegue automatico de las 06:16
UTC de ese dia termino con exito (paso en verde, con `set -o pipefail` exterior
y `set -e` interior) y aun asi dejo STATIC_ROOT sin manifiesto.

**Tres correcciones del pipeline de despliegue** (`.github/workflows/deploy.yml`):
1. `3ff1e65` -- retirado `--clear` de collectstatic, que vaciaba STATIC_ROOT
   antes de regenerar y convertia cualquier fallo posterior en una caida total.
   Anadida barrera dura que aborta el despliegue si el manifiesto no existe o
   esta vacio, para que el paso no pueda volver a reportar exito dejando el
   sitio inservible.
2. `d113f58` -- anadido `assessment_v2/` a los patrones de reinicio condicional
   de ambas Always-on Tasks. Sin ello, un cambio que tocara solo las estrategias
   del motor se desplegaba al disco pero ningun worker se reiniciaba, dejando
   produccion ejecutando codigo viejo de forma indefinida y silenciosa.
3. `2d330e2` -- el paso de recarga de la web app usaba `curl -sf`, que aborta
   sin dejar rastro del motivo, y el reinicio de workers estaba condicionado a
   `if: success()` de ese paso. Tres despliegues seguidos fallaron en la recarga
   y arrastraron consigo el reinicio, que quedo omitido las tres veces. Ahora se
   captura el codigo HTTP y el cuerpo, se imprimen, y se anexan por SSH a
   `/home/MiguelAeTxio/SWAP/deploy_reload_history.txt` -- artefacto descargable
   por sftp, porque el log de Actions vive en un host de Azure
   (`productionresultssa0`) fuera de la red alcanzable por el modelo, sondeado
   ocho veces y fijo por job. El reinicio pasa a depender de
   `steps.deploy.outcome == 'success'`, que es su unica precondicion real.
   Los tres fallos de recarga resultaron ser transitorios y se resolvieron
   solos: probable limite de peticiones de la API de PythonAnywhere.

**Documentacion.** `37fcc2d` anadio la seccion LOGS a
`DOCS/MAINS/SESSION_VARIABLES.md` con las rutas reales del servidor
(web access/error/server y los dos always-on), confirmadas contra el panel de
PythonAnywhere. Hasta entonces el PVR de `com-file-request` bloqueaba toda
solicitud de logs del proyecto por ausencia de esas variables.

**Cambio de visibilidad del repositorio.** Miguel Angel hizo publico
`campustudionline_repo` durante la sesion, para recuperar minutos de GitHub
Actions. Auditoria previa entregada antes de la decision: arbol limpio de
credenciales, claves GCP del incidente del 2026-07-24 efectivamente purgadas
del historial (`git log --all` vacio), `.env` nunca versionado y 0 forks. Se
dejo constancia de que la exposicion del motor y sus prompts es irreversible y
de que existian alternativas (esperar al reinicio de cuota, subir el limite de
gasto, o el despliegue manual que ya estaba preparado). Decision del propietario.

---

## 3. Arquitectura del Motor (Referencia)

### 3.1. Pipeline de Generacion (Skeleton-First)
ExamCreateView.post
  -> generate_exam_task.delay(exam_uuid, context_text, topic)
    -> AcademicDeductor.get_context_metadata(subject)
      -> Fase 1: classify_subject_identity (IA Gemini)
      -> Fase 2: deduce_itinerary / deduce_level / deduce_immersion_mode (Python)
    -> ExamFactory.get_strategy(archetype_id, sub_archetype_id, ...)
    -> strategy.get_exam_skeleton() -> ExamSection + ExamItem (vacios)
    -> [bucle por seccion] strategy.get_user_prompt + get_system_prompt
      -> _safe_generate_content -> Gemini API
      -> dirtyjson.loads -> mapeo por UUID -> db_item.save()
    -> exam.status = READY

### 3.2. Pipeline de Calificacion
ExamSubmitView.post
  -> ExamFactory.get_strategy(...)
  -> GradingOrchestrator.grade_submission(submission, strategy)
    -> [por seccion][por item] strategy.grade_item(item, student_input)
    -> apply_rigor_adjustment(raw_score)
    -> kill-switches: CDS-KILL, ITIN_INV, ARCH_HEALTH, ARCH_HUM, ARCH_SOC
    -> gating: ARCH_LANG Non-Compensation Rule
    -> _generate_qualitative_feedback (Voz del Catedratico)
  -> submission.grading_report = report
  -> exam.status = GRADED

### 3.3. Widgets Implementados (22/22)
W-TECH-CALC, W-PROC-ACTION, W-CLIN-SCAN, W-OBJ-STRIKE, W-HUM-TEXT,
W-TXT-CLOZE, W-MIX-MATCH, W-LAW-NAV, W-COMM-DIALOG, W-AUDIO-INSTR,
W-MUS-SCORE, W-ART-IDENT, W-CALLI-PAD, W-PORTFOLIO, W-PHILO-IPA,
W-PHILO-ECDO, W-PHILO-OCR-PALE, W-DOC-RESOURCES, W-CASE-ECOE,
W-MEDI-LAYOUT, W-OCR-PRO, W-INSTR-SELECTOR

### 3.4. Motores de Calificacion (20/20)
PRM-STRIKE, RBT-CANON, RBT-SHORT-LANG, RPP-TRAZA, CDS-KILL,
DRA-HOLO, DRA-HOLO-LIT, BMT-SHIFT, ILC-CONTEXT, EV-PALE,
EV-DIAC-VAL, EV-NORM-ANALYSIS, EV-TRA-PRECISION, EV-TRA-PRECISION-TECH,
EV-ICON-ART, EV-MUS-ANAL, CLO-OPEN, CLO-MULTI, MAT-LINK, DIA-INTERACT

---

## 4. Registro de Sesiones

NOTA DE AUDITORIA (PAA -- 2026-05-09): Tabla reconstruida via PAA desde historial Git.
S001-S008: Etapa Pre-v5.0 sin certificacion contra fuentes primarias UGR.
S009+: Fase de Certificacion con Fidelidad 100% UGR garantizada.

S001  2026-03-18  Pre-v5.0 SUB-LIN-INSTR/MINOR       Refactorizacion subatomica inicial. Sin certificacion UGR.
S002  2026-03-19  Pre-v5.0 SUB-LIN-PHILO              Refactorizacion PHILO. Motores EV-DIAC-VAL y EV-PALE. Sin certificacion UGR.
S003  2026-03-19  Pre-v5.0 SUB-LIN-NORM               Refactorizacion NORM. Motor EV-NORM-ANALYSIS. Sin certificacion UGR.
S004  2026-03-19  Pre-v5.0 Blindaje documental         Reescritura integra del anexo V06. V06DOC_WORD_OF_GOD revertido en S009.
S005  2026-03-19  Pre-v5.0 SUB-LIN-TRA-TECH           Refactorizacion TRA-TECH. Jerarquia errores FTI. Sin certificacion UGR.
S006  2026-03-22  Pre-v5.0 SUB-LIN-NORM bis           Nueva sesion NRA NORM. Calibracion x1.7. Sin certificacion UGR.
S007  2026-03-23  Pre-v5.0 TRA-TECH quirurgico         Reconstruccion quirurgica post-sobrescritura. Hoja de ruta reescrita.
S008  2026-03-25  Pre-v5.0 Infraestructura             Correccion AttributeError users/views.py. Resolucion OSError NFS.
S009  2026-04-19  v5.0 SUB-LIN-INSTR cert.            INICIO CERTIFICACION REAL. 12 errores corregidos. Constelacion v5.0.
S010  2026-04-20  v5.1 SUB-LIN-MINOR/PHILO/ECDO       9 lenguas MINOR. Tri-destreza PHILO. Desmembramiento ECDO. v5.1.
S011  2026-04-20  v5.1 SUB-LIN-NORM/TRA-TECH/LIT      Rama Lenguas CERRADA. SDK google-genai 1.55.0->1.73.1. v5.1.
S012  2026-04-21  v5.2 Sincronizacion + HUM Fase A    W-DOC-RESOURCES. DRA-HOLO-LIT. Arranque Humanidades. v5.2.
S013  2026-04-22  v5.3 Humanidades cert.              6 subarquetipos HUM. Rama Humanidades CERRADA. v5.3.
S014  2026-04-25  v5.4 Ciencias de la Salud cert.     18 subarquetipos SALUD. DECISION: siempre segregar. Rama CERRADA. v5.4.
S015  2026-04-26  v5.5 CSJ pasos S1-S4                9 subarquetipos Derecho+Economia.
S016  2026-04-27  v5.5 CSJ pasos S5-S10               19 subarquetipos totales CSJ. Rama CERRADA. v5.5.
S017  2026-04-28  v5.6 Ingenieria cert.               17 subarquetipos Ingenieria. Rama CERRADA. v5.6.
S018  2026-05-02  v5.7 Ciencias cert.                 SUB-SCI-DATA (fuente UCM GIDIA). Rama Ciencias CERRADA. v5.7.
S019  2026-05-11  v5.9 Auditoria Fidelidad 87/87       86 CONFORMES + 1 leve. AUTORIZADA para implementacion.
S020  2026-05-16  Resolucion TRA-LIT + Apertura        SUB-LIN-TRA-LIT resuelto. PEAs models/main.py + gemini_schemas.py.
S021  2026-05-24  Implementacion core 12/17 archivos   PEAs base.py, logic.py, factory.py, 6 strategies, tasks.py, views.py, quotas.py.
S022  2026-05-25  Implementacion cierre 17/17 archivos exam_take.html (22 widgets), exam_report.html, validate_v06_engines.py. SYNTAX OK.
S023  2026-05-26  Auditoria TLA + Certificacion        11 incidencias: 9 resueltas, 2 cerradas. ITIN_DOC certificado V06DOC_LEVELS. Modo Occidentalizacion (ja/ar/el). Selector rango verificado. Fase Implementacion CERTIFICADA. collectstatic ejecutado.
S024  2026-07-27  Pipeline E2E VERIFICADO (ARCH_SCI)   7 defectos corregidos, ninguno detectable por lectura: additionalProperties en el schema (ff562bb), 2 NameError en generate_exam_task (7504fd9), filtro 'split' inexistente (5c78a00), URL de entrega con prefijo erroneo (4f72fce), cadena JS partida que anulaba todo el script (5656bce), clave fantasma en el informe (7e8b3f9). Cada uno tapaba al siguiente. Los seis puntos (a-f) cerrados para ARCH_SCI ejecutando, no leyendo. Desvio: caida total de produccion por manifiesto de estaticos ausente + 3 correcciones del pipeline de despliegue. Pendiente: 5 arquetipos, W-TXT-CLOZE, ITIN_DOC, japones.
