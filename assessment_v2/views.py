# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from decimal import Decimal
import json
import re

from .models.main import Exam, Submission
from .services.engine.factory import ExamFactory
from .services.quotas import QuotaService
from .services.engine.logic import AcademicDeductor, GradingOrchestrator
from orchestrator.tasks import generate_exam_task
from contents.models import ContentMaterial, ContentCopy
from contents.utils import extract_toc_from_markdown, extract_content_range

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
                # Automatiza los metadatos usando el estándar de calidad de la plataforma
                metadata = AcademicDeductor.get_context_metadata(subject, context_title=content.title)
                
                # Use the centralized utility to get a clean, filtered TOC
                # Usa la utilidad centralizada para obtener un TOC limpio y filtrado
                toc = extract_toc_from_markdown(content.markdown_content, filter_metadata=True)
                
                context.update({
                    'content_material': content,
                    'toc': toc,
                    'system_deduction': {
                        'subject_name': subject.name,
                        'archetype': metadata['archetype_id'],
                        'sub_archetype': metadata['sub_archetype_id'], # Fixed: Using dynamic sub_archetype / Corregido: Uso de sub_archetype dinámico
                        'itinerary': metadata['itinerary_id'],
                        'level': metadata['pedagogical_level']
                    }
                })
        return render(request, self.template_name, context)

    def post(self, request):
        # Validate quotas before consuming API resources
        # Valida las cuotas antes de consumir recursos de la API
        allowed, reason = QuotaService.check_exam_eligibility(request.user)
        if not allowed:
            messages.error(request, f"Límite: {reason}")
            return redirect('assessment_v2:exam_create')

        content = get_object_or_404(ContentMaterial, id=request.POST.get('content_id'))
        
        # SINE QUA NON: Retrieve the mandatory study copy for this user/content
        # SINE QUA NON: Recupera la copia de estudio obligatoria para este usuario/contenido
        content_copy = get_object_or_404(ContentCopy, user=request.user, original_content=content)
        
        subject = content.subject.first()
        metadata = AcademicDeductor.get_context_metadata(subject, context_title=content.title)
        
        # Use the centralized utility to correctly extract the content range
        # Usa la utilidad centralizada para extraer correctamente el rango de contenido
        start_idx = request.POST.get('start_index')
        end_idx = request.POST.get('end_index')
        context_text = extract_content_range(content.markdown_content, start_idx, end_idx)

        # Relational header creation
        # Creación de la cabecera relacional
        exam = Exam.objects.create(
            user=request.user,
            content_copy=content_copy,  # LINKED: Business Rule Compliance
            archetype_id=metadata['archetype_id'],
            sub_archetype_id=metadata['sub_archetype_id'], # IDENTITY PERSISTENCE / PERSISTENCIA DE IDENTIDAD
            itinerary_id=metadata['itinerary_id'],
            pedagogical_level=metadata['pedagogical_level']
        )
        
        # Launch asynchronous generation task with scoped context
        # Lanza la tarea de generación asíncrona con el contexto acotado
        generate_exam_task.delay(exam.uuid, context_text=context_text[:40000], topic=content.title)
        return redirect('assessment_v2:exam_generating', uuid=exam.uuid)

class ExamGeneratingView(LoginRequiredMixin, DetailView):
    """
    Displays the generation progress feedback.
    ---
    Muestra el feedback del progreso de generación.
    """
    model = Exam
    template_name = 'assessment_v2/exam_generating.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

class ExamStatusView(LoginRequiredMixin, View):
    """
    Endpoint for UI polling to check generation status.
    ---
    Endpoint para el sondeo de la interfaz para verificar el estado de generación.
    """
    def get(self, request, uuid):
        exam = get_object_or_404(Exam, uuid=uuid, user=request.user)
        if exam.status == 'READY':
            return JsonResponse({'status': 'READY', 'url': reverse('assessment_v2:take_exam', args=[uuid])})
        return JsonResponse({'status': exam.status})

class ExamTakeView(LoginRequiredMixin, DetailView):
    """
    Main interface for taking the exam using relational widget rendering.
    ---
    Interfaz principal para realizar el examen usando el renderizado de widgets relacionales.
    """
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
            
            # Instantiate strategy via factory to access the quality-grading engine
            # Instancia la estrategia a través de la factoría para acceder al motor de calificación
            strategy = ExamFactory.get_strategy(
                archetype_id=exam.archetype_id, 
                sub_archetype_id=exam.sub_archetype_id,
                pedagogical_level=exam.pedagogical_level, 
                itinerary_id=exam.itinerary_id
            )
            
            with transaction.atomic():
                # Persist official submission (V06DOC_TEMPLATES)
                # Persiste la entrega oficial (V06DOC_TEMPLATES)
                submission = Submission.objects.create(
                    exam=exam,
                    student_responses=data,
                    submitted_at=timezone.now()
                )
                
                # EXECUTE SPECIALIZED GRADING (Handles Section-Level Kill Switches)
                # EJECUTA LA CALIFICACIÓN ESPECIALIZADA (Gestiona anulación de secciones)
                GradingOrchestrator.grade_submission(submission, strategy)

                exam.status = 'GRADED'
                exam.save(update_fields=['status', 'updated_at'])

            return JsonResponse({'status': 'SUCCESS', 'url': reverse('assessment_v2:exam_report', args=[uuid])})
        except Exception as e:
            return JsonResponse({'status': 'ERROR', 'message': str(e)}, status=400)

class ExamReportView(LoginRequiredMixin, DetailView):
    """
    Displays the detailed grading report (V06DOC_METADATA).
    ---
    Muestra el informe detallado de calificación (V06DOC_METADATA).
    """
    model = Exam
    template_name = 'assessment_v2/exam_report.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submission'] = get_object_or_404(Submission, exam=self.object)
        return context
