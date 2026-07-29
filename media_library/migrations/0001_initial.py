# Migración inicial de media_library, escrita a mano según
# com-migrations sección 1 (el modelo escribe modelo + migración en el
# mismo commit). Django 5.0.7.

import django.db.models.deletion
from django.db import migrations, models

import media_library.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MediaCatalog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        help_text=(
                            "Identificador interno estable, p. ej. OPENI."
                        ),
                        max_length=32,
                        unique=True,
                        verbose_name="Código",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=120, verbose_name="Nombre"),
                ),
                (
                    "homepage_url",
                    models.URLField(
                        blank=True,
                        max_length=500,
                        verbose_name="Página del catálogo",
                    ),
                ),
                (
                    "api_base_url",
                    models.URLField(
                        blank=True,
                        help_text=(
                            "Se rellena solo cuando el endpoint ha sido "
                            "verificado contra la documentación vigente "
                            "del catálogo."
                        ),
                        max_length=500,
                        verbose_name="URL base de la API",
                    ),
                ),
                (
                    "is_enabled",
                    models.BooleanField(
                        default=True,
                        help_text=(
                            "Permite retirar un catálogo sin borrar su "
                            "historial."
                        ),
                        verbose_name="Habilitado",
                    ),
                ),
                ("notes", models.TextField(blank=True, verbose_name="Notas")),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="Fecha de alta",
                    ),
                ),
            ],
            options={
                "verbose_name": "Catálogo Multimedia",
                "verbose_name_plural": "Catálogos Multimedia",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="MediaLicense",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        help_text=(
                            "Identificador estable, p. ej. CC-BY-SA-4.0."
                        ),
                        max_length=40,
                        unique=True,
                        verbose_name="Código",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=160, verbose_name="Nombre"),
                ),
                (
                    "url",
                    models.URLField(
                        blank=True,
                        max_length=500,
                        verbose_name="URL de la licencia",
                    ),
                ),
                (
                    "allows_commercial_use",
                    models.BooleanField(
                        default=False,
                        help_text=(
                            "Por defecto falso: una licencia desconocida "
                            "nunca se presume comercialmente reutilizable."
                        ),
                        verbose_name="Permite uso comercial",
                    ),
                ),
                (
                    "allows_derivatives",
                    models.BooleanField(
                        default=True,
                        help_text=(
                            "Falso en licencias ND: recortar o escalar no "
                            "es lícito."
                        ),
                        verbose_name="Permite obras derivadas",
                    ),
                ),
                (
                    "requires_attribution",
                    models.BooleanField(
                        default=True,
                        verbose_name="Exige atribución",
                    ),
                ),
                (
                    "requires_share_alike",
                    models.BooleanField(
                        default=False,
                        verbose_name="Exige compartir igual",
                    ),
                ),
                ("notes", models.TextField(blank=True, verbose_name="Notas")),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="Fecha de alta",
                    ),
                ),
            ],
            options={
                "verbose_name": "Licencia Multimedia",
                "verbose_name_plural": "Licencias Multimedia",
                "ordering": ["code"],
            },
        ),
        migrations.CreateModel(
            name="MediaResource",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "external_id",
                    models.CharField(
                        blank=True,
                        default=None,
                        help_text=(
                            "Nulo, nunca cadena vacía, cuando el "
                            "catálogo no aporta identificador: MySQL "
                            "admite varios NULL en un índice único, y "
                            "no soporta constraints condicionales."
                        ),
                        max_length=255,
                        null=True,
                        verbose_name="Identificador en el catálogo",
                    ),
                ),
                (
                    "source_page_url",
                    models.URLField(
                        blank=True,
                        max_length=1000,
                        verbose_name="URL de la ficha de origen",
                    ),
                ),
                (
                    "source_file_url",
                    models.URLField(
                        max_length=1000,
                        verbose_name="URL de origen del archivo",
                    ),
                ),
                (
                    "license_url",
                    models.URLField(
                        blank=True,
                        help_text=(
                            "Enlace específico del archivo cuando el "
                            "catálogo lo proporciona. Si está vacío se "
                            "usa el de la licencia."
                        ),
                        max_length=1000,
                        verbose_name="URL de licencia del archivo",
                    ),
                ),
                (
                    "file",
                    models.ImageField(
                        height_field="height",
                        max_length=255,
                        upload_to=(
                            media_library.models.media_resource_upload_to
                        ),
                        verbose_name="Archivo almacenado",
                        width_field="width",
                    ),
                ),
                (
                    "checksum",
                    models.CharField(
                        help_text=(
                            "Evita almacenar dos veces la misma imagen."
                        ),
                        max_length=64,
                        unique=True,
                        verbose_name="Checksum SHA-256",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        blank=True,
                        max_length=300,
                        verbose_name="Título",
                    ),
                ),
                (
                    "author",
                    models.CharField(
                        blank=True,
                        max_length=300,
                        verbose_name="Autor",
                    ),
                ),
                (
                    "attribution_text",
                    models.TextField(
                        blank=True,
                        help_text=(
                            "Cadena lista para mostrar en la interfaz."
                        ),
                        verbose_name="Texto de atribución",
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="Descripción"),
                ),
                (
                    "search_query",
                    models.CharField(
                        blank=True,
                        max_length=500,
                        verbose_name="Consulta que lo encontró",
                    ),
                ),
                (
                    "content_type",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        verbose_name="Tipo de contenido",
                    ),
                ),
                (
                    "file_size",
                    models.PositiveIntegerField(
                        default=0,
                        verbose_name="Tamaño en bytes",
                    ),
                ),
                (
                    "width",
                    models.PositiveIntegerField(
                        default=0,
                        verbose_name="Anchura",
                    ),
                ),
                (
                    "height",
                    models.PositiveIntegerField(
                        default=0,
                        verbose_name="Altura",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pendiente de verificación"),
                            ("verified", "Verificado"),
                            ("failed", "Verificación fallida"),
                            ("retired", "Retirado"),
                        ],
                        default="pending",
                        max_length=16,
                        verbose_name="Estado",
                    ),
                ),
                (
                    "verified_at",
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        verbose_name="Fecha de verificación",
                    ),
                ),
                (
                    "verification_error",
                    models.TextField(
                        blank=True,
                        verbose_name="Error de verificación",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="Fecha de alta",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        verbose_name="Última modificación",
                    ),
                ),
                (
                    "catalog",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="resources",
                        to="media_library.mediacatalog",
                        verbose_name="Catálogo de procedencia",
                    ),
                ),
                (
                    "license",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="resources",
                        to="media_library.medialicense",
                        verbose_name="Licencia",
                    ),
                ),
            ],
            options={
                "verbose_name": "Recurso Multimedia",
                "verbose_name_plural": "Recursos Multimedia",
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="mediaresource",
            index=models.Index(
                fields=["status"],
                name="media_resource_status_idx",
            ),
        ),
        migrations.AddConstraint(
            model_name="mediaresource",
            constraint=models.UniqueConstraint(
                fields=("catalog", "external_id"),
                name="unique_external_id_per_catalog",
            ),
        ),
    ]
