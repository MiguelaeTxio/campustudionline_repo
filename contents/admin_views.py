# /home/MiguelAeTxio/CampuStudiOnline/contents/admin_views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from .models import FreeContentSubCategory

@user_passes_test(lambda u: u.is_staff)
def ajax_load_subcategories(request):
    """
    Vista AJAX para cargar dinámicamente las subcategorías en el admin
    basado en la master_category seleccionada.
    """
    master_category_id = request.GET.get('master_category_id')
    if master_category_id:
        subcategories = FreeContentSubCategory.objects.filter(master_category_id=master_category_id).order_by('name')
        return JsonResponse(list(subcategories.values('id', 'name')), safe=False)
    return JsonResponse([], safe=False)
