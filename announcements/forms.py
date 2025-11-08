"""
Forms for the Announcements application.
"""
from django import forms
from .models import Announcement


class AnnouncementForm(forms.ModelForm):
    """
    Form for creating and editing Announcements.
    """

    class Meta:
        model = Announcement
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Título breve y descriptivo",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Escribe aquí los detalles del anuncio...",
                }
            ),
        }
        labels = {
            "title": "Título del Anuncio",
            "content": "Descripción Completa del Anuncio",
        }
        help_texts = {
            "title": "Máximo 200 caracteres.",
            "content": "Detalla la información que quieres compartir.",
        }
