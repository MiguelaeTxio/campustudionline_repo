# /home/MiguelAeTxio/CampuStudiOnline/assessment/admin.py
from django.contrib import admin
from .models import Assessment, Question, UserAnswer, AssessmentSettings


@admin.register(AssessmentSettings)
class AssessmentSettingsAdmin(admin.ModelAdmin):
    """
    Admin interface for the singleton AssessmentSettings model.
    """

    def has_add_permission(self, request):
        # Prevent adding new instances if one already exists
        return not AssessmentSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deleting the settings instance
        return False


class QuestionInline(admin.TabularInline):
    """
    Allows viewing and editing questions directly from the assessment view.
    """

    model = Question
    extra = 0
    readonly_fields = ("question_text", "question_type", "model_answer")
    can_delete = False
    show_change_link = True
    classes = ("collapse",)


class UserAnswerInline(admin.TabularInline):
    """
    Allows viewing user answers directly from the question view.
    """

    model = UserAnswer
    extra = 0
    readonly_fields = ("user", "answer_text", "answered_at", "score", "feedback")
    can_delete = False
    show_change_link = True
    classes = ("collapse",)


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for the Assessment model.
    """

    list_display = ("id", "content_copy", "user", "status", "created_at")
    list_filter = ("status", "created_at", "user")
    search_fields = ("user__username", "content_copy__original_content__title")
    autocomplete_fields = ("content_copy", "user")
    inlines = [QuestionInline]
    date_hierarchy = "created_at"


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for the Question model.
    """

    list_display = ("id", "assessment", "question_type", "short_question_text")
    list_filter = ("question_type", "assessment__user")
    search_fields = ("question_text", "assessment__user__username")
    autocomplete_fields = ("assessment",)
    inlines = [UserAnswerInline]

    def short_question_text(self, obj):
        return (
            obj.question_text[:75] + "..."
            if len(obj.question_text) > 75
            else obj.question_text
        )

    short_question_text.short_description = "Question Text"


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for the UserAnswer model.
    """

    list_display = ("id", "question", "user", "answered_at", "score")
    list_filter = ("answered_at", "user", "score")
    search_fields = ("user__username", "question__question_text")
    autocomplete_fields = ("question", "user")
    readonly_fields = ("question", "user", "answer_text", "answered_at")
    fieldsets = (
        (
            None,
            {"fields": ("question", "user", "answered_at", "answer_text")},
        ),
        (
            "Evaluation and Feedback",
            {
                "fields": ("score", "feedback"),
                "classes": ("collapse",),
            },
        ),
    )
