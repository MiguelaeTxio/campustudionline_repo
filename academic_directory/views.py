# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/academic_directory/views.py
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import Count, Q, OuterRef, Subquery, Exists
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST

from academic_structure.models import University, Branch, Degree, Subject, AcademicYear
from contents.models import ContentMaterial, FavoriteFolder
from contents.utils import annotate_is_favorite
# [CLEANUP HITO 6] Eliminada importación de Assessment
from orchestrator.models import ContentRequest

ACADEMIC_DIRECTORY_TEMPLATE = "academic_directory/academic_level_detail.html"

def university_list_view(request):
    universities_qs = University.objects.all().order_by("name")

    paginator = Paginator(universities_qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_title": "Universidades",
        "breadcrumb": [{"name": "Directorio Académico", "url": reverse("academic_directory:university_list")}],
        "current_level_name": "Directorio Académico",
        "next_level_name": "Universidades",
        "next_level_items": page_obj,
        "next_url_name": "academic_directory:branch_list",
    }
    return render(request, ACADEMIC_DIRECTORY_TEMPLATE, context)


def branch_list_view(request, university_slug):
    university = get_object_or_404(University, slug=university_slug)
    branches_qs = Branch.objects.filter(university=university).order_by("name")

    paginator = Paginator(branches_qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    breadcrumb = [
        {"name": "Directorio Académico", "url": reverse("academic_directory:university_list")},
        {"name": university.name, "url": reverse("academic_directory:branch_list", kwargs={"university_slug": university.slug})},
    ]

    context = {
        "page_title": f"{university.name} - Ramas",
        "breadcrumb": breadcrumb,
        "current_level_name": university.name,
        "next_level_name": "Ramas de Conocimiento",
        "next_level_items": page_obj,
        "university_slug": university_slug,
        "next_url_name": "academic_directory:degree_list",
    }
    return render(request, ACADEMIC_DIRECTORY_TEMPLATE, context)


def degree_list_view(request, university_slug, branch_slug):
    branch = get_object_or_404(Branch.objects.select_related("university"), slug=branch_slug, university__slug=university_slug)
    degrees_qs = Degree.objects.filter(branch=branch).order_by("name")

    paginator = Paginator(degrees_qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    breadcrumb = [
        {"name": "Directorio Académico", "url": reverse("academic_directory:university_list")},
        {"name": branch.university.name, "url": reverse("academic_directory:branch_list", kwargs={"university_slug": branch.university.slug})},
        {"name": branch.name, "url": reverse("academic_directory:degree_list", kwargs={"university_slug": branch.university.slug, "branch_slug": branch.slug})},
    ]

    context = {
        "page_title": f"{branch.name} - Titulaciones",
        "breadcrumb": breadcrumb,
        "current_level_name": branch.name,
        "next_level_name": "Titulaciones",
        "next_level_items": page_obj,
        "university_slug": university_slug,
        "branch_slug": branch_slug,
        "next_url_name": "academic_directory:academic_year_list",
    }
    return render(request, ACADEMIC_DIRECTORY_TEMPLATE, context)


def academic_year_list_view(request, university_slug, branch_slug, degree_slug):
    degree = get_object_or_404(Degree.objects.select_related("branch__university"), slug=degree_slug, branch__slug=branch_slug, branch__university__slug=university_slug)
    academic_years_qs = AcademicYear.objects.filter(degree=degree).order_by("year")

    paginator = Paginator(academic_years_qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    for year_obj in page_obj:
        year_obj.name = f"Año {year_obj.year}"

    breadcrumb = [
        {"name": "Directorio Académico", "url": reverse("academic_directory:university_list")},
        {"name": degree.branch.university.name, "url": reverse("academic_directory:branch_list", kwargs={"university_slug": degree.branch.university.slug})},
        {"name": degree.branch.name, "url": reverse("academic_directory:degree_list", kwargs={"university_slug": degree.branch.university.slug, "branch_slug": degree.branch.slug})},
        {"name": degree.name, "url": reverse("academic_directory:academic_year_list", kwargs={"university_slug": degree.branch.university.slug, "branch_slug": degree.branch.slug, "degree_slug": degree.slug})},
    ]

    context = {
        "page_title": f"{degree.name} - Años Académicos",
        "breadcrumb": breadcrumb,
        "current_level_name": degree.name,
        "next_level_name": "Años Académicos",
        "next_level_items": page_obj,
        "university_slug": university_slug,
        "branch_slug": branch_slug,
        "degree_slug": degree_slug,
        "next_url_name": "academic_directory:subject_list",
    }
    return render(request, ACADEMIC_DIRECTORY_TEMPLATE, context)


def subject_list_view(request, university_slug, branch_slug, degree_slug, year):
    academic_year = get_object_or_404(AcademicYear.objects.select_related("degree__branch__university"), year=year, degree__slug=degree_slug, degree__branch__slug=branch_slug, degree__branch__university__slug=university_slug)
    subjects_qs = Subject.objects.filter(academic_year=academic_year).select_related('content_hash_family__content_material').order_by("name")

    paginator = Paginator(subjects_qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    breadcrumb = [
        {"name": "Directorio Académico", "url": reverse("academic_directory:university_list")},
        {"name": academic_year.degree.branch.university.name, "url": reverse("academic_directory:branch_list", kwargs={"university_slug": academic_year.degree.branch.university.slug})},
        {"name": academic_year.degree.branch.name, "url": reverse("academic_directory:degree_list", kwargs={"university_slug": academic_year.degree.branch.university.slug, "branch_slug": academic_year.degree.branch.slug})},
        {"name": academic_year.degree.name, "url": reverse("academic_directory:academic_year_list", kwargs={"university_slug": academic_year.degree.branch.university.slug, "branch_slug": academic_year.degree.branch.slug, "degree_slug": academic_year.degree.slug})},
        {"name": f"Año {year}", "url": reverse("academic_directory:subject_list", kwargs={"university_slug": academic_year.degree.branch.university.slug, "branch_slug": academic_year.degree.branch.slug, "degree_slug": academic_year.degree.slug, "year": year})},
    ]

    context = {
        "page_title": f"{academic_year.degree.name} - Año {year} - Asignaturas",
        "breadcrumb": breadcrumb,
        "current_level_name": f"Año {year}",
        "next_level_name": "Asignaturas",
        "next_level_items": page_obj,
        "university_slug": university_slug,
        "branch_slug": branch_slug,
        "degree_slug": degree_slug,
        "year": year,
        "next_url_name": "academic_directory:public_content_list",
    }
    return render(request, ACADEMIC_DIRECTORY_TEMPLATE, context)


def public_content_list_view(request, university_slug, branch_slug, degree_slug, year, subject_slug):
    subject = get_object_or_404(Subject.objects.select_related("academic_year__degree__branch__university", "content_hash_family"), slug=subject_slug, academic_year__year=year, academic_year__degree__slug=degree_slug, academic_year__degree__branch__slug=branch_slug, academic_year__degree__branch__university__slug=university_slug)
    
    # --- Reparación Quirúrgica: Visibilidad Híbrida (M2M + HashFamily) ---
    material_ids = list(subject.content_materials.filter(is_public=True).values_list('pk', flat=True))
    if subject.content_hash_family and subject.content_hash_family.content_material:
        m_family = subject.content_hash_family.content_material
        if m_family.is_public and m_family.pk not in material_ids:
            material_ids.append(m_family.pk)
    public_contents_qs = ContentMaterial.objects.filter(pk__in=material_ids)

    public_contents_qs = annotate_is_favorite(public_contents_qs, request.user)

    paginator = Paginator(public_contents_qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    breadcrumb = [
        {"name": "Directorio Académico", "url": reverse("academic_directory:university_list")},
        {"name": subject.academic_year.degree.branch.university.name, "url": reverse("academic_directory:branch_list", kwargs={"university_slug": subject.academic_year.degree.branch.university.slug})},
        {"name": subject.academic_year.degree.branch.name, "url": reverse("academic_directory:degree_list", kwargs={"university_slug": subject.academic_year.degree.branch.university.slug, "branch_slug": subject.academic_year.degree.branch.slug})},
        {"name": subject.academic_year.degree.name, "url": reverse("academic_directory:academic_year_list", kwargs={"university_slug": subject.academic_year.degree.branch.university.slug, "branch_slug": subject.academic_year.degree.branch.slug, "degree_slug": subject.academic_year.degree.slug})},
        {"name": f"Año {year}", "url": reverse("academic_directory:subject_list", kwargs={"university_slug": subject.academic_year.degree.branch.university.slug, "branch_slug": subject.academic_year.degree.branch.slug, "degree_slug": subject.academic_year.degree.slug, "year": year})},
        {"name": subject.name, "url": reverse("academic_directory:public_content_list", kwargs={"university_slug": subject.academic_year.degree.branch.university.slug, "branch_slug": subject.academic_year.degree.branch.slug, "degree_slug": subject.academic_year.degree.slug, "year": year, "subject_slug": subject.slug})},
    ]

    context = {
        "page_title": f"{subject.name} - Contenidos Públicos",
        "breadcrumb": breadcrumb,
        "current_level_name": subject.name,
        "subject": subject,
        "next_level_name": None,
        "next_level_items": None, 
        "public_contents": page_obj,
    }
    return render(request, ACADEMIC_DIRECTORY_TEMPLATE, context)

@login_required
@require_POST
def request_content_view(request):
    subject_id = request.POST.get("subject_id")
    subject = get_object_or_404(Subject, pk=subject_id)
    content_request, created = ContentRequest.objects.get_or_create(subject=subject)

    if request.user not in content_request.requesters.all():
        content_request.requesters.add(request.user)
        messages.success(request, f'Tu solicitud de contenido para "{subject.name}" ha sido registrada con éxito.')
    else:
        messages.info(request, f'Ya habías solicitado contenido para "{subject.name}". Hemos anotado tu interés de nuevo.')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('academic_directory:university_list')))
