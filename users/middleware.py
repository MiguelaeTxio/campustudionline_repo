# users/middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings


class SecuritySetupMiddleware:
    """
    Middleware que actúa como un "Punto de Control de Seguridad".

    Este middleware se asegura de que cualquier usuario autenticado no pueda
    navegar por el sitio si no tiene una clave pública de cifrado registrada
    en su perfil.

    Lógica:
    1. Se ejecuta en cada petición.
    2. Si el usuario no está autenticado, no hace nada.
    3. Si el usuario está autenticado:
       a. Comprueba si el campo 'public_key' en su UserProfile tiene un valor.
       b. Si NO tiene valor, y la URL solicitada NO es la página de configuración
          de seguridad, la de logout, o la API para guardar la clave, redirige
          forzosamente al usuario a la página de configuración de seguridad.
    4. Esto evita bucles de redirección y garantiza que la configuración
       de seguridad sea un paso ineludible.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. No aplicar la lógica para usuarios no autenticados.
        if not request.user.is_authenticated:
            return self.get_response(request)

        # 2. Definir las URLs que siempre deben ser accesibles para evitar bucles.
        allowed_urls = [
            reverse("users:setup_security"),
            reverse("users:save_crypto_keys"),
            reverse("logout"),
        ]
        # También permitir el acceso a los archivos estáticos y de medios.
        is_allowed_path = (
            request.path_info in allowed_urls
            or request.path_info.startswith(settings.STATIC_URL)
            or (settings.MEDIA_URL and request.path_info.startswith(settings.MEDIA_URL))
        )

        # 3. Comprobar si el usuario tiene una clave pública.
        # Usamos un bloque try/except para ser robustos en caso de que el perfil
        # no existiera por alguna razón anómala.
        # ESTA ES LA LÓGICA CORRECTA PORQUE LAS CLAVES ESTÁN EN EL PERFIL
        try:
            # Aquí se comprueba el campo 'public_key' del UserProfile
            has_public_key = bool(request.user.userprofile.public_key)
        except AttributeError:
            has_public_key = False

        # 4. La condición de redirección:
        # Si el usuario NO tiene clave y NO está intentando acceder a una ruta permitida...
        if not has_public_key and not is_allowed_path:
            # ...redirigirlo a la página de configuración.
            return redirect("users:setup_security")

        # Si todo está en orden, procesar la petición normalmente.
        response = self.get_response(request)
        return response
