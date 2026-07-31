# Hito 38: Adquisición y Licenciamiento de Imágenes para Evaluaciones

## Objetivo del Hito

Dotar al motor de evaluación (H06) de imágenes **reales, verificadas y
con licencia registrada**, e invertir el flujo de generación para que
el ítem se redacte a partir de la imagen recuperada, y no al revés.

---

## Contexto de Arranque

Este hito toma el relevo de H06, que queda pausado el 2026-07-29 en
S026 porque H38 lo bloquea: los ítems `W-CLIN-SCAN` de ARCH_HEALTH
dependen de imágenes que hoy no existen.

Estado en que queda H06, para no perderlo de vista:

- Pipeline verificado de extremo a extremo en producción para
  ARCH_SCI (S024), ARCH_LANG (S025) y ARCH_TECH (S026).
- ARCH_HEALTH depende de este hito.
- ARCH_SOC y ARCH_HUM **no** dependen de él: quedan libres y son el
  arranque natural cuando H06 se reanude. Son además los que deben
  ejercitar `source_text`, que lleva dos sesiones anunciado y sin
  probarse nunca.

No se ha aplicado ningún puente ni parche provisional sobre las
instrucciones de URL inventada. Están intactas a propósito, por
decisión explícita de Miguel Ángel — no son un descuido, y retirarlas
antes de que exista el servicio de recuperación solo degradaría los
enunciados sin ganar nada a cambio.

---

## Contexto Técnico (hallazgo de S026, 2026-07-29)

### El defecto

Cinco estrategias instruyen explícitamente al modelo para que invente
URLs de imagen:

- `assessment_v2/services/engine/strategies/health.py` líneas 167, 317,
  977 y 1025. La 977 es tajante: *«Para W-CLIN-SCAN incluye siempre una
  URL de imagen en media_assets»*.
- `science.py` líneas 705 y 753.
- `tech.py` línea 760.
- `humanities.py` línea 799 (EV-ICON-ART).

El único código de toda la plataforma que escribe algo en
`media_assets` es `orchestrator/tasks.py:1291`, y es **audio**:

```python
if audio_url: db_item.content['media_assets'] = [audio_url]
```

No existe generador de imágenes, ni almacenamiento de imágenes en la
app `contents`, ni servicio de recuperación. Se le pide al modelo una
URL que no puede conocer, la alucina, y `exam_take.html:228-238` la
pinta como `<img>` roto.

### Evidencia real

Examen `5c200071` (ARCH_HEALTH, Anatomía, 2026-07-29):

- Ítem 163 → `https://medlib.ugr.es/imagenes/torso_anatomico_01.jpg`
  — dominio institucional inventado de principio a fin.
- Ítem 164 → `https://upload.wikimedia.org/wikipedia/commons/4/4e/
  Chest_x-ray_PA_and_lateral.jpg` — **la forma es correcta**: así se
  estructuran de verdad las URLs de Wikimedia Commons, con dos
  directorios derivados de un hash. El modelo inventó el hash.

**Conclusión operativa:** la forma de la URL no permite distinguir una
válida de una inventada. Cualquier salvaguarda basada en patrones está
condenada. La única verificación fiable es pedir el recurso y
comprobar que responde.

### Alcance

- `W-CLIN-SCAN` (bloque ILC-CONTEXT) en ARCH_HEALTH, ARCH_SCI y
  ARCH_TECH.
- `EV-ICON-ART` en ARCH_HUM.

S024 (ARCH_SCI) y S025 (ARCH_LANG) no lo detectaron por azar: a
ninguno de los dos exámenes le tocó un ítem con imagen.

### Decisión de Miguel Ángel (S026)

No se aplica puente ni parche provisional. Las evaluaciones no están
abiertas a usuarios reales, de modo que un examen roto no causa daño;
lo que procede es resolver el asunto de las imágenes bien y de una
vez. Las instrucciones de inventar URLs **se dejan como están** hasta
que este hito las sustituya por el contrato nuevo.

### Restricción de licencias — matiz importante

CampuStudiOnline es **hoy uso no comercial**: no hay actividad
económica dada de alta, ni como empresa ni como autónomo, y el acceso
es gratuito. Por tanto las licencias con cláusula NC (CC BY-NC,
CC BY-NC-SA, CC BY-NC-ND) **sí son utilizables ahora mismo**, y el
catálogo disponible es ancho.

Pero los modelos `SubscriptionPlan` y `UserSubscription` ya existen en
el código: la plataforma está preparada para cobrar. El día que se
active, cada imagen NC de la biblioteca pasa a ser material que hay
que retirar, y las licencias no se renegocian a posteriori.

La respuesta correcta **no es prohibir NC hoy**, sino registrar la
licencia como dato de cada imagen. Así, el día del cambio, localizar y
sustituir las NC es una consulta y no una auditoría manual. La
atribución (autor, licencia, enlace) hay que almacenarla igualmente
porque CC BY y CC BY-SA la exigen, de modo que el campo de licencia
sale prácticamente gratis.

### Catálogos candidatos

- **Open-i** (National Library of Medicine): ~3,7 millones de imágenes
  de ~1,2 millones de artículos de PubMed Central, más 7.470
  radiografías de tórax con informe radiológico, 67.517 imágenes de la
  colección de Historia de la Medicina y 2.064 ilustraciones
  ortopédicas. Tiene API y **filtro por tipo de licencia**, que es lo
  que lo convierte en el candidato principal.
- **Public Health Image Library (CDC)**: mayoritariamente dominio
  público.
- **Wikimedia Commons**: API de búsqueda real, licencias por archivo.
- **Gray's Anatomy** (edición de 1918): dominio público.
- **Bassett Collection** (Stanford): CC BY-SA 4.0.

---

## Registro de Sesiones

### S026 — 2026-07-29 — Apertura del hito

Hito abierto en esta sesión, como desvío de H06. El trabajo de S026 se
dedicó en su mayor parte a H06 y está registrado en su anexo; aquí
queda únicamente lo relativo a las imágenes.

El hallazgo llegó al generar el examen `5c200071` (Anatomía) durante
la campaña E2E de H06: los ítems `W-CLIN-SCAN` pedían observar
imágenes inexistentes. La investigación descartó una a una las
hipótesis baratas y terminó en un hueco de diseño, no en un defecto de
implementación — el detalle completo está en la sección de contexto
técnico de este mismo anexo.

Se descartó expresamente una salvaguarda por forma de URL, después de
comprobar que el modelo produce indistintamente dominios inventados de
principio a fin y URLs con la estructura correcta de Wikimedia Commons
y el hash inventado. No hay patrón que distinga una válida de una
falsa; solo sirve pedir el recurso.

Se corrigió además una suposición equivocada del modelo durante la
sesión: dio por hecho que la plataforma cobraba, al ver
`SubscriptionPlan` en el código, y de ahí dedujo que las licencias no
comerciales quedaban descartadas. Es falso — no hay actividad
económica dada de alta y el acceso es gratuito. La conclusión correcta
no es prohibir las licencias NC hoy, sino registrar la licencia como
dato de cada imagen para que el día que se active el cobro sea una
consulta y no una auditoría manual.

---

### S027 — 2026-07-30 — Cierre completo del hito

Sesión larga y densa: los siete puntos de la hoja de ruta quedan
cerrados, verificados con datos reales de producción en cada paso, y
con dos incidencias reales encontradas y corregidas ya fuera de la
hoja de ruta original.

**Punto 1 — Modelo de datos** (`2e8b0b0`). App nueva `media_library`
(opción C sobre las tres planteadas: independiente y modular, decisión
de Miguel Ángel). Tres modelos: `MediaCatalog`, `MediaLicense`,
`MediaResource`, con `checksum` SHA-256 único, `upload_to` particionado
por hash, y estado de verificación explícito. Migración de esquema
(`0001`) y de datos (`0002`, siembra de catálogos y 11 licencias)
separadas a propósito, según `com-migrations` sección 2.3. Hallazgo de
diseño verificado contra el propio código de Django 5.0.7:
`supports_partial_indexes=False` en MySQL hace que cualquier
`UniqueConstraint` con `condition` se omita en silencio, sin error de
migración — la constraint de `external_id` se rediseñó como
`null=True` + constraint incondicional (MySQL admite varios `NULL` en
un índice único), verificado con `SHOW INDEX` real en producción.

**Desvío de sesión — reparación de `orchestrator` (commiteado y
revertido)**. Al comprobar la constraint anterior se encontró que
`orchestrator` tiene 6 claves ajenas y 3 constraints declaradas en los
modelos que no existen en la base de datos real — las migraciones
`0001`/`0002` de esa app están aplicadas con 4 ms de diferencia entre
sí, marca de un historial reparado a mano en su día durante el
renombrado de `content_automation` a `orchestrator` (confirmado por
Miguel Ángel). Se escribió una migración de reparación
(`4f678b9`), que en el primer despliegue real falló por
`TransactionManagementError` (el `RunPython` no declaraba
`atomic=False`, y MySQL no admite DDL dentro de una transacción). El
fallo abortó todo antes de escribir nada — verificado con los propios
logs del servidor, incluida una falsa alarma inicial sobre pérdida de
datos que quedó descartada al comparar los conteos reales antes y
después. Se decidió revertir el commit completo (`803cca6`) en lugar
de arreglarlo a mitad de otro hito, y encauzar la reparación de fondo
hacia H21 (Refactorización del Orquestador), que es donde corresponde.
**No forma parte del cierre de H38** — queda como incidencia
documentada, no resuelta.

**Punto 2 — Servicio de recuperación** (`a5944a3`, `32c6e86`).
Decisión explícita de Miguel Ángel: Wikimedia Commons en exclusiva,
sin catálogo de contingencia. Motivo medido en producción, no
supuesto: sobre 8 peticiones reales a la API de Open-i, 3 terminaron
en timeout (37,5% de fallo), y de 10 elementos reales de su colección
PMC ninguno traía un solo campo de licencia — el código de terceros
auditado en GitHub que parseaba `item.license` lo hacía sobre un
supuesto que sus propios autores tampoco habían confirmado. Wikimedia,
en cambio, respondió 6/6 en las pruebas de fiabilidad y el vocabulario
de `extmetadata` coincidió con la documentación oficial en los tres
archivos reales consultados. `media_library/services.py`:
`search()` y `verify_and_store()`, con verificación de contenido real
vía Pillow antes de guardar — no solo la cabecera `Content-Type`, que
puede mentir o venir de una descarga truncada; defecto real encontrado
durante la propia verificación (`IntegrityError` por `width`/`height`
en `None` cuando Pillow no puede decodificar la imagen) y corregido
antes de desplegar.

**Punto 3 — Inversión del flujo** (`90e76ed`, ampliado en `1372f51`).
`generate_multimodal_item_content()` en `gemini_service.py` y
`_generate_item_image_content()` en `orchestrator/tasks.py`, enganchado
como posprocesado aislado tras el éxito de cada sección, con
degradación segura: si falla, el ítem conserva el contenido de la
llamada por lotes en vez de quedar peor. Ampliado a `W-ART-IDENT`
(Historia del Arte) a petición explícita de Miguel Ángel — antes de
construir soporte multi-imagen se consultó la propia constelación
documental del hito (`V06DOC_WIDGETS.md`, `V06DOC_BLOCKS.md`,
certificación UGR) y se confirmó que la instrucción original de
`humanities.py` (3 imágenes por ítem) era un defecto respecto a la
propia especificación certificada, no una necesidad real: el widget
usa una única obra. Se corrigió a una imagen, sin tocar ninguna
plantilla.

**Punto 4 — Retirada de URL inventada** (`1b34639`, completado para
`humanities.py` en `1372f51`). Las cinco estrategias ya no piden URLs
que no pueden conocer.

**Puntos 5 y 6** (`4c484f1`). Atribución (autor, licencia, enlace) en
`exam_take.html` y `exam_report.html`, solo donde el dato existe de
verdad. `logic.py` propaga `media_assets`/`media_attribution` al
informe de calificación. Corregido también el defecto documentado de
`orchestrator/tasks.py:1291` (sobrescritura de `media_assets` en lugar
de fusión) — y se encontró que el propio código nuevo del punto 3
tenía el mismo patrón, corregido igual en los dos sitios con un
helper único (`_set_media_asset`), probado reproduciendo el bug
original.

**Punto 7 — Prueba E2E real** (`70fc6fc`, refinado en `f70ba5f`).
Examen real generado en producción sobre la asignatura Anatomía (la
misma que originó el hito). Generación completa sin excepciones, pero
la ejecución real reveló tres cosas que ninguna lectura de código
hubiera mostrado:

1. Los dos ítems `W-CLIN-SCAN` del examen recibieron la misma imagen
   — el conjunto de exclusión de duplicados se reiniciaba en cada
   sección en lugar de vivir a nivel de examen. Corregido y verificado
   reproduciendo el escenario exacto.
2. Wikimedia devolvió `CC BY 2.5`, versión no contemplada por la tabla
   de mapeo fija del punto 2 (solo cubría 3.0/4.0). Cayó a `UNKNOWN`
   — comportamiento seguro por diseño, pero con pérdida real de
   información conocida. Sustituido por un reconocedor genérico por
   expresión regular que cubre cualquier versión de CC, con migración
   de siembra (`0004`) para las versiones históricas que Wikimedia usa
   de verdad.
3. **Bloqueo de infraestructura, no de código**: la imagen real
   devolvía 404 en producción porque `/media/` solo lo sirve Django
   bajo `DEBUG` y el *mapping* de archivos estáticos en el panel Web
   de PythonAnywhere, pendiente desde el arranque del hito, seguía sin
   hacerse. Resuelto por Miguel Ángel durante la propia sesión,
   verificado con una petición HTTP real (`200`, `image/jpeg`, tamaño
   exacto coincidente con el archivo original).

Un segundo examen real, generado por Miguel Ángel de forma independiente
tras dar el hito por cerrado, confirmó que el punto 6 funcionaba (dos
imágenes distintas dentro del mismo examen) pero reveló un cuarto
hallazgo: dos exámenes *distintos* de la misma asignatura convergían en
la misma imagen para el primer ítem, porque la consulta de búsqueda
dependía solo del título de la asignatura, idéntico entre generaciones.
Corregido en `f70ba5f` enriqueciendo la consulta con el título de la
propia sección (dato real ya disponible, no inventado) y, de paso, se
corrigió también el recurso ya existente que había quedado en `UNKNOWN`
antes del arreglo de licencias — sin volver a consultar Wikimedia,
reutilizando `license_url`, que ya estaba guardado correctamente desde
el principio.

**Despliegue**: 11 commits, 11 despliegues verdes salvo uno
(`70fc6fc`), que falló por *timeout* de `curl` esperando la API de
recarga de PythonAnywhere (código de salida 28, no un fallo de
código) — la migración y el reinicio de workers de ese mismo
despliegue sí tuvieron éxito; resuelto con una recarga manual de
Miguel Ángel y verificado. Cada despliegue que tocó
`orchestrator/tasks.py` se verificó con datos reales — timestamps
correlacionados con el arranque real de `hp_worker`/`heavy_worker`, y
en un caso, captura directa del panel de PythonAnywhere con ambos
servicios en `Starting`.

**Fuera de alcance, documentado y no tocado**: un error preexistente
en `assessment_v2.services.tracking` (`unsupported operand type(s) for
+=: 'float' and 'decimal.Decimal'`) salió a la luz durante la prueba
E2E real — no impidió que el examen se completara, pero el registro de
consumo de tokens de esa generación se perdió. Es una incidencia
propia, no de H38.

---

### S028 — 2026-07-31 — PCH: marcador movido a H06

Sin trabajo nuevo propio de H38 en esta sesión. Miguel Ángel confirmó
la reanudación de H06 ("Continuamos con las evaluaciones"), y el
enrutador (`CAMPUSTUDIONLINE_ANNEX_ROUTER.md`) mueve el marcador
`← EN PROGRESO` de H38 a H06, conforme a `nfs-campustudionline-pch`
Caso B. H38 queda sin marca de estado por estar terminado — los siete
puntos de su hoja de ruta original siguen cerrados y verificados,
según registro de S027.

---

## Hoja de Ruta para la Siguiente Sesión (LEY SUPREMA)

**Hito H38 completado.** Los siete puntos de la hoja de ruta original
están cerrados y verificados con datos reales de producción, no solo
con despliegues verdes. No queda ningún punto pendiente propio de este
hito.

Cabos sueltos que no forman parte del cierre, para quien retome
cualquiera de ellos:

- **Reparación de `orchestrator`** (6 claves ajenas y 3 constraints
  ausentes en la base de datos real, migración de datos con 4 ms de
  diferencia entre sí — historial reparado a mano en su día). Pertenece
  a H21. Diagnóstico completo en la bitácora de esta sesión.
- **`assessment_v2.services.tracking`**: error preexistente con
  `Decimal`/`float` al registrar uso de tokens, detectado durante la
  prueba E2E de hoy. No es de H38.
- **`W-ART-IDENT` con más de una obra por ítem**: hoy usa una sola,
  alineado con la certificación UGR vigente. Si algún día se quisiera
  comparar varias obras en el mismo ítem, hace falta rediseñar también
  la plantilla (`exam_take.html`), no solo el servicio.
- **Paso manual pendiente que sí se resolvió hoy**: el *mapping* de
  `/media/` en PythonAnywhere ya está hecho y verificado — no queda
  nada por hacer ahí.

El hito EN PROGRESO en el enrutador sigue siendo H38 — esta sesión no
incluyó un PCH explícito, así que el marcador no se mueve aquí. La
decisión natural para la siguiente sesión, ya anotada desde S026: H06
queda pausado desde S026 precisamente porque H38 lo bloqueaba, y el
bloqueo ha desaparecido. Su arranque natural son ARCH_SOC y ARCH_HUM
—que además deben ejercitar `source_text`, pendiente desde hace dos
sesiones—, y ahora también sirve para probar `W-ART-IDENT` con datos
reales por primera vez. Queda a decisión explícita de Miguel Ángel
mover el marcador.
