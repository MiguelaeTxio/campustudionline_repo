# Migración de datos escrita a mano según com-migrations sección 1.
#
# Decisión explícita de Miguel Ángel (S027, 2026-07-30): el servicio de
# recuperación de H38 se construye exclusivamente contra Wikimedia
# Commons, sin plan de contingencia hacia ningún otro catálogo.
#
# Motivo verificado en la propia sesión, contra el servidor real, no de
# oídas: sobre 8 peticiones independientes al endpoint de búsqueda de
# Open-i, 3 terminaron en timeout de lectura (37.5% de fallo). Además,
# sobre 10 elementos reales de la colección PMC, ninguno trae ningún
# campo relacionado con licencia — el código de terceros auditado que
# sí leía item.license lo hacía sobre un supuesto nunca confirmado por
# sus propios autores (caían a "Unknown" por defecto).
#
# No se borra la fila: el catálogo queda deshabilitado, no eliminado,
# para conservar el historial de la decisión y no romper ninguna FK si
# alguna vez existiera un MediaResource que lo referenciara (hoy no
# existe ninguno).

from django.db import migrations

NOTAS = (
    "DESHABILITADO el 2026-07-30 por decisión explícita de Miguel "
    "Ángel: el servicio de H38 se construye en exclusiva contra "
    "Wikimedia Commons, sin catálogo de contingencia. Motivo medido "
    "en producción: 37.5% de fallo (timeout) en 8 peticiones "
    "independientes, y ausencia total de campo de licencia en 10 "
    "elementos reales de la colección PMC."
)


def disable_openi_catalog(apps, schema_editor):
    """
    Disable the Open-i catalog row, keep it for historical record.
    ---
    Deshabilita la fila de Open-i. No la borra: conserva el motivo de
    la decisión en sus propias notas.
    """
    catalog_model = apps.get_model("media_library", "MediaCatalog")
    catalog_model.objects.filter(code="OPENI").update(
        is_enabled=False,
        notes=NOTAS,
    )


def reenable_openi_catalog(apps, schema_editor):
    """
    Restore the Open-i catalog to its previously seeded state.
    ---
    Revierte al estado sembrado en 0002, por si la migración necesita
    deshacerse.
    """
    catalog_model = apps.get_model("media_library", "MediaCatalog")
    catalog_model.objects.filter(code="OPENI").update(
        is_enabled=True,
        notes=(
            "Candidato principal: expone API de búsqueda y permite "
            "filtrar por tipo de licencia. La URL base de la API se "
            "rellena al verificarla contra su documentación."
        ),
    )


class Migration(migrations.Migration):

    dependencies = [
        ("media_library", "0002_seed_catalogs_and_licenses"),
    ]

    operations = [
        migrations.RunPython(
            disable_openi_catalog,
            reenable_openi_catalog,
        ),
    ]
