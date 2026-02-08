from django.contrib import admin
from .models import SubscriptionPlan, UserSubscription, TokenUsage, CostLog, Exam, Submission

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'daily_exam_limit', 'monthly_price', 'is_active')

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'is_active', 'end_date')
    search_fields = ('user__username', 'user__email')

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'user', 'archetype_id', 'status', 'created_at')
    list_filter = ('status', 'archetype_id', 'created_at')
    search_fields = ('uuid', 'user__username')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('exam', 'final_score', 'passed', 'submitted_at')

@admin.register(TokenUsage)
class TokenUsageAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'input_tokens_total', 'output_tokens_total', 'estimated_cost_usd')

@admin.register(CostLog)
class CostLogAdmin(admin.ModelAdmin):
    list_display = ('operation_type', 'cost_usd', 'timestamp')
