# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment/views.py
import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST, require_GET
from django.db import transaction
from django.http import JsonResponse, Http404
from django.utils import timezone
from django.template.loader import render_to_string

from .models import Assessment, Question, UserAnswer
from contents.models import ContentCopy
from orchestrator.tasks import generate_assessment_from_content_task, correct_assessment_task
from .utils import get_assessment_context, check_user_assessment_limits

logger = logging.getLogger(__name__)


def log_timestamp(message):
    logger.info(f"[{timezone.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] {message}")


@login_required
@require_POST
@transaction.atomic
def generate_ai_assessment(request, copy_pk):
    try:
        # Bloqueo de fila para evitar duplicidad por race-condition
        user_copy = ContentCopy.objects.select_for_update().get(pk=copy_pk, user=request.user)
    except ContentCopy.DoesNotExist:
        messages.error(request, "No se encontró la copia de estudio solicitada.")
        return redirect("study_room:copy_directory_root")

    redirect_url = reverse("study_room:edit_copy", kwargs={"pk": user_copy.pk})

    blocking_statuses = [
        Assessment.AssessmentStatus.PENDING,
        Assessment.AssessmentStatus.PROCESSING,
        Assessment.AssessmentStatus.COMPLETED,
        Assessment.AssessmentStatus.CORRECTING,
        Assessment.AssessmentStatus.RESULTS_AVAILABLE,
        Assessment.AssessmentStatus.GENERATION_FAILED_RETRYABLE,
        Assessment.AssessmentStatus.GENERATION_FAILED_QUOTA,
        Assessment.AssessmentStatus.CORRECTION_FAILED_RETRYABLE,
    ]
    
    if Assessment.objects.filter(
        user=request.user, content_copy=user_copy, status__in=blocking_statuses
    ).exists():
        messages.info(
            request,
            "Ya hay una evaluación en curso o activa para este material.",
        )
        return redirect(redirect_url)

    limit_data = check_user_assessment_limits(request.user)
    if not limit_data["can_create_new"]:
        messages.error(
            request,
            "Has alcanzado tu límite de evaluaciones. Inténtalo más tarde.",
        )
        return redirect(redirect_url)

    try:
        assessment = Assessment.objects.create(
            user=request.user,
            content_copy=user_copy,
            status="PENDING",
        )
        generate_assessment_from_content_task.delay(assessment.id)
        messages.success(
            request,
            "Evaluación solicitada correctamente. Te avisaremos cuando esté lista.",
        )

    except Exception as e:
        logger.error(f"Error al crear evaluación: {e}", exc_info=True)
        messages.error(request, "Hubo un error técnico al procesar tu solicitud.")

    return redirect(redirect_url)


@login_required
def take_assessment(request, pk):
    try:
        assessment = Assessment.objects.select_related("content_copy__original_content").prefetch_related("questions").get(
            pk=pk,
            user=request.user,
        )
    except Assessment.DoesNotExist:
        messages.error(request, "Evaluación no encontrada.")
        return redirect("study_room:copy_directory_root")

    user_copy = assessment.content_copy

    if assessment.status != "COMPLETED":
        messages.warning(
            request,
            f"Esta evaluación no está lista. Estado actual: {assessment.get_status_display()}.",
        )
        return redirect(reverse("study_room:edit_copy", kwargs={"pk": user_copy.pk}))

    if UserAnswer.objects.filter(
        question__assessment=assessment, user=request.user
    ).exists():
        messages.info(
            request, "Ya has completado esta evaluación. Redirigiendo a resultados."
        )
        return redirect("assessment:view_results", pk=assessment.pk)

    if not assessment.was_viewed:
        assessment.was_viewed = True
        assessment.save(update_fields=["was_viewed"])

    context = {
        "assessment": assessment,
        "user_copy": user_copy,
        "page_title": "Completar Autoevaluación",
    }
    return render(request, "assessment/take_assessment.html", context)


@login_required
@require_POST
def submit_assessment(request, pk):
    try:
        assessment = Assessment.objects.select_related("content_copy").get(pk=pk, user=request.user)
    except Assessment.DoesNotExist:
        messages.error(request, "Evaluación no encontrada al intentar enviar.")
        return redirect("study_room:copy_directory_root")

    user_copy = assessment.content_copy
    redirect_url = reverse("study_room:edit_copy", kwargs={"pk": user_copy.pk})

    if UserAnswer.objects.filter(
        question__assessment=assessment, user=request.user
    ).exists():
        messages.warning(request, "Ya has enviado esta evaluación previamente.")
        return redirect("assessment:view_results", pk=assessment.pk)

    questions = assessment.questions.all()
    answers_to_create = []

    for question in questions:
        user_answer_text = request.POST.get(f"answer_q_{question.pk}", "").strip()
        answers_to_create.append(
            UserAnswer(
                question=question,
                user=request.user,
                answer_text=user_answer_text,
            )
        )

    try:
        with transaction.atomic():
            UserAnswer.objects.bulk_create(answers_to_create)
            assessment.status = "AWAITING_CORRECTION"
            assessment.questions_processed = 0
            assessment.total_questions_expected = questions.count()
            assessment.save(
                update_fields=[
                    "status",
                    "questions_processed",
                    "total_questions_expected",
                ]
            )
            correct_assessment_task.delay(assessment.id)
            messages.success(
                request,
                "Respuestas enviadas. La corrección ha comenzado.",
            )
    except Exception as e:
        logger.error(f"Error en submit_assessment: {e}", exc_info=True)
        messages.error(request, "Error al procesar respuestas.")
        return redirect(redirect_url)

    return redirect(redirect_url)


@login_required
def view_results(request, pk):
    try:
        assessment = Assessment.objects.select_related("content_copy__original_content").prefetch_related(
            "questions__user_answers"
        ).get(pk=pk, user=request.user)
    except Assessment.DoesNotExist:
        messages.error(request, "Resultados no encontrados.")
        return redirect("study_room:copy_directory_root")

    user_copy = assessment.content_copy
    user_answers_qs = UserAnswer.objects.filter(
        question__assessment=assessment, user=request.user
    ).select_related("question")

    if not assessment.was_viewed:
        assessment.was_viewed = True
        assessment.save(update_fields=["was_viewed"])

    if not user_answers_qs.exists() and assessment.status not in [
        "RESULTS_AVAILABLE",
        "CORRECTION_EXPIRED",
        "CORRECTING",
    ]:
        messages.error(request, "Aún no has completado esta evaluación.")
        return redirect("assessment:take_assessment", pk=assessment.pk)

    assessment_context = get_assessment_context(request.user, user_copy)
    is_correcting = assessment_context["status"] == "CORRECTING"

    context = {
        "assessment": assessment,
        "user_copy": user_copy,
        "user_answers": user_answers_qs,
        "is_correcting": is_correcting,
        "page_title": "Resultados",
        "assessment_context": assessment_context,
    }
    return render(request, "assessment/view_results.html", context)


@login_required
@require_GET
def get_assessment_status(request, assessment_pk):
    try:
        assessment = Assessment.objects.get(pk=assessment_pk, user=request.user)
        progress = 0
        if assessment.total_questions_expected > 0:
            progress = round(
                (assessment.questions_processed / assessment.total_questions_expected)
                * 100
            )
        data = {
            "status": assessment.status,
            "progress": progress,
            "processed_count": assessment.questions_processed,
            "total_count": assessment.total_questions_expected,
        }
        return JsonResponse(data)
    except Assessment.DoesNotExist:
        return JsonResponse({"status": "NOT_FOUND", "progress": 0}, status=404)
    except Exception as e:
        return JsonResponse({"status": "ERROR", "message": str(e)}, status=500)


@login_required
@require_GET
def get_assessment_panel_content(request, copy_pk):
    try:
        user_copy = ContentCopy.objects.get(pk=copy_pk, user=request.user)
    except ContentCopy.DoesNotExist:
        # Aquí devolvemos un HTML vacío o error porque es una llamada AJAX para un panel
        return JsonResponse({"html": "<div class='alert alert-danger'>Copia no encontrada</div>"})

    assessment_context = get_assessment_context(request.user, user_copy)

    html = render_to_string(
        "assessment/partials/assessment_status_block.html",
        {"assessment_context": assessment_context},
        request=request,
    )
    return JsonResponse({"html": html})


@login_required
@require_POST
def retry_assessment_generation(request, assessment_pk):
    try:
        assessment = Assessment.objects.select_related("content_copy").get(
            pk=assessment_pk,
            user=request.user,
        )
    except Assessment.DoesNotExist:
        messages.error(request, "Evaluación no encontrada.")
        return redirect("study_room:copy_directory_root")

    user_copy = assessment.content_copy
    generate_assessment_from_content_task.delay(assessment.id)
    messages.info(request, "Reintentando generación...")
    return redirect(reverse("study_room:edit_copy", kwargs={"pk": user_copy.pk}))


@login_required
@require_POST
def cancel_assessment_generation(request, assessment_pk):
    try:
        assessment = Assessment.objects.get(pk=assessment_pk, user=request.user)
    except Assessment.DoesNotExist:
        messages.error(request, "Evaluación no encontrada.")
        return redirect("study_room:copy_directory_root")

    user_copy = assessment.content_copy

    cancellable_statuses = [
        Assessment.AssessmentStatus.PENDING,
        Assessment.AssessmentStatus.GENERATION_FAILED_RETRYABLE,
        Assessment.AssessmentStatus.GENERATION_FAILED_QUOTA,
        Assessment.AssessmentStatus.GENERATION_FAILED_FATAL,
    ]

    if assessment.status in cancellable_statuses:
        assessment.status = Assessment.AssessmentStatus.USER_CANCELLED
        assessment.save(update_fields=["status"])
        messages.success(request, "Evaluación cancelada.")
    else:
        messages.error(request, "No se puede cancelar en este estado.")

    return redirect(reverse("study_room:edit_copy", kwargs={"pk": user_copy.pk}))


@login_required
@require_POST
def mark_as_viewed_ajax(request, pk):
    try:
        assessment = Assessment.objects.get(pk=pk, user=request.user)
        if not assessment.was_viewed:
            assessment.was_viewed = True
            assessment.save(update_fields=["was_viewed"])
            return JsonResponse({"status": "success", "message": "Marcado como visto."})
        return JsonResponse({"status": "already_viewed", "message": "Ya visto."})
    except Assessment.DoesNotExist:
        return JsonResponse({"status": "error", "message": "No encontrado"}, status=404)


@login_required
def take_assessment_demo(request):
    # Mock data for demo...
    return render(request, "assessment/take_assessment.html", {})
