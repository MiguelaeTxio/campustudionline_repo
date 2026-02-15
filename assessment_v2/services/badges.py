# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/badges.py
from assessment_v2.models.main import Exam
from django.db.models import Count

class BadgeService:
    """
    Servicio centralizado para la gestión de indicadores visuales (Badges).
    Sincronizado con los estados de la tarea Celery.
    
    ---
    
    Centralized service for visual indicator (Badge) management.
    Synchronized with Celery task states.
    """
    @staticmethod
    def get_user_badges(user):
        """
        Calculates the number of assessments in key states for a given user.
        ---
        Calcula el número de evaluaciones en estados clave para un usuario dado.
        """
        if not user.is_authenticated:
            return {}
        
        status_counts = Exam.objects.filter(user=user).values('status').annotate(total=Count('status'))
        
        badges = {
            'generating': 0,
            'ready': 0,
            'grading': 0,
        }
        
        for item in status_counts:
            # PENDING or GENERATING are considered work in progress (Yellow Badge/Spinner)
            # PENDIENTE o GENERANDO se consideran trabajo en curso (Badge Amarillo/Spinner)
            if item['status'] in ['PENDING', 'GENERATING']:
                badges['generating'] += item['total']
            elif item['status'] == 'READY':
                badges['ready'] = item['total']
            elif item['status'] == 'GRADING':
                badges['grading'] += item['total']
                
        return badges
