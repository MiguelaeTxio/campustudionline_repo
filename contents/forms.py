# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/contents/forms.py
from django import forms
from .models import ContentMaterial, FavoriteFolder

# --- CONSTANTES PARA EL FORMULARIO DINÁMICO ---
class ContentMaterialForm(forms.ModelForm):
    is_public = forms.ChoiceField(
        choices=[(True, "Público"), (False, "Privado")],
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Visibilidad", initial=True,
    )

    class Meta:
        model = ContentMaterial
        fields = ["title", "short_description", "markdown_content", "is_public"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control form-control-lg"}),
            "short_description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "markdown_content": forms.Textarea(attrs={"class": "form-control", "id": "markdown-editor"}),
        }
        labels = {
            "title": "Título", "short_description": "Descripción Corta",
            "markdown_content": "Contenido",
        }

class FavoriteFolderForm(forms.ModelForm):
    class Meta:
        model = FavoriteFolder
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la nueva carpeta'}),
        }
        labels = {
            'name': 'Nombre de la Carpeta',
        }
