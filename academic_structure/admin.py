from django.contrib import admin
from django.utils.html import format_html
import json
from .models import University, Branch, Degree, AcademicYear, Subject


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "url")
    search_fields = ("name", "code")


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "university")
    search_fields = ("name", "university__name")
    list_filter = ("university",)


@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    list_display = ("name", "branch", "degree_type")
    search_fields = ("name", "branch__name")
    list_filter = ("branch__university", "branch", "degree_type")


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('year', 'degree')
    search_fields = ('degree__name',)
    list_filter = ('degree__branch__university', 'degree__branch', 'degree')
    ordering = ('degree__name', 'year')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "get_degree", "get_year", "semester", "subject_type")
    search_fields = ("name", "academic_year__degree__name")
    list_filter = (
        "academic_year__degree__branch__university",
        "academic_year__degree__branch",
        "academic_year__degree",
        "academic_year__year",
        "subject_type",
    )

    readonly_fields = (
        "display_learning_objectives",
        "display_course_content_outline",
        "display_bibliography",
    )

    fieldsets = (
        (None, {
            "fields": ("name", "academic_year", "semester", "subject_type")
        }),
        ("Detalles de la Guía Docente (Inputs para la IA)", {
            "classes": ("collapse",),
            "fields": (
                "display_learning_objectives",
                "display_course_content_outline",
                "display_bibliography",
            ),
        }),
    )

    @admin.display(description='Titulación', ordering='academic_year__degree__name')
    def get_degree(self, obj):
        return obj.academic_year.degree

    @admin.display(description='Año', ordering='academic_year__year')
    def get_year(self, obj):
        return obj.academic_year.year

    def _display_json_field(self, obj_data, default_text="No disponible."):
        """
        Función auxiliar para renderizar un campo JSON de forma legible.
        """
        if not obj_data:
            return default_text
        
        # Formatea el JSON para que sea legible (pretty-print)
        formatted_json = json.dumps(obj_data, indent=2, ensure_ascii=False)
        
        # Usa <pre> para respetar los saltos de línea y la indentación
        return format_html("<pre><code>{}</code></pre>", formatted_json)

    def display_learning_objectives(self, obj):
        return self._display_json_field(
            obj.learning_objectives, 
            "No hay objetivos de aprendizaje disponibles."
        )
    display_learning_objectives.short_description = "Objetivos de Aprendizaje"

    def display_course_content_outline(self, obj):
        return self._display_json_field(
            obj.course_content_outline,
            "No hay temario disponible."
        )
    display_course_content_outline.short_description = "Temario del Curso"

    def display_bibliography(self, obj):
        return self._display_json_field(
            obj.bibliography,
            "No hay bibliografía disponible."
        )
    display_bibliography.short_description = "Bibliografía"
