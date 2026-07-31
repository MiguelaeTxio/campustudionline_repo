# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06 -- HITO 6: SISTEMA DE AUTOEVALUACIONES CON IA

## 1. Descripcion del Hito

Motor de autoevaluacion con IA basado en arquetipos y subarquetipos academicos.
82 subarquetipos certificados. 22 widgets de evaluacion. 20 motores de calificacion.

---

## 2. HOJA DE RUTA PARA LA PROXIMA SESION (LEY SUPREMA - INELUDIBLE)

**ESTADO DEL PIPELINE:** VERIFICADO en produccion de extremo a extremo para
ARCH_SCI (S024), ARCH_LANG (S025), ARCH_TECH (S026) y ARCH_SOC (S028, seis
puntos completos). ARCH_HEALTH (S028): puntos a-d y f verificados con
imagenes reales de H38 confirmadas en produccion; punto e (calificacion)
solo con camino de fallo, pendiente con respuesta real. ARCH_HUM (S028):
`source_text` confirmado por fin en `W-HUM-TEXT`; puntos e-f solo con
camino de fallo, pendiente con respuesta real.
**FECHA DE ULTIMA ACTUALIZACION:** 2026-07-31
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

Actualizada en S026. El hito se pausa aqui para atender H38 (imagenes de
evaluacion), que bloquea ARCH_HEALTH. Al reanudar, este es el estado real:
ARCH_SCI, ARCH_LANG y ARCH_TECH quedan verificados; ARCH_HEALTH depende de H38;
ARCH_SOC y ARCH_HUM estan libres de esa dependencia y son el arranque natural.

PASO 1 -- Completar la prueba E2E de los arquetipos restantes
- PRIMERO ARCH_SOC (Economia Politica) y ARCH_HUM (Antropologia social), que NO
  dependen de imagenes y por tanto no esperan a H38. Las copias existen y
  arrastran el aviso rojo de `assessment_status == ERROR` del lote del
  2026-05-28, que desaparece al generar un examen que llegue a READY.
- DESPUES ARCH_HEALTH (Anatomia), una vez H38 entregue imagenes reales. El
  examen `5c200071` quedo generado pero con los `W-CLIN-SCAN` inservibles.
- Verificar los seis puntos (a-f) en cada uno, EJECUTANDO.
- ATENCION ESPECIAL a `source_text`, que sigue SIN ejercitarse nunca pese a
  llevar dos sesiones anunciado. Lo piden items `W-HUM-TEXT` en humanities y
  social, asi que ARCH_SOC y ARCH_HUM son justamente donde toca. Leer antes la
  correccion del RESULTADO DE S026: `source_text` NO alimenta el panel lateral
  -- eso es `section_stimulus`, otro canal distinto, tambien sin ejercitar.
- Los defectos de S025 y los tres de S026 eran todos transversales, no
  especificos de un arquetipo, asi que lo que queda deberia ir mas rapido.
- Verificar de paso que el centinela `<<NL>>` se comporta en arquetipos con
  listas y pasos numerados, no solo en los que emiten codigo.

PASO 2 -- Estreno de SD_LIST (comprension oral) -- RIESGO ALTO
Requiere un examen de SUB-LIN-INSTR (copias disponibles: Catalan, Frances,
Italiano Maior). El disparador de audio de `orchestrator/tasks.py` (~linea 1212)
vive DENTRO del `try` cuyo `except` cuenta reintento local: si
`_generate_item_audio` lanza, el fallo se registra como "Error Parseo JSON", se
reintenta 3 veces y aborta la seccion con `AIServiceCriticalError`, tumbando el
examen entero. Es decir, un fallo de audio es bloqueante Y se disfraza de error
de parseo. Tenerlo presente al diagnosticar.

PASO 3 -- CLO-OPEN, sin cobertura posible hoy
`CLO-OPEN` lo emite unicamente `SUB-LIN-PHILO`, y no existe copia de estudio de
ninguna asignatura filologico-diacronica (gramatica historica, filologia latina,
linguistica historica). Confirmar con Miguel Angel si existe tal asignatura en
la estructura academica; si no, queda como pendiente justificado, no como
omision. "El Espanol Actual: Norma y Uso" caera previsiblemente en
`SUB-LIN-NORM`, que es CLO-MULTI otra vez.

PASO 4 -- Japones / wanakana, sin cobertura posible hoy
`bindOccidentalInput` solo contempla `ja`, `ar` y `el`; el chino cae en la rama
generica, de modo que la copia de Minor Chino NO ejercita wanakana. Hace falta
una copia de una asignatura de japones. Mismo tratamiento que el PASO 3.

PASO 5 -- ITIN_DOC en Magisterio
Pendiente desde el anexo anterior: confirmar que `AcademicDeductor` le asigna
`ITIN_DOC`.

PASO 6 -- Selector de dificultad UG / Endurecido (decision de Miguel Angel, S025)
Criterio fijado por Miguel Angel: **manda lo que haga la UGR**. Lo que sea licito
y no discrepe en exceso se implanta como estandar; lo que endurezca por encima
del sistema de acreditacion va a un selector de dificultad que elija el usuario,
con nivel estandar (UG) y dificil (endurecido).
- El barajado desplegado en S025 NO es endurecimiento y se queda como estandar:
  no toca ninguna regla de puntuacion, solo elimina un artefacto del generador.
- Contenido candidato del modo endurecido: (a) distractores en W-MIX-MATCH, hoy
  6 contra 6, de modo que la ultima pareja es gratis por eliminacion; (b)
  extender la penalizacion a `CLO-MULTI`, que lleva `no_negative_marking` fijo en
  el codigo sin ninguna cita UGR que lo respalde -- a diferencia del caso de
  SUB-LIN-INSTR, que si la tiene.
- CONFIRMADO en `V06DOC_BLOCKS.md` (lineas 12 y 15): la formula
  `A - E/(N-1)` de PRM-STRIKE es la correccion por azar UGR, y el
  `NO_NEGATIVE_MARKING` de SD_READ/SD_LIST en SUB-LIN-INSTR es una regla
  explicita de la Guia Oficial del Candidato CLM-UGR, no una omision.

PASO 7 -- Densidad de items (verificar normativa ANTES de tocar skeletons)
El examen 229 tuvo CINCO items, uno por seccion, de modo que cada item pesa el
20% de la nota final y un acierto por azar la mueve dos decimas. Ningun documento
V06 fija la densidad: la determinan los skeletons de cada Estrategia. El
"densidad UGR (17 items)" que aparece en el historial es del sistema anterior a
este hito. Subir la densidad NO es endurecer, es medir mejor, asi que iria al
estandar -- pero verificar la normativa real antes de tocar ningun skeleton.

PASO 8 -- Decidir apertura a usuarios reales
El panel de evaluacion de `edit_copy.html` esta condicionado a
`request.user.is_staff or request.user.id == 1`; el resto ve "En Mantenimiento".
Abrir implica relajar esa condicion.

---

### DEUDA TECNICA ABIERTA

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
