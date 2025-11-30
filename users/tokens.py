# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/users/tokens.py
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Generador de tokens robusto para la activación de cuentas.
    Genera un hash estable basado en el ID del usuario, su estado de activación
    y la fecha de creación, en lugar de campos volátiles como el hash de la contraseña.
    """
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) + str(user.is_active)
        )

account_activation_token = AccountActivationTokenGenerator()
