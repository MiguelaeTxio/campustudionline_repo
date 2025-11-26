"""
Views for the Announcements application.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Announcement
from .forms import AnnouncementForm
from django.core.paginator import Paginator


@login_required
def announcement_list(request):
    """
    Displays a list of all published announcements, ordered by creation date.
    """
    announcement_qs = Announcement.objects.all().order_by('-created_at')
    paginator = Paginator(announcement_qs, 10)  # Show 10 announcements per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "announcements": page_obj,
        "show_tour": True,
    }
    return render(request, "announcements/announcement_list.html", context)


@login_required
def create_announcement(request):
    """
    Allows an authenticated user to create a new announcement.
    """
    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            new_announcement = form.save(commit=False)
            new_announcement.author = request.user
            new_announcement.save()
            messages.success(request, "¡Tu anuncio ha sido publicado exitosamente!")
            return redirect("announcements:announcement_list")
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = AnnouncementForm()

    context = {
        "announcement_form": form
    }
    return render(request, "announcements/create_announcement.html", context)
