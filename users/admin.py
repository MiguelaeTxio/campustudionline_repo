# /users/admin.py
# ATENCIÓN!!! La aplicación de users se llama 'users' pero el Namespace a usar es 'users'.
# ATENCIÓN!!! La aplicación de users se llama 'users' pero el Namespace a usar es 'users'.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, UserProfile, ArchivedKey, RecommendationCode

# Ya no necesitamos importar 'User' ni des-registrarlo.


class UserProfileInline(admin.StackedInline):
    fk_name = "user"
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Perfil Adicional"
    # El resto de tu inline se mantiene igual, lo incluimos para que sea completo
    fieldsets = (
        (
            "Información Personal Adicional",
            {"fields": ("phone", "degree", "current_year", "university")},
        ),
        (
            "Datos para el Portafolio",
            {
                "fields": (
                    "public_personal_description",
                    "professional_title",
                    "hobbies",
                    "work_experience",
                )
            },
        ),
        (
            "Criptografía (E2EE)",
            {
                "fields": (
                    "public_key",
                    "encrypted_private_key",
                    "encryption_salt",
                )
            },
        ),
        (
            "Configuración de Privacidad del Portafolio",
            {
                "classes": ("collapse",),
                "fields": (
                    "show_phone_in_portfolio",
                    "show_degree_in_portfolio",
                    "show_current_year_in_portfolio",
                    "show_university_in_portfolio",
                    "show_hobbies_in_portfolio",
                    "show_work_experience_in_portfolio",
                    "show_personal_description_in_portfolio",
                    "show_professional_title_in_portfolio",
                    "show_short_messages_in_portfolio",
                    "show_user_links_in_portfolio",
                    "show_chat_rooms_in_portfolio",
                ),
            },
        ),
        ("Seguimiento de Actividad", {"fields": ("last_checked_chat_activity",)}),
        (
            "Preferencias de Comunicación",
            {"fields": ("accepts_marketing",)},
        ),
        (
            "Sistema de Atribución y Referidos",
            {
                "classes": ("collapse",),
                "fields": (
                    "referred_by",
                    "has_claimed_copy_incentive",
                    "has_claimed_assessment_incentive",
                ),
            },
        ),
    )
    readonly_fields = (
        "profile_created_at",
        "profile_updated_at",
        "last_checked_chat_activity",
    )


# Usamos el decorador @admin.register, que es la forma moderna y limpia de registrar.
@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]  # Añadimos el profile para editarlo junto al user
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "get_phone_profile",
        "get_last_checked_chat",
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = BaseUserAdmin.list_filter + ("userprofile__accepts_marketing",)

    @admin.display(description="Teléfono (Perfil)")
    def get_phone_profile(self, instance):
        # Usamos un try-except que es más robusto que hasattr
        try:
            return instance.userprofile.phone
        except UserProfile.DoesNotExist:
            return None

    @admin.display(
        description="Última Rev. Chat (Perfil)",
        ordering="userprofile__last_checked_chat_activity",
    )
    def get_last_checked_chat(self, instance):
        try:
            if instance.userprofile.last_checked_chat_activity:
                return instance.userprofile.last_checked_chat_activity.strftime(
                    "%Y-%m-%d %H:%M"
                )
        except UserProfile.DoesNotExist:
            return None
        return None


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "phone",
        "accepts_marketing",
        "show_chat_rooms_in_portfolio",
        "last_checked_chat_activity",
    )
    list_display_links = ("user",)
    search_fields = ("user__username", "phone")
    list_filter = (
        "accepts_marketing",
        "show_chat_rooms_in_portfolio",
        "profile_created_at",
        "profile_updated_at",
    )
    readonly_fields = (
        "profile_created_at",
        "profile_updated_at",
        "last_checked_chat_activity",
    )
    autocomplete_fields = ("user",)
    fieldsets = (
        (None, {"fields": ("user",)}),
        (
            "Información de Contacto y Perfil",
            {
                "fields": (
                    "phone",
                    "degree",
                    "current_year",
                    "university",
                    "hobbies",
                    "work_experience",
                )
            },
        ),
        (
            "Datos para el Portafolio Público",
            {"fields": ("public_personal_description", "professional_title")},
        ),
        (
            "Criptografía (E2EE)",
            {
                "fields": (
                    "public_key",
                    "encrypted_private_key",
                    "encryption_salt",
                )
            },
        ),
        (
            "Configuración de Privacidad del Portafolio",
            {
                "classes": ("collapse",),
                "fields": (
                    "show_phone_in_portfolio",
                    "show_degree_in_portfolio",
                    "show_current_year_in_portfolio",
                    "show_university_in_portfolio",
                    "show_hobbies_in_portfolio",
                    "show_work_experience_in_portfolio",
                    "show_personal_description_in_portfolio",
                    "show_professional_title_in_portfolio",
                    "show_short_messages_in_portfolio",
                    "show_user_links_in_portfolio",
                    "show_chat_rooms_in_portfolio",
                ),
            },
        ),
        (
            "Preferencias de Comunicación",
            {"fields": ("accepts_marketing",)},
        ),
        (
            "Seguimiento y Timestamps",
            {
                "fields": (
                    "last_checked_chat_activity",
                    "profile_created_at",
                    "profile_updated_at",
                )
            },
        ),
        (
            "Sistema de Atribución y Referidos",
            {
                "classes": ("collapse",),
                "fields": (
                    "referred_by",
                    "has_claimed_copy_incentive",
                    "has_claimed_assessment_incentive",
                ),
            },
        ),
    )


@admin.register(ArchivedKey)
class ArchivedKeyAdmin(admin.ModelAdmin):
    list_display = ("profile", "archived_at")
    search_fields = ("profile__user__username",)
    list_filter = ("archived_at",)
    readonly_fields = ("profile", "encrypted_private_key", "archived_at")


@admin.register(RecommendationCode)
class RecommendationCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "vendor", "get_status", "redeemed_by", "date_redeemed")
    list_filter = ("vendor", "date_redeemed") # Eliminamos 'is_used'
    search_fields = ("code", "vendor__username", "vendor__email", "redeemed_by__username")
    autocomplete_fields = ("vendor", "redeemed_by")
    readonly_fields = ("date_redeemed",)

    @admin.display(description='Estado', ordering='redeemed_by')
    def get_status(self, obj):
        return "USADO" if obj.redeemed_by else "DISPONIBLE"
