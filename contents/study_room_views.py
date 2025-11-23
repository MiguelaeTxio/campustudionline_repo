# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/contents/study_room_views.py
import logging
import lxml.html
from lxml import etree
from copy import deepcopy
import json
from django.db import transaction
from django.db.models import Exists, Q, Subquery, OuterRef, Case, When, Value, IntegerField, CharField
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils.html import escape
from django.utils import timezone

from .models import ContentMaterial as Content, ContentCopy, Annotation, FavoriteFolder, FreeContentMasterCategory, FreeContentSubCategory
from academic_structure.models import Subject, University, Branch, Degree, AcademicYear
from assessment.models import Assessment
from assessment.utils import (
    annotate_content_copy_queryset_with_assessment_states,
    get_assessment_context
)
from .views import markdown_to_html_internal, parse_yaml_front_matter

logger = logging.getLogger("contents")

def _wrap_selection_in_span(root, position_data, span_attributes):
    start_xpath = position_data['start_container_xpath']
    start_offset = position_data['start_offset']
    end_xpath = position_data['end_container_xpath']
    end_offset = position_data['end_offset']

    start_nodes = root.xpath(start_xpath)
    end_nodes = root.xpath(end_xpath)
    if not start_nodes or not end_nodes:
        raise ValueError("No se encontraron los nodos de inicio o fin de la selección.")

    start_node = start_nodes[0]
    end_node = end_nodes[0]

    def extract_text_info(node, offset):
        if isinstance(node, lxml.etree._ElementUnicodeResult):
            parent = node.getparent()
            is_tail = (parent.tail == node)
            text = parent.tail if is_tail else parent.text
            return parent, is_tail, text[:offset], text[offset:]
        else:
            text = node.text or ""
            return node, False, text[:offset], text[offset:]

    start_parent, start_is_tail, start_before, start_after = extract_text_info(start_node, start_offset)
    end_parent, end_is_tail, end_before, end_after = extract_text_info(end_node, end_offset)

    if start_parent is end_parent:
        full_middle = (start_after or "")[:len(start_after or "") - len(end_after or "")]
        new_span = lxml.html.Element('span', attrib=span_attributes)
        new_span.text = full_middle
        new_span.tail = end_after

        if start_is_tail:
            start_parent.tail = start_before
            start_parent.addnext(new_span)
        else:
            start_parent.text = start_before
            start_parent.insert(0, new_span)
    else:
        if start_is_tail:
            start_parent.tail = start_before
        else:
            start_parent.text = start_before

        if end_is_tail:
            end_parent.tail = end_after
        else:
            end_parent.text = end_after

        container = lxml.html.Element('span', attrib=span_attributes)
        container.text = start_after

        in_between = []
        collecting = False
        for el in root.iter():
            if el is start_parent:
                collecting = True
            if collecting:
                in_between.append(el)
            if el is end_parent:
                break
        
        for el in in_between[1:-1]:
            container.append(deepcopy(el))

        last = deepcopy(end_parent)
        if not end_is_tail:
            last.text = end_before
        else:
            last.tail = end_before
        container.append(last)

        start_parent.addnext(container)

@login_required
@transaction.atomic
def create_content_copy(request, pk, subject_pk=None):
    original_content = get_object_or_404(Content, pk=pk)
    subject_context = None

    # Lógica simplificada: Se confía en que el frontend envía el subject_pk cuando es necesario.
    if subject_pk:
        subject_context = get_object_or_404(Subject, pk=subject_pk)

    # Comprobaciones de negocio (límites, permisos) se mantienen.
    if ContentCopy.objects.filter(user=request.user).count() >= 6:
        messages.error(request, "Has alcanzado el límite de 6 copias de estudio. Por favor, elimina alguna para poder crear una nueva.")
        return redirect(original_content.get_absolute_url())

    if not original_content.is_public and original_content.creator != request.user:
        messages.error(request, "No tienes permiso para crear una copia de este contenido.")
        return redirect(original_content.get_absolute_url())
    
    existing_copy = ContentCopy.objects.filter(
        original_content=original_content,
        user=request.user,
        subject_context=subject_context
    ).first()

    if existing_copy:
        messages.info(request, "Ya tienes una copia de este contenido para esta asignatura. Redirigiendo a tu Sala de Estudio.")
        return redirect("study_room:edit_copy", pk=existing_copy.pk)
    
    link_to_original = reverse("contents:content_detail", kwargs={"pk": original_content.pk})
    watermark_html = f"""<div class="watermark alert alert-info mb-4"><p><strong>Contenido Original:</strong> {original_content.title}</p><p><strong>Autor:</strong> {original_content.creator.username}</p><p><strong>Fecha de creación:</strong> {original_content.created_at.strftime('%d/%m/%Y')}</p><p><a href="{link_to_original}" class="alert-link">Ver contenido original</a></p></div>"""
    _, markdown_body = parse_yaml_front_matter(original_content.get_full_markdown_content())
    original_html = markdown_to_html_internal(markdown_body)
    content_with_watermark = watermark_html + original_html
    
    new_copy = ContentCopy.objects.create(
        original_content=original_content,
        user=request.user,
        html_content=content_with_watermark,
        is_public=False,
        subject_context=subject_context
    )
    
    favorites_folder, _ = FavoriteFolder.objects.get_or_create(
        user=request.user,
        folder_type=FavoriteFolder.FOLDER_TYPE_FAVORITES,
        defaults={'name': 'Mis Favoritos'}
    )
    favorites_folder.materials.add(original_content)
    
    messages.success(request, f"Se ha creado una copia de '{original_content.title}' y el original se ha añadido a 'Mis Favoritos'.")
    
    return redirect("study_room:copy_directory_root")

@login_required
def edit_copy(request, pk):
    content_copy = get_object_or_404(ContentCopy, pk=pk, user=request.user)
    FAILURE_STATUSES = [Assessment.AssessmentStatus.GENERATION_FAILED_RETRYABLE, Assessment.AssessmentStatus.GENERATION_FAILED_QUOTA, Assessment.AssessmentStatus.GENERATION_FAILED_FATAL, Assessment.AssessmentStatus.CORRECTION_FAILED_RETRYABLE, Assessment.AssessmentStatus.CORRECTION_FAILED_FATAL,]
    latest_assessment = Assessment.objects.filter(content_copy=content_copy).order_by('-created_at').first()
    if latest_assessment and latest_assessment.status in FAILURE_STATUSES and not latest_assessment.was_viewed:
        latest_assessment.was_viewed = True
        latest_assessment.save(update_fields=['was_viewed'])
        logger.info(f"Notificación de fallo para Assessment ID {latest_assessment.id} marcada como vista.")
    if request.method == "POST":
        content_copy.html_content = request.POST.get("html_content", content_copy.html_content)
        content_copy.is_public = request.POST.get("is_public") == "on"
        content_copy.save(update_fields=["html_content", "is_public"])
        return JsonResponse({"status": "success", "message": "Cambios guardados."})
    db_annotations = content_copy.annotations.all().order_by("created_at")
    csrf_token = get_token(request)
    annotation_config = {"createAnnotationUrl": reverse("study_room:create_annotation", kwargs={"pk": content_copy.pk}), "deleteAnnotationUrlBase": reverse("study_room:delete_annotation", kwargs={"pk": "00000000-0000-0000-0000-000000000000"}), "csrfToken": csrf_token,}
    assessment_context = get_assessment_context(request.user, content_copy)
    assessment_polling_config = {}
    if assessment_context.get('status') in ["GENERANDOSE", "CORRIGIENDOSE"]:
        if assessment_context.get('raw_assessment'):
            assessment_polling_config = {"statusUrl": reverse("assessment:get_assessment_status", kwargs={"assessment_pk": assessment_context['raw_assessment'].pk}), "panelUpdateUrl": reverse("assessment:get_assessment_panel_content", kwargs={"copy_pk": content_copy.pk}), "csrfToken": csrf_token,}
    context = {"content_copy": content_copy, "annotations": db_annotations, "annotation_config": json.dumps(annotation_config), "assessment_polling_config": json.dumps(assessment_polling_config), "assessment_context": assessment_context}
    return render(request, "contents/study_room/edit_copy.html", context)

def get_academic_breadcrumbs(university_slug=None, branch_slug=None, degree_slug=None, year=None, subject_slug=None):
    breadcrumbs = []
    if university_slug:
        uni = get_object_or_404(University, slug=university_slug)
        breadcrumbs.append({"name": uni.name, "url": reverse("study_room:academic_directory_university", args=[uni.slug])})
        if branch_slug:
            branch = get_object_or_404(Branch, slug=branch_slug, university=uni)
            breadcrumbs.append({"name": branch.name, "url": reverse("study_room:academic_directory_branch", args=[uni.slug, branch.slug])})
            if degree_slug:
                degree = get_object_or_404(Degree, slug=degree_slug, branch=branch)
                breadcrumbs.append({"name": degree.name, "url": reverse("study_room:academic_directory_degree", args=[uni.slug, branch.slug, degree.slug])})
                if year:
                    breadcrumbs.append({"name": f"Año {year}", "url": reverse("study_room:academic_directory_year", args=[uni.slug, branch.slug, degree.slug, year])})
                    if subject_slug:
                        subject = get_object_or_404(Subject, slug=subject_slug, academic_year__year=year, academic_year__degree=degree)
                        breadcrumbs.append({"name": subject.name, "url": "#"})
    return breadcrumbs

@login_required
def user_copies_list(request, university_slug=None, branch_slug=None, degree_slug=None, year=None, subject_slug=None, master_slug=None, sub_slug=None):
    """
    Vista resiliente y centrada en el usuario para listar copias de estudio.
    Se apoya en UserStudyNavigation para la estructura visual (sidebar)
    y usa esta vista solo para filtrar el contenido final.
    """
    # Base QuerySet: Solo las copias del usuario
    # [MODIFICADO] Se añade anotación de estados de evaluación para la UI
    base_qs = ContentCopy.objects.filter(user=request.user).select_related(
        "original_content",
        "subject_context"
    ).order_by("-updated_at")
    
    base_copies = annotate_content_copy_queryset_with_assessment_states(base_qs, request.user)

    context = {
        "page_title": "Mi Sala de Estudio", 
        "show_tour": True,
        "breadcrumbs": [{"name": "Sala de Estudio", "url": reverse("study_room:copy_directory_root")}]
    }
    
    items_list = []
    level_name = "root"

    # --- MODO 1: NAVEGACIÓN ACADÉMICA ---
    if any([university_slug, branch_slug, degree_slug, year, subject_slug]):
        if subject_slug:
            items_list = base_copies.filter(subject_context__slug=subject_slug)
            try:
                subj_name = items_list.first().subject_context.name if items_list.exists() else subject_slug
            except AttributeError:
                subj_name = subject_slug
            
            context.update({
                "page_title": f"Copias de {subj_name}",
                "level_name": "academic_copies"
            })
            context["breadcrumbs"].append({"name": "Académico", "url": "#"})
            context["breadcrumbs"].append({"name": subj_name, "url": "#"})

        elif year and degree_slug:
            subject_ids = base_copies.filter(
                subject_context__academic_year__year=year,
                subject_context__academic_year__degree__slug=degree_slug
            ).values_list("subject_context_id", flat=True).distinct()
            
            items_list = Subject.objects.filter(id__in=subject_ids).order_by("name")
            context.update({"page_title": f"Asignaturas del Año {year}", "level_name": "subjects"})

        elif degree_slug:
             items_list = [] 
             context.update({"page_title": f"Grado: {degree_slug}", "level_name": "years"})
             
        else:
            pass

    # --- MODO 2: CONTENIDO LIBRE ---
    elif any([master_slug, sub_slug]):
        if sub_slug:
            items_list = base_copies.filter(original_content__sub_category__slug=sub_slug)
            context.update({"page_title": f"Categoría: {sub_slug}", "level_name": "free_copies"})
        elif master_slug:
            sub_ids = base_copies.filter(
                original_content__master_category__slug=master_slug
            ).values_list("original_content__sub_category_id", flat=True).distinct()
            items_list = FreeContentSubCategory.objects.filter(id__in=sub_ids)
            context.update({"page_title": f"Sección: {master_slug}", "level_name": "sub_categories"})

    # --- MODO 3: RAÍZ (Dashboard) ---
    else:
        items_list = base_copies
        context.update({"page_title": "Resumen Reciente", "level_name": "dashboard"})

    if items_list is not None:
        context["page_obj"] = Paginator(items_list, 10).get_page(request.GET.get("page"))
    else:
         context["page_obj"] = None

    template_name = "contents/study_room/copy_list.html"
    if request.htmx:
        template_name = "contents/study_room/_copy_list_partial.html"
        
    return render(request, template_name, context)

@require_POST
@login_required
@transaction.atomic
def create_annotation(request, pk):
    content_copy = get_object_or_404(ContentCopy, pk=pk, user=request.user)
    try:
        data = request.POST
        annotation_type = data.get('annotation_type')
        content = data.get('content', '')
        color = data.get('color')
        selected_text = data.get('selected_text', '').strip()
        
        position_data = {
            'start_container_xpath': data.get('start_container_xpath'),
            'start_offset': int(data.get('start_offset', 0)),
            'end_container_xpath': data.get('end_container_xpath'),
            'end_offset': int(data.get('end_offset', 0))
        }

        if not all([annotation_type, color, selected_text, position_data['start_container_xpath'], position_data['end_container_xpath']]):
            return JsonResponse({"status": "error", "message": "Faltan datos para crear la anotación."}, status=400)

        annotation = Annotation.objects.create(
            copy=content_copy, user=request.user, annotation_type=annotation_type,
            content=content, color=color, selected_text=selected_text,
            position=json.dumps(position_data)
        )

        root = lxml.html.fromstring(f"<div>{content_copy.html_content}</div>")
        
        span_attributes = {
            "class": "annotation-highlight", "id": f"annotation-{annotation.id}",
        }
        
        style = ""
        if annotation.annotation_type == 'highlight': style = f"background-color: {annotation.color};"
        elif annotation.annotation_type == 'note': 
            style = f"border-bottom: 2px dotted {annotation.color}; cursor: pointer;"
            escaped_content = escape(annotation.content or 'Nota vacía.')
            popover_content = escaped_content.replace('\r\n', '<br>').replace('\n', '<br>')
            span_attributes.update({
                'data-bs-toggle': 'popover', 'data-bs-trigger': 'hover focus',
                'data-bs-title': 'Nota', 'data-bs-content': popover_content,
                'data-bs-html': 'true'
            })
        elif annotation.annotation_type == 'mark': style = f"color: {annotation.color}; font-weight: bold;"
        
        if style:
            span_attributes["style"] = style

        _wrap_selection_in_span(root, position_data, span_attributes)

        updated_html = "".join([lxml.html.tostring(child, encoding='unicode') for child in root.iterchildren()])
        content_copy.html_content = updated_html
        content_copy.save(update_fields=['html_content'])

        annotation_data = {
            "id": str(annotation.id),
            "annotation_type": annotation.annotation_type,
            "annotation_type_display": annotation.get_annotation_type_display(),
            "content": annotation.content,
            "color": annotation.color,
            "selected_text": annotation.selected_text,
            "created_at": annotation.created_at.isoformat(),
        }

        return JsonResponse({
            "status": "success", "message": "Anotación creada con éxito.",
            "annotation": annotation_data, "content_html": updated_html,
        })
    except Exception as e:
        logger.error(f"Error creando anotación para la copia {pk}: {e}", exc_info=True)
        return JsonResponse({"status": "error", "message": "Ocurrió un error inesperado al crear la anotación."}, status=500)


@require_POST
@login_required
def delete_annotation(request, pk):
    annotation = get_object_or_404(Annotation, pk=pk)
    copy = annotation.copy
    can_delete = (annotation.user == request.user or copy.user == request.user or request.user.is_staff)

    if not can_delete:
        return JsonResponse({'status': 'error', 'message': 'No tienes permiso para eliminar esta anotación.'}, status=403)

    try:
        with transaction.atomic():
            root = lxml.html.fromstring(f"<div>{copy.html_content}</div>")
            span_to_remove = root.find(f'.//span[@id="annotation-{annotation.id}"]')

            if span_to_remove is not None:
                parent = span_to_remove.getparent()
                previous = span_to_remove.getprevious()
                
                unwrapped_content = (span_to_remove.text or '') + (span_to_remove.tail or '')

                if previous is not None:
                    previous.tail = (previous.tail or '') + unwrapped_content
                else:
                    parent.text = (parent.text or '') + unwrapped_content
                
                parent.remove(span_to_remove)
                
                updated_html = "".join([lxml.html.tostring(child, encoding='unicode') for child in root.iterchildren()])
                copy.html_content = updated_html
                copy.save(update_fields=['html_content'])

            annotation.delete()
            return JsonResponse({'status': 'success', 'content_html': copy.html_content})
    except Exception as e:
        logger.error(f"Error al eliminar la anotación {pk}: {e}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': 'Error interno del servidor al eliminar la anotación.'}, status=500)


@login_required
@require_POST
def delete_copy(request, pk):
    content_copy = get_object_or_404(ContentCopy, pk=pk, user=request.user)
    content_copy.delete()
    messages.success(request, 'La copia ha sido eliminada.')
    return redirect("study_room:copy_directory_root")

@login_required
@require_POST
def change_copy_visibility(request, pk):
    content_copy = get_object_or_404(ContentCopy, pk=pk, user=request.user)
    content_copy.is_public = not content_copy.is_public
    content_copy.save(update_fields=["is_public"])
    status = "pública" if content_copy.is_public else "privada"
    messages.success(request, f"La visibilidad de la copia ahora es {status}.")
    return redirect("study_room:edit_copy", pk=content_copy.pk)
