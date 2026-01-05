from django import forms
from django.core.exceptions import ValidationError

LANGUAGES = [
    ('es', 'Español (España)'),
    ('en', 'Inglés (UK/US)'),
    ('fr', 'Francés'),
    ('de', 'Alemán'),
    ('it', 'Italiano'),
    ('pt', 'Portugués'),
    ('zh', 'Chino (Mandarín)'),
    ('ja', 'Japonés'),
    ('ru', 'Ruso'),
    ('ar', 'Árabe'),
]

SOURCE_LANGUAGES = [('auto', 'Detectar Automáticamente')] + LANGUAGES

class TranslationForm(forms.Form):
    source_lang = forms.ChoiceField(
        choices=SOURCE_LANGUAGES,
        label="Idioma de Origen",
        initial='auto',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    target_lang = forms.ChoiceField(
        choices=LANGUAGES,
        label="Idioma de Destino",
        initial='es',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    text_content = forms.CharField(
        required=False,
        widget=forms.HiddenInput(), # Oculto, se llenará vía JS desde el editor personalizado
        label="Texto"
    )
    document = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label="Documento (PDF/DOCX)"
    )
