# /home/MiguelAeTxio/CampuStudiOnline/contents/forms.py
from django import forms
from .models import ContentMaterial, KnowledgeArea, Discipline, MainCategory, Topic, FavoriteFolder

# --- CONSTANTES PARA EL FORMULARIO DINÁMICO ---
NEW_OPTION_ID_VALUE = "create-new"
NEW_OPTION_TEXT = "--- Crear Nueva Entrada ---"
PLACEHOLDER_OPTION_TEXT = "--- Seleccionar ---"

class ContentMaterialForm(forms.ModelForm):
    knowledge_area_form = forms.ModelChoiceField(
        queryset=KnowledgeArea.objects.all().order_by("name"),
        required=False, label="Área de Conocimiento",
        widget=forms.Select(attrs={"class": "form-select form-control category-select"}),
    )
    discipline_form = forms.ModelChoiceField(
        queryset=Discipline.objects.none(), required=False, label="Disciplina",
        widget=forms.Select(attrs={"class": "form-select form-control category-select"}),
    )
    main_category_form = forms.ModelChoiceField(
        queryset=MainCategory.objects.none(), required=False, label="Categoría Principal",
        widget=forms.Select(attrs={"class": "form-select form-control category-select"}),
    )
    topic_form_1 = forms.ModelChoiceField(
        queryset=Topic.objects.none(), required=False, label="Tema (Nivel 1)",
        widget=forms.Select(attrs={"class": "form-select form-control category-select theme-level"}),
    )
    topic_form_2 = forms.ModelChoiceField(
        queryset=Topic.objects.none(), required=False, label="Sub-tema (Nivel 2)",
        widget=forms.Select(attrs={"class": "form-select form-control category-select theme-level"}),
    )
    topic_form_3 = forms.ModelChoiceField(
        queryset=Topic.objects.none(), required=False, label="Sub-tema (Nivel 3)",
        widget=forms.Select(attrs={"class": "form-select form-control category-select theme-level"}),
    )
    topic_form_4 = forms.ModelChoiceField(
        queryset=Topic.objects.none(), required=False, label="Sub-tema (Nivel 4)",
        widget=forms.Select(attrs={"class": "form-select form-control category-select theme-level"}),
    )
    new_topic_form = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control mt-1 new-category-input", "placeholder": "Nuevo Nombre de Tema/Sub-tema"}),
    )
    is_public = forms.ChoiceField(
        choices=[(True, "Público"), (False, "Privado")],
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Visibilidad", initial=True,
    )
    topic = forms.ModelChoiceField(
        queryset=Topic.objects.all(), required=False, widget=forms.HiddenInput()
    )

    class Meta:
        model = ContentMaterial
        fields = ["title", "short_description", "markdown_content", "is_public", "topic"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control form-control-lg"}),
            "short_description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "markdown_content": forms.Textarea(attrs={"class": "form-control", "id": "markdown-editor"}),
        }
        labels = {
            "title": "Título", "short_description": "Descripción Corta",
            "markdown_content": "Contenido",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.topic:
            path = []
            current = self.instance.topic
            while current:
                path.insert(0, current)
                current = current.parent
            if path:
                root_topic = path[0]
                main_category_instance = root_topic.main_category
                discipline = main_category_instance.discipline
                knowledge_area = discipline.knowledge_area
                self.initial["knowledge_area_form"] = knowledge_area.pk
                self.fields["discipline_form"].queryset = Discipline.objects.filter(knowledge_area=knowledge_area).order_by("name")
                self.initial["discipline_form"] = discipline.pk
                self.fields["main_category_form"].queryset = MainCategory.objects.filter(discipline=discipline).order_by("name")
                self.initial["main_category_form"] = main_category_instance.pk
                parent_queryset = Topic.objects.filter(main_category=main_category_instance, parent__isnull=True)
                for i, topic_in_path in enumerate(path, 1):
                    field_name = f"topic_form_{i}"
                    if field_name in self.fields:
                        self.fields[field_name].queryset = parent_queryset.order_by("name")
                        self.initial[field_name] = topic_in_path.pk
                        parent_queryset = Topic.objects.filter(parent=topic_in_path)

    def clean(self):
        cleaned_data = super().clean()
        last_valid_topic = None
        parent_obj_for_new_topic = None
        knowledge_area = self.cleaned_data.get("knowledge_area_form")
        discipline = self.cleaned_data.get("discipline_form")
        main_category = self.cleaned_data.get("main_category_form")
        parent_for_next_level = main_category
        for i in range(1, 5):
            field_name = f"topic_form_{i}"
            selected_topic = self.cleaned_data.get(field_name)
            if selected_topic:
                last_valid_topic = selected_topic
                parent_for_next_level = selected_topic
            else:
                break
        new_topic_name = self.cleaned_data.get("new_topic_form", "").strip()
        if new_topic_name:
            if not parent_for_next_level:
                self.add_error(None, "Selecciona una jerarquía completa antes de crear un nuevo tema.")
                return cleaned_data
            create_kwargs = {"name": new_topic_name}
            if isinstance(parent_for_next_level, MainCategory):
                create_kwargs["main_category"] = parent_for_next_level
            elif isinstance(parent_for_next_level, Topic):
                create_kwargs["parent"] = parent_for_next_level
            last_valid_topic, _ = Topic.objects.get_or_create(**create_kwargs)
        if last_valid_topic:
            cleaned_data["topic"] = last_valid_topic
        elif main_category:
            self.add_error(None, "La jerarquía está incompleta. Debes seleccionar o crear al menos un tema.")
        else:
            general_knowledge_area, _ = KnowledgeArea.objects.get_or_create(name="General")
            general_discipline, _ = Discipline.objects.get_or_create(name="General", knowledge_area=general_knowledge_area)
            general_category, _ = MainCategory.objects.get_or_create(name="General", discipline=general_discipline)
            general_topic, _ = Topic.objects.get_or_create(name="General", main_category=general_category)
            cleaned_data["topic"] = general_topic
        return cleaned_data

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
