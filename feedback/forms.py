from django import forms
from .models import FeedbackReport

class FeedbackReportForm(forms.ModelForm):
    class Meta:
        model = FeedbackReport
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Resumen breve del problema'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe el error o sugerencia con detalle...'}),
        }
