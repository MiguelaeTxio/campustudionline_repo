# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/orchestrator/forms.py
from django import forms
from django.urls import reverse_lazy
from .models import AutomationSettings, PendingContentTask, FreeContentRequest
from academic_structure.models import Branch, Degree
from contents.models import FreeContentMasterCategory, FreeContentSubCategory

class SeedFiltersForm(forms.ModelForm):
    seed_year = forms.ChoiceField(required=False, label="Año Académico", choices=[("", "---------")])
    class Meta:
        model = AutomationSettings
        fields = ['seed_branch', 'seed_degree', 'seed_year']
        labels = {'seed_branch': "Rama Académica", 'seed_degree': "Grado/Titulación"}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Lógica de inicialización omitida por brevedad...

class FreeCourseCreationForm(forms.Form):
    course_title = forms.CharField(label="Título del Curso", required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    prompt_text = forms.CharField(label="Descripción Detallada / Prompt", required=True, widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}))
    master_category = forms.ModelChoiceField(queryset=FreeContentMasterCategory.objects.all(), label="Categoría Maestra (Nivel 1)", required=True)
    sub_category = forms.ModelChoiceField(queryset=FreeContentSubCategory.objects.none(), label="Subcategoría (Nivel 2, Opcional)", required=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Lógica de inicialización omitida por brevedad...

class FreeContentRequestForm(forms.ModelForm):
    class Meta:
        model = FreeContentRequest
        fields = ["title", "detailed_prompt"]
        # Widgets y labels omitidos por brevedad...

class RejectionReasonForm(forms.Form):
    rejection_reason = forms.ChoiceField(choices=FreeContentRequest.REJECTION_CHOICES, required=True, label="Motivo del rechazo")

class ReviseTaskForm(forms.ModelForm):
    class Meta:
        model = PendingContentTask
        fields = ["course_title", "prompt_text"]
        # Widgets y labels omitidos por brevedad...
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["course_title"].required = True
        self.fields["prompt_text"].required = True
