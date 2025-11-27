# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/search/views.py
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q, Exists, OuterRef
from django.core.paginator import Paginator
from django.utils import timezone
import logging

from contents.utils import annotate_is_favorite
from contents.models import (
    ContentMaterial,
    ContentCopy,
    FavoriteFolder,
    FreeContentMasterCategory,
    FreeContentSubCategory,
)
from chat.models import ChatRoom, RoomMembership
from messaging.models import DirectChatSession
from academic_structure.models import University, Branch, Degree

logger = logging.getLogger(__name__)


@login_required
def search_home_view(request):
    """Displays top-level Free Content Master Categories."""
    master_categories_qs = FreeContentMasterCategory.objects.all()

    paginator = Paginator(master_categories_qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    breadcrumbs = [
        {"name": "Directorio de Contenidos Libres", "url": reverse("search:search_home")}
    ]
    context = {"page_obj": page_obj, "breadcrumbs": breadcrumbs, "show_tour": True}
    return render(request, "search/search_home.html", context)



@login_required
def free_content_category_detail_view(request, master_slug, sub_slug=None):
    """
    Handles navigation through the two-level free content hierarchy.
    """
    search_query = request.GET.get("q", "").strip()
    master_category = get_object_or_404(FreeContentMasterCategory, slug=master_slug)
    
    breadcrumbs = [
        {"name": "Directorio de Contenidos Libres", "url": reverse("search:search_home")},
        {"name": master_category.name, "url": master_category.get_absolute_url()},
    ]
    
    current_category = master_category
    child_items = master_category.sub_categories.all().order_by("display_order", "name")
    child_model_name = "Subcategorías"
    content_list = None
    is_leaf_node = False
    
    if sub_slug:
        sub_category = get_object_or_404(FreeContentSubCategory, slug=sub_slug, master_category=master_category)
        current_category = sub_category
        breadcrumbs.append({"name": sub_category.name, "url": sub_category.get_absolute_url()})
        child_items = []
        child_model_name = "Materiales de Contenido"
        content_list = sub_category.content_materials.filter(is_public=True).order_by("title")
        is_leaf_node = True

        content_list = annotate_is_favorite(content_list, request.user)
    else:
        content_list = master_category.content_materials.filter(is_public=True, sub_category__isnull=True).order_by("title")
        content_list = annotate_is_favorite(content_list, request.user)
        is_leaf_node = not child_items.exists() and content_list.exists()

    if breadcrumbs:
        breadcrumbs[-1]['url'] = '#'

    if search_query:
        if child_items: child_items = child_items.filter(name__icontains=search_query)
        if content_list: content_list = content_list.filter(Q(title__icontains=search_query) | Q(short_description__icontains=search_query))
    
    context = {
        "current_category": current_category,
        "child_items_with_urls": [{"obj": item, "url": item.get_absolute_url()} for item in child_items],
        "breadcrumbs": breadcrumbs,
        "child_model_name": child_model_name,
        "content_list": content_list,
        "search_query": search_query,
        "is_leaf_node": is_leaf_node,
        "show_tour": True,
    }
    return render(request, "search/category_detail.html", context)


@login_required
def global_search_view(request):
    # This view is out of scope for the current modification.
    search_query = request.GET.get("q", "").strip()
    selected_model_types = request.GET.getlist("model_type")
    user = request.user
    combined_results = []
    User = get_user_model()
    fallback_date = timezone.make_aware(timezone.datetime(1970, 1, 1))

    content_permission_q = Q(is_public=True) | Q(creator=user)
    content_search_q = Q(title__icontains=search_query) | Q(short_description__icontains=search_query)
    copy_permission_q = Q(is_public=True) | Q(user=user)
    copy_search_q = Q(original_content__title__icontains=search_query)
    user_search_q = Q(username__icontains=search_query)
    chat_room_permission_q = Q(memberships__user=user, memberships__status=RoomMembership.STATUS_MEMBER)
    chat_room_search_q = Q(name__icontains=search_query)
    direct_chat_permission_q = Q(user1=user, is_hidden_by_user1=False) | Q(user2=user, is_hidden_by_user2=False)
    direct_chat_search_q = Q(user1__username__icontains=search_query) | Q(user2__username__icontains=search_query)
    academic_search_q = Q(name__icontains=search_query)

    content_results_count = ContentMaterial.objects.filter(content_permission_q & content_search_q).distinct().count() if search_query else 0
    copy_results_count = ContentCopy.objects.filter(copy_permission_q & copy_search_q).distinct().count() if search_query else 0
    user_results_count = User.objects.filter(user_search_q).count() if search_query else 0
    chat_room_results_count = ChatRoom.objects.filter(chat_room_permission_q & chat_room_search_q).distinct().count() if search_query else 0
    direct_chat_results_count = DirectChatSession.objects.filter(direct_chat_permission_q & direct_chat_search_q).distinct().count() if search_query else 0
    total_chat_results_count = chat_room_results_count + direct_chat_results_count
    university_results_count = University.objects.filter(academic_search_q).count() if search_query else 0
    branch_results_count = Branch.objects.filter(academic_search_q).count() if search_query else 0
    degree_results_count = Degree.objects.filter(academic_search_q).count() if search_query else 0
    academic_structure_count = university_results_count + branch_results_count + degree_results_count

    if not selected_model_types and search_query:
        selected_model_types = ["material", "copy", "user", "chat", "academic"]

    if search_query:
        if "material" in selected_model_types:
            for item in ContentMaterial.objects.filter(content_permission_q & content_search_q).distinct().order_by("-updated_at"):
                combined_results.append({"type": "Material", "obj": item, "date": item.updated_at})
        if "copy" in selected_model_types:
            for item in ContentCopy.objects.filter(copy_permission_q & copy_search_q).select_related("original_content").distinct().order_by("-updated_at"):
                combined_results.append({"type": "Copia de Estudio", "obj": item, "date": item.updated_at})
        if "user" in selected_model_types:
            for item in User.objects.filter(user_search_q):
                combined_results.append({"type": "Usuario", "obj": item, "date": item.date_joined})
        if "chat" in selected_model_types:
            for item in ChatRoom.objects.filter(chat_room_permission_q & chat_room_search_q).distinct().order_by("-updated_at"):
                combined_results.append({"type": "Chat Grupal", "obj": item, "date": item.updated_at})
            for item in DirectChatSession.objects.filter(direct_chat_permission_q & direct_chat_search_q).select_related("user1", "user2").distinct().order_by("-updated_at"):
                combined_results.append({"type": "Chat Directo", "obj": {"session": item, "other_user": item.get_other_user(user)}, "date": item.updated_at})
        if "academic" in selected_model_types:
            for model, type_name in [(University, "Universidad"), (Branch, "Rama"), (Degree, "Grado Académico")]:
                for item in model.objects.filter(academic_search_q):
                    combined_results.append({"type": type_name, "obj": item, "date": fallback_date})
        combined_results.sort(key=lambda x: x["date"], reverse=True)

    paginator = Paginator(combined_results, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {
        "search_query": search_query, "page_obj": page_obj, "content_results_count": content_results_count,
        "copy_results_count": copy_results_count, "user_results_count": user_results_count,
        "total_chat_results_count": total_chat_results_count,
        "academic_structure_count": academic_structure_count, "selected_model_types": selected_model_types,
    }
    return render(request, "search/global_search_results.html", context)
