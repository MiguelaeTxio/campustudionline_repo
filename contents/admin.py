# /home/MiguelAeTxio/CampuStudiOnline/contents/admin.py
from django.contrib import admin, messages
from .models import (
    FavoriteFolder,
    KnowledgeArea,
    Discipline,
    MainCategory,
    Topic,
    ContentMaterial,
    ContentCopy,
    Annotation,
    FreeContentMasterCategory,
    FreeContentSubCategory,
)

try:
    from .preview_generator import (
        generate_static_previews,
    )
    GENERATOR_AVAILABLE = True
except ImportError:
    GENERATOR_AVAILABLE = False
    def generate_static_previews(queryset):
        raise NotImplementedError("El módulo contents.preview_generator no está disponible.")

@admin.action(description="Generar/Actualizar Sitio de Previews SEO")
def generate_public_previews_action_for_admin(modeladmin, request, queryset):
    if not GENERATOR_AVAILABLE:
        modeladmin.message_user(request, "Error: La función de generación de previews no está disponible.", messages.ERROR)
        return
    try:
        generate_static_previews(queryset)
        modeladmin.message_user(request, "Proceso de generación/actualización de previews SEO iniciado.", messages.SUCCESS)
    except Exception as e:
        modeladmin.message_user(request, f"Error crítico al generar previews: {e}", messages.ERROR)

@admin.register(FreeContentMasterCategory)
class FreeContentMasterCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'display_order', 'description')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ('display_order',)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

@admin.register(FreeContentSubCategory)
class FreeContentSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'master_category', 'slug', 'display_order')
    list_filter = ('master_category',)
    search_fields = ('name', 'master_category__name')
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ['master_category']
    list_editable = ('display_order',)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

@admin.register(KnowledgeArea)
class KnowledgeAreaAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "description")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ("name", "knowledge_area", "slug")
    list_filter = ("knowledge_area",)
    search_fields = ("name", "knowledge_area__name")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ["knowledge_area"]

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "discipline", "slug")
    list_filter = ("discipline__knowledge_area", "discipline")
    search_fields = ("name", "discipline__name")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ["discipline"]

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("__str__", "main_category", "parent", "slug")
    list_filter = ("main_category__discipline__knowledge_area", "main_category")
    search_fields = ("name", "parent__name", "main_category__name")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ["main_category", "parent"]
    list_per_page = 25

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

@admin.register(ContentMaterial)
class ContentMaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "get_category_display", "creator", "is_public", "updated_at")
    list_filter = ("is_free_content", "is_public", "master_category", "topic__main_category__discipline")
    search_fields = ("title", "creator__username", "topic__name", "master_category__name", "sub_category__name", "subject__name")
    actions = [generate_public_previews_action_for_admin]
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ["creator", "topic", "subject", "master_category", "sub_category"]
    fieldsets = (
        (None, {"fields": ("title", "is_free_content", "short_description", "creator", "is_public")}),
        ("Categorización Académica (Rellenar solo si NO es Contenido Libre)", {"fields": ("topic", "subject"), "classes": ("collapse",)}),
        ("Categorización de Contenido Libre (Rellenar solo si ES Contenido Libre)", {"fields": ("master_category", "sub_category"), "classes": ("collapse",)}),
        ("Contenido Fuente (Markdown)", {"fields": ("markdown_content",)}),
        ("Fechas Importantes", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    class Media:
        js = ('contents/js/admin_custom.js',)

    @admin.display(description="Categoría", ordering="topic")
    def get_category_display(self, obj):
        if obj.is_free_content:
            if obj.sub_category:
                return str(obj.sub_category)
            if obj.master_category:
                return str(obj.master_category)
            return "N/A (Libre)"
        if obj.topic:
            return str(obj.topic)
        return "N/A (Académico)"

    def delete_queryset(self, request, queryset):
        """
        [ROBUSTEZ] Sobrescribe la acción de borrado masivo.
        
        En lugar de llamar a queryset.delete() directamente, que no dispara
        las señales post_delete, este método itera sobre el queryset y llama
        al .delete() de cada instancia.
        
        Esto garantiza que todas las señales de limpieza y poda de jerarquías
        (tanto para contenido libre como académico) se ejecuten correctamente
        incluso en borrados masivos desde el panel de administración.
        """
        for obj in queryset:
            obj.delete()

@admin.register(ContentCopy)
class ContentCopyAdmin(admin.ModelAdmin):
    list_display = ("original_content", "user", "is_public", "updated_at")
    list_filter = ("is_public",)
    search_fields = ("original_content__title", "user__username")
    autocomplete_fields = ["original_content", "user"]

@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ("copy", "annotation_type", "created_at")
    list_filter = ("annotation_type",)
    search_fields = ("content", "copy__original_content__title")
    autocomplete_fields = ["copy"]

@admin.register(FavoriteFolder)
class FavoriteFolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'id')
    search_fields = ('name', 'user__username')
