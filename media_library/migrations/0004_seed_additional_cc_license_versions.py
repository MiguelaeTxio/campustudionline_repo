# Migración de datos escrita a mano según com-migrations sección 1.
#
# Motivo: verificado en produccion el 2026-07-30 (primera prueba E2E
# real de H38, examen de Anatomia) que Wikimedia Commons usa "CC BY
# 2.5" en la practica -- version historica no sembrada en 0002, que
# solo cubria 3.0 y 4.0. El recurso cayo a UNKNOWN, comportamiento
# seguro pero con perdida real de informacion de atribucion conocida.
#
# Se siembran las versiones historicas mas comunes en Commons para BY
# y BY-SA (1.0, 2.0, 2.5), que es donde de verdad concentra su uso el
# material antiguo del catalogo. Los terminos practicos (atribucion
# exigida, derivados permitidos, uso comercial permitido) son
# identicos entre versiones de una misma variante; solo cambia
# jurisdiccion/redaccion legal, irrelevante para el uso que le da esta
# plataforma.

from django.db import migrations

LICENCIAS_NUEVAS = [
    {
        "code": "CC-BY-1.0",
        "name": "Creative Commons Atribución 1.0",
        "url": "https://creativecommons.org/licenses/by/1.0/",
        "allows_commercial_use": True,
        "allows_derivatives": True,
        "requires_attribution": True,
        "requires_share_alike": False,
        "notes": "Version historica, sembrada al detectar uso real en Wikimedia Commons (S027).",
    },
    {
        "code": "CC-BY-2.0",
        "name": "Creative Commons Atribución 2.0",
        "url": "https://creativecommons.org/licenses/by/2.0/",
        "allows_commercial_use": True,
        "allows_derivatives": True,
        "requires_attribution": True,
        "requires_share_alike": False,
        "notes": "Version historica, sembrada al detectar uso real en Wikimedia Commons (S027).",
    },
    {
        "code": "CC-BY-2.5",
        "name": "Creative Commons Atribución 2.5",
        "url": "https://creativecommons.org/licenses/by/2.5/",
        "allows_commercial_use": True,
        "allows_derivatives": True,
        "requires_attribution": True,
        "requires_share_alike": False,
        "notes": (
            "Version encontrada en produccion (S027, primera prueba E2E "
            "de H38): File:Eye_orbit_anatomy_anterior2.jpg, Patrick J. "
            "Lynch. Motivo directo de esta migracion."
        ),
    },
    {
        "code": "CC-BY-SA-1.0",
        "name": "Creative Commons Atribución-CompartirIgual 1.0",
        "url": "https://creativecommons.org/licenses/by-sa/1.0/",
        "allows_commercial_use": True,
        "allows_derivatives": True,
        "requires_attribution": True,
        "requires_share_alike": True,
        "notes": "Version historica, sembrada al detectar uso real en Wikimedia Commons (S027).",
    },
    {
        "code": "CC-BY-SA-2.0",
        "name": "Creative Commons Atribución-CompartirIgual 2.0",
        "url": "https://creativecommons.org/licenses/by-sa/2.0/",
        "allows_commercial_use": True,
        "allows_derivatives": True,
        "requires_attribution": True,
        "requires_share_alike": True,
        "notes": "Version historica, sembrada al detectar uso real en Wikimedia Commons (S027).",
    },
    {
        "code": "CC-BY-SA-2.5",
        "name": "Creative Commons Atribución-CompartirIgual 2.5",
        "url": "https://creativecommons.org/licenses/by-sa/2.5/",
        "allows_commercial_use": True,
        "allows_derivatives": True,
        "requires_attribution": True,
        "requires_share_alike": True,
        "notes": "Version historica, sembrada al detectar uso real en Wikimedia Commons (S027).",
    },
]


def seed_additional_cc_versions(apps, schema_editor):
    """
    Add the missing historical CC BY / CC BY-SA versions, idempotently.
    ---
    Añade las versiones históricas de CC BY / CC BY-SA que faltaban,
    de forma idempotente (no toca las que ya existan).
    """
    license_model = apps.get_model("media_library", "MediaLicense")
    for entry in LICENCIAS_NUEVAS:
        license_model.objects.get_or_create(
            code=entry["code"],
            defaults={k: v for k, v in entry.items() if k != "code"},
        )


def remove_additional_cc_versions(apps, schema_editor):
    """
    Remove the seeded rows if unused, mirror of 0002's reverse.
    ---
    Retira las filas sembradas si no tienen recursos asociados, igual
    que el reverso de 0002.
    """
    license_model = apps.get_model("media_library", "MediaLicense")
    license_model.objects.filter(
        code__in=[e["code"] for e in LICENCIAS_NUEVAS],
        resources__isnull=True,
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("media_library", "0003_disable_openi_catalog"),
    ]

    operations = [
        migrations.RunPython(
            seed_additional_cc_versions,
            remove_additional_cc_versions,
        ),
    ]
