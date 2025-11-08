from django import forms
from .models import ShortMessage, UserLink
from users.models import UserProfile
from django.utils.translation import gettext_lazy as _


class ShortMessageForm(forms.ModelForm):
    class Meta:
        model = ShortMessage
        fields = ["content", "is_public"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Escribe tu mensaje corto aquí (máx. 500 caracteres si tienes un validador en el modelo)...",
                }
            ),
            "is_public": forms.CheckboxInput(),
        }
        labels = {
            "content": "Tu mensaje",
            "is_public": "¿Hacer este mensaje público en tu portafolio?",
        }
        help_texts = {
            "content": "Este mensaje se mostrará en tu portafolio si lo marcas como público y tienes activada la opción de mostrar mensajes cortos.",
            "is_public": "Si no está marcado, el mensaje no será visible para otros en tu portafolio público (funcionalidad futura podría permitirte verlo en privado).",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].widget.attrs.update(
            {"class": "form-control mb-2"}
        )
        self.fields["is_public"].widget.attrs.update(
            {"class": "form-check-input"}
        )


class UserLinkForm(forms.ModelForm):
    class Meta:
        model = UserLink
        fields = [
            "title",
            "url",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Ej: Mi perfil de GitHub, Blog Personal, LinkedIn..."
                }
            ),
            "url": forms.URLInput(
                attrs={"placeholder": "https://www.ejemplo.com/tu_enlace"}
            ),
        }
        labels = {
            "title": "Título del enlace",
            "url": "URL completa del enlace",
        }
        help_texts = {
            "title": "Un nombre descriptivo para tu enlace.",
            "url": "Asegúrate de incluir http:// o https:// al principio de la URL.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control mb-2"})
        self.fields["url"].widget.attrs.update({"class": "form-control"})


class UserProfileChatPrivacyForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["show_chat_rooms_in_portfolio"]
        labels = {
            "show_chat_rooms_in_portfolio": _(
                "Mostrar mi directorio de salas de chat en mi portafolio público"
            )
        }
        widgets = {
            "show_chat_rooms_in_portfolio": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }
        help_texts = {
            "show_chat_rooms_in_portfolio": _(
                "Si marcas esta opción, otros usuarios podrán ver a qué salas de chat perteneces desde tu portafolio. "
                "Si no la marcas, esta información será privada."
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
