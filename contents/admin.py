# /home/MiguelAeTxio/CampuStudiOnline/contents/admin.py
from django.contrib import admin, messages
from .models import (
    FavoriteFolder,
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

@admin.register(ContentMaterial)
class ContentMaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "creator", "is_public", "updated_at")
    list_filter = ("is_free_content", "is_public", "master_category", )
    search_fields = ("title", "creator__username", "master_category__name", "sub_category__name", "subject__name")
    actions = [generate_public_previews_action_for_admin]
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ["creator", "subject", "master_category", "sub_category"]
    fieldsets = (
        (None, {"fields": ("title", "is_free_content", "short_description", "creator", "is_public")}),
        ("Categorización Académica (Rellenar solo si NO es Contenido Libre)", {"fields": ("subject",), "classes": ("collapse",)}),
        ("Categorización de Contenido Libre (Rellenar solo si ES Contenido Libre)", {"fields": ("master_category", "sub_category"), "classes": ("collapse",)}),
        ("Contenido Fuente (Markdown)", {"fields": ("markdown_content",)}),
        ("Fechas Importantes", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    class Media:
        js = ('contents/js/admin_custom.js',)

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

@admin.register(FreeContentMasterCategory)
class FreeContentMasterCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "display_order", "slug")
    search_fields = ("name",)
    ordering = ("display_order", "name")

@admin.register(FreeContentSubCategory)
class FreeContentSubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "master_category", "display_order", "slug")
    search_fields = ("name", "master_category__name")
    list_filter = ("master_category",)
    autocomplete_fields = ["master_category"]
    ordering = ("master_category", "display_order", "name")
