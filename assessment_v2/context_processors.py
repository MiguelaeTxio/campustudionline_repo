from .services.badges import BadgeService

def assessment_badges(request):
    """
    Inyecta los contadores de exámenes en todas las plantillas.
    """
    if request.user.is_authenticated:
        return {
            'assessment_badges': BadgeService.get_user_badges(request.user)
        }
    return {'assessment_badges': {}}
