# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06 -- HITO 6: SISTEMA DE AUTOEVALUACIONES CON IA

## 1. Descripcion del Hito

Motor de autoevaluacion con IA basado en arquetipos y subarquetipos academicos.
82 subarquetipos certificados. 22 widgets de evaluacion. 20 motores de calificacion.

---

## 2. HOJA DE RUTA PARA LA PROXIMA SESION (LEY SUPREMA - INELUDIBLE)

**ESTADO DEL PIPELINE:** VERIFICADO en produccion de extremo a extremo para
ARCH_SCI (S024), ARCH_LANG (S025), ARCH_TECH (S026) y ARCH_SOC (S028, seis
puntos completos). ARCH_HEALTH: PASO 4 CERRADO en S030 por decision
explicita de Miguel Angel -- ver detalle completo mas abajo, incluida la
parte que quedo sin verificar (motor de calificacion real de ILC-CONTEXT
para el item 249, solo se ejercito el kill-switch de campo vacio).
ARCH_HUM: puntos e-f siguen pendientes de respuesta real. `SD_LIST`
(S028): CERRADO del todo. Motor de refinamiento `PENDING_AI_ANALYSIS`:
CONSTRUIDO Y VERIFICADO end-to-end en S029 (entorno controlado) y
en S030 verificado por segunda vez contra un examen 100% de produccion
(ver PASO 4); vive como hito propio (H39, PAUSADO).
**FECHA DE ULTIMA ACTUALIZACION:** 2026-08-05 (S030)
**NOTA:** el estado de seguimiento del hito (EN PROGRESO / PAUSADO) vive
exclusivamente en `CAMPUSTUDIONLINE_ANNEX_ROUTER.md`. Este anexo no lo declara,
conforme a la regla de oro 1 del PCH. La linea que antes decia
"ESTADO DEL HITO: EN PROGRESO" era una infraccion heredada, corregida en S026.

---

### REACTIVACION EN S028 -- 2026-07-31

Hito reactivado. H38 (Adquisicion y Licenciamiento de Imagenes para
Evaluaciones) cerro sus siete puntos en S027, verificados con datos
reales de produccion; el bloqueo que pausaba este hito desaparecio.
Miguel Angel confirmo la reanudacion explicitamente. La hoja de ruta
de reanudacion, redactada en S026 ("HOJA DE RUTA AL REANUDAR H06",
mas abajo), no se modifica -- sigue siendo la ley suprema tal cual
quedo escrita, con su orden PASO 1 (ARCH_SOC y ARCH_HUM primero,
despues ARCH_HEALTH ahora que H38 ya entrega imagenes reales) en
adelante.

---

### RESULTADO DE S028 -- ARCH_SOC CERRADO, ARCH_HEALTH VERIFICADO CON IMAGENES REALES DE H38, ARCH_HUM PARCIAL

**ARCH_SOC cerrado.** SUB-SOC-ECON-MGMT-ECO ("Economia Politica"), LVL_A,
examen `67a49ecd-21c2-49c8-a2a1-11426f387cfd`. Los seis puntos (a-f)
verificados EJECUTANDO: clasificacion correcta, skeleton de 2 secciones
(Microeconomia / Macroeconomia), 3 items con contenido real (2 opcion
multiple + 1 problema abierto Cobb-Douglas), widgets renderizados,
entrega calificada (nota 0,0833, verificada CORRECTA por calculo:
seccion 1 = (1,00+0,00)/2 = 0,5; seccion 2 = -0,33 por penalizacion
1/(N-1) en opcion incorrecta de 4; media de secciones = 1/12 = 0,0833),
informe con Valoracion del Catedratico. Centinela `<<NL>>` confirmado
sano en contenido con pasos numerados (Paso 1 a Paso 4 en lineas
separadas). Este subarquetipo no usa `W-HUM-TEXT`, no ejercita
`source_text`. El aviso rojo heredado del lote 2026-05-28 (examen
`df036475`, ERROR) queda resuelto.

**ARCH_HEALTH -- imagenes reales de H38 confirmadas en produccion.**
SUB-SAN-MED-BASIC ("Anatomia"), LVL_A, examen `2c1c80e4-f554-4dd3-8ff9-
e57a96e996d9`. Skeleton de 3 secciones (Anatomia Macroscopica,
Anatomia Radiologica, Histologia Microscopica), 3/3 items con contenido
real. Los dos items `W-CLIN-SCAN` muestran imagenes REALES y DISTINTAS
entre si -- globo ocular (Patrick J. Lynch, licencia UNKNOWN) y molde de
corrosion vascular (Own work, CC-BY-SA-4.0) -- confirmando en una
generacion fresca de esta sesion tanto el servicio de recuperacion como
la deduplicacion a nivel de examen (arreglo de S027) y la propagacion de
atribucion al informe (tambien con miniaturas e licencia visibles).
Ningun `<img>` roto, ningun dominio inventado. Puntos a-d y f cerrados
por lectura de pantalla real. Punto e (entrega y calificacion) queda
solo PARCIALMENTE verificado: el examen se entrego sin respuesta real
en los campos de interpretacion (nota final 0,0000), igual que en
ARCH_SOC placeholder y en ARCH_HUM -- valida el camino de entrega y el
kill-switch/penalizacion por campo vacio, pero no el motor de
calificacion real de EV-* /CDS-KILL contra una respuesta con contenido.

**ARCH_HUM -- parcial, pero con hallazgo bueno.** SUB-HUM-ANTH
("Antropologia social"), LVL_A, examen `025e14d7-a32e-4925-911e-
199fa4bb0070`. Clasificacion y skeleton correctos (2 secciones:
Comentario de Fuente Etnografica / Disertacion Comparativa
Intercultural), 2/2 items con contenido real. **`source_text`
CONFIRMADO por fin, tras dos sesiones anunciado sin ejercitarse**: el
item 175 trae el panel "Fuente Primaria" poblado por la IA con un
fragmento etnografico real (Kula Ring, terminologia nativa
soulava/mwali, analisis emic/etic), renderizado correctamente en
`W-HUM-TEXT`. El item 176 (disertacion comparativa) trae ese panel
vacio -- coherente con su propio enunciado (sin fuente asociada), no
confirmado por lectura de `humanities.py` todavia. Punto e-f solo
PARCIAL: ambos items se entregaron sin texto en "Ensayo Critico" (nota
0,0000), validando el kill-switch de PENALIZACION FORMAL HUMANIDADES
por campo vacio, pero no la calificacion real de un ensayo con
contenido. Miguel Angel decidio continuar sin repetir la prueba con
texto real -- queda pendiente si se retoma.

**Pendiente para cerrar del todo el punto e-f de ARCH_HEALTH y
ARCH_HUM:** repetir cualquiera de los dos examenes respondiendo con
contenido real, para verificar los motores de calificacion (no solo el
camino de fallo por campo vacio).

---

### RESULTADO DE S028 (CONTINUACION) -- ESTRENO Y REPARACION DE SD_LIST (COMPRENSION AUDITIVA), TRES DEFECTOS ENCADENADOS CORREGIDOS

**PASO 2 de la hoja de ruta, cerrado.** Riesgo alto confirmado y
corregido en produccion, con verificacion final positiva de Miguel
Angel ("el audio ahora se oye perfecto").

La nota de S026 que daba por buenas las copias Catalan/Frances/
Italiano Maior para `SUB-LIN-INSTR` resulto correcta solo para
**Italiano Maior** (`Lengua Moderna Maior Italiano: Avanzado 1`,
copy_id `cca8697a-bf99-4f45-9013-420beee675ba`, LVL_C) -- la IA
clasifico Catalan (`Idioma Moderno Inicial I: Catalan`, "Inicial")
correctamente como `SUB-LIN-MINOR` segun su propia definicion
certificada en V06DOC_SUBARCHETYPES v5.9, no como una confusion del
motor. No se llego a probar Frances.

**Tres defectos reales encadenados en la cadena de audio de `SD_LIST`,
diagnosticados con log de produccion real y corregidos uno a uno:**

1. `generate_audio_content` llamaba a `GEMINI_MODEL_NAME`
   (`gemini-2.5-flash`, solo texto) para generar audio nativo. Log real
   (`alwayson-log-209547.log`, 2026-07-31): `400 INVALID_ARGUMENT: This
   model only supports text output`. Corregido con
   `GEMINI_TTS_MODEL_NAME = "gemini-2.5-flash-preview-tts"` dedicado, y
   parametro `model` opcional anadido a `_execute_gemini_call` (sin
   afectar a ninguna llamada existente).
2. No se enviaba `speech_config` (voz), obligatorio para
   `response_modalities=["AUDIO"]` segun la documentacion oficial de
   Google. Anadida voz `Kore`.
3. `if response.data:` -- `GenerateContentResponse` usa `extra='forbid'`
   en `google-genai==1.55.0` (confirmado instalando la misma version
   pinneada en sandbox); ese acceso lanzaba `AttributeError`, atrapado
   en silencio por el `except` generico. Nunca se habia ejecutado
   porque el fallo del punto 1 abortaba antes. Eliminado el acceso
   roto; la ruta correcta (`candidates[].content.parts[].inline_data`)
   ya estaba escrita como fallback y ahora es la unica ruta.
4. (Cuarto defecto, encontrado en la SEGUNDA prueba real, tras
   desplegar los tres anteriores): el audio se generaba pero sonaba
   vacio -- Gemini TTS devuelve PCM crudo (mono, 16-bit, 24kHz), y
   `_generate_item_audio` lo guardaba tal cual con extension `.mp3`,
   sin contenedor. El navegador no puede decodificar PCM crudo como
   MP3. Corregido envolviendolo en un WAV real con el modulo estandar
   `wave` (igual que el ejemplo oficial de Google) y guardando como
   `.wav`. Plantilla actualizada para reconocer tambien `.wav` en el
   reproductor del item.

**Defecto adicional, ya presente antes de esta sesion, tambien
corregido:** `section_stimulus` (el guion que sirve de base al audio)
se mostraba siempre como texto legible en pantalla para cualquier
seccion que lo tuviera (linea 118 de `exam_take.html`), sin distinguir
`SD_LIST` (donde debe escucharse) de secciones de lectura como
`W-HUM-TEXT` (donde si debe leerse, verificado horas antes en esta
misma sesion con Antropologia). Corregido anadiendo la condicion
`section.subdivision_id != 'SD_LIST'`.

**Hallazgo aparte, documentado pero NO corregido en esta sesion:**
`assessment_media_utils.js` guarda la grabacion de voz del alumno
(Speaking, boton "Grabar") como `.mp3`/`audio-mpeg`, pero
`MediaRecorder` normalmente graba en `webm`/`ogg` -- posible mismatch
del mismo tipo que el punto 4 de arriba. Miguel Angel reporto no poder
reproducir una grabacion de prueba, coherente con esta sospecha, pero
no se ha investigado a fondo. Pendiente para otra sesion.

Commits: `2442bb6` (fallos 1-3 + fuga de `section_stimulus`),
`31cc2c7` (fallo 4, contenedor WAV). Ambos desplegados y verificados
paso a paso en GitHub Actions (incluido el patron de reinicio de
Primario y Pesado, que coincide literalmente con los archivos
tocados en ambos commits).

---

### RESULTADO DE S028 (CONTINUACION 2) -- GRABADORA DE VOZ (SPEAKING) REPARADA, DEFECTO DE BLOQUEO TOTAL DE NAVEGACION ENCONTRADO Y CORREGIDO, REGRESION PROPIA CORREGIDA

**Grabadora de voz (SD_SPEAK/W-COMM-DIALOG), etiquetado corregido y
reproduccion local anadida.** El boton "Grabar" grababa con
`MediaRecorder(stream)` sin especificar codec y luego renombraba el
blob a `.mp3`/`audio-mpeg` a la fuerza (el propio comentario del
codigo decia "Nota: WebM en realidad, pero renombramos"). Sin ninguna
forma de comprobar la grabacion antes de entregar. Corregido: deteccion
real del codec soportado (`audio/webm;codecs=opus`), etiquetado
correcto del Blob/File, y reproduccion local inmediata via
`URL.createObjectURL`. Verificado por Miguel Angel con una grabacion
real ("se ha escuchado perfectamente"). Alcance deliberadamente
acotado: NO conecta la grabacion con el backend ni con calificacion
real -- ver mas abajo el hallazgo de arquitectura mayor.

**Hallazgo de arquitectura mayor, NO abordado esta sesion, candidato a
hito propio.** El motor `DIA-INTERACT` (y `DRA-HOLO` y afines en
`social.py`/`languages.py`/`humanities.py`) esta disenado para devolver
siempre `PENDING_AI_ANALYSIS` con `pending_ai_refinement: True`, en
espera de un paso posterior de analisis por IA que **no existe en
ningun sitio del codigo**. `generate_multimodal_correction` ya existe
en `gemini_service.py` y ya adivina bien `mime_type="audio/webm"`, pero
no se llama desde ninguna parte. Afecta a tres arquetipos
(ARCH_LANG, ARCH_SOC, ARCH_HUM), no solo a Speaking. Motor de
refinamiento completo pendiente de diseno y sesion dedicada.

**Defecto de bloqueo TOTAL de navegacion, encontrado y corregido.**
Miguel Angel reporto "Siguiente estacion no funciona" -- el examen
quedaba atascado en la primera seccion, en cualquier examen, siempre.
Causa: `activateSection(0)`, llamada sincrona dentro de
`initExamEngine()` en el bloque de arranque de la pagina, hacia
`if (window.MathJax) { MathJax.typesetPromise([currentSec]); }`.
`window.MathJax` existe pronto (sincrono), pero `typesetPromise` se
adjunta mas tarde, cuando termina el arranque asincrono real de
MathJax -- la comprobacion pasaba pero la llamada lanzaba
`TypeError` sin capturar, cortando en seco el resto del script de
arranque: ni el listener global de ".btn-next-station" ni ningun
`AssessmentWidgets.init*()` llegaban a registrarse. Corregidos los
tres puntos que llamaban a `MathJax.typesetPromise` para comprobar
`typeof MathJax.typesetPromise === 'function'`, no solo la existencia
del objeto. Verificado por Miguel Angel: navegacion restaurada.
Corregida de paso, en el mismo commit, una perdida de datos real: el
manejo de archivos de audio en el envio final sobrescribia por
completo la respuesta de `DIA-INTERACT` (chat "Interaccion
Dialectica") si tambien existia una grabacion -- ahora se conserva
dentro de la clave `log`.

**Regresion propia, encontrada y corregida en la misma sesion.** Al
cambiar la extension del audio de `.mp3` a `.wav` (fallo 4 de mas
arriba), 7 puntos de `exam_take.html` que decidian "si el asset no es
`.mp3`, es una imagen" (`{% if not '.mp3' in asset %}`) empezaron a
tratar el propio audio `.wav` como imagen, mostrando el placeholder
roto "Recurso Visual" en items `W-OBJ-STRIKE` de `SD_LIST`. Corregidas
las 7 apariciones para excluir tambien `.wav`. Verificado por Miguel
Angel: ya no aparece el placeholder, se ve el reproductor de audio
correctamente.

**PASO 2 de la hoja de ruta (SD_LIST) queda cerrado del todo**, con
cuatro rondas de fix-verificacion-fix reales en produccion, todas
confirmadas por Miguel Angel con datos frescos.

Commits: `66af29d` (grabadora, etiquetado + reproduccion local),
`c69c881` (bloqueo de navegacion MathJax + perdida de datos
DIA-INTERACT), `9d2172f` (regresion propia .wav-como-imagen). Los
tres desplegados y verificados en GitHub Actions.

---

### RESULTADO DE S026 -- ARCH_TECH VERIFICADO, TRES DEFECTOS TRANSVERSALES DE PRESENTACION, Y APERTURA DE H38

**ARCH_TECH cerrado.** Los seis puntos (a-f) verificados EJECUTANDO sobre el
examen `4274e2df` (Algoritmica): clasificacion correcta (Ciencias Tecnicas e
Ingenieria, Resolutivo), esqueleto de 2 secciones, 3 items con contenido real,
widgets renderizados (W-OBJ-STRIKE y W-TECH-CALC), entrega calificada e informe
con Valoracion del Catedratico.

Calificacion comprobada como CORRECTA, no asumida: nota 0,2500 con items a 1,00
/ 0,00 / 0,00. No es la media de items (0,3333) sino la media POR SECCIONES,
(0,5 + 0,0) / 2, conforme a `logic.py:483`
(`final_score = total_exam_score / section_count`). Miguel Angel confirmo que
acerto el selector, respondio la segunda con texto basura a proposito y dejo la
tercera sin responder. No hay octavo defecto de calificacion.

**Tres defectos de presentacion, todos transversales a los seis arquetipos:**

1. `301d58d` -- Renderizado de formulas LaTeX. El arreglo de MathJax de
   d873394/0b3bfc2 solo habia llegado a contenidos. `assessment_v2`, creado
   despues en ec69b5f, nunca heredo la configuracion, y las copias de sala de
   estudio no la tuvieron nunca. `exam_take.html` cargaba el motor SIN
   configuracion, y MathJax 3 habilita por defecto unicamente `\(...\)`, no el
   dolar simple: como el contenido lo redacta Gemini, que alterna ambas
   notaciones, se renderizaba aproximadamente la mitad de las formulas de forma
   aparentemente aleatoria. `exam_report.html` no cargaba MathJax en absoluto.
   Configuracion canonica extraida a `templates/includes/_mathjax.html` e
   incluida en los cuatro ambitos.
   SEGURIDAD: se elimino `polyfill.io` de `exam_take.html`. Dominio adquirido
   por Funnull en febrero de 2024, inyectaba malware en dispositivos moviles en
   cualquier sitio que lo embebiera; suspendido por Namecheap el 27 de junio de
   2024.

2. `29158ad` -- Markdown del informe de correccion. `justification` y
   `qualitative_summary` se pintaban en crudo, sin `linebreaks` ni procesador,
   pese a que la IA los redacta EN Markdown. Se cableo `django-markdownify`,
   ya presente en requirements y usado hasta entonces solo por el tablon de
   anuncios, con una configuracion con nombre `assessment`. NO se define clave
   `default`: el filtro sin argumento de anuncios lanza KeyError, lo captura y
   cae en ajustes vacios, identico al comportamiento previo. Verificado leyendo
   el codigo del filtro, no por suposicion. `bleach` sanea la salida, lo que
   importa porque ese texto lo redacta un modelo de lenguaje.

3. `cfded37` -- Saltos de linea descartados por la API. ESTE ES EL HALLAZGO DE
   FONDO DE S026. Gemini, con `response_mime_type: application/json` y
   `response_schema` estricto, devuelve las cadenas SIN ningun escape de salto
   de linea. Comprobado pidiendole expresamente un bloque multilinea: el texto
   CRUDO, antes de parsear nada, llega con la indentacion intacta y el salto
   sencillamente ausente (`INICIOPrograma` pegado, cuatro espacios delante).
   El codigo del proyecto quedo EXONERADO probando por separado
   `clean_json_response` (su regex de blindaje LaTeX no toca `\n` porque `n`
   figura entre los escapes validos), `dirtyjson` (preserva tanto `\n` escapado
   como salto literal) y `response.text.strip()` (solo recorta extremos).
   Solucion: se instruye al modelo para que escriba cada salto como `<<NL>>`
   (`NEWLINE_DIRECTIVE`, anadida a `s_prompt` en `tasks.py` en un unico punto,
   de modo que cubre los seis arquetipos sin tocar los seis `get_system_prompt`)
   y se restituye al entrar en la base de datos (`_restore_newlines`, recorrido
   recursivo tras el parseo, cubre contenido, `grading_logic` y
   `section_stimulus`). La restitucion va en la persistencia y no en el
   renderizado, para mantener tontas las plantillas segun `com-standards`.
   Mecanismo ADITIVO: si el modelo omite el token, el texto se guarda igual que
   antes, sin regresion posible.
   CONFIRMADO EN PRODUCCION: primer examen generado despues del arreglo
   (`5c200071`, ARCH_HEALTH) trae 5, 8 y 1 saltos en sus tres feedbacks.

**CORRECCION A LA HOJA DE RUTA DE S025 SOBRE `source_text`.** El anexo afirmaba
que `source_text` "alimenta el panel lateral de los layouts SPLIT_TEXT". Es
INEXACTO y conviene no repetirlo: el panel lateral (`#side-stimulus-panel`) lo
alimenta `section_stimulus`, a nivel de SECCION, via el JS de
`exam_take.html:992-1000`, que exige `layoutMode === 'SPLIT_TEXT'` Y un
`.section-stimulus-content` no vacio. `source_text` es cosa del ITEM y solo lo
pintan dos ramas de plantilla: `W-HUM-TEXT` y `W-MEDI-LAYOUT`. Son dos canales
independientes. Auditados ambos en S026 y AMBOS SANOS por lectura: `source_text`
declarado en `ContentSchema` (`gemini_schemas.py:181`), pedido solo por items
`W-HUM-TEXT` (6 de 6 peticiones en humanities y social), renderizado en
`exam_take.html:285`, y persistido integro (`db_item.content = ai_content`, sin
seleccion de claves). `section_stimulus` declarado en `ExamSectionSchema:210` y
persistido en `tasks.py`. Sano por lectura NO ES sano: S024 y S025 demostraron
que la lectura no detecta esta clase de fallos. Sigue sin ejercitarse.

**ARCH_HEALTH bloqueado -- origen de H38.** Se genero el examen `5c200071`
(Anatomia, READY), y sus items `W-CLIN-SCAN` piden observar imagenes que no
existen. El motor instruye a la IA para que INVENTE URLs de imagen en cinco
estrategias, y no hay generador, ni almacenamiento, ni servicio de recuperacion
en toda la plataforma. Detalle completo en
`CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V38.md`. Miguel Angel decidio no aplicar
puente ni parche: las evaluaciones no estan abiertas a usuarios, de modo que un
examen roto no hace dano, y procede resolver las imagenes bien de una vez. Las
instrucciones de inventar URLs se dejan INTACTAS a proposito hasta que H38 las
sustituya -- no son un descuido.

---

### RESULTADO DE S025 -- ARCH_LANG VERIFICADO Y SIETE DEFECTOS TRANSVERSALES

Los seis puntos de verificacion quedan CERRADOS para ARCH_LANG / SUB-LIN-MINOR
(chino), verificados EJECUTANDO en produccion, no leyendo:

| Punto | Verificacion | Evidencia |
|---|---|---|
| a | Clasificacion IA correcta | ARCH_LANG / SUB-LIN-MINOR / zh, ITIN_MIN, LVL_B, BILINGUAL |
| b | Skeleton correcto del subarquetipo | 5 secciones exactas, en orden |
| c | Llenado completo de items | 5/5 con contenido real en chino |
| d | Widgets renderizados | W-OBJ-STRIKE, W-TXT-CLOZE y W-MIX-MATCH, vistos en navegador |
| e | Entrega y calificacion | nota final 0.7333 con parcialidad real por item |
| f | Informe con qualitative_summary | Valoracion del Catedratico renderizada |

Examen de referencia: `720f08c6-b68c-46f4-a224-65e53d2836a4` (id 229), generado,
respondido, entregado y calificado desde el navegador por Miguel Angel. El
examen previo `3b1bcdf8` (id 228) se genero bajo el esquema antiguo y se
descarto tras servir de evidencia; ambos sobre la copia de estudio
`Lengua Moderna Minor Chino: Intermedio 1`.

**Los siete defectos corregidos, todos TRANSVERSALES a los seis arquetipos y
ninguno detectable leyendo el codigo:**

| # | Defecto | Commit |
|---|---|---|
| 1 | `ContentSchema` no declaraba `cloze_options`: las instrucciones pedian a la IA un campo inexistente en el esquema estricto y se descartaba en silencio. Las opciones acababan en `options` con ids improvisados (G1_A..G6_C). Cloze irrellenable. | 4198780 |
| 2 | `ContentSchema` no declaraba `source_text`, consumido por el panel lateral de los layouts SPLIT_TEXT y pedido por mas de quince `task_instruction` de languages, humanities y social. | 4198780 |
| 3 | Desajuste de corchetes: la plantilla emitia `data-gap-id="[HUECO_ID_1]"` y el corrector buscaba `HUECO_ID_1`. Nota 0 en todo item cloze aunque el alumno acertase los seis huecos. | 4198780 |
| 4 | `_grade_mat_link` hacia `pairs.items()` sobre lo que el esquema entrega como lista. Reventaba la correccion del examen COMPLETO con `'list' object has no attribute 'items'`, visible en pantalla para el alumno. | b62a460 |
| 5 | W-MIX-MATCH irrealizable: la plantilla leia las columnas de `content.options` (vacio) y `content.targets` (campo inexistente). Ambas columnas en blanco. | b62a460 |
| 6 | `correct_answer` llegaba unas veces como texto de la opcion y otras como su identificador ('C'), mientras el navegador envia siempre el texto. En el caso de la letra, PRM-STRIKE marcaba INCORRECTA una respuesta acertada y ademas aplicaba la penalizacion 1/(N-1). | 4b483da |
| 7 | La recoleccion de respuestas se bifurca por `block_type` y el render por `widget_id`: RBT-CANON se pinta como radios pero se recogia como campo de texto. La seleccion del alumno se enviaba como cadena vacia. | aa9cda2 |

Se confirma de nuevo el patron de S024: **cada defecto tapaba al siguiente**. El
arreglo del cloze (1 y 3) estaba bien, pero no se habria visto funcionar nunca,
porque el defecto 4 tumbaba la correccion del examen entero antes de calcular
ninguna nota.

**Defecto de validez del instrumento, detectado por Miguel Angel probando.**
La IA emite las opciones con la solucion en PRIMER lugar de forma sistematica:
verificado sobre los DOCE huecos de cloze de los examenes 228 y 229, doce de
doce en posicion 1. Un alumno que no conozca la materia sacaba 6/6 eligiendo
siempre la primera opcion. Corregido barajando en el servidor, en presentacion
(`ExamTakeView`), con semilla estable por `uuid` de item y `gap_id`, y no en
generacion: cubre los examenes ya generados y deja intacto el orden almacenado,
del que depende la resolucion posicional de `correct_answer` en
`_choice_equivalents`. Mismo patron ya aplicado a los destinos de W-MIX-MATCH.
Commit 27bd6ca.

**Incidencia de infraestructura ajena al hito.** Dos despliegues consecutivos
fallaron sin ejecutar un solo paso (11 segundos, sin runner asignado): el
repositorio estaba en PRIVADO y la cuota de minutos de Actions se habia agotado.
Miguel Angel lo devolvio a publico y el relanzamiento paso. Ademas se corrigio
`deploy.yml`: el paso de reinicio de Always-on Tasks llevaba
`if: steps.deploy.outcome == 'success'`, y GitHub antepone un `success()`
implicito a toda condicion sin funcion de estado, de modo que seguia atado al
exito del paso anterior. El desacople que el comentario del 2026-07-27 decia
haber implantado nunca fue efectivo, y volvio a morder hoy: fallo la recarga
web, el paso salio `skipped` y los dos workers quedaron con codigo viejo en
silencio. Commit 99a10b3.

**Correccion documental.** Este anexo daba por publico el repositorio desde
S024. Estuvo en privado hasta el 2026-07-28.

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

### HOJA DE RUTA AL REANUDAR H06 -- EN ESTE ORDEN

Reescrita por completo en S030 (cierre de sesion), sustituyendo integramente
la version anterior -- ver mas arriba en este mismo anexo (secciones
"RESULTADO DE S029", "RESULTADO DE S030" y la correccion posterior) para el
historial completo, no se pierde nada, solo se deja de repetir aqui.

**RESUMEN DE S029 (sesion muy larga, 27 commits):** PASO 1, 2 y 3 cerrados
del todo con verificacion real. El motor `PENDING_AI_ANALYSIS` (antiguo
PASO 5) se construyo, se verifico end-to-end y se formalizo como hito propio
(H39, PAUSADO) via PCH. H38 (imagenes) recibio cuatro correcciones reales en
cadena (exclusion de PDF, consulta en dos niveles, traduccion IA,
verificacion semantica), todas verificadas en produccion. PASO 4 avanzo
mucho pero no quedo cerrado al final de esa sesion.

**RESUMEN DE S030:** PASO 4 retomado y cerrado del todo con verificacion
real completa (ver "RESULTADO DE S030" y su correccion posterior, mas abajo
en este mismo anexo, para el detalle completo -- incluye el fix de HTML
crudo en `media_attribution.text`, commit `c56cd40`, desplegado y verificado
paso a paso). **No queda ningun paso pendiente de la hoja de ruta anterior
a este punto.** La sesion siguiente arranca directamente en el PASO 6.

PASO 1 -- CLO-OPEN -- CERRADO DEL TODO (ver detalle completo mas arriba,
sin cambios en S029/S030 respecto a como quedo documentado).

PASO 2 -- Japones / wanakana -- CERRADO DEL TODO (ver detalle completo mas
arriba, sin cambios en S029/S030 respecto a como quedo documentado).

PASO 3 -- ITIN_DOC en Magisterio -- CERRADO DEL TODO (ver detalle completo
mas arriba, sin cambios en S029/S030 respecto a como quedo documentado).

PASO 4 -- Cerrar del todo el punto e-f de ARCH_HEALTH y ARCH_HUM --
CERRADO DEL TODO EN S030, CON VERIFICACION REAL COMPLETA (ver "RESULTADO DE
S030" y su correccion posterior, mas abajo, para el detalle final real,
incluido el motor `ILC-CONTEXT` ya ejercitado en produccion con contenido
real, no solo con el kill-switch de campo vacio).
El bloqueo original (motor `PENDING_AI_ANALYSIS` inexistente) ya no existe
-- el motor esta construido y verificado (ver H39). En S029 se retomo con
el examen real `8dd7b72d-8085-46e5-a759-6eb44e791213` (SUB-SAN-MED-BASIC,
ITIN_ROT, LVL_A), generado sobre la copia de estudio real de Anatomia:

- Items 248 y 249 (`ILC-CONTEXT`/`W-CLIN-SCAN`): ambos sin imagen
  (`media_assets: None`) al generarse, porque el examen se creo ANTES de
  las correcciones de H38 de esta misma sesion. Se investigo la causa real
  (no una conjetura): la busqueda de Wikimedia devolvia 5/5 PDFs para el
  item 248, y tras excluirlos, 0 resultados totales -- la consulta generica
  nunca fue lo bastante especifica. Corregido con los cuatro niveles de
  busqueda documentados en la seccion H38 de este mismo commit.
- Item 248: repoblado a mano con el pipeline real corregido (no un examen
  nuevo, el mismo item 248 actualizado en la BD). Resultado verificado:
  imagen real del triangulo femoral (Gray1238.png, plate real de Gray's
  Anatomy), stem coherente con el tema, pasando la verificacion semantica
  real. **Este resultado SI esta confirmado.**
- Item 249: **ESTADO REAL AL CIERRE -- NO CONFIRMADO, REQUIERE
  REVERIFICACION AL RETOMAR.** Se intento repoblar dos veces. El primer
  intento (script improvisado con una consulta generica demasiado pobre,
  error del propio modelo, no del pipeline real) devolvio una imagen de
  orbita ocular, claramente incorrecta para una radiografia de torax. El
  segundo intento, ya con la consulta generica real (titulo de seccion +
  asignatura) y excluyendo el recurso ya asignado al item 248, aparento
  completarse pero Miguel Angel senalo al cierre de la sesion que el
  resultado mostrado (una imagen de rodilla/rotula, con el texto de
  atribucion renderizado como HTML en crudo en vez de procesado) no se
  correspondia con lo que el modelo describia, y que "el ultimo script no
  se ejecuta". **No se ha verificado con certeza en que estado quedo el
  item 249 en la base de datos real.** Primera accion de la proxima sesion:
  consultar item 249 en produccion (`ExamItem.objects.get(id=249)`,
  inspeccionar `content.media_assets` y `content.stem` reales) antes de dar
  nada por hecho, y corregir tambien el renderizado en crudo del HTML de
  atribucion si se confirma (buscar donde se muestra `media_attribution.text`
  en `exam_take.html` -- probablemente esta usando el HTML crudo que
  Wikimedia devuelve en `extmetadata` sin sanear ni convertir a texto
  plano, mismo tipo de fallo que el del stem sin markdown corregido hoy,
  pero al reves: aqui sobra HTML en vez de faltar).
- Items 248/249 aun no se han respondido de verdad por Miguel Angel dentro
  del examen `8dd7b72d` -- la respuesta con contenido real que cierra el
  PASO 4 sigue pendiente.

**Los 5 puntos que aqui figuraban ("Siguiente sesion, en este orden") se
ejecutaron y verificaron todos en S030 -- ver "RESULTADO DE S030" y su
correccion posterior para el detalle real de cada uno. No hay nada
pendiente de este bloque.**

---

### RESULTADO DE S030 -- PASO 4 CERRADO POR DECISION DE MIGUEL ANGEL, HTML CRUDO EN ATRIBUCION CORREGIDO EN ORIGEN, refine_pending_ai_items_task VERIFICADO POR SEGUNDA VEZ CONTRA PRODUCCION REAL

**Estado real del item 249 verificado primero, sin asumir nada** (ver
punto pendiente dejado por S029): `content.media_assets` SI tenia una
imagen real (no la url inventada ni el hueco vacio que se temia), pero
era el recurso de globo ocular ya usado en el examen `2c1c80e4` de S028
(`MediaResource id=2`), con un `stem` coherente con esa imagen pero
incoherente con la seccion real del item ("Anatomia Radiologica --
Semiologia"). Conclusion: ni el primer intento improvisado de S029 dejo
el item en un estado "roto" en el sentido tecnico -- dejo un item
END-TO-END coherente pero sobre el tema equivocado, reutilizando un
recurso ya usado en otro examen.

**Item 249 repoblado con el pipeline real** (`_generate_item_image_content`
de `orchestrator/tasks.py`, la misma funcion que usa el bucle de
produccion, no un script paralelo), excluyendo `MediaResource id=2` y con
consultas orientadas a radiografia de torax normal. Resultado: imagen real
verificada semanticamente (`Chest_X-ray.jpg`, `MediaResource id=6`,
CC-BY-SA-4.0), `stem` y `keywords` coherentes con "Anatomia Radiologica --
Semiologia" (radiografia PA de torax normal, paciente preempleo
asintomatico). Persistido en el item real, no en un examen nuevo.

**HTML crudo en `media_attribution.text` -- confirmado como defecto real
y sistemico, no anecdotico.** El recurso recien creado (`id=6`) trajo
`attribution: <span class="int-own-work" lang="en">Own work</span>`
directamente del campo `Credit` de Wikimedia -- mismo tipo de fallo que ya
tenia el recurso del item 248 (`Gray1238.png`, lista `<ul><li>` completa
con enlaces). Como las plantillas `exam_take.html`/`exam_report.html`
imprimen `media_attribution.text` sin `|safe` (Django autoescapa por
defecto), ese HTML nunca se renderizaba como marcado -- se veia
literalmente en pantalla con las etiquetas, confirmado visualmente en
capturas reales de Miguel Angel. Corregido en origen: `strip_tags()`
aplicado en `media_library/services.py::search()` sobre `Artist`/`Credit`
antes de que `verify_and_store()` los persista (commit `c56cd40`,
desplegado y verificado paso a paso en el Action -- los 8 pasos en verde,
incluida la barrera de manifiesto de `collectstatic`). Backfill de datos
(sin migracion, sin cambio de esquema) sobre los dos `MediaResource` ya
afectados (`id=5` Gray1238.png, `id=6` Chest_X-ray.jpg) y sobre los
`ExamItem` que ya tenian la copia sucia en su propio `content` (items
**170** y **248** -- el 170 no se habia detectado hasta este barrido).
Verificado con capturas reales de pantalla tras el fix: ambos items
muestran la atribucion limpia en produccion.

**Cierre del PASO 4 -- decision explicita de Miguel Angel, no verificacion
completa segun el criterio original de la hoja de ruta.** Miguel Angel
respondio el examen `8dd7b72d` en produccion real:
- Item 250 (histologia, opcion multiple): correcto, nota 1,00.
- Item 249 (radiografia de torax, `ILC-CONTEXT`): campo de interpretacion
  dejado VACIO. Nota 0,00, mismo camino de fallo por campo vacio que ya
  se habia validado en S028/S029. **El motor de calificacion real de
  `ILC-CONTEXT` contra una interpretacion radiologica con contenido
  SIGUE SIN EJERCITARSE.** Miguel Angel decidio cerrar el PASO 4 sin este
  punto, de forma explicita.
- Item 248 (triangulo femoral, `RBT-CANON`): respuesta deliberadamente
  disparatada ("tiene un huevo mas grande que el otro"), para probar el
  motor de calificacion real contra contenido no vacio. Resultado
  confirmado en dos fases reales de produccion: nota inicial 0,60
  ("Revision IA en curso", credito obtenido con nota acumulada 0,5333),
  y tras encolarse sola `refine_pending_ai_items_task` y completar su
  revision en profundidad (notificacion push + email reales recibidos
  con la nota ya actualizada), la nota bajo a 0,00 con una justificacion
  coherente ("responde de manera totalmente inapropiada... no define
  ninguno de los cinco terminos pedidos"), nota acumulada final 0,3333.
  **Esta SI es la primera verificacion E2E de `refine_pending_ai_items_task`
  contra un examen 100% de produccion** (S029 lo verifico en un entorno
  controlado) -- relevante tambien para la hoja de ruta de H39, aunque
  ese hito siga PAUSADO y este anexo no la modifique.

**Resumen para quien retome cualquier trabajo futuro sobre `ILC-CONTEXT`/
`W-CLIN-SCAN`:** el motor de calificacion real de ese tipo de item, con
una interpretacion clinica/radiologica de contenido real (ni vacia ni
disparatada), no tiene ninguna verificacion en produccion todavia -- ni
en H06 ni en H39. Si se retoma, usar un item `ILC-CONTEXT` cualquiera
(no necesariamente el 249) con una respuesta real de contenido.

---

### CORRECCION A "RESULTADO DE S030" -- ILC-CONTEXT SI SE EJERCITO CON CONTENIDO REAL, PASO 4 CERRADO DE VERDAD

El bloque anterior (commit `ca48b3d`) quedo escrito en una rama de la
sesion S030 que no continuo -- una confusion puntual de Miguel Angel al
leer la pregunta de cierre, aclarada por el mismo despues. En la rama que
si continuo (misma sesion), el trabajo siguio un paso mas:

**Item 249 (`ILC-CONTEXT`) respondido con una interpretacion radiologica
real** (lectura sistematica de la radiografia de torax PA: penetracion,
rotacion, campos pulmonares, senos costofrenicos, silueta cardiomediastinica,
traquea, cupulas diafragmaticas, burbuja gastrica). El examen `8dd7b72d` ya
estaba en `status='GRADED'` (no se puede reenviar por la UI real,
`ExamSubmitView` exige `status='READY'`), asi que se ejercito el motor real
directamente contra la `Submission` id 22 ya persistida:

1. `strategy.grade_item()` (la misma funcion real de `HealthStrategy`) sobre
   el item 249 con la interpretacion real -- resultado sincrono correcto,
   0.6 provisional, `PENDING_AI_ANALYSIS`.
2. Primer intento de sustituir el `item_rep` dentro de `grading_report`
   fallo por un error propio (comparacion `item_id == 249` como entero,
   cuando el contrato real de `GradingOrchestrator.grade_submission` lo
   guarda como `str(item.id)` -- linea 472 de `logic.py`). Diagnosticado y
   corregido antes de continuar, sin dejarlo pasar como si hubiera
   funcionado.
3. Segundo intento, con el `item_id` como string y las claves exactas del
   contrato: sustitucion correcta, y `refine_pending_ai_items_task`
   ejecutada en directo (no `.delay()`, la funcion real invocada
   sincronamente) hizo la llamada real a Gemini, evaluo el contenido real
   de la respuesta y produjo una nota final de **0.7**, con una
   justificacion especifica y no generica: acierta simetria clavicular,
   traquea y senos costofrenicos, pero no desglosa individualmente el arco
   aortico ni el ventriculo izquierdo (los mete dentro de "silueta
   cardiomediastinica") y no cuantifica ni el criterio de inspiracion
   (9-10 arcos costales) ni el valor de corte del ICT (<=0.50).
   `submission.final_score` recalculado a 0.5667, `passed=True`.
   Notificaciones reales enviadas (push + email), con los dos fallos ya
   catalogados como deuda tecnica (VAPID UserSub 23, WNS UserSub 14) y sin
   incidencias nuevas.

**Conclusion real, sustituyendo la de `ca48b3d`:** el motor de calificacion
de `ILC-CONTEXT` SI quedo verificado en produccion con contenido real, no
solo con el kill-switch de campo vacio. El PASO 4 de H06 queda cerrado
del todo, sin ningun punto pendiente de verificacion.

---

PASO 5 -- Motor de refinamiento PENDING_AI_ANALYSIS -- MOVIDO A HITO PROPIO
(H39, PAUSADO)
Ya no es tarea de H06. Construido, verificado end-to-end y documentado en
`CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V39.md`. Ver ese anexo para su propia
hoja de ruta (verificacion de `ILC-CONTEXT`/`DIA-INTERACT` con datos reales,
decision sobre el widget de audio no conectado, `send_unified_notification`
roto).

PASO 6 -- **PUNTO DE ENTRADA REAL DE LA PROXIMA SESION.** Selector de
dificultad UG / Endurecido (decision de Miguel Angel, S025)
Sin cambios en S030. Criterio fijado por Miguel Angel: manda lo que haga la
UGR. Candidatos ampliados en S029: penalizacion de `CLO-MULTI` Y `CLO-OPEN`
(ver PASO 1 mas arriba para el detalle del hallazgo de `CLO-OPEN`), mas
distractores extra en `W-MIX-MATCH`.

PASO 7 -- Densidad de items (verificar normativa ANTES de tocar skeletons)
Sin cambios en S030.

PASO 8 -- Decidir apertura a usuarios reales
Sin cambios en S030.

**Fuera de esta hoja de ruta, deuda tecnica que no bloquea nada de lo
anterior pero sigue abierta (ver seccion "DEUDA TECNICA ABIERTA" mas abajo
para el detalle completo):** `send_unified_notification` roto en
`_send_exam_failure_notification`; dos fallos preexistentes de push (VAPID
UserSub 23, WNS UserSub 14); aviso de limite de 6 copias de estudio
pendiente de reproducir en caliente; y, nuevo en S030, el nombre de archivo
sin extension real que genera `verify_and_store()` en
`media_library/services.py` cuando la URL de origen de Wikimedia trae query
string pegada al nombre (`nombre_archivo = url.rsplit("/", 1)[-1]` no la
separa) -- cosmetico, sin incidencia conocida en produccion hasta ahora, no
se ha tocado.

---
---

### DEUDA TECNICA ABIERTA

**-2. Anadida en S029 -- `send_unified_notification` roto en
`_send_exam_failure_notification`.** Llamada con firma que no coincide con
la funcion real (`core/utils.py`: espera `subject_template`,
`body_template_prefix`, `context` dict; se le pasa texto literal traducido
y una URL como si fueran esos parametros) y con nombres de URL de la app
`assessment` legacy (`assessment:view_results`, `assessment:take_assessment`)
en vez de `assessment_v2`. Envuelto en el `try/except` de la funcion, falla
silenciosamente cada vez -- el email de fallo de examen si llega
(`send_mail` es una llamada aparte), pero el push nunca. No corregido en
S029, encontrado leyendo codigo para no replicar el patron en
`_send_grading_refinement_notification` (que usa el patron probado de
`_send_completion_notifications` en su lugar).

**-3. Anadida en S029 -- dos fallos preexistentes de push detectados
verificando `_send_grading_refinement_notification`.** UserSubscription ID
23: `WebPushException 403 Forbidden -- las credenciales VAPID de la
cabecera no corresponden a las usadas al crear la suscripcion` (la clave
VAPID del servidor cambio en algun momento sin invalidar suscripciones
antiguas). UserSubscription ID 14 (Windows/WNS): `400 Bad Request` sin
cuerpo de respuesta. Ninguno de los dos es nuevo ni causado por el PASO 5
-- aparecen identicos en logs de sesiones anteriores (ver
`_send_completion_notifications`). No investigado a fondo, anotado para
una sesion de limpieza de suscripciones push obsoletas.

**-1. Anadida en S029 -- aviso de limite de 6 copias de estudio, reportado
como no visto por Miguel Angel. PENDIENTE DE REPRODUCCION EN CALIENTE, NO
CONFIRMADO.** Miguel Angel reporto que al intentar crear una copia de
estudio estando ya sobre el limite de 6 (`ContentCopy.objects.filter(user=
request.user).count() >= 6` en `contents/study_room_views.py:114`), no vio
ningun aviso -- `messages.error(...)` seguido de redirect a
`original_content.get_absolute_url()`. Revision de codigo (vista, plantilla
`content_detail.html`, `base.html` con `{% if messages %}` dentro de
`<main>`, orden de middleware) no encuentra ningun defecto obvio -- todo
estructuralmente correcto por lectura. El log de errores del intervalo
(`CampuStudiOnline_009.txt`) no muestra ninguna excepcion asociada a ese
intento concreto -- si encontro, en cambio, un `AttributeError` real y no
relacionado (`Exam.was_viewed`, corregido en el commit `8d4a2fe`, ver mas
abajo). **No se confirma que ambos hallazgos esten conectados.** Pendiente:
reproducir en caliente (forzar el limite de nuevo con el log a la vista en
el momento exacto) en vez de seguir infiriendo de logs pasados.

**0. Anadida en S025 -- correccion de `deploy.yml`: VERIFICADA EN EL PROPIO CIERRE.**
El `if: always() && steps.deploy.outcome == 'success'` del paso de reinicio de
Always-on Tasks (99a10b3) quedo comprobado en produccion sin buscarlo: el
despliegue del commit de cierre de S025 volvio a fallar en el paso 4 (recarga web
via API de PythonAnywhere) y el paso 5 **se ejecuto igualmente**, en lugar de
salir `skipped` como habia ocurrido esa misma manana con aa9cda2. El desacople es
por tanto real y esta confirmado con evidencia.

**0-bis. Anadida en S025 -- la recarga web via API falla de forma intermitente.**
Dos de los despliegues de S025 fallaron en el paso 4 con la llamada a
`/api/v0/user/MiguelAeTxio/webapps/.../reload/`, y ambos habian desplegado el
codigo correctamente en el paso 3. En el primer caso un relanzamiento sin cambios
paso a la primera, lo que apunta a intermitencia del lado de PythonAnywhere y no
a un defecto del workflow. El codigo HTTP y el cuerpo de cada intento quedan
registrados en `SWAP/deploy_reload_history.txt`, en el servidor, precisamente
para poder diagnosticarlo sin depender de los logs de Actions. Revisar ese
historial en S026 antes de decidir si merece reintento automatico en el propio
paso.

**0-ter. Anadida en S025 -- controles de verificacion, otra vez a mano.**
S025 volvio a improvisar los mismos tres controles que S024 dejo apuntados
(`py_compile`, `node --check` sobre el fragmento JS extraido, y render real via
`django.test.Client`), y los tres encontraron cosas. Siguen sin automatizar. El
render via `django.test.Client` fue ademas decisivo para descartar un falso
diagnostico: probo que el `<script>` con las opciones del cloze SI se emitia
correctamente, y que el problema estaba en la lectura de la pantalla, no en el
codigo.

### DEUDA TECNICA HEREDADA DE S024

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
S025  2026-07-28  Pipeline E2E VERIFICADO (ARCH_LANG)  7 defectos corregidos, todos transversales y ninguno detectable por lectura: ContentSchema no declaraba cloze_options ni source_text (4198780), desajuste de corchetes en gap_id que daba 0 en todo cloze (4198780), pairs.items() sobre lista que tumbaba la correccion entera (b62a460), W-MIX-MATCH con las dos columnas vacias (b62a460), correct_answer como letra penalizando aciertos (4b483da), RBT-CANON recogido como texto pese a pintarse como radios (aa9cda2). Defecto de validez detectado por Miguel Angel probando: solucion siempre en primera posicion, 12/12 huecos en dos examenes; barajado en servidor con semilla estable (27bd6ca). Los seis puntos (a-f) cerrados para ARCH_LANG con el examen 720f08c6, nota 0.7333. Incidencia: 2 despliegues fallidos por cuota de Actions agotada con el repo en privado; y desacople real del reinicio de workers en deploy.yml, que nunca fue efectivo por el success() implicito (99a10b3). Criterio fijado: manda la UGR; lo que endurezca por encima va a selector UG/Endurecido. Pendiente: 4 arquetipos, source_text, SD_LIST, CLO-OPEN y japones sin copia.
