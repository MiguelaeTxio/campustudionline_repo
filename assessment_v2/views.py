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
import random

from .models.main import Exam, Submission
from .services.engine.factory import ExamFactory
from .services.quotas import QuotaService
from .services.engine.logic import GradingOrchestrator
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
            
            # Use the centralized utility to get a clean, filtered TOC
            # Usa la utilidad centralizada para obtener un TOC limpio y filtrado
            toc = extract_toc_from_markdown(content.markdown_content, filter_metadata=True)
            
            context.update({
                'content_material': content,
                'toc': toc,
            })
        return render(request, self.template_name, context)

    def post(self, request):
        # Validate quotas before consuming API resources
        # Valida las cuotas antes de consumir recursos de la API
        allowed, reason = QuotaService.check_exam_eligibility(request.user)
        content = get_object_or_404(ContentMaterial, id=request.POST.get('content_id'))
        content_copy = get_object_or_404(ContentCopy, user=request.user, original_content=content)

        if not allowed:
            messages.error(request, f"Límite: {reason}")
            return redirect('study_room:edit_copy', pk=content_copy.pk)
        
        # Use the centralized utility to correctly extract the content range
        # Usa la utilidad centralizada para extraer correctamente el rango de contenido
        start_idx = request.POST.get('start_index')
        end_idx = request.POST.get('end_index')
        context_text = extract_content_range(content.markdown_content, start_idx, end_idx)

        # [PASO 6 H06 - S031] Selector de dificultad UGR/ENDURECIDO, elegido
        # por el alumno en el formulario. Nunca deducido por la IA. Valor no
        # reconocido (manipulación de POST) cae de forma segura al default
        # certificado (UGR), nunca a ENDURECIDO.
        difficulty_mode = request.POST.get('difficulty_mode', Exam.DifficultyMode.UGR)
        if difficulty_mode not in Exam.DifficultyMode.values:
            difficulty_mode = Exam.DifficultyMode.UGR

        # Relational header creation — minimal, no AI classification here.
        # Classification is delegated exclusively to generate_exam_task (single responsibility).
        # Creación de la cabecera relacional — mínima, sin clasificación IA aquí.
        # La clasificación se delega exclusivamente a generate_exam_task (responsabilidad única).
        # Ref: V06DOC_LOGIC_MAPPING V1.3 — ERROR 5 (doble clasificación eliminada).
        exam = Exam.objects.create(
            user=request.user,
            content_copy=content_copy,
            status='PENDING',
            difficulty_mode=difficulty_mode
        )
        
        # Launch asynchronous generation task with scoped context
        # Lanza la tarea de generación asíncrona con el contexto acotado
        generate_exam_task.delay(exam.uuid, context_text=context_text[:40000], topic=content.title)
        
        # Redirección con mensaje para disparar el modal en la vista de edición de copia
        messages.success(request, "Su evaluación se está generando. Ya le avisaremos cuando esté lista.", extra_tags="show_generating_modal")
        return redirect('study_room:edit_copy', pk=content_copy.pk)

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
        # [HITO 06] Enforce 24h expiration rule (Tolerance Zero)
        return Exam.objects.filter(
            user=self.request.user, 
            status='READY',
            expiration_date__gt=timezone.now()
        ).prefetch_related('sections__items')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exam = context['object']
        
        # BARRERA DE FUEGO (Data Leak Protection): Sanitización en memoria
        # Aseguramos que la vista NUNCA entregue metadatos críticos a la plantilla HTML
        for section in exam.sections.all():
            for item in section.items.all():
                if isinstance(item.content, dict) and item.content.get('options'):
                    clean_opts = []
                    import ast
                    for opt in item.content['options']:
                        # 1. Rescatar diccionarios convertidos a string accidentalmente
                        if isinstance(opt, str) and opt.strip().startswith('{'):
                            try:
                                opt = ast.literal_eval(opt)
                            except:
                                pass
                        # 2. Estandarizar salida asegurando que SIEMPRE hay un 'text' limpio y NADA MAS
                        if isinstance(opt, dict):
                            clean_opts.append({'text': str(opt.get('text', opt.get('value', str(opt))))})
                        else:
                            clean_opts.append({'text': str(opt)})
                    item.content['options'] = clean_opts

                # [S025] W-MIX-MATCH: las dos columnas se derivan de
                # grading_logic.pairs, que es la unica fuente de verdad del
                # emparejamiento. La IA no rellena content.options ni
                # content.targets para este widget, asi que la plantilla
                # pintaba ambas columnas vacias y el ejercicio era
                # irrealizable. Se deriva aqui, en memoria, sin persistir.
                #
                # Los destinos se BARAJAN con una semilla estable (el uuid del
                # item): si se mostrasen en el mismo orden que los elementos,
                # el ejercicio se resolveria emparejando fila con fila sin
                # saber la materia. La semilla fija evita que el orden cambie
                # al recargar la pagina a mitad de examen.
                if getattr(item, 'widget_id', None) == 'W-MIX-MATCH':
                    raw_pairs = item.grading_logic.get('pairs') if isinstance(item.grading_logic, dict) else None
                    parejas = []
                    if isinstance(raw_pairs, list):
                        for p in raw_pairs:
                            if isinstance(p, dict) and p.get('izquierdo') is not None:
                                parejas.append((str(p.get('izquierdo')), str(p.get('derecho', ''))))
                    elif isinstance(raw_pairs, dict):
                        parejas = [(str(k), str(v)) for k, v in raw_pairs.items()]

                    if parejas:
                        if not isinstance(item.content, dict):
                            item.content = {}
                        item.content['options'] = [{'text': izq} for izq, _ in parejas]
                        destinos = [der for _, der in parejas]
                        # [PASO 6 H06 - S031] Modo ENDURECIDO: candidato de
                        # S029 ("distractores extra en W-MIX-MATCH"). Los
                        # señuelos viven en grading_logic.distractors (nunca
                        # se persisten en content), no corresponden a ningún
                        # 'izquierdo' real y por tanto nunca pueden puntuar
                        # como par correcto en _grade_mat_link -- solo amplían
                        # la columna de destino que ve el alumno.
                        raw_distractors = item.grading_logic.get('distractors') if isinstance(item.grading_logic, dict) else None
                        if isinstance(raw_distractors, list):
                            destinos += [str(d) for d in raw_distractors if d]
                        random.Random(str(item.uuid)).shuffle(destinos)
                        item.content['targets'] = destinos

                # [S025] BARAJADO DE PRESENTACION — validez del instrumento.
                # La IA emite las opciones con la solucion en primer lugar de forma
                # sistematica: verificado en los examenes 228 y 229, donde los doce
                # huecos de cloze tenian la respuesta correcta como primera opcion.
                # Sin barajar, la seccion se resuelve al 100% eligiendo siempre la
                # primera opcion, sin conocer la materia. Agravado porque CLO-MULTI
                # va con no_negative_marking y RBT-CANON no penaliza: ahi acertar por
                # azar sale gratis.
                #
                # Se baraja aqui, en presentacion, y no en la generacion, por dos
                # razones: cubre tambien los examenes ya generados, y deja intacto el
                # orden almacenado, del que depende la resolucion posicional de
                # correct_answer ('C' = tercera opcion) en _choice_equivalents.
                # La semilla es estable (uuid del item, y gap_id en el cloze) para que
                # el orden no cambie al recargar la pagina a mitad de examen.
                if isinstance(item.content, dict):
                    semilla = str(item.uuid)

                    opciones = item.content.get('options')
                    if isinstance(opciones, list) and len(opciones) > 1:
                        barajadas = list(opciones)
                        random.Random(semilla + ':options').shuffle(barajadas)
                        item.content['options'] = barajadas

                    grupos = item.content.get('cloze_options')
                    if isinstance(grupos, list) and grupos:
                        nuevos = []
                        for grupo in grupos:
                            if (isinstance(grupo, dict)
                                    and isinstance(grupo.get('options'), list)
                                    and len(grupo['options']) > 1):
                                ops = list(grupo['options'])
                                random.Random(semilla + ':' + str(grupo.get('gap_id'))).shuffle(ops)
                                grupo = dict(grupo, options=ops)
                            nuevos.append(grupo)
                        item.content['cloze_options'] = nuevos
        
        return context

class ExamSubmitView(LoginRequiredMixin, View):
    """
    Processes student submissions and executes the grading logic.
    ---
    Procesa las entregas de los estudiantes y ejecuta la lógica de calificación.
    """
    def post(self, request, uuid):
        exam = get_object_or_404(Exam, uuid=uuid, user=request.user, status='READY')
        
        # [HITO 06] Security Check: Expiration
        if exam.expiration_date and exam.expiration_date < timezone.now():
            return JsonResponse({'status': 'ERROR', 'message': 'EXPIRED: El examen ha caducado (Regla 24h).'}, status=403)

        try:
            data = json.loads(request.body)
            
            # Instantiate strategy via factory to access the quality-grading engine
            # Instancia la estrategia a través de la factoría para acceder al motor de calificación
            strategy = ExamFactory.get_strategy(
                archetype_id=exam.archetype_id, 
                sub_archetype_id=exam.sub_archetype_id,
                pedagogical_level=exam.pedagogical_level, 
                itinerary_id=exam.itinerary_id,
                target_language_code=exam.target_language_code,
                # [PASO 6 H06 - S031] Gobierna BaseExamStrategy._is_hardened()
                # -- penalización de CLO-OPEN/CLO-MULTI en tiempo de calificación.
                difficulty_mode=exam.difficulty_mode
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

                # [PASO 5 H06 - S029] Si quedaron items en PENDING_AI_ANALYSIS
                # (DRA-HOLO, ILC-CONTEXT, DIA-INTERACT), se encola el
                # refinamiento real por IA en segundo plano. on_commit, no
                # .delay() directo: evita que el worker Celery arranque
                # antes de que esta transaccion haya confirmado la fila de
                # Submission en la base de datos.
                has_pending_refinement = any(
                    item_rep.get('pending_ai_refinement')
                    for sec_rep in (submission.grading_report or {}).get('sections', [])
                    for item_rep in sec_rep.get('items', [])
                )
                if has_pending_refinement:
                    from orchestrator.tasks import refine_pending_ai_items_task
                    transaction.on_commit(
                        lambda sid=submission.id: refine_pending_ai_items_task.delay(sid)
                    )

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
        submission = get_object_or_404(Submission, exam=self.object)
        context['submission'] = submission
        # [PASO 5 H06 - S029] Para el banner de "revision en curso por IA".
        context['has_pending_refinement'] = any(
            item_rep.get('pending_ai_refinement')
            for sec_rep in (submission.grading_report or {}).get('sections', [])
            for item_rep in sec_rep.get('items', [])
        )
        return context
