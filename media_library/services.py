# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/media_library/services.py
"""
Wikimedia Commons retrieval and verification service.
---
Servicio de recuperación y verificación contra Wikimedia Commons.

Diseño verificado en sesión S027 contra el servidor real, no de
memoria: la API oficial (MediaWiki action API, generator=search +
imageinfo + extmetadata) respondió 6/6 en pruebas de fiabilidad, y el
vocabulario de licencia (LicenseShortName, LicenseUrl, UsageTerms,
AttributionRequired) coincide con la documentación oficial de la
extensión CommonsMetadata en los tres archivos reales consultados.

Por decisión explícita de Miguel Ángel, este es el único catálogo
activo: no hay plan de contingencia hacia ningún otro proveedor.

Dos responsabilidades deliberadamente separadas:
- search(): consulta la API de búsqueda, no descarga nada.
- verify_and_store(): hace la petición HTTP real al archivo de imagen
  (no al endpoint de metadatos) y solo si responde 200 con
  content-type de imagen lo descarga y lo persiste. Esto es el
  requisito raíz de H38: nunca se guarda una URL sin haberla
  comprobado en el momento.

Ninguna de las dos funciones lanza excepción por un fallo esperable de
red: devuelven un resultado con el error registrado, para que el
llamador (la generación de un examen) pueda seguir sin bloquearse.
"""

import hashlib
import io
import logging

import requests
from django.core.files.base import ContentFile
from django.db import IntegrityError
from django.utils import timezone
from django.utils.html import strip_tags
from PIL import Image, UnidentifiedImageError

from .models import MediaCatalog, MediaLicense, MediaResource

logger = logging.getLogger(__name__)

API_URL = "https://commons.wikimedia.org/w/api.php"

# Wikimedia exige identificación de clientes automatizados; sin esto
# hay riesgo de limitación de tasa. Verificado contra la politica
# real de la Fundacion en la documentacion de la API.
USER_AGENT = (
    "CampuStudiOnline/1.0 "
    "(https://github.com/MiguelaeTxio/campustudionline_repo; "
    "proyecto academico, H38 media_library)"
)

EXTMETADATA_FILTER = "|".join([
    "LicenseShortName",
    "LicenseUrl",
    "UsageTerms",
    "Copyrighted",
    "Attribution",
    "AttributionRequired",
    "Artist",
    "Credit",
    "ImageDescription",
])

# [S027 - correccion tras E2E real] Wikimedia devolvio "CC BY 2.5" en
# produccion, version no contemplada por la tabla fija original (solo
# 3.0/4.0). En vez de seguir enumerando versiones a mano, se reconoce
# el patron estandar de Creative Commons con una expresion regular:
# cubre CUALQUIER version (1.0, 2.0, 2.5, 3.0, 4.0...) para BY, BY-SA,
# BY-NC, BY-ND, BY-NC-SA, BY-NC-ND. Si el codigo resultante no esta
# sembrado en MediaLicense (verify_and_store lo comprueba), sigue
# cayendo a UNKNOWN exactamente igual que antes -- esto NUNCA inventa
# una licencia, solo deja de perder informacion real por una tabla
# incompleta.
import re as _re

_CC_LICENSE_PATTERN = _re.compile(
    r"^CC\s+(BY-NC-SA|BY-NC-ND|BY-SA|BY-NC|BY-ND|BY)\s+(\d+\.\d+)$",
    _re.IGNORECASE,
)


def _normalize_license_code(license_raw):
    """
    Normalize a Wikimedia LicenseShortName into our MediaLicense.code
    format, for ANY Creative Commons version.
    ---
    Normaliza un LicenseShortName de Wikimedia al formato de
    MediaLicense.code, para CUALQUIER version de Creative Commons.
    Nunca adivina un codigo para algo que no encaje en el patron
    estandar; en ese caso devuelve None y el llamador cae a UNKNOWN,
    igual que antes.
    """
    if not license_raw:
        return None
    limpio = license_raw.strip()
    if limpio.upper() == "CC0":
        return "CC0-1.0"
    if limpio.lower() in ("public domain", "pd"):
        return "PD"
    m = _CC_LICENSE_PATTERN.match(limpio)
    if not m:
        return None
    variante, version = m.group(1).upper(), m.group(2)
    return f"CC-{variante}-{version}"


# [S027 - backfill de recursos existentes] Formato real observado:
# https://creativecommons.org/licenses/by/2.5
# https://creativecommons.org/licenses/by-sa/4.0/
# https://creativecommons.org/publicdomain/zero/1.0/
_CC_LICENSE_URL_PATTERN = _re.compile(
    r"creativecommons\.org/licenses/(by(?:-nc-sa|-nc-nd|-sa|-nc|-nd)?)/(\d+\.\d+)",
    _re.IGNORECASE,
)


def resolve_license_from_url(license_url):
    """
    Same normalization as _normalize_license_code, but from the license
    URL instead of the LicenseShortName text.
    ---
    Misma normalizacion que _normalize_license_code, pero a partir de
    la URL de la licencia en lugar del texto LicenseShortName. Se
    usa para reconstruir el codigo correcto de recursos que quedaron
    en UNKNOWN antes de que existiera el reconocedor por texto (S027):
    el dato ya estaba guardado en license_url, no hacia falta volver a
    consultar Wikimedia. Nunca inventa una licencia: si no encaja en
    el patron estandar de CC, devuelve None.
    """
    if not license_url:
        return None
    if "publicdomain/zero" in license_url.lower():
        return "CC0-1.0"
    m = _CC_LICENSE_URL_PATTERN.search(license_url)
    if not m:
        return None
    variante, version = m.group(1).upper(), m.group(2)
    return f"CC-{variante}-{version}"

# Con Content-Type de imagen no basta un prefijo simple: algunos
# servidores devuelven "image/jpeg; charset=binary" u otras variantes.
_ALLOWED_IMAGE_PREFIXES = ("image/",)


class WikimediaSearchError(Exception):
    """La búsqueda contra la API de Wikimedia falló tras reintentar."""


def _session():
    """
    Build a requests session with the identifying header set once.
    ---
    Construye una sesión con la cabecera de identificación fijada una
    sola vez, para no repetirla en cada llamada.
    """
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT})
    return s


def search(query, limit=5, timeout=20):
    """
    Search Wikimedia Commons file namespace for a text query.
    ---
    Busca en el espacio de nombres de archivos de Wikimedia Commons.
    Devuelve una lista de diccionarios ya aplanados (no la respuesta
    cruda de la API), uno por resultado, con las claves:
    title, url, descriptionurl, mime, width, height, size,
    license_code (ya mapeado, puede ser None), license_raw,
    license_url, usage_terms, attribution_required, artist, credit.

    No descarga ni verifica nada — eso es responsabilidad de
    verify_and_store(). Puede lanzar WikimediaSearchError si la API no
    responde tras los reintentos.
    """
    # [FIX S029] gsrnamespace=6 (espacio de nombres File:) incluye PDFs,
    # no solo imagenes -- Wikimedia los almacena en el mismo namespace.
    # Verificado en vivo: la busqueda de texto completo para una consulta
    # academica real ("Anatomía Macroscópica — Nomenclatura Anatomía")
    # devolvio 5/5 resultados en PDF (revistas cientificas, un texto legal,
    # un libro de anatomia veterinaria), 0 imagenes reales -- verify_and_
    # store los rechazo correctamente a los 5, pero el item se quedo sin
    # imagen. Se excluye el tipo exacto que causo el problema con la
    # sintaxis de EXCLUSION (-filemime:), confirmada fiable por la
    # documentacion oficial de CirrusSearch -- la sintaxis de INCLUSION
    # positiva (filetype:image) tiene errores conocidos y documentados
    # que excluyen SVG por accidente (T374182), no se usa aqui a proposito.
    query_sin_pdf = f"{query} -filemime:application/pdf"
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": query_sin_pdf,
        "gsrnamespace": 6,
        "gsrlimit": limit,
        "prop": "imageinfo",
        "iiprop": "url|extmetadata|size|mime|user",
        "iiextmetadatafilter": EXTMETADATA_FILTER,
    }
    session = _session()
    ultimo_error = None
    data = None
    for intento in range(3):
        try:
            r = session.get(API_URL, params=params, timeout=timeout)
            data = r.json()
            break
        except (requests.RequestException, ValueError) as e:
            ultimo_error = e
            logger.warning(
                "Wikimedia search intento %s fallido: %r", intento + 1, e
            )
    if data is None:
        raise WikimediaSearchError(
            "Busqueda en Wikimedia Commons fallo tras 3 intentos: "
            + repr(ultimo_error)
        )

    pages = data.get("query", {}).get("pages", {})
    resultados = []
    for page in pages.values():
        infos = page.get("imageinfo") or []
        if not infos:
            continue
        info = infos[0]
        ext = info.get("extmetadata", {})

        def _valor(clave, ext=ext):
            return (ext.get(clave) or {}).get("value")

        license_raw = _valor("LicenseShortName")
        resultados.append({
            "title": page.get("title", ""),
            "url": info.get("url", ""),
            "descriptionurl": info.get("descriptionurl", ""),
            "mime": info.get("mime", ""),
            "width": info.get("width") or 0,
            "height": info.get("height") or 0,
            "size": info.get("size") or 0,
            "license_code": _normalize_license_code(license_raw),
            "license_raw": license_raw,
            "license_url": _valor("LicenseUrl") or "",
            "usage_terms": _valor("UsageTerms") or "",
            "attribution_required": _valor("AttributionRequired"),
            # [FIX] Los campos Artist/Credit de Wikimedia Commons a veces
            # traen HTML crudo (ej. '<span class="int-own-work">Own
            # work</span>', o listas <ul><li> completas con enlaces en
            # citas bibliograficas). Como las plantillas de exam_take.html
            # y exam_report.html imprimen media_attribution.text sin
            # `|safe` (Django autoescapa por defecto), ese HTML nunca se
            # renderiza como marcado -- se ve literalmente en pantalla como
            # texto con etiquetas, tal como confirmo Miguel Angel para el
            # item 249 del examen 8dd7b72d en S030. Se sanea aqui, en el
            # origen, para que ningun MediaResource nuevo vuelva a
            # persistir HTML en author/attribution_text.
            "artist": strip_tags(_valor("Artist") or "").strip(),
            "credit": strip_tags(_valor("Credit") or "").strip(),
        })
    return resultados


def verify_and_store(resultado, search_query=""):
    """
    Verify a search result via a real HTTP request and store it.
    ---
    Verifica un resultado de search() haciendo la petición HTTP real
    al archivo (no reutiliza nada de la respuesta de búsqueda como
    prueba de que el archivo existe) y, solo si responde 200 con
    content-type de imagen, lo descarga y crea el MediaResource.

    Devuelve (MediaResource, creado: bool) en éxito. Si la
    verificación falla, devuelve (None, False) y deja constancia del
    motivo en el logger — nunca lanza excepción por un fallo de red,
    porque este servicio puede llamarse durante la generación de un
    examen y un catálogo caído no debe tumbarla.

    Si el checksum ya existe en la base (misma imagen ya guardada),
    devuelve el MediaResource existente sin volver a descargar.
    """
    url = resultado.get("url", "")
    if not url:
        logger.warning("verify_and_store: resultado sin url, se omite")
        return None, False

    session = _session()
    try:
        r = session.get(url, timeout=30, stream=True)
    except requests.RequestException as e:
        logger.warning("Fallo al verificar %s: %r", url, e)
        return None, False

    content_type = r.headers.get("Content-Type", "")
    if r.status_code != 200 or not content_type.startswith(
        _ALLOWED_IMAGE_PREFIXES
    ):
        logger.warning(
            "Verificacion rechazada para %s: status=%s content-type=%s",
            url, r.status_code, content_type,
        )
        return None, False

    contenido = r.content

    # La cabecera Content-Type puede estar mal puesta o la descarga
    # puede haberse truncado (visto hoy mismo con otro proveedor). La
    # unica prueba real de que es una imagen es que Pillow la decodifique
    # y nos de sus dimensiones reales, que es lo que persistimos —
    # nunca se confia en el mecanismo automatico de width_field/
    # height_field de Django, que ante un fallo de decodificacion deja
    # esos campos en None y provoca un IntegrityError en el guardado.
    try:
        imagen = Image.open(io.BytesIO(contenido))
        imagen.verify()
        # verify() invalida el objeto para lecturas posteriores; se
        # reabre para poder leer las dimensiones con seguridad.
        imagen = Image.open(io.BytesIO(contenido))
        ancho, alto = imagen.size
    except (UnidentifiedImageError, OSError, ValueError) as e:
        logger.warning(
            "Contenido descargado de %s no es una imagen decodificable: %r",
            url, e,
        )
        return None, False

    checksum = hashlib.sha256(contenido).hexdigest()

    existente = MediaResource.objects.filter(checksum=checksum).first()
    if existente is not None:
        logger.info("Imagen ya existente (checksum coincide): %s", url)
        return existente, False

    catalog = MediaCatalog.objects.filter(
        code="WIKIMEDIA", is_enabled=True
    ).first()
    if catalog is None:
        logger.error(
            "Catalogo WIKIMEDIA no encontrado o deshabilitado; "
            "no se puede registrar el recurso."
        )
        return None, False

    codigo_licencia = resultado.get("license_code") or "UNKNOWN"
    licencia = MediaLicense.objects.filter(code=codigo_licencia).first()
    if licencia is None:
        licencia = MediaLicense.objects.get(code="UNKNOWN")

    nombre_archivo = url.rsplit("/", 1)[-1] or (checksum + ".bin")

    recurso = MediaResource(
        catalog=catalog,
        license=licencia,
        external_id=resultado.get("title") or None,
        source_page_url=resultado.get("descriptionurl", ""),
        source_file_url=url,
        license_url=resultado.get("license_url", ""),
        checksum=checksum,
        title=resultado.get("title", ""),
        author=resultado.get("artist", ""),
        attribution_text=resultado.get("credit", ""),
        description="",
        search_query=search_query,
        content_type=content_type,
        file_size=len(contenido),
        width=ancho,
        height=alto,
        status=MediaResource.Status.VERIFIED,
        verified_at=timezone.now(),
    )
    recurso.file.save(nombre_archivo, ContentFile(contenido), save=False)
    try:
        recurso.save()
    except IntegrityError:
        # Carrera con otra verificacion concurrente que guardo el
        # mismo checksum entre nuestra comprobacion y este save().
        existente = MediaResource.objects.filter(checksum=checksum).first()
        logger.info(
            "IntegrityError al guardar %s, ya existia (carrera): %s",
            url, existente,
        )
        return existente, False

    return recurso, True
