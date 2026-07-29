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

## Hoja de Ruta para la Siguiente Sesión (LEY SUPREMA)

### 1. Modelo de datos de recursos

Crear el modelo de recurso multimedia con, como mínimo: URL de origen,
archivo almacenado localmente, autor, licencia, URL de la licencia,
catálogo de procedencia, consulta que lo encontró, y fecha de
verificación. Migración escrita en el mismo commit que el modelo, según
`com-migrations` sección 1.

### 2. Servicio de recuperación y verificación

Consulta contra catálogo permitido, verificación **real** por petición
HTTP (código 200 y `content-type` de imagen), descarga y
almacenamiento local. El almacenamiento local no es un lujo: resuelve
los enlaces rotos y evita el hotlinking masivo, que Wikimedia
desaconseja expresamente.

### 3. Inversión del flujo de generación

Hoy la IA escribe la pregunta y después inventa la URL. Debe ser al
revés: recuperar la imagen primero, verificarla, y pasársela a Gemini
de forma multimodal —capacidad que `core/services/gemini_service.py`
ya tiene, según registra su propio log— para que redacte `stem` y
`grading_logic` **sobre esa imagen concreta**.

Motivo: si se busca imagen para una pregunta ya escrita, se acaba con
una radiografía patológica ilustrando una pregunta sobre anatomía
normal.

### 4. Retirada de las instrucciones de URL inventada

Sustituir en las cinco estrategias (health, science, tech, humanities)
la orden de incluir URL por el contrato nuevo del servicio de
recuperación. No antes: mientras no exista el servicio, retirarlas solo
degradaría los enunciados sin ganar nada.

### 5. Atribución en la interfaz

Mostrar autor, licencia y enlace en `exam_take.html` y en
`exam_report.html`. No es cortesía: es la condición de las licencias
CC BY y CC BY-SA.

### 6. Corregir la sobrescritura de `media_assets`

`orchestrator/tasks.py:1291` **sobrescribe** la lista entera con la URL
del audio en lugar de añadirla. Hoy es inocuo porque no hay imágenes
reales; en cuanto las haya, un ítem con imagen y audio perdería la
imagen.

### 7. Prueba E2E

Generar un examen de ARCH_HEALTH con imagen real y recorrer los seis
puntos de control (a-f) ejecutando en producción, nunca leyendo
código, según la metodología que S024 y S025 dejaron asentada.
