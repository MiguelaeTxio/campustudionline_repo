# /home/MiguelAeTxio/CampuStudiOnline/delivery_note_processor/admin.py
from django.contrib import admin
from .models import Vehicle, DeliveryNote

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('code', 'license_plate', 'vehicle_type')
    search_fields = ('code', 'license_plate')
    list_per_page = 25

@admin.register(DeliveryNote)
class DeliveryNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle', 'status', 'uploaded_at', 'processed_at')
    list_filter = ('status', 'vehicle')
    search_fields = ('id', 'vehicle__code', 'vehicle__license_plate')
    readonly_fields = (
        'uploaded_at',
        'processed_at',
        'processed_data',
        'original_image'
    )
    list_per_page = 25
    date_hierarchy = 'uploaded_at'
