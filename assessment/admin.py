from django.contrib import admin
from django.urls import path, include
from django.utils.html import format_html
from django.urls import reverse
from .models import Assessment, Question, UserAnswer, AssessmentSettings

@admin.register(AssessmentSettings)
class AssessmentSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request): return not AssessmentSettings.objects.exists()
    def has_delete_permission(self, request, obj=None): return False

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    readonly_fields = ("question_text", "widget_type", "model_answer")
    can_delete = False
    show_change_link = True
    classes = ("collapse",)

class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    extra = 0
    readonly_fields = ("user", "answer_text", "answered_at", "score", "feedback")
    can_delete = False
    show_change_link = True
    classes = ("collapse",)

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [path("assessment-management/", include("assessment.admin_urls"))]
        return custom_urls + urls
    list_display = ("id", "content_copy", "user", "archetype", "status_badge", "created_at", "control_actions")
    list_filter = ("archetype", "status", "created_at", "user")
    search_fields = ("user__username", "content_copy__original_content__title")
    autocomplete_fields = ("content_copy", "user")
    inlines = [QuestionInline]
    date_hierarchy = "created_at"
    @admin.display(description="Estado", ordering="status")
    def status_badge(self, obj):
        colors = {Assessment.AssessmentStatus.PENDING: "#6c757d", Assessment.AssessmentStatus.PROCESSING: "#007bff", Assessment.AssessmentStatus.COMPLETED: "#28a745", Assessment.AssessmentStatus.RESULTS_AVAILABLE: "#28a745"}
        color = colors.get(obj.status, "#6c757d")
        return format_html('<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 10px; font-weight: bold;">{}</span>', color, obj.get_status_display())
    @admin.display(description="Acciones de Control")
    def control_actions(self, obj):
        buttons = []
        if obj.status in [Assessment.AssessmentStatus.PROCESSING, Assessment.AssessmentStatus.CORRECTING]:
            buttons.append(f'<a href="{reverse("admin:assessment_admin:assessment_pause_task", args=[obj.pk])}" class="button">Pausar</a>')
        return format_html(" ".join(buttons)) if buttons else "N/A"

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "assessment", "widget_type", "short_question_text")
    list_filter = ("widget_type", "assessment__user")
    search_fields = ("question_text", "assessment__user__username")
    autocomplete_fields = ("assessment",)
    inlines = [UserAnswerInline]
    def short_question_text(self, obj): return obj.question_text[:75] + "..."

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "user", "answered_at", "score")
    list_filter = ("answered_at", "user", "score")
    autocomplete_fields = ("question", "user")
    readonly_fields = ("question", "user", "answer_text", "answered_at")
