# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/contents/models.py
import uuid
import markdown
import bleach
from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from treebeard.mp_tree import MP_Node # Importado para el modelo FavoriteFolder
from academic_structure.models import Subject

MARKDOWN_EXTENSIONS = [
    "markdown.extensions.fenced_code", "markdown.extensions.codehilite",
    "markdown.extensions.tables", "markdown.extensions.attr_list",
    "markdown.extensions.toc", "markdown.extensions.sane_lists",
    "markdown.extensions.nl2br", "pymdownx.betterem", "pymdownx.tilde",
    "pymdownx.magiclink", "pymdownx.superfences", "pymdownx.tasklist",
]
MARKDOWN_EXTENSION_CONFIGS = {
    "markdown.extensions.codehilite": {
        "css_class": "highlight", "guess_lang": False, "noclasses": False,
    },
}
ALLOWED_TAGS = [
    "p", "br", "strong", "em", "del", "ul", "ol", "li", "a", "img", "hr",
    "h1", "h2", "h3", "h4", "h5", "h6", "pre", "code", "span", "div",
    "blockquote", "table", "thead", "tbody", "tr", "th", "td", "input",
    "details", "summary",
]
ALLOWED_ATTRIBUTES = {
    "*": ["class", "id", "style"], "a": ["href", "title", "target"],
    "img": ["src", "alt", "title", "width", "height"],
    "input": ["type", "checked", "disabled"], "code": ["class"],
    "div": ["class"], "span": ["class"],
}

def _is_node_empty(node):
    if isinstance(node, Topic):
        return not node.subtopics.exists() and not node.content_materials.exists()
    if isinstance(node, MainCategory):
        return not node.root_topics.exists()
    if isinstance(node, Discipline):
        return not node.main_categories.exists()
    if isinstance(node, KnowledgeArea):
        return not node.disciplines.exists()
    return False

def _is_free_node_empty(node):
    if isinstance(node, FreeContentCategory):
        return not node.content_materials.exists()
    if isinstance(node, FreeContentTopic):
        return not node.categories.exists()
    return False

class KnowledgeArea(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, verbose_name="Nombre del Área")
    slug = models.SlugField(max_length=300, unique=True, blank=True, default="")
    description = models.TextField(blank=True, verbose_name="Descripción")
    has_free_content = models.BooleanField(default=False, verbose_name="Tiene Contenido Libre")

    class Meta:
        verbose_name = "Área de Conocimiento"
        verbose_name_plural = "1. Áreas de Conocimiento"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            proposed_slug = base_slug
            while KnowledgeArea.objects.filter(slug=proposed_slug).exists():
                unique_suffix = uuid.uuid4().hex[:8]
                proposed_slug = f"{base_slug}-{unique_suffix}"
            self.slug = proposed_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("search:academic_area_detail", kwargs={"area_slug": self.slug})

class Discipline(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    knowledge_area = models.ForeignKey(
        KnowledgeArea, on_delete=models.CASCADE, related_name="disciplines",
        verbose_name="Área de Conocimiento",
    )
    name = models.CharField(max_length=255, verbose_name="Nombre de la Disciplina")
    slug = models.SlugField(max_length=300, unique=True, blank=True, default="")
    has_free_content = models.BooleanField(default=False, verbose_name="Tiene Contenido Libre")

    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "2. Disciplinas"
        ordering = ["knowledge_area", "name"]
        unique_together = ("knowledge_area", "name")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            proposed_slug = base_slug
            while Discipline.objects.filter(slug=proposed_slug).exists():
                unique_suffix = uuid.uuid4().hex[:8]
                proposed_slug = f"{base_slug}-{unique_suffix}"
            self.slug = proposed_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "search:academic_discipline_detail",
            kwargs={"area_slug": self.knowledge_area.slug, "discipline_slug": self.slug},
        )

    def delete(self, *args, **kwargs):
        knowledge_area_to_check = self.knowledge_area
        super().delete(*args, **kwargs)
        if _is_node_empty(knowledge_area_to_check):
            PROTECTED_KNOWLEDGE_AREAS = [
                "Biografías", "Desarrollo Personal", "Formación Profesional",
                "General", "Historia de la Música"
            ]
            if knowledge_area_to_check.name not in PROTECTED_KNOWLEDGE_AREAS:
                knowledge_area_to_check.delete()

class MainCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    discipline = models.ForeignKey(
        Discipline, on_delete=models.CASCADE, related_name="main_categories",
        verbose_name="Disciplina",
    )
    name = models.CharField(max_length=255, verbose_name="Nombre de la Categoría")
    slug = models.SlugField(max_length=300, unique=True, blank=True, default="")
    has_free_content = models.BooleanField(default=False, verbose_name="Tiene Contenido Libre")

    class Meta:
        verbose_name = "Categoría Principal"
        verbose_name_plural = "3. Categorías Principales"
        ordering = ["discipline", "name"]
        unique_together = ("discipline", "name")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            proposed_slug = base_slug
            while MainCategory.objects.filter(slug=proposed_slug).exists():
                unique_suffix = uuid.uuid4().hex[:8]
                proposed_slug = f"{base_slug}-{unique_suffix}"
            self.slug = proposed_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "search:academic_main_category_detail",
            kwargs={
                "area_slug": self.discipline.knowledge_area.slug,
                "discipline_slug": self.discipline.slug,
                "main_category_slug": self.slug,
            },
        )

    def delete(self, *args, **kwargs):
        discipline_to_check = self.discipline
        super().delete(*args, **kwargs)
        if _is_node_empty(discipline_to_check):
            discipline_to_check.delete()

class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    main_category = models.ForeignKey(
        MainCategory, on_delete=models.CASCADE, related_name="root_topics",
        verbose_name="Categoría Principal Raíz", null=True, blank=True,
        help_text="Asignar solo si este es un tema de primer nivel.",
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True,
        related_name="subtopics", verbose_name="Tema Padre",
        help_text="Asignar si este es un sub-tema de otro tema.",
    )
    name = models.CharField(max_length=255, verbose_name="Nombre del Tema")
    slug = models.SlugField(max_length=300, unique=True, blank=True, default="")
    has_free_content = models.BooleanField(default=False, verbose_name="Tiene Contenido Libre")

    class Meta:
        verbose_name = "Tema"
        verbose_name_plural = "4. Temas (Jerarquía)"
        ordering = ["name"]
        unique_together = ("parent", "name")

    def clean(self):
        super().clean()
        if self.parent and self.main_category:
            raise ValidationError(
                "Un tema no puede tener simultáneamente un 'Tema Padre' y una 'Categoría Principal Raíz'."
            )
        if not self.parent and not self.main_category:
            raise ValidationError(
                "Un tema debe tener o un 'Tema Padre' o una 'Categoría Principal Raíz'."
            )
        if self.pk and self.parent and self.pk == self.parent.pk:
            raise ValidationError("Un tema no puede ser su propio padre.")

    def __str__(self):
        if self.parent:
            return f"{self.parent} -> {self.name}"
        return self.name

    def save(self, *args, **kwargs):
        self.clean()
        if not self.slug:
            root_category = self.get_root_category()
            if root_category:
                base_slug = slugify(f"{root_category.discipline.slug}-{root_category.name}-{self.name}")
            else:
                base_slug = slugify(self.name) # Fallback para casos inesperados

            proposed_slug = base_slug
            while Topic.objects.filter(slug=proposed_slug).exists():
                unique_suffix = uuid.uuid4().hex[:6]
                proposed_slug = f"{base_slug}-{unique_suffix}"
            self.slug = proposed_slug
        super().save(*args, **kwargs)

    def get_root_category(self):
        if self.main_category:
            return self.main_category
        if self.parent:
            return self.parent.get_root_category()
        return None

    def get_slug_path(self):
        if self.parent:
            return f"{self.parent.get_slug_path()}/{self.slug}"
        return self.slug

    def get_absolute_url(self):
        root = self.get_root_category()
        if not root:
            return reverse("search:search_home")
        return reverse(
            "search:academic_topic_detail",
            kwargs={
                "area_slug": root.discipline.knowledge_area.slug,
                "discipline_slug": root.discipline.slug,
                "main_category_slug": root.slug,
                "topic_slug_path": self.get_slug_path(),
            },
        )

    def delete(self, *args, **kwargs):
        parent_to_check = self.parent
        main_category_to_check = self.main_category
        super().delete(*args, **kwargs)
        if parent_to_check and _is_node_empty(parent_to_check):
            parent_to_check.delete()
        if main_category_to_check and _is_node_empty(main_category_to_check):
            main_category_to_check.delete()

# --- NUEVA ARQUITECTURA DE CATEGORÍAS MAESTRAS PARA CONTENIDO LIBRE ---
class FreeContentMasterCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, verbose_name="Nombre de la Categoría Maestra")
    slug = models.SlugField(max_length=300, unique=True, blank=True, default="")
    description = models.TextField(blank=True, verbose_name="Descripción")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Orden de Visualización")

    class Meta:
        verbose_name = "Categoría Maestra de Contenido Libre"
        verbose_name_plural = "A. Categorías Maestras (Nivel 1)"
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("search:free_master_detail", kwargs={"master_slug": self.slug})

class FreeContentSubCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    master_category = models.ForeignKey(
        FreeContentMasterCategory,
        on_delete=models.CASCADE,
        related_name="sub_categories",
        verbose_name="Categoría Maestra Padre",
    )
    name = models.CharField(max_length=255, verbose_name="Nombre de la Subcategoría")
    slug = models.SlugField(max_length=300, unique=True, blank=True, default="")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Orden de Visualización")

    class Meta:
        verbose_name = "Subcategoría de Contenido Libre"
        verbose_name_plural = "A.1. Subcategorías (Nivel 2)"
        ordering = ["master_category", "display_order", "name"]
        unique_together = ('master_category', 'name')

    def __str__(self):
        return f"{self.master_category.name} -> {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.master_category.name}-{self.name}")
            proposed_slug = base_slug
            counter = 1
            while FreeContentSubCategory.objects.filter(slug=proposed_slug).exists():
                proposed_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = proposed_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "search:free_sub_detail",
            kwargs={"master_slug": self.master_category.slug, "sub_slug": self.slug},
        )

# -- HIERARCHY FOR FREE CONTENT (LEGACY - A SER DEPRECIADA) --

class FreeContentTopic(models.Model):
    """
    Representa el Nivel 1 de la jerarquía para Contenido Libre.
    Ej: "Historia de la Música", "Formación Profesional".
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, verbose_name="Nombre del Tema de Contenido Libre")
    slug = models.SlugField(max_length=300, unique=True, blank=True, default="")

    class Meta:
        verbose_name = "Tema de Contenido Libre (Legacy)"
        verbose_name_plural = "B. Temas de Contenido Libre (Legacy)"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            proposed_slug = base_slug
            while FreeContentTopic.objects.filter(slug=proposed_slug).exists():
                unique_suffix = uuid.uuid4().hex[:8]
                proposed_slug = f"{base_slug}-{unique_suffix}"
            self.slug = proposed_slug
        super().save(*args, **kwargs)


class FreeContentCategory(models.Model):
    """
    Representa el Nivel 2 de la jerarquía para Contenido Libre.
    Ej: "Rock Progresivo", "Mecánica".
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.ForeignKey(
        FreeContentTopic, on_delete=models.CASCADE, related_name="categories",
        verbose_name="Tema Padre",
    )
    name = models.CharField(max_length=255, verbose_name="Nombre de la Categoría de Contenido Libre")
    slug = models.SlugField(max_length=300, unique=True, blank=True, default="")

    class Meta:
        verbose_name = "Categoría de Contenido Libre (Legacy)"
        verbose_name_plural = "C. Categorías de Contenido Libre (Legacy)"
        ordering = ["topic", "name"]
        unique_together = ("topic", "name")

    def __str__(self):
        return f"{self.topic.name} -> {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.topic.name}-{self.name}")
            proposed_slug = base_slug
            counter = 1
            while FreeContentCategory.objects.filter(slug=proposed_slug).exists():
                proposed_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = proposed_slug
        super().save(*args, **kwargs)

class ContentMaterial(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=512, verbose_name="Título del Curso")
    slug = models.SlugField(max_length=600, unique=True, blank=True, default="")
    short_description = models.TextField(verbose_name="Descripción Corta")
    
    # -- ACADEMIC HIERARCHY --
    topic = models.ForeignKey(
        Topic, on_delete=models.PROTECT, related_name="content_materials",
        verbose_name="Clasificación Académica",
        null=True, blank=True, help_text="Usar solo para contenido académico estructurado.",
    )
    # -- FREE CONTENT HIERARCHY (LEGACY) --
    free_category = models.ForeignKey(
        "FreeContentCategory", on_delete=models.PROTECT, related_name="content_materials",
        verbose_name="Clasificación de Contenido Libre (Legacy)",
        null=True, blank=True, help_text="Usar solo para contenido libre no estructurado.",
    )
    # -- NEW FREE CONTENT HIERARCHY --
    master_category = models.ForeignKey(
        "FreeContentMasterCategory", on_delete=models.PROTECT, related_name="content_materials",
        verbose_name="Categoría Maestra (Nivel 1)",
        null=True, blank=True, help_text="Asignar solo para contenido libre.",
    )
    sub_category = models.ForeignKey(
        "FreeContentSubCategory", on_delete=models.PROTECT, related_name="content_materials",
        verbose_name="Subcategoría (Nivel 2)",
        null=True, blank=True, help_text="Asignar solo si el contenido pertenece a una subcategoría específica.",
    )

    subject = models.ManyToManyField(
        "academic_structure.Subject",
        blank=True,
        related_name="content_materials",
        verbose_name="Asignaturas Académicas Asociadas",
    )
    markdown_content = models.TextField(verbose_name="Contenido (Markdown)")
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name="created_content",
    )
    is_free_content = models.BooleanField(
        default=False, db_index=True, verbose_name="Es Contenido Libre"
    )
    is_public = models.BooleanField(default=True, verbose_name="¿Es Público?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Material de Contenido"
        verbose_name_plural = "D. Materiales de Contenido"
        ordering = ["-updated_at"]
        constraints = [
            models.CheckConstraint(
                check=(
                    (Q(is_free_content=True) & Q(master_category__isnull=False) & Q(topic__isnull=True)) |
                    (Q(is_free_content=False) & Q(master_category__isnull=True) & Q(topic__isnull=False))
                ),
                name='content_hierarchy_is_exclusive'
            )
        ]

    def __str__(self):
        return self.title

    def _render_markdown_to_html(self):
        if not self.markdown_content:
            return ""
        html_output = markdown.markdown(
            self.markdown_content, extensions=MARKDOWN_EXTENSIONS,
            extension_configs=MARKDOWN_EXTENSION_CONFIGS,
        )
        return bleach.clean(
            html_output, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES
        )

    def get_full_markdown_content(self):
        """
        Ensambla el contenido completo desde los GeneratedContentChunk asociados.
        Esta es la fuente de verdad para el contenido generado por automatización.
        """
        # Usamos hasattr para evitar un RelatedObjectDoesNotExist si la relación no existe
        if hasattr(self, 'source_task') and self.source_task:
            chunks = self.source_task.content_chunks.all().order_by('order')
            if chunks.exists():
                return '\n\n'.join(chunk.content for chunk in chunks)
        
        # Fallback para contenido creado manualmente o antes de la refactorización.
        return self.markdown_content

    def save(self, *args, **kwargs):
        # Regla de negocio: El contenido libre creado por el staff es siempre público.
        if self.is_free_content and self.creator and self.creator.is_staff:
            self.is_public = True

        if (not self.slug or ContentMaterial.objects.filter(slug=self.slug)
            .exclude(pk=self.pk).exists()):
            base_slug = slugify(self.title)
            proposed_slug = base_slug
            while ContentMaterial.objects.filter(slug=proposed_slug).exists():
                unique_suffix = uuid.uuid4().hex[:8]
                proposed_slug = f"{base_slug}-{unique_suffix}"

            self.slug = proposed_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("contents:content_detail", kwargs={"pk": self.pk})

    def delete(self, *args, **kwargs):
        topic_to_check = self.topic
        free_category_to_check = self.free_category
        super().delete(*args, **kwargs)
        if topic_to_check and _is_node_empty(topic_to_check):
            topic_to_check.delete()
        
        if free_category_to_check:
            if _is_free_node_empty(free_category_to_check):
                parent_topic_to_check = free_category_to_check.topic
                free_category_to_check.delete()
                if parent_topic_to_check and _is_free_node_empty(parent_topic_to_check):
                    parent_topic_to_check.delete()


class ContentCopy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_content = models.ForeignKey(
        ContentMaterial, on_delete=models.CASCADE, verbose_name="Contenido Original",
        related_name="derived_copies", help_text="Contenido original del que se deriva esta copia.",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Usuario",
        related_name="user_copies", help_text="Usuario que ha creado esta copia personalizada.",
    )
    subject_context = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="study_copies",
        verbose_name="Asignatura de Contexto",
        help_text="Asignatura específica para la cual se creó esta copia de estudio.",
    )
    html_content = models.TextField(
        verbose_name="Contenido con Anotaciones (HTML)",
        help_text="El cuerpo del contenido con las anotaciones y marcados integrados.",
    )
    is_public = models.BooleanField(
        verbose_name="¿Es público?", default=False,
        help_text="Marca esta casilla si quieres que esta copia sea visible para todos los usuarios. Si no, solo tú podrás verla.",
    )
    created_at = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Última actualización", auto_now=True)

    class Meta:
        verbose_name = "Sala de Estudio - Copia"
        verbose_name_plural = "E. Sala de Estudio - Copias"
        ordering = ["-updated_at"]
        unique_together = ["original_content", "user", "subject_context"]

    def __str__(self):
        context = f"para la asignatura '{self.subject_context.name}'" if self.subject_context else "de contenido libre"
        return f"Copia de '{self.original_content.title}' por {self.user.username} {context}"

    def get_absolute_url(self):
        return reverse("study_room:edit_copy", kwargs={"pk": self.pk})

class Annotation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ANNOTATION_TYPES = [("highlight", "Subrayado"), ("note", "Nota"), ("mark", "Marcado")]
    copy = models.ForeignKey(
        ContentCopy, on_delete=models.CASCADE, verbose_name="Copia de Contenido",
        related_name="annotations", help_text="Copia de contenido a la que pertenece esta anotación.",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Usuario Creador",
        related_name="created_annotations", help_text="Usuario que creó esta anotación.",
    )
    annotation_type = models.CharField(
        verbose_name="Tipo de Anotación", max_length=20, choices=ANNOTATION_TYPES,
        help_text="Tipo de anotación (subrayado, nota, marcado).",
    )
    content = models.TextField(
        verbose_name="Contenido",
        help_text="Texto de la anotación (para tipo 'nota') o el texto del DOM seleccionado (para 'subrayado', 'marcado').",
    )
    selected_text = models.TextField(
        verbose_name="Texto Seleccionado del DOM", blank=True, null=True,
        help_text="El texto exacto seleccionado del DOM al que se refiere esta anotación (importante para notas con referencia).",
    )
    position = models.TextField(
        verbose_name="Posición", help_text="Información de posición en el documento (formato JSON).",
    )
    color = models.CharField(
        verbose_name="Color", max_length=20,
        help_text="Color de la anotación en formato hexadecimal o nombre de color CSS.",
    )
    created_at = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Última actualización", auto_now=True)

    class Meta:
        verbose_name = "Sala de Estudio - Anotación"
        verbose_name_plural = "F. Sala de Estudio - Anotaciones"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.get_annotation_type_display()} por {self.user.username} en copia de '{self.copy.original_content.title}'"

    def get_absolute_url(self):
        base_url = self.copy.get_absolute_url()
        return f"{base_url}#annotation-{self.id}"

class FavoriteFolder(MP_Node):
    # Tipos de carpetas del sistema
    FOLDER_TYPE_FAVORITES = 'FAV'
    FOLDER_TYPE_PUBLICATIONS = 'PUB'
    FOLDER_TYPE_USER = 'USR' # Carpeta creada por el usuario

    FOLDER_TYPE_CHOICES = [
        (FOLDER_TYPE_FAVORITES, 'Mis Favoritos'),
        (FOLDER_TYPE_PUBLICATIONS, 'Mis Publicaciones'),
        (FOLDER_TYPE_USER, 'Carpeta de Usuario'),
    ]

    # Campos de treebeard (MP_Node)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # Forzamos UUID para coherencia
    name = models.CharField(max_length=255, verbose_name="Nombre de la Carpeta")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorite_folders",
        verbose_name="Usuario",
    )
    materials = models.ManyToManyField(
        ContentMaterial,
        related_name="favorite_folders",
        blank=True,
        verbose_name="Materiales Favoritos",
    )
    # Nuevo campo para el tipo de carpeta (Sistema o Usuario)
    folder_type = models.CharField(
        max_length=3,
        choices=FOLDER_TYPE_CHOICES,
        default=FOLDER_TYPE_USER,
        verbose_name="Tipo de Carpeta",
    )

    class Meta:
        verbose_name = "Carpeta de Favoritos"
        verbose_name_plural = "G. Carpetas de Favoritos"
        ordering = ["path"]
        # Se asegura que solo haya una carpeta de sistema del mismo tipo por usuario en la raíz

    def __str__(self):
        return f"{self.name} ({self.get_folder_type_display()})"
    
    def get_absolute_url(self):
        # La URL de detalle de la carpeta se resuelve a través del UUID
        return reverse('contents:favorite_folder_detail', args=[str(self.id)])
    
    # Propiedad para indicar si es una carpeta de sistema
    @property
    def is_system_folder(self):
        return self.folder_type in [self.FOLDER_TYPE_FAVORITES, self.FOLDER_TYPE_PUBLICATIONS]
    
    # Validación para evitar que las carpetas de usuario tengan folder_type de sistema
    def clean(self):
        if self.folder_type == self.FOLDER_TYPE_USER and self.name in ['Mis Favoritos', 'Mis Publicaciones']:
            raise ValidationError("Los nombres 'Mis Favoritos' y 'Mis Publicaciones' están reservados para las carpetas de sistema.")
        # Validación para evitar que carpetas de sistema tengan padre
        if self.is_system_folder and self.get_parent():
             raise ValidationError(f"La carpeta de sistema '{self.name}' no puede tener una carpeta padre.")
