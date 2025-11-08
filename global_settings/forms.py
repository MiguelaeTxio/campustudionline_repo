from django import forms

# --- START OF MODIFICATION ---
# We no longer import 'User' directly. Instead, we use the 'get_user_model' function.
from django.contrib.auth import get_user_model

# This function returns the active user model from settings.py (in our case, users.CustomUser)
# We assign it to the 'User' variable so we don't have to change the rest of the code.
User = get_user_model()
# --- END OF MODIFICATION ---

TEMPLATE_CHOICES = [
    ("admin_manual_welcome", "Bienvenida Manual"),
    ("admin_service_outage", "Aviso de Mantenimiento Programado"),
    ("admin_general_announcement", "Anuncio General"),
]

USER_SELECTION_CHOICES = [
    ("all", "Todos los usuarios activos"),
    ("selected", "Usuarios seleccionados manualmente"),
]


class AdminEmailForm(forms.Form):
    user_selection_type = forms.ChoiceField(
        choices=USER_SELECTION_CHOICES,
        label="Enviar a:",
        widget=forms.RadioSelect,
        initial="selected",
    )
    # This queryset now correctly points to the CustomUser model.
    selected_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_active=True).order_by("username"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Usuarios Específicos (si se eligió arriba)",
    )
    email_template = forms.ChoiceField(
        choices=TEMPLATE_CHOICES, label="Plantilla de Correo"
    )
    asunto = forms.CharField(
        max_length=200,
        label="Asunto del Correo",
        required=False,
        help_text="Requerido para 'Anuncio General' y 'Aviso de Mantenimiento'.",
    )

    fecha_hora_mantenimiento = forms.CharField(
        max_length=100,
        required=False,
        label="Fecha y Hora del Mantenimiento",
        help_text="Ej: Lunes 15 de Mayo a las 23:00 CET",
    )
    duracion_mantenimiento = forms.CharField(
        max_length=100,
        required=False,
        label="Duración Estimada",
        help_text="Ej: 2 horas",
    )
    mensaje_adicional_mantenimiento = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
        label="Mensaje Adicional (Mantenimiento)",
        help_text="Información extra sobre el mantenimiento.",
    )

    cuerpo_mensaje_general = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 10}),
        required=False,
        label="Cuerpo del Mensaje (Anuncio General)",
    )

    def clean(self):
        cleaned_data = super().clean()
        user_selection_type = cleaned_data.get("user_selection_type")
        selected_users = cleaned_data.get("selected_users")
        email_template = cleaned_data.get("email_template")
        asunto = cleaned_data.get("asunto")

        if user_selection_type == "selected" and not selected_users:
            self.add_error(
                "selected_users",
                "Debes seleccionar al menos un usuario si eliges 'Usuarios seleccionados manualmente'.",
            )

        if (
            email_template in ["admin_service_outage", "admin_general_announcement"]
            and not asunto
        ):
            self.add_error(
                "asunto", "Este campo es obligatorio para la plantilla seleccionada."
            )

        if email_template == "admin_service_outage":
            if not cleaned_data.get("fecha_hora_mantenimiento"):
                self.add_error(
                    "fecha_hora_mantenimiento",
                    "Este campo es requerido para el aviso de mantenimiento.",
                )
            if not cleaned_data.get("duracion_mantenimiento"):
                self.add_error(
                    "duracion_mantenimiento",
                    "Este campo es requerido para el aviso de mantenimiento.",
                )

        if email_template == "admin_general_announcement":
            if not cleaned_data.get("cuerpo_mensaje_general"):
                self.add_error(
                    "cuerpo_mensaje_general",
                    "El cuerpo del mensaje es requerido para un anuncio general.",
                )

        return cleaned_data
