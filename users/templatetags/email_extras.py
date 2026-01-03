from django import template
from django.core.signing import TimestampSigner
from django.urls import reverse
from django.conf import settings

register = template.Library()

@register.simple_tag
def get_unsubscribe_url(user):
    """
    Genera una URL de baja firmada criptográficamente para el usuario.
    No requiere que el usuario esté logueado para funcionar (1-click unsubscribe).
    """
    if not user or not user.pk:
        return "#"
    
    signer = TimestampSigner()
    # Firmamos el ID del usuario. Formato resultante: "ID:TIMESTAMP:SIGNATURE"
    signed_token = signer.sign(user.pk)
    
    relative_url = reverse('users:unsubscribe', args=[signed_token])
    
    # Construir URL absoluta
    base_url = getattr(settings, 'SITE_URL', 'https://www.campustudionline.com')
    return f"{base_url}{relative_url}"
