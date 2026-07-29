# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/media_library/models.py
"""
Data model for the verified media resource library.
---
Modelo de datos de la biblioteca de recursos multimedia verificados.

Cada recurso guarda su procedencia y su licencia como dato, no como
suposición: el día que la plataforma pase a uso comercial, retirar el
material con cláusula NC debe ser una consulta a la base de datos y no
una auditoría manual imagen por imagen.
"""

import uuid
from pathlib import Path

from django.db import models


def media_resource_upload_to(instance, filename):
    """
    Build a checksum-partitioned storage path for a media resource.
    ---
    Construye la ruta de almacenamiento del archivo, particionada por
    los primeros dígitos de su checksum, para no acumular decenas de
    miles de archivos en un único directorio. Si el checksum todavía no
    se ha calculado, el archivo cae en una partición aparte con nombre
    aleatorio, nunca sobre otro archivo existente.
    """
    checksum = (instance.checksum or "").strip().lower()
    extension = Path(filename).suffix.lower() or ".bin"
    if len(checksum) >= 4:
        return (
            f"media_library/{checksum[:2]}/{checksum[2:4]}/"
            f"{checksum}{extension}"
        )
    return f"media_library/unsorted/{uuid.uuid4().hex}{extension}"


class MediaCatalog(models.Model):
    """
    Allow-listed external source from which resources are retrieved.
    ---
    Catálogo externo permitido del que se recuperan recursos. La propia
    existencia de la fila es la autorización: el servicio de
    recuperación nunca consulta un catálogo que no esté aquí y
    habilitado.
    """

    code = models.CharField(
        max_length=32,
        unique=True,
        verbose_name="Código",
        help_text="Identificador interno estable, p. ej. OPENI.",
    )
    name = models.CharField(max_length=120, verbose_name="Nombre")
    homepage_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Página del catálogo",
    )
    api_base_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="URL base de la API",
        help_text=(
            "Se rellena solo cuando el endpoint ha sido verificado "
            "contra la documentación vigente del catálogo."
        ),
    )
    is_enabled = models.BooleanField(
        default=True,
        verbose_name="Habilitado",
        help_text="Permite retirar un catálogo sin borrar su historial.",
    )
    notes = models.TextField(blank=True, verbose_name="Notas")
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de alta",
    )

    class Meta:
        verbose_name = "Catálogo Multimedia"
        verbose_name_plural = "Catálogos Multimedia"
        ordering = ["name"]

    def __str__(self):
        return self.name


class MediaLicense(models.Model):
    """
    License terms attached to a stored media resource.
    ---
    Condiciones de licencia asociadas a un recurso almacenado. Los
    booleanos no son informativos: son el criterio de la consulta que
    localizará el material no reutilizable cuando cambien las
    circunstancias de la plataforma.
    """

    code = models.CharField(
        max_length=40,
        unique=True,
        verbose_name="Código",
        help_text="Identificador estable, p. ej. CC-BY-SA-4.0.",
    )
    name = models.CharField(max_length=160, verbose_name="Nombre")
    url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="URL de la licencia",
    )
    allows_commercial_use = models.BooleanField(
        default=False,
        verbose_name="Permite uso comercial",
        help_text=(
            "Por defecto falso: una licencia desconocida nunca se "
            "presume comercialmente reutilizable."
        ),
    )
    allows_derivatives = models.BooleanField(
        default=True,
        verbose_name="Permite obras derivadas",
        help_text="Falso en licencias ND: recortar o escalar no es lícito.",
    )
    requires_attribution = models.BooleanField(
        default=True,
        verbose_name="Exige atribución",
    )
    requires_share_alike = models.BooleanField(
        default=False,
        verbose_name="Exige compartir igual",
    )
    notes = models.TextField(blank=True, verbose_name="Notas")
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de alta",
    )

    class Meta:
        verbose_name = "Licencia Multimedia"
        verbose_name_plural = "Licencias Multimedia"
        ordering = ["code"]

    def __str__(self):
        return self.code


class MediaResource(models.Model):
    """
    A media file retrieved from a catalog, verified and stored locally.
    ---
    Recurso multimedia recuperado de un catálogo, verificado mediante
    petición real y almacenado en local. El almacenamiento local no es
    un lujo: evita los enlaces rotos y el hotlinking masivo, que
    Wikimedia desaconseja expresamente.
    """

    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente de verificación"
        VERIFIED = "verified", "Verificado"
        FAILED = "failed", "Verificación fallida"
        RETIRED = "retired", "Retirado"

    catalog = models.ForeignKey(
        MediaCatalog,
        on_delete=models.PROTECT,
        related_name="resources",
        verbose_name="Catálogo de procedencia",
    )
    license = models.ForeignKey(
        MediaLicense,
        on_delete=models.PROTECT,
        related_name="resources",
        verbose_name="Licencia",
    )
    external_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default=None,
        verbose_name="Identificador en el catálogo",
        help_text=(
            "Nulo, nunca cadena vacía, cuando el catálogo no aporta "
            "identificador: MySQL admite varios NULL en un índice "
            "único, y no soporta constraints condicionales."
        ),
    )
    source_page_url = models.URLField(
        max_length=1000,
        blank=True,
        verbose_name="URL de la ficha de origen",
    )
    source_file_url = models.URLField(
        max_length=1000,
        verbose_name="URL de origen del archivo",
    )
    license_url = models.URLField(
        max_length=1000,
        blank=True,
        verbose_name="URL de licencia del archivo",
        help_text=(
            "Enlace específico del archivo cuando el catálogo lo "
            "proporciona. Si está vacío se usa el de la licencia."
        ),
    )
    file = models.ImageField(
        upload_to=media_resource_upload_to,
        max_length=255,
        width_field="width",
        height_field="height",
        verbose_name="Archivo almacenado",
    )
    checksum = models.CharField(
        max_length=64,
        unique=True,
        verbose_name="Checksum SHA-256",
        help_text="Evita almacenar dos veces la misma imagen.",
    )
    title = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Título",
    )
    author = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Autor",
    )
    attribution_text = models.TextField(
        blank=True,
        verbose_name="Texto de atribución",
        help_text="Cadena lista para mostrar en la interfaz.",
    )
    description = models.TextField(blank=True, verbose_name="Descripción")
    search_query = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Consulta que lo encontró",
    )
    content_type = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Tipo de contenido",
    )
    file_size = models.PositiveIntegerField(
        default=0,
        verbose_name="Tamaño en bytes",
    )
    width = models.PositiveIntegerField(default=0, verbose_name="Anchura")
    height = models.PositiveIntegerField(default=0, verbose_name="Altura")
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Estado",
    )
    verified_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de verificación",
    )
    verification_error = models.TextField(
        blank=True,
        verbose_name="Error de verificación",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de alta",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última modificación",
    )

    class Meta:
        verbose_name = "Recurso Multimedia"
        verbose_name_plural = "Recursos Multimedia"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["status"],
                name="media_resource_status_idx",
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=("catalog", "external_id"),
                name="unique_external_id_per_catalog",
            ),
        ]

    def __str__(self):
        return self.title or self.checksum[:12]
