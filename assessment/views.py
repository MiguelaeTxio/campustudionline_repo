# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment/views.py
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST, require_GET
from django.db import transaction
from django.http import JsonResponse
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
def generate_ai_assessment(request, copy_pk):
    user_copy = get_object_or_404(ContentCopy, pk=copy_pk, user=request.user)
    redirect_url = reverse("study_room:edit_copy", kwargs={"pk": user_copy.pk})

    # [REFACTORIZADO] Ampliamos la lista de estados que bloquean la creación para
    # incluir los estados de reintento y los que esperan acción del usuario.
    # Una nueva evaluación solo se permite si la anterior ha terminado (con o sin éxito).
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
            "Ya hay una evaluación en curso o esperando tu acción para este material. Por favor, espera a que finalice o complétala.",
        )
        return redirect(redirect_url)

    limit_data = check_user_assessment_limits(request.user)
    if not limit_data["can_create_new"]:
        messages.error(
            request,
            "Has alcanzado tu límite de evaluaciones diarias o semanales. Por favor, inténtalo más tarde.",
        )
        return redirect(redirect_url)

    try:
        assessment = Assessment.objects.create(
            user=request.user,
            content_copy=user_copy,
            status="PENDING",
        )
        # generate_assessment_from_content_task.delay(assessment.id)
        messages.success(
            request,
            "¡Estupendo! Hemos puesto tu autoevaluación en la cola de generación. Te avisaremos cuando esté lista.",
        )

    except Exception as e:
        logger.error(
            f"GENERATE_VIEW: Error inesperado al crear evaluación para copy {copy_pk}: {e}",
            exc_info=True,
        )
        messages.error(
            request,
            f"Hubo un error inesperado al iniciar la creación de tu evaluación: {e}",
        )

    return redirect(redirect_url)


@login_required
def take_assessment(request, pk):
    assessment = get_object_or_404(
        Assessment.objects.select_related("content_copy__original_content").prefetch_related("questions"),
        pk=pk,
        user=request.user,
    )
    user_copy = assessment.content_copy

    if assessment.status != "COMPLETED":
        messages.warning(
            request,
            f"Esta evaluación aún no está lista o ya está en corrección. Su estado actual es: {assessment.get_status_display()}.",
        )
        return redirect(reverse("study_room:edit_copy", kwargs={"pk": user_copy.pk}))

    if UserAnswer.objects.filter(
        question__assessment=assessment, user=request.user
    ).exists():
        messages.info(
            request, "Ya has completado esta evaluación. Redirigiendo a tus resultados."
        )
        return redirect("assessment:view_results", pk=assessment.pk)

    if not assessment.was_viewed:
        assessment.was_viewed = True
        assessment.save(update_fields=["was_viewed"])
        log_timestamp(
            f"TAKE_ASSESSMENT: Marcado Assessment ID {assessment.id} como 'visto'."
        )

    context = {
        "assessment": assessment,
        "user_copy": user_copy,
        "page_title": "Completar Autoevaluación",
    }
    return render(request, "assessment/take_assessment.html", context)


@login_required
@require_POST
def submit_assessment(request, pk):
    assessment = get_object_or_404(
        Assessment.objects.select_related("content_copy"), pk=pk, user=request.user
    )
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
            assessment.status = "CORRECTING"
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
            log_timestamp(
                f"SUBMIT_VIEW: Encolada tarea de corrección para Assessment ID: {assessment.id}"
            )
            messages.success(
                request,
                "¡Hemos recibido tus respuestas! La corrección ha comenzado. Te avisaremos cuando tus resultados estén listos.",
            )
    except Exception as e:
        logger.error(
            f"Error en submit_assessment para Assessment ID {assessment.id}: {e}",
            exc_info=True,
        )
        messages.error(
            request,
            "Hubo un error inesperado al procesar tus respuestas. Por favor, inténtalo de nuevo.",
        )
        return redirect(redirect_url)

    return redirect(redirect_url)


@login_required
def view_results(request, pk):
    assessment = get_object_or_404(
        Assessment.objects.select_related("content_copy__original_content").prefetch_related(
            "questions__user_answers"
        ),
        pk=pk,
        user=request.user,
    )
    user_copy = assessment.content_copy
    user_answers_qs = UserAnswer.objects.filter(
        question__assessment=assessment, user=request.user
    ).select_related("question")

    if not assessment.was_viewed:
        assessment.was_viewed = True
        assessment.save(update_fields=["was_viewed"])
        log_timestamp(
            f"VIEW_RESULTS: Marcado Assessment ID {assessment.id} como 'visto'."
        )

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
        "page_title": "Resultados de la Autoevaluación",
        "assessment_context": assessment_context,
    }
    return render(request, "assessment/view_results.html", context)


@login_required
@require_GET
def get_assessment_status(request, assessment_pk):
    log_timestamp(f"API_STATUS: Petición recibida para Assessment ID: {assessment_pk}")
    try:
        assessment = get_object_or_404(Assessment, pk=assessment_pk, user=request.user)
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
        log_timestamp(
            f"API_STATUS: Enviando respuesta para Assessment ID {assessment_pk}: {data}"
        )
        return JsonResponse(data)
    except Assessment.DoesNotExist:
        log_timestamp(f"API_STATUS: Assessment ID {assessment_pk} NO ENCONTRADO.")
        return JsonResponse({"status": "NOT_FOUND", "progress": 0}, status=404)
    except Exception as e:
        log_timestamp(
            f"API_STATUS: ERROR en vista para Assessment ID {assessment_pk}: {e}"
        )
        return JsonResponse({"status": "ERROR", "message": str(e)}, status=500)


@login_required
@require_GET
def get_assessment_panel_content(request, copy_pk):
    user_copy = get_object_or_404(ContentCopy, pk=copy_pk, user=request.user)
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
    assessment = get_object_or_404(
        Assessment.objects.select_related("content_copy"),
        pk=assessment_pk,
        user=request.user,
    )
    # [REFACTORIZADO] El sistema ahora reintenta automáticamente. Esta vista está obsoleta.
    messages.error(
        request,
        "Esta función ya no es necesaria. El sistema reintentará generar tu evaluación automáticamente si ocurre un problema.",
    )
    user_copy = assessment.content_copy
    return redirect(reverse("study_room:edit_copy", kwargs={"pk": user_copy.pk}))


@login_required
@require_POST
def cancel_assessment_generation(request, assessment_pk):
    assessment = get_object_or_404(Assessment, pk=assessment_pk, user=request.user)
    # [REFACTORIZADO] La cancelación manual ya no es soportada por la nueva lógica de estados.
    messages.error(
        request,
        "La cancelación manual de una generación en curso ya no está disponible.",
    )
    user_copy = assessment.content_copy
    return redirect(reverse("study_room:edit_copy", kwargs={"pk": user_copy.pk}))


@login_required
@require_POST
def mark_as_viewed_ajax(request, pk):
    assessment = get_object_or_404(Assessment, pk=pk, user=request.user)
    if not assessment.was_viewed:
        assessment.was_viewed = True
        assessment.save(update_fields=["was_viewed"])
        log_timestamp(
            f"MARK_AS_VIEWED_AJAX: Marcado Assessment ID {assessment.id} como 'visto'."
        )
        return JsonResponse({"status": "success", "message": "Marcado como visto."})
    return JsonResponse(
        {"status": "already_viewed", "message": "Ya estaba marcado como visto."}
    )


@login_required
def take_assessment_demo(request):
    """
    Renders the take_assessment template with mock data
    to be used exclusively by the guided tour.
    """

    class FakeOriginalContent:
        title = "Contenido de Demostración"

    class FakeUserCopy:
        pk = "00000000-0000-0000-0000-000000000000"
        original_content = FakeOriginalContent()

    class FakeAssessment:
        pk = 9999

        class FakeQuestions:
            def all(self):
                class FakeQuestion:
                    def __init__(self, pk, text):
                        self.pk = pk
                        self.question_text = text

                return [
                    FakeQuestion(1, "¿Cuál es el propósito de la visita guiada?"),
                    FakeQuestion(
                        2, "Explica la función del botón 'Enviar para Evaluación'."
                    ),
                    FakeQuestion(
                        3,
                        "Describe qué información se encuentra en el encabezado de esta página.",
                    ),
                ]

        questions = FakeQuestions()

    context = {
        "assessment": FakeAssessment(),
        "user_copy": FakeUserCopy(),
        "page_title": "Demostración de Autoevaluación",
    }
    return render(request, "assessment/take_assessment.html", context)
