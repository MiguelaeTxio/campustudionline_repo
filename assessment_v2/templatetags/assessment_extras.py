# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/templatetags/assessment_extras.py
from django import template

register = template.Library()


@register.filter(name="split")
def split(value, separator=" "):
    """
    Splits a string into a list using the given separator.
    Django has no built-in 'split' filter; exam_take.html already used one to
    lay out the IPA and palaeography symbol palettes (W-PHILO-IPA,
    W-PHILO-OCR-PALE), which made the template impossible to compile.
    Returns an empty list for empty values so a missing palette degrades into
    no buttons instead of a 500.
    ---
    Divide una cadena en una lista usando el separador indicado.
    Django no trae filtro 'split'; exam_take.html ya lo usaba para desplegar
    las paletas de simbolos IPA y de paleografia (W-PHILO-IPA,
    W-PHILO-OCR-PALE), lo que hacia imposible compilar la plantilla.
    Devuelve lista vacia ante valores vacios, de modo que una paleta ausente
    degrada a "ningun boton" en vez de a un 500.
    Uso: {% for sym in "a b c"|split:" " %}
    """
    if value is None:
        return []
    return str(value).split(separator)
