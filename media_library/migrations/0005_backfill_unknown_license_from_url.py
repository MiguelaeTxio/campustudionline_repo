# Migración de datos escrita a mano según com-migrations sección 1.
#
# Motivo: verificado en produccion el 2026-07-30 (segundo examen real
# generado tras el arreglo de licencias de la migracion 0003/servicio):
# el recurso del ojo (Eye_orbit_anatomy_anterior2.jpg) seguia marcado
# UNKNOWN pese a que el reconocedor generico ya sabe leer "CC BY 2.5".
# Motivo real: ese recurso se creo ANTES del arreglo, y la
# deduplicacion por checksum de verify_and_store devuelve el registro
# ya existente tal cual -- nunca reevalua su licencia en cada busqueda
# posterior.
#
# No hace falta volver a consultar Wikimedia: license_url ya estaba
# guardado correctamente desde el principio (es un campo que se llena
# siempre, independientemente de si el codigo de licencia se resolvio
# o no). Se re-deriva el codigo a partir de esa URL ya guardada.
#
# Logica de reconocimiento duplicada aqui a proposito, en vez de
# importar media_library.services: las migraciones no deben depender
# de codigo de aplicacion que usa el registro de modelos actual
# (services.py importa MediaResource/MediaLicense a nivel de modulo),
# solo del estado historico expuesto por apps.get_model. Es una
# funcion pura de una sola linea de logica, el riesgo de duplicarla es
# minimo y evita cualquier acoplamiento con el estado de la app.

import re

from django.db import migrations

_CC_LICENSE_URL_PATTERN = re.compile(
    r"creativecommons\.org/licenses/(by(?:-nc-sa|-nc-nd|-sa|-nc|-nd)?)/(\d+\.\d+)",
    re.IGNORECASE,
)


def _codigo_desde_url(license_url):
    if not license_url:
        return None
    if "publicdomain/zero" in license_url.lower():
        return "CC0-1.0"
    m = _CC_LICENSE_URL_PATTERN.search(license_url)
    if not m:
        return None
    variante, version = m.group(1).upper(), m.group(2)
    return f"CC-{variante}-{version}"


def backfill_unknown_licenses(apps, schema_editor):
    """
    Re-link UNKNOWN-licensed resources to their real license via URL.
    ---
    Re-vincula los recursos con licencia UNKNOWN a su licencia real,
    derivada de license_url, que ya estaba guardado correctamente.
    Idempotente: si no hay coincidencia o la licencia real no esta
    sembrada, la fila se deja como estaba.
    """
    resource_model = apps.get_model("media_library", "MediaResource")
    license_model = apps.get_model("media_library", "MediaLicense")

    reasignados = 0
    for recurso in resource_model.objects.filter(license__code="UNKNOWN"):
        codigo = _codigo_desde_url(recurso.license_url)
        if not codigo:
            continue
        licencia_real = license_model.objects.filter(code=codigo).first()
        if licencia_real is None:
            continue
        recurso.license = licencia_real
        recurso.save(update_fields=["license"])
        reasignados += 1
    print(f"  [backfill] {reasignados} recurso(s) reasignados desde UNKNOWN")


def noop_reverse(apps, schema_editor):
    """
    Irreversible on purpose: which resources were UNKNOWN before this
    migration is not recorded anywhere to restore.
    ---
    Irreversible a proposito: que recursos estaban en UNKNOWN antes de
    esta migracion no queda registrado en ningun sitio para revertir.
    """
    return None


class Migration(migrations.Migration):

    dependencies = [
        ("media_library", "0004_seed_additional_cc_license_versions"),
    ]

    operations = [
        migrations.RunPython(
            backfill_unknown_licenses,
            noop_reverse,
        ),
    ]
