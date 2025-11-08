from django.contrib import admin
from .models import AcademicChatLink


@admin.register(AcademicChatLink)
class AcademicChatLinkAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo AcademicChatLink.
    Permite gestionar la conexión entre asignaturas y salas de chat.
    """

    list_display = (
        "subject",
        "chat_room",
        "get_university_name",
        "get_degree_name",
        "get_enrolled_students_count",
    )
    list_select_related = (
        "subject__academic_year__degree__branch__university",
        "subject__academic_year__degree",
        "chat_room",
    )
    list_filter = ("subject__academic_year__degree__branch__university", "subject__academic_year__year")
    search_fields = (
        "subject__name",
        "subject__academic_year__degree__name",
        "chat_room__name",
        "access_code",
    )
    raw_id_fields = ("subject", "chat_room")
    filter_horizontal = ("enrolled_students",)
    readonly_fields = ("id", "access_code")

    fieldsets = (
        (None, {"fields": ("id", "subject", "chat_room", "access_code")}),
        (
            "Gestión de Alumnos",
            {
                "classes": ("collapse",),
                "fields": ("enrolled_students",),
                "description": "Seleccione los usuarios que están oficialmente matriculados en esta asignatura.",
            },
        ),
    )

    @admin.display(
        description="Universidad", ordering="subject__academic_year__degree__branch__university__name"
    )
    def get_university_name(self, obj):
        return obj.subject.academic_year.degree.branch.university.name

    @admin.display(description="Titulación", ordering="subject__academic_year__degree__name")
    def get_degree_name(self, obj):
        return obj.subject.academic_year.degree.name

    @admin.display(description="Nº Alumnos Matriculados")
    def get_enrolled_students_count(self, obj):
        return obj.enrolled_students.count()
