from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html  # For creating safe HTML links
from .models import MaintenanceSettings
from . import (
    admin_views,
)  # Assuming your view is in global_settings/admin_views.py


@admin.register(MaintenanceSettings)
class MaintenanceSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "maintenance_mode_active",
        "admin_actions",
    )  # Add admin_actions to the list view

    # Do not allow adding new instances if one already exists (Singleton)
    def has_add_permission(self, request):
        return not MaintenanceSettings.objects.exists()

    # Do not allow deleting the single instance
    def has_delete_permission(self, request, obj=None):
        return False

    # Override get_urls to add our custom URL for the email sending view
    def get_urls(self):
        urls = super().get_urls()  # Get the standard ModelAdmin URLs

        # Define the URL for our email sending view
        # The URL will be relative to the base URL of this ModelAdmin in the admin.
        # Ex: /admin/global_settings/maintenancesettings/send-email/
        custom_urls = [
            path(
                "send-email/",  # The part of the URL we are adding
                self.admin_site.admin_view(
                    admin_views.send_custom_email_view
                ),  # Wrap the view with admin_view
                name="global_settings_send_custom_email",  # Unique name for this URL (useful for reverse)
            )
        ]
        return (
            custom_urls + urls
        )  # Add our custom URLs to the existing ones

    # Method to display a link in the admin list view
    def admin_actions(self, obj):
        # 'obj' is the MaintenanceSettings instance, although we don't use it directly for this general link.
        # We create the URL to our custom view using 'reverse'.
        # The format 'admin:app_label_modelname_action' is common, but here we use the name we gave it in get_urls.
        # To be more robust, we use the full name 'admin:global_settings_send_custom_email'.

        # Build the URL using the 'admin' namespace and the name we gave the URL in get_urls
        url = reverse("admin:global_settings_send_custom_email")
        return format_html(
            '<a class="button" href="{}">Enviar Correo a Usuarios</a>', url
        )

    admin_actions.short_description = (
        "Acciones de Correo"  # Title of the column in the admin
    )
    admin_actions.allow_tags = True  # Necessary for format_html to work in older versions
