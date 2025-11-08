# /home/MiguelAeTxio/CampuStudiOnline/contents/study_room_forms.py
"""
Formularios para la funcionalidad de Sala de Estudio.
"""
from django import forms
from .models import ContentCopy, Annotation


class ContentCopyForm(forms.ModelForm):
    """
    Formulario para crear o editar una copia personalizada de contenido.
    """
    class Meta:
        model = ContentCopy
        fields = ["html_content", "is_public"]
        widgets = {
            "html_content": forms.HiddenInput(),
            "is_public": forms.CheckboxInput(
                attrs={"class": "form-check-input", "id": "id_is_public"}
            ),
        }
        labels = {
            "is_public": "¿Hacer esta copia pública?",
        }
        help_texts = {
            "is_public": "Si marcas esta opción, tu copia con anotaciones será visible para todos los usuarios.",
        }


class AnnotationForm(forms.ModelForm):
    """
    Formulario para crear o editar una anotación.
    Este formulario se utiliza principalmente a través de AJAX.
    """
    class Meta:
        model = Annotation
        fields = ["annotation_type", "content", "position", "color"]
        widgets = {
            "annotation_type": forms.Select(attrs={"class": "form-select", "id": "id_annotation_type"}),
            "content": forms.Textarea(
                attrs={"class": "form-control", "id": "id_content", "rows": 3}
            ),
            "position": forms.HiddenInput(),
            "color": forms.TextInput(
                attrs={"class": "form-control", "id": "id_color", "type": "color"}
            ),
        }
