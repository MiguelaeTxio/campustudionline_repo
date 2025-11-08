# /home/MiguelAeTxio/CampuStudiOnline/delivery_note_processor/forms.py
from django import forms
from .models import DeliveryNote, Vehicle

class DeliveryNoteUploadForm(forms.ModelForm):
    """
    Formulario para la subida de la imagen de un albarán.
    """
    class Meta:
        model = DeliveryNote
        fields = ['original_image']
        labels = {
            'original_image': 'Archivo del Albarán',
        }
        widgets = {
            'original_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/png, image/jpeg',
            })
        }
        help_texts = {
            'original_image': 'Por favor, sube una imagen clara y legible (PNG o JPG).',
        }


class VehicleResolutionForm(forms.ModelForm):
    """
    Formulario para crear un nuevo vehículo cuando el código extraído
    por la IA no se encuentra en la base de datos.
    """
    class Meta:
        model = Vehicle
        fields = ['code', 'license_plate', 'vehicle_type']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'license_plate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1234 ABC'}),
            'vehicle_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Furgoneta Renault'}),
        }

    def __init__(self, *args, **kwargs):
        extracted_code = kwargs.pop('extracted_code', None)
        super().__init__(*args, **kwargs)
        if extracted_code:
            self.fields['code'].initial = extracted_code


