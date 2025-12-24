from django.contrib import admin
from .models import AcademicEvent

@admin.register(AcademicEvent)
class AcademicEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'event_type', 'start_time', 'end_time', 'subject')
    list_filter = ('event_type', 'start_time', 'user')
    search_fields = ('title', 'description', 'user__username', 'subject__name')
    date_hierarchy = 'start_time'
    autocomplete_fields = ['user', 'subject']
