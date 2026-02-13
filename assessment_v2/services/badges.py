# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/badges.py
from assessment_v2.models.main import Exam
from django.db.models import Count

class BadgeService:
    """
    Servicio centralizado para la gestión de indicadores visuales (Badges).
    Sincronizado con los estados de la tarea Celery.
    """
    @staticmethod
    def get_user_badges(user):
        if not user.is_authenticated:
            return {}
        
        status_counts = Exam.objects.filter(user=user).values('status').annotate(total=Count('status'))
        
        badges = {
            'generating': 0,
            'ready': 0,
            'grading': 0,
        }
        
        for item in status_counts:
            # PENDING o GENERATING se consideran trabajo en curso (Badge Amarillo/Spinner)
            if item['status'] in [Exam.STATUS_PENDING, Exam.STATUS_GENERATING]:
                badges['generating'] += item['total']
            elif item['status'] == Exam.STATUS_READY:
                badges['ready'] = item['total']
            # 'grading' se implementará en la fase de corrección
                
        return badges
