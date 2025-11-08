# chat/forms.py
from django import forms
from .models import ChatRoom


class ChatRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = [
            "name",
            "description",
            "is_private",
        ]  # Campos que el usuario podrá rellenar
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej: Discusión General de Python",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Opcional: Describe brevemente el propósito de la sala",
                }
            ),
            "is_private": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "name": "Nombre de la Sala",
            "description": "Descripción (opcional)",
            "is_private": "¿Marcar como Sala Privada?",
        }
        help_texts = {
            "name": "El nombre debe ser único y descriptivo.",
            "is_private": "Las salas privadas no aparecerán en la lista pública general y requerirán gestión de miembros (funcionalidad futura).",
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        # Verificamos si ya existe una sala con ese nombre (ignorando mayúsculas/minúsculas para ser más amigable)
        # El modelo ya tiene unique=True, pero esta validación da un error más amigable en el formulario.
        if ChatRoom.objects.filter(name__iexact=name).exists():
            # Si estamos editando una sala existente, permitimos el mismo nombre
            if not self.instance or self.instance.name.lower() != name.lower():
                raise forms.ValidationError(
                    "Ya existe una sala con este nombre. Por favor, elige otro."
                )
        return name
