# /home/MiguelAeTxio/CampuStudiOnline/contents/signals.py
import logging
from django.db.models.signals import m2m_changed, post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django.urls import reverse, NoReverseMatch

from .models import (
    ContentMaterial,
    KnowledgeArea,
    Discipline,
    MainCategory,
    Topic,
)
from academic_structure.models import Subject, Degree, Branch, University, AcademicYear
from announcements.models import Announcement

logger = logging.getLogger(__name__)


# ==============================================================================
# SEÑAL PARA FORZAR LA VISIBILIDAD PÚBLICA DE CONTENIDO ACADÉMICO
# ==============================================================================
@receiver(m2m_changed, sender=ContentMaterial.subject.through)
def force_academic_content_to_be_public(sender, instance, action, **kwargs):
    """
    Señal que se dispara cuando se añaden asignaturas a un ContentMaterial.

    Si a un material se le asocia al menos una asignatura, se fuerza a que
    sea público, garantizando el cumplimiento de la regla de negocio.
    """
    if action == "post_add":
        if isinstance(instance, ContentMaterial):
            if not instance.is_public:
                instance.is_public = True
                instance.save(update_fields=['is_public'])
                logger.info(
                    f"ContentMaterial (ID: {instance.pk}) forzado a público "
                    f"debido a su asociación con una asignatura académica."
                )


# ==============================================================================
# SEÑALES PARA ANUNCIOS Y NOTIFICACIONES
# ==============================================================================
@receiver(post_save, sender=ContentMaterial)
def create_announcement_for_new_public_content(sender, instance, created, **kwargs):
    """
    Señal que se activa después de guardar un ContentMaterial.

    Crea un Anuncio si el ContentMaterial es nuevo y público.
    """
    if created and instance.is_public:
        logger.info(f"Detectado nuevo ContentMaterial público (ID: {instance.pk}). Intentando crear anuncio.")
        try:
            local_datetime = timezone.localtime(instance.created_at)
            datetime_str = local_datetime.strftime("%d/%m/%Y a las %H:%M")
        except Exception as e:
            logger.warning(f"No se pudo formatear fecha para anuncio de Contenido ID {instance.pk}: {e}")
            datetime_str = "(fecha no disponible)"
        announcement_content_md = (f"¡Hola a todos!\n\nSe ha añadido nuevo material público a la plataforma:\n\n- **Título:** {instance.title}\n- **Autor:** {instance.creator.username if instance.creator else 'Sistema'}\n- **Publicado el:** {datetime_str}\n\n")
        try:
            content_url = instance.get_absolute_url()
            link_md = f"Puedes verlo aquí: **[{instance.title}]({content_url})**"
            announcement_content_md += f"{link_md}\n"
        except (NoReverseMatch, Exception) as e:
            logger.error(f"Error al generar enlace para Contenido ID {instance.pk}: {e}")
        try:
            author = instance.creator
            if not author:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                author = User.objects.filter(is_superuser=True, is_active=True).first()
            if author:
                Announcement.objects.create(title=f"Nuevo Material Disponible: {instance.title}", content=announcement_content_md, author=author)
                logger.info(f"Anuncio creado con éxito para ContentMaterial (ID: {instance.pk}).")
            else:
                logger.error(f"No se pudo crear el anuncio para {instance.pk} porque no se encontró un autor válido.")
        except Exception as e:
            logger.error(f"ERROR al crear anuncio automático para ContentMaterial (ID: {instance.pk}): {e}", exc_info=True)


# ==============================================================================
# LÓGICA DE ACTUALIZACIÓN DE ESTADO ACADÉMICO (REFACTORIZADA)
# ==============================================================================
def _propagate_academic_status_update(subjects_to_check):
    """
    Función auxiliar que recalcula el flag 'has_public_content' para un
    conjunto de asignaturas y propaga el cambio hacia arriba en la jerarquía
    académica (Año -> Grado -> Rama -> Universidad).

    Args:
        subjects_to_check (Iterable[Subject]): Un queryset o lista de
            objetos Subject cuyo estado necesita ser re-evaluado.
    """
    if not subjects_to_check:
        return

    # Se recalcula el estado de las asignaturas afectadas.
    for sub in subjects_to_check:
        new_status = sub.content_materials.filter(
            is_public=True, is_free_content=False
        ).exists()
        if sub.has_public_content != new_status:
            Subject.objects.filter(pk=sub.pk).update(
                has_public_content=new_status
            )

    # Se identifican los ancestros únicos para evitar recálculos redundantes.
    ancestors_to_check = Subject.objects.filter(
        pk__in=[s.pk for s in subjects_to_check]
    ).select_related('academic_year__degree__branch__university')

    # Se propaga el estado hacia arriba de forma eficiente.
    years = {s.academic_year for s in ancestors_to_check if s.academic_year}
    for ay in years:
        new_status = ay.subjects.filter(has_public_content=True).exists()
        if ay.has_public_content != new_status:
            AcademicYear.objects.filter(pk=ay.pk).update(has_public_content=new_status)

    degrees = {ay.degree for ay in years if ay.degree}
    for degree in degrees:
        new_status = degree.academic_years.filter(has_public_content=True).exists()
        if degree.has_public_content != new_status:
            Degree.objects.filter(pk=degree.pk).update(has_public_content=new_status)

    branches = {d.branch for d in degrees if d.branch}
    for branch in branches:
        new_status = branch.degrees.filter(has_public_content=True).exists()
        if branch.has_public_content != new_status:
            Branch.objects.filter(pk=branch.pk).update(has_public_content=new_status)

    universities = {b.university for b in branches if b.university}
    for university in universities:
        new_status = university.branches.filter(has_public_content=True).exists()
        if university.has_public_content != new_status:
            University.objects.filter(pk=university.pk).update(has_public_content=new_status)


# ==============================================================================
# SEÑALES PARA SINCRONIZACIÓN DE ESTADO ACADÉMICO (ROBUSTECIDAS)
# ==============================================================================
@receiver(m2m_changed, sender=ContentMaterial.subject.through)
def update_academic_hierarchy_on_m2m_change(sender, instance, action, pk_set, **kwargs):
    """
    Se dispara cuando cambia la relación M2M entre ContentMaterial y Subject.
    Utiliza la lógica centralizada para actualizar la jerarquía.
    """
    if action not in ["post_add", "post_remove", "post_clear"]:
        return

    subjects_to_check_ids = set()
    if isinstance(instance, ContentMaterial):
        if instance.is_free_content:
            return
        subjects_to_check_ids.update(pk_set)
    elif isinstance(instance, Subject):
        subjects_to_check_ids.add(instance.pk)
    else:
        return

    if not subjects_to_check_ids:
        return

    _propagate_academic_status_update(
        Subject.objects.filter(pk__in=subjects_to_check_ids)
    )


@receiver(pre_delete, sender=ContentMaterial)
def cache_subjects_on_content_pre_delete(sender, instance, **kwargs):
    """
    [NUEVO] Antes de borrar un ContentMaterial, guarda temporalmente en el
    objeto la lista de asignaturas asociadas. Esto es crucial porque en
    post_delete, la relación m2m ya no existe, especialmente en borrados
    masivos desde el admin.
    """
    if not instance.is_free_content:
        # Se adjunta la lista de Pks al objeto en memoria.
        instance._subjects_to_update_on_delete = list(instance.subject.all())


@receiver(post_delete, sender=ContentMaterial)
def update_academic_hierarchy_on_content_post_delete(sender, instance, **kwargs):
    """
    [NUEVO] Después de borrar un ContentMaterial, usa la lista guardada en
    pre_delete para recalcular el estado de las asignaturas que han
    quedado huérfanas y propagar el cambio.
    """
    subjects_to_update = getattr(instance, '_subjects_to_update_on_delete', [])
    if subjects_to_update:
        _propagate_academic_status_update(subjects_to_update)


@receiver(post_delete, sender=Subject)
def handle_subject_deletion(sender, instance, **kwargs):
    """
    Se dispara DESPUÉS de que una Subject se elimina para asegurar
    la consistencia de la jerarquía superior.
    """
    # Se pasa la única asignatura eliminada a la lógica central.
    _propagate_academic_status_update([instance])


# ==============================================================================
# SEÑALES PARA SINCRONIZACIÓN DE ESTADO DE CONTENIDO (LIBRE)
# ==============================================================================
@receiver(post_save, sender=ContentMaterial)
@receiver(post_delete, sender=ContentMaterial)
def update_intellectual_hierarchy_content_status(sender, instance, **kwargs):
    """
    Actualiza el flag 'has_free_content' en la jerarquía intelectual.
    Esta señal reacciona a cambios en ContentMaterial que son
    explícitamente marcados como 'is_free_content = True'.
    """
    if not instance.is_free_content:
        return

    topic_id = instance.topic_id
    if not topic_id:
        return
    try:
        topic = Topic.objects.get(pk=topic_id)
    except Topic.DoesNotExist:
        return

    # Inicia el recálculo desde el topic del material afectado hacia arriba.
    current_topic = topic
    while current_topic:
        has_direct_content = ContentMaterial.objects.filter(
            topic=current_topic, is_public=True, is_free_content=True
        ).exists()
        has_child_content = current_topic.subtopics.filter(
            has_free_content=True
        ).exists()
        new_status = has_direct_content or has_child_content

        if current_topic.has_free_content != new_status:
            Topic.objects.filter(pk=current_topic.pk).update(
                has_free_content=new_status
            )
            current_topic = current_topic.parent
        else:
            # Optimización: Si el estado no ha cambiado, los ancestros tampoco.
            break

    # Propaga el cambio a los ancestros de nivel superior.
    main_category = topic.get_root_category()
    if not main_category:
        return

    category_has_content = main_category.root_topics.filter(
        has_free_content=True
    ).exists()
    if main_category.has_free_content != category_has_content:
        MainCategory.objects.filter(pk=main_category.pk).update(
            has_free_content=category_has_content
        )

    discipline = main_category.discipline
    discipline_has_content = discipline.main_categories.filter(
        has_free_content=True
    ).exists()
    if discipline.has_free_content != discipline_has_content:
        Discipline.objects.filter(pk=discipline.pk).update(
            has_free_content=discipline_has_content
        )

    knowledge_area = discipline.knowledge_area
    area_has_content = knowledge_area.disciplines.filter(
        has_free_content=True
    ).exists()
    if knowledge_area.has_free_content != area_has_content:
        KnowledgeArea.objects.filter(pk=knowledge_area.pk).update(
            has_free_content=area_has_content
        )
