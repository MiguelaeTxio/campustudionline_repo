# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/admin.py
from django.contrib import admin
from django.urls import path, include
from django.utils.html import format_html
from .models.main import Exam, Submission
from .models.plans import SubscriptionPlan, UserSubscription
from .models.tracking import TokenUsage, CostLog

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    """
    Administración de Exámenes con integración de Dashboard personalizado.
    """
    def get_urls(self):
        urls = super().get_urls()
        # Inyectamos las rutas del dashboard personalizado dentro del contexto de Exam
        custom_urls = [
            path('management/', include('assessment_v2.admin_urls')),
        ]
        return custom_urls + urls

    list_display = ('uuid_short', 'user', 'archetype_id', 'status_badge', 'created_at')
    list_filter = ('status', 'archetype_id', 'created_at')
    search_fields = ('uuid', 'user__username')
    readonly_fields = ('uuid', 'created_at', 'updated_at')

    @admin.display(description="UUID")
    def uuid_short(self, obj):
        return str(obj.uuid)[:8]

    @admin.display(description="Estado", ordering="status")
    def status_badge(self, obj):
        colors = {
            'PENDING': "#fd7e14",
            'GENERATING': "#007bff",
            'READY': "#28a745",
            'GRADED': "#20c997",
            'ERROR': "#dc3545",
        }
        color = colors.get(obj.status, "#6c757d")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 10px; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'daily_exam_limit', 'monthly_price', 'is_active')

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'is_active', 'end_date')
    search_fields = ('user__username', 'user__email')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('exam', 'final_score', 'passed', 'submitted_at')

@admin.register(TokenUsage)
class TokenUsageAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'input_tokens_total', 'output_tokens_total', 'estimated_cost_usd')

@admin.register(CostLog)
class CostLogAdmin(admin.ModelAdmin):
    list_display = ('operation_type', 'cost_usd', 'timestamp')
