# Migración de datos escrita a mano según com-migrations sección 1.
# Siembra el conjunto inicial de catálogos permitidos y de licencias
# conocidas. Separada de 0001 a propósito (com-migrations 2.3): un
# fallo de datos no debe bloquear la creación del esquema.

from django.db import migrations

CATALOGS = [
    {
        "code": "OPENI",
        "name": "Open-i (National Library of Medicine)",
        "homepage_url": "https://openi.nlm.nih.gov/",
        "is_enabled": True,
        "notes": (
            "Candidato principal: expone API de búsqueda y permite "
            "filtrar por tipo de licencia. La URL base de la API se "
            "rellena al verificarla contra su documentación."
        ),
    },
    {
        "code": "WIKIMEDIA",
        "name": "Wikimedia Commons",
        "homepage_url": "https://commons.wikimedia.org/",
        "is_enabled": True,
        "notes": (
            "API de búsqueda real y licencia declarada por archivo. "
            "Desaconseja expresamente el hotlinking, de ahí que el "
            "archivo se almacene siempre en local."
        ),
    },
    {
        "code": "CDC_PHIL",
        "name": "Public Health Image Library (CDC)",
        "homepage_url": "https://phil.cdc.gov/",
        "is_enabled": False,
        "notes": (
            "Mayoritariamente dominio público, pero sin API pública "
            "verificada: queda deshabilitado hasta que exista una vía "
            "de consulta programática o se decida el alta manual."
        ),
    },
]

LICENSES = [
    {
        "code": "PD",
        "name": "Dominio público",
        "url": "",
        "allows_commercial_use": True,
        "allows_derivatives": True,
        "requires_attribution": False,
        "requires_share_alike": False,
        "notes": (
            "Obras sin derechos vigentes u obras del gobierno de EE. UU. "
            "La atribución no es exigible, pero se registra igualmente."
        ),
    },
    {
        "code": "CC0-1.0",
        "name": "CC0 1.0 Universal",
        "url": "https://creativecommons.org/publicdomain/zero/1.0/",
        "allows_commercial_use": True,
        "allows_derivatives": True,
        "requires_attribution": False,
        "requires_share_alike": False,
        "notes": "",
    },
    {
        "code": "CC-BY-3.0",
        "name": "Creative Commons Atribución 3.0",
        "url": "https://creativecommons.org/licenses/by/3.0/",
        "allows_commercial_use": True,
        "allows_derivatives": True,
        "requires_attribution": True,
        "requires_share_alike": False,
        "notes": "",
    },
    {
        "code": "CC-BY-4.0",
        "name": "Creative Commons Atribución 4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/",
        "allows_commercial_use": True,
        "allows_derivatives": True,
        "requires_attribution": True,
        "requires_share_alike": False,
        "notes": "",
    },
    {
        "code": "CC-BY-SA-3.0",
        "name": "Creative Commons Atribución-CompartirIgual 3.0",
        "url": "https://creativecommons.org/licenses/by-sa/3.0/",
        "allows_commercial_use": True,
        "allows_derivatives": True,
        "requires_attribution": True,
        "requires_share_alike": True,
        "notes": "",
    },
    {
        "code": "CC-BY-SA-4.0",
        "name": "Creative Commons Atribución-CompartirIgual 4.0",
        "url": "https://creativecommons.org/licenses/by-sa/4.0/",
        "allows_commercial_use": True,
        "allows_derivatives": True,
        "requires_attribution": True,
        "requires_share_alike": True,
        "notes": "",
    },
    {
        "code": "CC-BY-ND-4.0",
        "name": "Creative Commons Atribución-SinDerivadas 4.0",
        "url": "https://creativecommons.org/licenses/by-nd/4.0/",
        "allows_commercial_use": True,
        "allows_derivatives": False,
        "requires_attribution": True,
        "requires_share_alike": False,
        "notes": "No admite recorte ni escalado de la imagen.",
    },
    {
        "code": "CC-BY-NC-4.0",
        "name": "Creative Commons Atribución-NoComercial 4.0",
        "url": "https://creativecommons.org/licenses/by-nc/4.0/",
        "allows_commercial_use": False,
        "allows_derivatives": True,
        "requires_attribution": True,
        "requires_share_alike": False,
        "notes": (
            "Utilizable mientras la plataforma sea de acceso gratuito y "
            "sin actividad económica dada de alta."
        ),
    },
    {
        "code": "CC-BY-NC-SA-4.0",
        "name": (
            "Creative Commons Atribución-NoComercial-CompartirIgual 4.0"
        ),
        "url": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
        "allows_commercial_use": False,
        "allows_derivatives": True,
        "requires_attribution": True,
        "requires_share_alike": True,
        "notes": "",
    },
    {
        "code": "CC-BY-NC-ND-4.0",
        "name": (
            "Creative Commons Atribución-NoComercial-SinDerivadas 4.0"
        ),
        "url": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
        "allows_commercial_use": False,
        "allows_derivatives": False,
        "requires_attribution": True,
        "requires_share_alike": False,
        "notes": "",
    },
    {
        "code": "UNKNOWN",
        "name": "Licencia sin determinar",
        "url": "",
        "allows_commercial_use": False,
        "allows_derivatives": False,
        "requires_attribution": True,
        "requires_share_alike": False,
        "notes": (
            "Marcador conservador. Un recurso con esta licencia no debe "
            "publicarse: se retiene solo para poder investigar su "
            "procedencia."
        ),
    },
]


def seed_reference_data(apps, schema_editor):
    """
    Create the initial catalogs and licenses if they are missing.
    ---
    Da de alta los catálogos y licencias iniciales. Es idempotente: si
    la fila ya existe por su código, no se toca, para no pisar ajustes
    hechos a mano desde el panel de administración.
    """
    catalog_model = apps.get_model("media_library", "MediaCatalog")
    license_model = apps.get_model("media_library", "MediaLicense")
    for entry in CATALOGS:
        catalog_model.objects.get_or_create(
            code=entry["code"],
            defaults={
                key: value
                for key, value in entry.items()
                if key != "code"
            },
        )
    for entry in LICENSES:
        license_model.objects.get_or_create(
            code=entry["code"],
            defaults={
                key: value
                for key, value in entry.items()
                if key != "code"
            },
        )


def unseed_reference_data(apps, schema_editor):
    """
    Remove the seeded rows that are still unused.
    ---
    Retira las filas sembradas que no tengan recursos asociados. Las
    que sí los tengan quedan intactas: borrarlas rompería la integridad
    referencial protegida por PROTECT.
    """
    catalog_model = apps.get_model("media_library", "MediaCatalog")
    license_model = apps.get_model("media_library", "MediaLicense")
    catalog_model.objects.filter(
        code__in=[entry["code"] for entry in CATALOGS],
        resources__isnull=True,
    ).delete()
    license_model.objects.filter(
        code__in=[entry["code"] for entry in LICENSES],
        resources__isnull=True,
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("media_library", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            seed_reference_data,
            unseed_reference_data,
        ),
    ]
