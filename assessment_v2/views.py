# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.db import transaction
from decimal import Decimal
import json

from .models.main import Exam, Submission, ExamItem
from .services.engine.factory import ExamFactory
from .services.quotas import QuotaService
from .services.engine.logic import AcademicDeductor
from orchestrator.tasks import generate_exam_task
from contents.models import ContentMaterial, ContentCopy

class ExamCreateView(LoginRequiredMixin, View):
    """
    Handles the configuration and launching of a new assessment session.
    ---
    Gestiona la configuración y el lanzamiento de una nueva sesión de evaluación.
    """
    template_name = 'assessment_v2/exam_create.html'

    def get(self, request):
        content_id = request.GET.get('content_id')
        context = {}
        if content_id:
            try:
                content = ContentMaterial.objects.get(id=content_id)
            except (ContentMaterial.DoesNotExist, ValueError):
                copy = get_object_or_404(ContentCopy, id=content_id, user=request.user)
                content = copy.original_content
            
            subject = content.subject.first()
            if subject:
                # Automate metadata using the platform's quality standard
                metadata = AcademicDeductor.get_context_metadata(subject)
                context.update({
                    'content_material': content,
                    'system_deduction': metadata
                })
        return render(request, self.template_name, context)

    def post(self, request):
        # Validate quotas before consuming API resources
        allowed, reason = QuotaService.check_exam_eligibility(request.user)
        if not allowed:
            messages.error(request, f"Límite: {reason}")
            return redirect('assessment_v2:exam_create')

        content = get_object_or_404(ContentMaterial, id=request.POST.get('content_id'))
        subject = content.subject.first()
        metadata = AcademicDeductor.get_context_metadata(subject)
        
        # Relational header creation
        exam = Exam.objects.create(
            user=request.user,
            archetype_id=metadata['archetype_id'],
            itinerary_id=metadata['itinerary_id'],
            pedagogical_level=metadata['pedagogical_level']
        )
        
        # Launch asynchronous generation task (V06DOC_STRUCTURE)
        generate_exam_task.delay(exam.uuid, context_text=content.markdown_content[:40000], topic=content.title)
        return redirect('assessment_v2:exam_generating', uuid=exam.uuid)

class ExamGeneratingView(LoginRequiredMixin, DetailView):
    """Displays the generation progress feedback."""
    model = Exam
    template_name = 'assessment_v2/exam_generating.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

class ExamStatusView(LoginRequiredMixin, View):
    """Endpoint for UI polling to check generation status."""
    def get(self, request, uuid):
        exam = get_object_or_404(Exam, uuid=uuid, user=request.user)
        if exam.status == 'READY':
            return JsonResponse({'status': 'READY', 'url': reverse('assessment_v2:take_exam', args=[uuid])})
        return JsonResponse({'status': exam.status})

class ExamTakeView(LoginRequiredMixin, DetailView):
    """Main interface for taking the exam using relational widget rendering."""
    model = Exam
    template_name = 'assessment_v2/exam_take.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_queryset(self):
        return Exam.objects.filter(user=self.request.user, status='READY').prefetch_related('sections__items')

class ExamSubmitView(LoginRequiredMixin, View):
    """
    Processes student submissions and executes the grading logic.
    ---
    Procesa las entregas de los estudiantes y ejecuta la lógica de calificación.
    """
    def post(self, request, uuid):
        exam = get_object_or_404(Exam, uuid=uuid, user=request.user, status='READY')
        try:
            data = json.loads(request.body)
            responses = data.get('responses', {})
            
            # Instantiate strategy via factory to access the quality-grading engine
            strategy = ExamFactory.get_strategy(exam.archetype_id, exam.pedagogical_level, exam.itinerary_id)
            
            total_score, report = Decimal('0.0'), {}
            with transaction.atomic():
                for item_id, student_input in responses.items():
                    item = ExamItem.objects.get(id=item_id, section__exam=exam)
                    score, item_report = strategy.grade_item(item, student_input)
                    total_score += score
                    report[item_id] = {"score": float(score), "report": item_report}

                # Persist official submission (V06DOC_TEMPLATES)
                Submission.objects.create(
                    exam=exam,
                    student_responses=responses,
                    grading_report=report,
                    final_score=max(total_score, Decimal('0.0'))
                )
                exam.status = 'GRADED'
                exam.save(update_fields=['status'])

            return JsonResponse({'status': 'SUCCESS', 'url': reverse('assessment_v2:exam_report', args=[uuid])})
        except Exception as e:
            return JsonResponse({'status': 'ERROR', 'message': str(e)}, status=400)
