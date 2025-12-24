from django import forms
from django.utils.translation import gettext_lazy as _
from .models import AcademicEvent

class AcademicEventForm(forms.ModelForm):
    class Meta:
        model = AcademicEvent
        fields = ['title', 'subject', 'event_type', 'start_time', 'end_time', 'is_all_day', 'location', 'description']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ej: Examen de Cálculo')}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ej: Aula 304')}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'is_all_day': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
