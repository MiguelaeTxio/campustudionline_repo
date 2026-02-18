import logging
from django.db import transaction
from django.apps import apps
from django.urls import reverse
from django.db.models import Prefetch, Q
from django.utils import timezone
from contents.models import UserStudyNavigation, FavoriteFolder, ContentCopy

logger = logging.getLogger(__name__)

class NavigationTreeBuilder:
    """
    Servicio encargado de construir y actualizar la estructura jerárquica
    de navegación para la Sala de Estudio de un usuario.
    Genera un JSON optimizado para renderizado en frontend.
    """

    def __init__(self, user):
        self.user = user

    def build_and_save(self):
        """
        Construye el árbol completo y lo guarda en el modelo UserStudyNavigation.
        """
        try:
            tree_structure = self._build_tree()
            
            # Update or Create (Atomic)
            UserStudyNavigation.objects.update_or_create(
                user=self.user,
                defaults={'navigation_tree': tree_structure}
            )
            logger.info(f"Árbol de navegación actualizado para usuario: {self.user.username}")
        except Exception as e:
            logger.error(f"Error construyendo árbol de navegación para {self.user.username}: {e}", exc_info=True)

    def _build_tree(self):
        return {
            "favorites": self._build_favorites_section(),
            "study_copies": self._build_copies_section(),
            "meta": {
                "user_id": self.user.id,
                "username": self.user.username
            }
        }

    def _build_favorites_section(self):
        # Obtenemos la raíz de favoritos del usuario
        root_folders = FavoriteFolder.objects.filter(
            user=self.user, 
            depth=1
        ).order_by('path')

        favorites_tree = []
        for folder in root_folders:
            folder_node = self._serialize_folder_recursive(folder)
            favorites_tree.append(folder_node)
            
        return favorites_tree

    def _serialize_folder_recursive(self, folder):
        node = {
            "id": str(folder.id),
            "name": folder.name,
            "type": "folder",
            "is_system": folder.is_system_folder,
            "folder_type": folder.folder_type,
            "url": folder.get_absolute_url() if hasattr(folder, 'get_absolute_url') else '#',
            "children": [],
            "materials": []
        }

        # Serializar Materiales dentro de la carpeta
        materials = folder.materials.filter(is_public=True).values(
            'id', 'title', 'slug', 'updated_at'
        ).order_by('-updated_at')
        
        for mat in materials:
            node["materials"].append({
                "id": str(mat['id']),
                "title": mat['title'],
                "slug": mat['slug'],
                "type": "material",
            })

        # Recursión para subcarpetas
        children = folder.get_children()
        for child in children:
            node["children"].append(self._serialize_folder_recursive(child))
            
        return node

    def _build_copies_section(self):
        # Evitamos importación circular obteniendo el modelo dinámicamente
        Assessment = apps.get_model('assessment_v2', 'Exam')
        
        # Subquery para obtener el estado de la evaluación más reciente
        

        # Anotamos el queryset para evitar N+1 consultas
        Assessment = apps.get_model('assessment_v2', 'Exam')
        
        # [FIX V24] Filtrado estricto para coincidir con Dashboard
        visible_statuses = ['PENDING', 'GENERATING', 'READY', 'IN_PROGRESS', 'COMPLETED', 'GRADING', 'GRADED', 'ERROR']
        
        now = timezone.now()
        assessments_qs = Assessment.objects.filter(
            status__in=visible_statuses
        ).exclude(
            status__in=['EXPIRED_UNTAKEN', 'CORRECTION_EXPIRED', 'USER_CANCELLED']
        ).exclude(
            Q(status='COMPLETED') & (Q(expiration_date__lte=now) | Q(expiration_date__isnull=True))
        ).exclude(
            Q(status='RESULTS_AVAILABLE') & Q(results_expiration_date__lte=now)
        ).order_by('-created_at')

        copies_qs = ContentCopy.objects.filter(user=self.user).prefetch_related(
            Prefetch('assessments', queryset=assessments_qs, to_attr='_active_assessments')
        ).select_related(
            'original_content', 'subject_context'
        ).order_by('-updated_at')

        structure = {
            "academic": {},
            "free": []
        }

        for copy in copies_qs:
            copy_data = {
                "id": str(copy.id),
                "title": copy.original_content.title,
                "original_id": str(copy.original_content.id),
                "updated_at": copy.updated_at.isoformat(),
                "url": copy.get_absolute_url() if hasattr(copy, 'get_absolute_url') else '#',
                "assessment_status": copy._active_assessments[0].status if getattr(copy, '_active_assessments', []) else None,
                "assessment_viewed": copy._active_assessments[0].was_viewed if getattr(copy, '_active_assessments', []) else None,
                "exam_url": reverse("assessment_v2:take_exam", args=[copy._active_assessments[0].uuid]) if getattr(copy, "_active_assessments", []) and copy._active_assessments[0].status == "READY" else None,
            }

            if copy.subject_context:
                subj_name = copy.subject_context.name
                if subj_name not in structure["academic"]:
                    structure["academic"][subj_name] = []
                structure["academic"][subj_name].append(copy_data)
            else:
                structure["free"].append(copy_data)

        return structure

def refresh_user_navigation(user):
    if not user:
        return
    builder = NavigationTreeBuilder(user)
    builder.build_and_save()
