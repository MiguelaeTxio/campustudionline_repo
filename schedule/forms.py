from django import forms
from django.utils.translation import gettext_lazy as _
from .models import AcademicEvent

class AcademicEventForm(forms.ModelForm):
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        subject_name = self.cleaned_data.get('subject_name_display')
        if subject_name:
            from academic_structure.models import Subject
            # Buscar coincidencia exacta (ignora mayúsculas)
            subj = Subject.objects.filter(name__iexact=subject_name).first()
            if subj:
                instance.subject = subj
        if commit:
            instance.save()
        return instance

    class Meta:
        model = AcademicEvent
        fields = ['title', 'subject_name_display', 'event_type', 'start_time', 'end_time', 'is_all_day', 'location', 'description']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ej: Examen de Cálculo')}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ej: Aula 304')}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'subject_name_display': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ej: Matemáticas, Yoga, Marketing...')}),
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'is_all_day': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
