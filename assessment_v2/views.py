from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext as _
import re

from .models.main import Exam
from .services.quotas import QuotaService
from orchestrator.tasks import generate_exam_task
from contents.models import ContentMaterial, ContentCopy
from contents.utils import extract_toc_from_markdown, extract_content_range
from academic_structure.models import Subject

class ExamCreateView(LoginRequiredMixin, View):
    template_name = 'assessment_v2/exam_create.html'

    def _deduce_academic_parameters(self, subject):
        """
        Implementación del algoritmo V06DOC_LOGIC_MAPPING (V1.1) usando Regex.
        """
        if not subject:
            return 'ARCH_GEN', 'SUB_GEN', 'ITIN_GEN', 'LVL_B'

        name_norm = subject.name.lower()
        
        # 1. ARQUETIPO (Regex Estructural)
        if re.search(r'(lengua|idioma|language)', name_norm):
            archetype = 'ARCH_LANG'
            sub_archetype = 'SUB_LIN_CERT'
        else:
            try:
                branch = subject.academic_year.degree.branch.name.lower()
                if 'artes' in branch or 'humanidades' in branch:
                    archetype = 'ARCH_HUM'
                    sub_archetype = 'SUB_HUM_GEN'
                elif 'salud' in branch or 'medicina' in branch:
                    archetype = 'ARCH_HEALTH'
                    sub_archetype = 'SUB_SAN_GEN'
                elif 'ingeniería' in branch or 'arquitectura' in branch or 'ciencias' in branch:
                    archetype = 'ARCH_TECH'
                    sub_archetype = 'SUB_TEC_GEN'
                elif 'sociales' in branch or 'jurídicas' in branch:
                    archetype = 'ARCH_SOC'
                    sub_archetype = 'SUB_SOC_GEN'
                else:
                    archetype = 'ARCH_GEN'
                    sub_archetype = 'SUB_GEN'
            except AttributeError:
                archetype = 'ARCH_GEN'
                sub_archetype = 'SUB_GEN'

        # 2. ITINERARIO (Regex Explícito)
        if re.search(r'\bmaior\b', name_norm):
            itinerary = 'ITIN_MAI'
        elif re.search(r'\bminor\b', name_norm):
            itinerary = 'ITIN_MIN'
        else:
            if subject.subject_type in [Subject.SubjectType.CORE, Subject.SubjectType.MANDATORY, Subject.SubjectType.BASIC]:
                itinerary = 'ITIN_MAI'
            elif subject.subject_type == Subject.SubjectType.OPTIONAL:
                itinerary = 'ITIN_MIN'
            else:
                itinerary = 'ITIN_GEN'

        # 3. NIVEL (Regex Semántico)
        level = None
        if re.search(r'\b(inicial|básico|basico|a1|a2|intro)\b', name_norm):
             level = 'LVL_A'
        elif re.search(r'\b(intermedio|b1|b2)\b', name_norm):
             level = 'LVL_B'
        elif re.search(r'\b(avanzado|superior|c1|c2)\b', name_norm):
             level = 'LVL_C'
             
        if not level: # Fallback por Año
            year = subject.academic_year.year if subject.academic_year else 1
            if year <= 2: level = 'LVL_A'
            elif year == 3: level = 'LVL_B'
            else: level = 'LVL_C'

        return archetype, sub_archetype, itinerary, level

    def get(self, request):
        content_id = request.GET.get('content_id')
        context = {}
        
        if content_id:
            try:
                content = ContentMaterial.objects.get(id=content_id)
            except ContentMaterial.DoesNotExist:
                copy = get_object_or_404(ContentCopy, id=content_id)
                content = copy.original_content
            
            context['content_material'] = content
            context['toc'] = extract_toc_from_markdown(content.markdown_content)
            
            subject = content.subject.first()
            if subject:
                arch, sub, itin, lvl = self._deduce_academic_parameters(subject)
                context['system_deduction'] = {
                    'archetype': arch, 'itinerary': itin, 'level': lvl,
                    'subject_name': subject.name
                }
            
        return render(request, self.template_name, context)

    def post(self, request):
        allowed, reason = QuotaService.check_exam_eligibility(request.user)
        if not allowed:
            messages.error(request, f"Límite alcanzado: {reason}")
            return redirect('assessment_v2:exam_create')

        content_id = request.POST.get('content_id')
        start_index = request.POST.get('start_index')
        end_index = request.POST.get('end_index')
        
        content = get_object_or_404(ContentMaterial, id=content_id)
        subject = content.subject.first()

        if start_index and end_index:
            context_text = extract_content_range(content.markdown_content, start_index, end_index)
        else:
            context_text = content.markdown_content[:50000]

        archetype, sub_archetype, itinerary, level = self._deduce_academic_parameters(subject)

        exam = Exam.objects.create(
            user=request.user,
            archetype_id=archetype,
            sub_archetype_id=sub_archetype,
            itinerary_id=itinerary,
            pedagogical_level=level,
            status=Exam.STATUS_PENDING
        )

        generate_exam_task.delay(exam.uuid, context_text=context_text, topic=content.title)
        
        return redirect('assessment_v2:exam_generating', uuid=exam.uuid)

class ExamGeneratingView(LoginRequiredMixin, DetailView):
    model = Exam
    template_name = 'assessment_v2/exam_generating.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    def get_queryset(self): return Exam.objects.filter(user=self.request.user)

class ExamStatusView(LoginRequiredMixin, View):
    def get(self, request, uuid):
        exam = get_object_or_404(Exam, uuid=uuid, user=request.user)
        if exam.status == Exam.STATUS_READY:
            url = reverse('assessment_v2:take_exam', args=[uuid])
            return JsonResponse({'status': 'READY', 'url': url, 'HX-Redirect': url})
        elif exam.status == Exam.STATUS_ERROR:
             return JsonResponse({'status': 'ERROR', 'message': exam.error_log})
        return JsonResponse({'status': exam.status})

class ExamTakeView(LoginRequiredMixin, DetailView):
    model = Exam
    template_name = 'assessment_v2/exam_take_placeholder.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    def get_queryset(self): return Exam.objects.filter(user=self.request.user, status=Exam.STATUS_READY)
