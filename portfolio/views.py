from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from chat.models import ChatRoom, RoomMembership
from contents.models import ContentMaterial
from users.models import UserProfile

from .forms import UserProfileChatPrivacyForm, ShortMessageForm, UserLinkForm
from .models import ShortMessage, UserLink


def public_portfolio_detail(request, username):
    User = get_user_model()
    portfolio_user = get_object_or_404(User, username=username)
    user_profile = UserProfile.objects.filter(user=portfolio_user).first()
    short_messages_query = ShortMessage.objects.filter(user=portfolio_user)
    user_links_query = UserLink.objects.filter(user=portfolio_user)

    has_public_materials = ContentMaterial.objects.filter(
        creator=portfolio_user, is_public=True
    ).exists()
    has_private_materials = False

    is_portfolio_owner = request.user.is_authenticated and request.user == portfolio_user
    if is_portfolio_owner:
        has_private_materials = ContentMaterial.objects.filter(
            creator=portfolio_user, is_public=False
        ).exists()

    show_materials_section = has_public_materials or (
        is_portfolio_owner and has_private_materials
    )

    chat_rooms_info = []
    chat_privacy_form = None
    show_chat_rooms_directory_flag = False
    show_chat_rooms_section = False
    show_private_chat_config_message = False
    last_checked_activity = None

    if user_profile:
        show_chat_rooms_directory_flag = (
            user_profile.show_chat_rooms_in_portfolio
        )
        if is_portfolio_owner:
            last_checked_activity = user_profile.last_checked_chat_activity
            user_profile.last_checked_chat_activity = timezone.now()
            user_profile.save(update_fields=["last_checked_chat_activity"])
            chat_privacy_form = UserProfileChatPrivacyForm(instance=user_profile)
            show_chat_rooms_section = True
            if not show_chat_rooms_directory_flag:
                show_private_chat_config_message = True
        elif show_chat_rooms_directory_flag:
            show_chat_rooms_section = True

        memberships = RoomMembership.objects.filter(
            user=portfolio_user, status=RoomMembership.STATUS_MEMBER
        ).select_related("room")

        if memberships.exists():
            for membership in memberships:
                room = membership.room
                has_new_messages = False
                if is_portfolio_owner and last_checked_activity:
                    if room.updated_at and room.updated_at > last_checked_activity:
                        has_new_messages = True
                room_url = reverse("chat:room_detail", kwargs={"room_slug": room.slug})
                chat_rooms_info.append(
                    {
                        "room": room,
                        "url": room_url,
                        "has_new_messages": has_new_messages,
                    }
                )

    context = {
        "portfolio_user": portfolio_user,
        "profile": user_profile,
        "short_messages": [],
        "user_links": [],
        "profile_info": {},
        "show_materials_section": show_materials_section,
        "chat_rooms_info": chat_rooms_info,
        "chat_privacy_form": chat_privacy_form,
        "is_portfolio_owner": is_portfolio_owner,
        "show_chat_rooms_section": show_chat_rooms_section,
        "is_chat_directory_public": show_chat_rooms_directory_flag,
        "show_private_chat_config_message": show_private_chat_config_message,
        "show_tour": is_portfolio_owner,
    }

    description_visible = False
    title_visible = False
    if user_profile:
        if portfolio_user.email:
            context["profile_info"]["Email"] = portfolio_user.email
        if user_profile.show_phone_in_portfolio and user_profile.phone:
            context["profile_info"]["Teléfono"] = user_profile.phone
        if user_profile.show_degree_in_portfolio and user_profile.degree:
            context["profile_info"]["Carrera"] = user_profile.degree
        if (
            user_profile.show_current_year_in_portfolio
            and user_profile.current_year
        ):
            context["profile_info"]["Curso Actual"] = user_profile.current_year
        if user_profile.show_university_in_portfolio and user_profile.university:
            context["profile_info"]["Universidad"] = user_profile.university
        if (
            user_profile.show_hobbies_in_portfolio
            and user_profile.hobbies
        ):
            context["profile_info"]["Gustos e Intereses"] = user_profile.hobbies
        if (
            user_profile.show_work_experience_in_portfolio
            and user_profile.work_experience
        ):
            context["profile_info"][
                "Experiencia Laboral"
            ] = user_profile.work_experience
        if (
            user_profile.show_personal_description_in_portfolio
            and user_profile.public_personal_description
        ):
            description_visible = True
        if (
            user_profile.show_professional_title_in_portfolio
            and user_profile.professional_title
        ):
            title_visible = True
        if user_profile.show_short_messages_in_portfolio:
            context["short_messages"] = (
                short_messages_query.filter(is_public=True)
                if hasattr(ShortMessage, "is_public")
                else short_messages_query
            )
        if user_profile.show_user_links_in_portfolio:
            context["user_links"] = user_links_query

    is_portfolio_empty = (
        not context["profile_info"]
        and not context["user_links"]
        and not context["short_messages"]
        and not description_visible
        and not title_visible
        and not show_materials_section
        and not (chat_rooms_info and show_chat_rooms_section)
    )
    context["is_portfolio_empty"] = is_portfolio_empty
    return render(request, "portfolio/public_portfolio_detail.html", context)


@login_required
@require_POST
def update_chat_privacy_settings(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    form = UserProfileChatPrivacyForm(request.POST, instance=user_profile)
    if form.is_valid():
        form.save()
        messages.success(
            request,
            "Tu configuración de privacidad para las salas de chat ha sido actualizada.",
        )
    else:
        for field, error_list in form.errors.items():
            for error in error_list:
                messages.error(
                    request, f"Error en '{form.fields[field].label}': {error}"
                )
    return redirect("portfolio:public_portfolio_detail", username=request.user.username)


@login_required
def create_short_message(request):
    if request.method == "POST":
        form = ShortMessageForm(request.POST)
        if form.is_valid():
            short_message = form.save(commit=False)
            short_message.user = request.user
            short_message.save()
            messages.success(request, "¡Tu mensaje corto ha sido añadido con éxito!")
            return redirect(
                "portfolio:public_portfolio_detail", username=request.user.username
            )
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(
                        request,
                        f"Error en '{form.fields[field].label if field in form.fields else field}': {error}",
                    )
    else:
        form = ShortMessageForm()
    context = {
        "form": form,
        "page_title": "Añadir Nuevo Mensaje Corto a tu Portafolio",
    }
    return render(request, "portfolio/create_short_message.html", context)


@login_required
def create_user_link(request):
    if request.method == "POST":
        form = UserLinkForm(request.POST)
        if form.is_valid():
            user_link = form.save(commit=False)
            user_link.user = request.user
            user_link.save()
            messages.success(request, "¡Tu enlace ha sido añadido con éxito!")
            return redirect(
                "portfolio:public_portfolio_detail", username=request.user.username
            )
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(
                        request,
                        f"Error en '{form.fields[field].label if field in form.fields else field}': {error}",
                    )
    else:
        form = UserLinkForm()
    context = {
        "form": form,
        "page_title": "Añadir Nuevo Enlace de Interés a tu Portafolio",
    }
    return render(request, "portfolio/create_user_link.html", context)


@login_required
@require_POST
def delete_short_message(request, pk):
    message = get_object_or_404(ShortMessage, pk=pk)
    if message.user != request.user:
        messages.error(request, "No tienes permiso para borrar este mensaje.")
        return HttpResponseForbidden("No tienes permiso para borrar este mensaje.")
    message.delete()
    messages.success(request, "El mensaje corto ha sido eliminado con éxito.")
    return redirect("portfolio:public_portfolio_detail", username=request.user.username)


@login_required
@require_POST
def delete_user_link(request, pk):
    link = get_object_or_404(UserLink, pk=pk)
    if link.user != request.user:
        messages.error(request, "No tienes permiso para borrar este enlace.")
        return HttpResponseForbidden("No tienes permiso para borrar este enlace.")
    link.delete()
    messages.success(request, "El enlace ha sido eliminado con éxito.")
    return redirect("portfolio:public_portfolio_detail", username=request.user.username)
