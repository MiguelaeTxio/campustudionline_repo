# /home/MiguelAeTxio/CampuStudiOnline/academic_chat/decorators.py
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import AcademicChatLink


def user_can_access_academic_chat(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        chat_slug = kwargs.get("chat_slug")
        chat_link = get_object_or_404(
            AcademicChatLink.objects.select_related(
                "group", "subject", "chat_room__creator"
            ),
            slug=chat_slug,
        )
        kwargs["academic_link"] = chat_link

        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        has_permission = False

        required_group = chat_link.group
        if required_group and request.user.groups.filter(id=required_group.id).exists():
            has_permission = True

        if not has_permission:
            if chat_link.enrolled_students.filter(pk=request.user.pk).exists():
                has_permission = True

        if has_permission:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied(
                "No tienes permiso para acceder a esta sala de chat."
            )

    return _wrapped_view
