# /home/MiguelAeTxio/CampuStudiOnline/content_automation/forms.py
# El namespace de la app es 'content_automation'

from django import forms
from django.urls import reverse_lazy
from .models import PendingContentTask, FreeContentRequest, AutomationSettings
from academic_structure.models import Branch, Degree
from contents.models import FreeContentMasterCategory, FreeContentSubCategory


class SeedFiltersForm(forms.ModelForm):
    """
    [REFACTORIZADO V2] Formulario "inteligente" para configurar las semillas de generación.
    Se define `seed_year` explícitamente como ChoiceField para asegurar el widget correcto.
    """
    seed_year = forms.ChoiceField(
        required=False,
        label="Año Académico",
        choices=[("", "---------")] # Se poblará dinámicamente
    )
    
    class Meta:
        model = AutomationSettings
        fields = ['seed_branch', 'seed_degree', 'seed_year']
        labels = {
            'seed_branch': "Rama Académica",
            'seed_degree': "Grado/Titulación",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # URLs para los endpoints de HTMX
        get_filters_url = reverse_lazy('admin:content_automation:get_academic_filters')

        # Configurar widgets con atributos de clase y HTMX
        self.fields['seed_branch'].widget.attrs.update({
            'class': 'form-control',
            'hx-get': get_filters_url,
            'hx-target': '#id_seed_degree',
            'hx-trigger': 'change',
            'hx-indicator': '.htmx-indicator'
        })
        self.fields['seed_degree'].widget.attrs.update({
            'class': 'form-control',
            'hx-get': get_filters_url,
            'hx-target': '#id_seed_year',
            'hx-trigger': 'change',
            'hx-indicator': '.htmx-indicator'
        })
        self.fields['seed_year'].widget.attrs.update({'class': 'form-control'})
        
        # Lógica para poblar los campos dependientes
        if self.instance and self.instance.seed_branch:
            self.fields['seed_degree'].queryset = Degree.objects.filter(
                branch=self.instance.seed_branch
            ).order_by('name')
        else:
            self.fields['seed_degree'].queryset = Degree.objects.none()

        if self.instance and self.instance.seed_degree:
            try:
                duration = self.instance.seed_degree.duration_in_years
                year_map = {1: "Primero", 2: "Segundo", 3: "Tercero", 4: "Cuarto", 5: "Quinto"}
                year_choices = [("", "---------")] + [(year_map.get(y), year_map.get(y)) for y in range(1, duration + 1) if y in year_map]
                self.fields['seed_year'].choices = year_choices
            except (TypeError, ValueError):
                self.fields['seed_year'].choices = [("", "---------")]
        else:
            self.fields['seed_year'].choices = [("", "---------")]

        # Si hay datos en el POST, asegurar que los querysets son correctos para la validación
        if 'seed_branch' in self.data:
            try:
                branch_id = int(self.data.get('seed_branch'))
                self.fields['seed_degree'].queryset = Degree.objects.filter(branch_id=branch_id).order_by('name')
            except (ValueError, TypeError):
                pass
        
        if 'seed_degree' in self.data:
            try:
                degree_id = int(self.data.get('seed_degree'))
                degree = Degree.objects.get(pk=degree_id)
                duration = degree.duration_in_years
                year_map = {1: "Primero", 2: "Segundo", 3: "Tercero", 4: "Cuarto", 5: "Quinto"}
                year_choices = [("", "---------")] + [(year_map.get(y), year_map.get(y)) for y in range(1, duration + 1) if y in year_map]
                self.fields['seed_year'].choices = year_choices
            except (ValueError, TypeError, Degree.DoesNotExist):
                pass


class FreeCourseCreationForm(forms.Form):
    """
    [REFACTORIZADO] Formulario de servicio para la creación de cursos libres.
    Recopila toda la información necesaria, incluida la nueva jerarquía.
    """
    course_title = forms.CharField(
        label="Título del Curso",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: Introducción a la Física Cuántica"}),
        help_text="El título que tendrá el material de contenido final."
    )
    prompt_text = forms.CharField(
        label="Descripción Detallada / Prompt",
        required=True,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Describe en detalle el tema, los puntos clave a cubrir, el público objetivo..."}),
        help_text="Una descripción clara y detallada produce mejores resultados."
    )
    master_category = forms.ModelChoiceField(
        queryset=FreeContentMasterCategory.objects.all().order_by('display_order', 'name'),
        label="Categoría Maestra (Nivel 1)",
        required=True,
        help_text="Selecciona la categoría principal para clasificar este contenido."
    )
    sub_category = forms.ModelChoiceField(
        queryset=FreeContentSubCategory.objects.none(),
        label="Subcategoría (Nivel 2, Opcional)",
        required=False,
        help_text="Selecciona la subcategoría específica si aplica."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configuración de atributos HTMX para la carga dinámica
        get_subcategories_url = reverse_lazy('admin:content_automation:get_sub_categories_for_master')
        self.fields['master_category'].widget.attrs.update({
            'hx-get': get_subcategories_url,
            'hx-target': '#subcategory-selector-container',
            'hx-trigger': 'change',
            'hx-indicator': '.htmx-indicator',
        })

        # Lógica para poblar el queryset de subcategorías dinámicamente
        if 'master_category' in self.data:
            try:
                master_id = self.data.get('master_category')
                self.fields['sub_category'].queryset = FreeContentSubCategory.objects.filter(
                    master_category_id=master_id
                ).order_by('display_order', 'name')
            except (ValueError, TypeError):
                pass # El queryset permanecerá vacío si el ID no es válido


class FreeContentRequestForm(forms.ModelForm):
    """
    Formulario para que los usuarios soliciten la creación de contenido libre.
    """
    class Meta:
        model = FreeContentRequest
        fields = ["title", "detailed_prompt"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej: Un curso sobre la historia de la computación",
                }
            ),
            "detailed_prompt": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Describe qué temas te gustaría que se trataran, el nivel de profundidad (introductorio, avanzado), y cualquier otro detalle que consideres importante.",
                }
            ),
        }
        labels = {
            "title": "Título Sugerido para el Contenido",
            "detailed_prompt": "Descripción de tu Solicitud",
        }
        help_texts = {
            "title": "Un título claro nos ayuda a entender tu idea.",
            "detailed_prompt": "Cuanto más detallada sea tu descripción, mejor podremos evaluar tu solicitud.",
        }

class RejectionReasonForm(forms.Form):
    """
    Formulario para que los administradores seleccionen un motivo al rechazar
    una solicitud de contenido libre, tanto para acciones individuales como en lote.
    """
    rejection_reason = forms.ChoiceField(
        choices=FreeContentRequest.REJECTION_CHOICES,
        required=True,
        label="Motivo del rechazo",
        widget=forms.Select(attrs={"class": "form-control"})
    )

class ReviseTaskForm(forms.ModelForm):
    """
    Formulario para la revisión y corrección de una tarea de generación de contenido
    existente antes de re-encolarla.
    """

    class Meta:
        model = PendingContentTask
        fields = ["course_title", "prompt_text"]
        widgets = {
            "course_title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej: Introducción a la Física Cuántica",
                }
            ),
            "prompt_text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 10,
                    "placeholder": "Revisa y corrige el prompt original. Una descripción clara y detallada produce mejores resultados.",
                }
            ),
        }
        labels = {
            "course_title": "Título del Curso",
            "prompt_text": "Descripción Detallada / Prompt (Corregido)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["course_title"].required = True
        self.fields["prompt_text"].required = True
