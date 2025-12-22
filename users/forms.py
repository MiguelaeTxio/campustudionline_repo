# /users/forms.py
from django.utils.safestring import mark_safe
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import UserProfile, RecommendationCode
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.utils.translation import gettext_lazy as _


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label=_("Correo electrónico"),
        help_text=_(
            "Requerido. Se utilizará para notificaciones y recuperación de cuenta."
        ),
    )
    email2 = forms.EmailField(
        required=True, label=_("Confirmar correo electrónico")
    )
    terms_accepted = forms.BooleanField(
        required=True,
        label=mark_safe('He leído y acepto el <a href="/core/legal/aviso-legal/" target="_blank">Aviso Legal</a> y la <a href="/core/legal/privacidad/" target="_blank">Política de Privacidad</a>.'),
        error_messages={'required': _("Debes aceptar los términos y condiciones para registrarte.")}
    )
    first_name = forms.CharField(required=False, label=_("Nombre (opcional)"))
    last_name = forms.CharField(required=False, label=_("Apellidos (opcional)"))
    
    referral_code = forms.CharField(
        required=False,
        label=_("Código de Invitación (Opcional)"),
        max_length=4,
        help_text=_("Si tienes un código de 4 dígitos de un representante, introdúcelo aquí."),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: A4K7'})
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, label="")

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.CheckboxInput, ReCaptchaV2Checkbox)):
                continue

            css_classes = "form-control"

            if field_name in ["password1", "password2"]:
                css_classes += " password-toggle-field"

            field.widget.attrs.update({"class": css_classes})

        if "password2" in self.fields:
            self.fields["password2"].label = _("Confirmación de contraseña")
            self.fields["password2"].help_text = _(
                "Introduce la misma contraseña que antes, para verificación."
            )

    def clean(self):
        cleaned_data = super().clean()
        email1 = cleaned_data.get("email")
        email2 = cleaned_data.get("email2")

        if email1 and email2 and email1 != email2:
            self.add_error(
                "email2",
                _("Las direcciones de correo electrónico no coinciden."),
            )

        return cleaned_data

    def clean_referral_code(self):
        code = self.cleaned_data.get("referral_code")
        if code:
            code = code.strip().upper()
            try:
                rec_code = RecommendationCode.objects.get(code=code)
                if rec_code.redeemed_by:
                    raise forms.ValidationError(_("Este código de invitación ya ha sido utilizado."))
            except RecommendationCode.DoesNotExist:
                raise forms.ValidationError(_("El código de invitación no es válido."))
            return code
        return None

    def clean_username(self):
        username = self.cleaned_data.get("username")
        User = get_user_model()

        if not username:
            return username

        existing_user = User.objects.filter(username__iexact=username).first()

        if existing_user:
            if existing_user.is_active:
                raise forms.ValidationError(
                    _("Este nombre de usuario ya está en uso. Por favor, elige otro.")
                )
            else:
                raise forms.ValidationError(
                    _(
                        "Este nombre de usuario ya está registrado. Si te pertenece, por favor, utiliza el correo electrónico asociado a la cuenta para continuar."
                    )
                )

        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        User = get_user_model()

        if not email:
            return email

        existing_user = User.objects.filter(email__iexact=email).first()

        if existing_user:
            if existing_user.is_active:
                raise forms.ValidationError(
                    _(
                        "Esta dirección de correo electrónico ya está registrada. Por favor, utiliza otra."
                    )
                )
            else:
                raise forms.ValidationError(
                    _("Cuenta inactiva detectada."), code="inactive_account"
                )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get("email", "")
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        if commit:
            user.save()
            UserProfile.objects.get_or_create(user=user)
        return user


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(label=_("Correo electrónico"), required=True)

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "first_name", "last_name")
        labels = {
            "username": _("Nombre de usuario"),
            "first_name": _("Nombre"),
            "last_name": _("Apellidos"),
        }
        help_texts = {
            "username": None,
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_email(self):
        current_email = self.cleaned_data.get("email")
        User = get_user_model()
        if (
            current_email
            and User.objects.filter(email__iexact=current_email)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError(
                _(
                    "Esta dirección de correo electrónico ya está en uso por otro usuario."
                )
            )
        return current_email


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "phone",
            "degree",
            "current_year",
            "university",
            "hobbies",
            "work_experience",
            "public_personal_description",
            "professional_title",
            "show_phone_in_portfolio",
            "show_degree_in_portfolio",
            "show_current_year_in_portfolio",
            "show_university_in_portfolio",
            "show_hobbies_in_portfolio",
            "show_work_experience_in_portfolio",
            "show_chat_rooms_in_portfolio",
            "show_personal_description_in_portfolio",
            "show_professional_title_in_portfolio",
            "show_short_messages_in_portfolio",
            "show_user_links_in_portfolio",
        ]
        widgets = {
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Tu número de teléfono"),
                }
            ),
            "degree": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Ej: Ingeniería Informática"),
                }
            ),
            "current_year": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Ej: 3º Grado, Máster en IA"),
                }
            ),
            "university": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Nombre de tu universidad"),
                }
            ),
            "hobbies": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": _(
                        "Describe brevemente tus gustos o áreas de interés"
                    ),
                }
            ),
            "work_experience": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": _(
                        "Describe brevemente tu experiencia laboral relevante"
                    ),
                }
            ),
            "public_personal_description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": _(
                        "Escribe aquí una breve descripción sobre ti para tu portafolio."
                    ),
                }
            ),
            "professional_title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Ej: Desarrollador Python | Entusiasta de la IA"),
                }
            ),
            "show_phone_in_portfolio": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "show_degree_in_portfolio": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "show_current_year_in_portfolio": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "show_university_in_portfolio": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "show_hobbies_in_portfolio": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "show_work_experience_in_portfolio": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "show_chat_rooms_in_portfolio": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "show_personal_description_in_portfolio": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "show_professional_title_in_portfolio": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "show_short_messages_in_portfolio": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "show_user_links_in_portfolio": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }
        labels = {
            "phone": _("Número de teléfono"),
            "degree": _("Carrera o Estudios Principales"),
            "current_year": _("Curso o Año Actual"),
            "university": _("Universidad o Centro de Estudios"),
            "hobbies": _("Describe tus gustos e intereses"),
            "work_experience": _("Describe tu experiencia laboral relevante"),
            "public_personal_description": _(
                "Descripción Personal (para el portafolio)"
            ),
            "professional_title": _(
                "Tu Título Profesional o Headline (para el portafolio)"
            ),
            "show_phone_in_portfolio": _(
                "Mostrar mi teléfono en el portafolio público."
            ),
            "show_degree_in_portfolio": _(
                "Mostrar mi carrera en el portafolio público."
            ),
            "show_current_year_in_portfolio": _(
                "Mostrar mi curso actual en el portafolio público."
            ),
            "show_university_in_portfolio": _(
                "Mostrar mi universidad en el portafolio público."
            ),
            "show_hobbies_in_portfolio": _(
                "Mostrar mis gustos/intereses en el portafolio público."
            ),
            "show_work_experience_in_portfolio": _(
                "Mostrar mi experiencia laboral en el portafolio público."
            ),
            "show_chat_rooms_in_portfolio": _(
                "Mostrar mis salas de chat en el portafolio público."
            ),
            "show_personal_description_in_portfolio": _(
                "Mostrar mi descripción personal en el portafolio."
            ),
            "show_professional_title_in_portfolio": _(
                "Mostrar mi título profesional en el portafolio."
            ),
            "show_short_messages_in_portfolio": _(
                "Mostrar mis mensajes cortos en el portafolio público."
            ),
            "show_user_links_in_portfolio": _(
                "Mostrar mis enlaces de interés en el portafolio público."
            ),
        }
        help_texts = {
            "phone": _("Este campo es opcional."),
            "public_personal_description": _(
                'Esta descripción aparecerá en la sección "Sobre mí" de tu portafolio si la marcas como visible.'
            ),
            "professional_title": _(
                "Este título aparecerá bajo tu nombre en tu portafolio si lo marcas como visible."
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        optional_fields = [
            "phone",
            "degree",
            "current_year",
            "university",
            "hobbies",
            "work_experience",
            "public_personal_description",
            "professional_title",
        ]
        for field_name in optional_fields:
            if field_name in self.fields:
                self.fields[field_name].required = False
