from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class PushTestForm(forms.Form):
    """
    Form to send a test push notification to a specific user.
    """

    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True).order_by("username"),
        label="Seleccionar Usuario",
        help_text="Elige el usuario que recibirá la notificación.",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    title = forms.CharField(
        label="Título de la Notificación",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Título que aparecerá en la notificación",
            }
        ),
    )
    body = forms.CharField(
        label="Cuerpo del Mensaje",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Texto principal del mensaje push.",
            }
        ),
    )
