# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/academic_structure/models.py
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
import uuid
import json
import hashlib

# [CORRECCIÓN] Se eliminan TODAS las importaciones de modelos a nivel de módulo
# para prevenir dependencias circulares. Las relaciones se definen con strings.

class TimeStampedModel(models.Model):
    """
    An abstract base model that provides self-managed creation and
    update date fields.
    """

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")

    class Meta:
        abstract = True


class ContentHashFamily(TimeStampedModel):
    """
    [NUEVO MODELO] Agrupa asignaturas con contenido idéntico.
    Centraliza el hash y el material de contenido generado, evitando duplicados.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hash = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        verbose_name="Hash de Contenido",
        help_text="SHA-256 hash del contenido canónico que define a esta familia."
    )
    content_material = models.OneToOneField(
        'contents.ContentMaterial',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='content_hash_family',
        verbose_name="Material de Contenido Asociado",
        help_text="El único material de contenido generado para esta familia."
    )

    class Meta:
        verbose_name = "Familia de Contenido"
        verbose_name_plural = "Familias de Contenido"
        ordering = ['-created_at']

    def __str__(self):
        return f"Familia Hash: {self.hash[:8]}... ({self.subjects.count()} Asignaturas)"


class University(TimeStampedModel):
    """
    Model to represent a University. It's the highest level in the academic hierarchy.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(
        max_length=20, unique=True, verbose_name="Código de Universidad"
    )
    name = models.CharField(max_length=255, verbose_name="Nombre de Universidad")
    url = models.URLField(
        max_length=512, blank=True, null=True, verbose_name="URL del Portal de Estudios"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        default="",
        help_text=_("Unique identifier for URLs."),
    )
    has_public_content = models.BooleanField(
        default=False,
        verbose_name="Tiene Contenido Público",
        help_text="Se actualiza automáticamente. Indica si alguna asignatura descendiente tiene material público."
    )

    class Meta:
        verbose_name = "Universidad"
        verbose_name_plural = "Universidades"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            max_len = self._meta.get_field("slug").max_length
            base_slug = base_slug[:max_len]

            proposed_slug = base_slug
            counter = 1
            while (
                University.objects.filter(slug=proposed_slug)
                .exclude(pk=self.pk)
                .exists()
            ):
                suffix = f"-{counter}"
                truncated_slug = base_slug[: (max_len - len(suffix))]
                proposed_slug = f"{truncated_slug}{suffix}"
                counter += 1
            self.slug = proposed_slug
        super().save(*args, **kwargs)


class Branch(TimeStampedModel):
    """
    Model to represent a Branch of Knowledge within a University.
    Ex: 'Health Sciences', 'Engineering and Architecture'.
    It's the second level of the hierarchy.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name="branches",
        verbose_name="Universidad",
    )
    name = models.CharField(max_length=255, verbose_name="Nombre de Rama")
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        default="",
        help_text=_("Unique identifier for URLs."),
    )
    has_public_content = models.BooleanField(
        default=False,
        verbose_name="Tiene Contenido Público",
        help_text="Se actualiza automáticamente. Indica si alguna asignatura descendiente tiene material público."
    )

    class Meta:
        verbose_name = "Rama de Conocimiento"
        verbose_name_plural = "Ramas de Conocimiento"
        ordering = ["university__name", "name"]
        unique_together = ("university", "name")

    def __str__(self):
        return f"{self.name} ({self.university.name})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.university.code}-{self.name}")
            max_len = self._meta.get_field("slug").max_length
            base_slug = base_slug[:max_len]

            proposed_slug = base_slug
            counter = 1
            while (
                Branch.objects.filter(slug=proposed_slug).exclude(pk=self.pk).exists()
            ):
                suffix = f"-{counter}"
                truncated_slug = base_slug[: (max_len - len(suffix))]
                proposed_slug = f"{truncated_slug}{suffix}"
                counter += 1
            self.slug = proposed_slug
        super().save(*args, **kwargs)


class Degree(TimeStampedModel):
    """
    Model to represent a Degree (Bachelor's, Master's, PhD).
    Now related to a Branch of Knowledge.
    """

    class DegreeType(models.TextChoices):
        BACHELOR = "GR", "Grado"
        MASTER = "MA", "Máster"
        PHD = "DO", "Doctorado"
        OTHER = "OT", "Otro"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="degrees",
        verbose_name="Rama de Conocimiento",
    )
    code = models.CharField(max_length=20, verbose_name="Código de Titulación")
    name = models.CharField(max_length=255, verbose_name="Nombre de Titulación")
    degree_type = models.CharField(
        max_length=2,
        choices=DegreeType.choices,
        default=DegreeType.BACHELOR,
        verbose_name="Tipo de Titulación",
    )
    url = models.URLField(
        max_length=512, blank=True, null=True, verbose_name="URL de la Titulación"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        default="",
        help_text=_("Unique identifier for URLs."),
    )
    has_public_content = models.BooleanField(
        default=False,
        verbose_name="Tiene Contenido Público",
        help_text="Se actualiza automáticamente. Indica si alguna asignatura descendiente tiene material público."
    )

    @property
    def duration_in_years(self):
        """Calcula dinámicamente la duración encontrando el año máximo de sus asignaturas."""
        max_year = self.academic_years.aggregate(models.Max('year'))['year__max']
        return max_year or 0

    class Meta:
        verbose_name = "Titulación"
        verbose_name_plural = "Titulaciones"
        ordering = ["branch__name", "name"]
        unique_together = ("branch", "name")

    def __str__(self):
        return f"{self.name} ({self.branch.name})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(
                f"{self.branch.university.code}-{self.branch.name}-{self.name}"
            )
            max_len = self._meta.get_field("slug").max_length
            base_slug = base_slug[:max_len]

            proposed_slug = base_slug
            counter = 1
            while (
                Degree.objects.filter(slug=proposed_slug).exclude(pk=self.pk).exists()
            ):
                suffix = f"-{counter}"
                truncated_slug = base_slug[: (max_len - len(suffix))]
                proposed_slug = f"{truncated_slug}{suffix}"
                counter += 1
            self.slug = proposed_slug
        super().save(*args, **kwargs)


class AcademicYear(TimeStampedModel):
    """
    Represents a specific academic year within a degree. E.g., "1st Year", "2nd Year".
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    degree = models.ForeignKey(
        Degree,
        on_delete=models.CASCADE,
        related_name="academic_years",
        verbose_name="Titulación",
    )
    year = models.PositiveSmallIntegerField("Año")
    has_public_content = models.BooleanField(
        default=False,
        verbose_name="Tiene Contenido Público",
        help_text="Se actualiza automáticamente. Indica si alguna asignatura de este año tiene material público."
    )

    class Meta:
        verbose_name = "Año Académico"
        verbose_name_plural = "Años Académicos"
        ordering = ["degree__name", "year"]
        unique_together = ("degree", "year")

    def __str__(self):
        return f"{self.year}º Año de {self.degree.name}"


class Subject(TimeStampedModel):
    """
    Model to represent a Subject of a Degree.
    """

    class SubjectType(models.TextChoices):
        CORE = "TR", "Troncal"
        MANDATORY = "OB", "Obligatoria"
        OPTIONAL = "OP", "Optativa"
        BASIC = "BA", "Formación Básica"
        OTHER = "OT", "Otra"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        related_name="subjects",
        verbose_name="Año Académico",
        null=True, 
        blank=True
    )
    
    # [REFACTOR] Se añade la relación con la familia de contenido.
    content_hash_family = models.ForeignKey(
        ContentHashFamily,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subjects',
        verbose_name="Familia de Contenido",
        help_text="Vincula esta asignatura a una familia de contenido idéntico."
    )

    name = models.CharField(max_length=255, verbose_name="Nombre de Asignatura")
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        default="",
        help_text=_("Unique identifier for URLs."),
    )

    subject_type = models.CharField(
        max_length=3, choices=SubjectType.choices, verbose_name="Tipo de Asignatura"
    )
    semester = models.PositiveSmallIntegerField(
        verbose_name="Semestre", null=True, blank=True
    )
    has_public_content = models.BooleanField(
        default=False,
        verbose_name="Tiene Contenido Público",
        help_text="Se actualiza automáticamente. Indica si esta asignatura tiene material público."
    )
    
    learning_objectives = models.JSONField(
        "Objetivos de Aprendizaje",
        default=list,
        blank=True,
        null=True,
        help_text="Lista de objetivos de aprendizaje extraídos de la guía docente.",
    )
    course_content_outline = models.JSONField(
        "Esquema de Contenidos",
        default=list,
        blank=True,
        null=True,
        help_text="Lista unificada del temario teórico y práctico.",
    )
    bibliography = models.JSONField(
        "Bibliografía",
        default=dict,
        blank=True,
        null=True,
        help_text="Diccionario con bibliografía fundamental y complementaria.",
    )
    
    # [REFACTOR] El campo content_hash se elimina de este modelo.
    # La lógica de unicidad ahora es manejada por ContentHashFamily.

    def _calculate_content_hash(self):
        """Calcula un hash determinista del contenido clave para la detección de duplicados."""
        from .utils import normalize_json_for_hash
        
        data = {
            'objectives': self.learning_objectives,
            'outline': self.course_content_outline,
            'bibliography': self.bibliography,
        }
        
        normalized_data = normalize_json_for_hash(data)
        
        return hashlib.sha256(normalized_data.encode('utf-8')).hexdigest()

    def __str__(self):
        year_str = f" (Año {self.academic_year.year})" if self.academic_year else ""
        return f"{self.name}{year_str}"


    def save(self, *args, **kwargs):
        # [REFACTOR] Se elimina el cálculo y asignación del hash.
        # Esta lógica ahora se gestionará centralizadamente a través de un comando.

        if not self.slug:
            slug_parts = [
                self.academic_year.degree.branch.university.code,
                self.academic_year.degree.name,
                self.name,
                f"year-{self.academic_year.year}",
            ]
            if self.semester:
                slug_parts.append(f"sem-{self.semester}")

            base_slug = slugify("-".join(filter(None, map(str, slug_parts))))

            max_len = self._meta.get_field("slug").max_length
            base_slug = base_slug[:max_len]

            proposed_slug = base_slug
            while (
                Subject.objects.filter(slug=proposed_slug).exclude(pk=self.pk).exists()
            ):
                unique_suffix = uuid.uuid4().hex[:4]
                truncated_slug = base_slug[: (max_len - len(unique_suffix) - 1)]
                proposed_slug = f"{truncated_slug}-{unique_suffix}"

            self.slug = proposed_slug
        
        super().save(*args, **kwargs)
        
    def is_content_generation_locked(self):
        """
        [GUARDIÁN LÓGICO REFACTORIZADO] Comprueba si la generación de contenido
        para esta asignatura debe estar bloqueada. El bloqueo se produce si:
        1. Su familia de contenido ya tiene un ContentMaterial asociado.
        2. Ya existe CUALQUIER PendingContentTask para CUALQUIER asignatura
           de la misma familia (independientemente del estado de la tarea).
        3. [NUEVO] La asignatura tiene material de contenido vinculado directamente.
        """
        # [CORRECCIÓN] Importación local para romper el ciclo.
        from orchestrator.models import PendingContentTask

        # 1. Comprobación directa de contenido vinculado (Prioridad Máxima)
        if self.content_materials.exists():
            return True

        if self.content_hash_family:
            # 2. Comprobar si ya existe material de contenido para la familia.
            if self.content_hash_family.content_material:
                return True

            # 3. Comprobar si hay tareas pendientes para cualquier asignatura de la familia.
            has_task = PendingContentTask.objects.filter(
                subject__content_hash_family=self.content_hash_family
            ).exclude(
                status__in=[
                    PendingContentTask.StatusChoices.COMPLETED,
                    PendingContentTask.StatusChoices.FAILED,
                    PendingContentTask.StatusChoices.FAILED_FATAL,
                ]
            ).exists()
            if has_task:
                return True
        
        # 4. Comprobar si hay tareas pendientes para esta asignatura específica (si no tiene familia)
        has_direct_task = PendingContentTask.objects.filter(
            subject=self
        ).exclude(
            status__in=[
                PendingContentTask.StatusChoices.COMPLETED,
                PendingContentTask.StatusChoices.FAILED,
                PendingContentTask.StatusChoices.FAILED_FATAL,
            ]
        ).exists()

        return has_direct_task

    def get_public_status(self):
        """
        [REFACTORIZADO] Determina el estado del contenido de cara al público,
        basándose en el estado de la FAMILIA de contenido.
        """
        # [CORRECCIÓN] Importación local para romper el ciclo.
        from orchestrator.models import ContentRequest

        # Comprobación directa de contenido
        if self.content_materials.filter(is_public=True).exists():
            return 'HAS_CONTENT'

        if not self.content_hash_family:
            return 'REQUESTABLE'

        # Si la familia ya tiene material público, todas las asignaturas lo reflejan.
        if (
            self.content_hash_family.content_material and 
            self.content_hash_family.content_material.is_public
        ):
            return 'HAS_CONTENT'

        # Comprobar si hay solicitudes para CUALQUIER asignatura de la familia.
        # La solicitud más reciente determina el estado.
        latest_request = ContentRequest.objects.filter(
            subject__content_hash_family=self.content_hash_family
        ).order_by('-created_at').first()

        if latest_request:
            status = latest_request.status
            if status == ContentRequest.StatusChoices.IN_PROGRESS:
                return 'IN_PROGRESS'
            if status == ContentRequest.StatusChoices.PENDING:
                return 'REQUEST_PENDING'

        return 'REQUESTABLE'

    class Meta:
        verbose_name = "Asignatura"
        verbose_name_plural = "Asignaturas"
        ordering = [
            "academic_year__degree__branch__university__name",
            "academic_year__degree__branch__name",
            "academic_year__degree__name",
            "academic_year__year",
            "semester",
            "name",
        ]
        unique_together = ("academic_year", "name", "semester")
