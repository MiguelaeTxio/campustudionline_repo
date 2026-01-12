from django.core.management.base import BaseCommand
from django.db import transaction
from academic_structure.models import Degree, Subject
from contents.models import ContentMaterial, ContentCopy

class Command(BaseCommand):
    help = 'Purga masiva de contenidos de lenguas UGR, protegiendo solo a Paris.'

    def handle(self, *args, **options):
        print("🔥 INICIANDO PURGA DE CONTENIDOS LINGÜÍSTICOS UGR")
        print("=" * 60)
        
        PROTECTED_USER = "parislegend83@gmail.com"
        LANGUAGE_DEGREES = [
            "Estudios Árabes e Islámicos",
            "Estudios Franceses",
            "Estudios Ingleses",
            "Lenguas Modernas y sus Literaturas",
            "Filología Hispánica",
            "Filología Clásica"
        ]

        with transaction.atomic():
            # 1. Obtener los Grados objetivo
            degrees = Degree.objects.filter(name__in=LANGUAGE_DEGREES)
            
            # 2. Obtener los IDs de los materiales que tienen copias de Paris
            protected_material_ids = ContentCopy.objects.filter(
                user__email=PROTECTED_USER
            ).values_list('original_content_id', flat=True)

            # 3. Buscar materiales vinculados a estas titulaciones que NO estén protegidos
            materials_to_delete = ContentMaterial.objects.filter(
                subject__academic_year__degree__in=degrees
            ).exclude(
                id__in=protected_material_ids
            ).distinct()

            count = materials_to_delete.count()
            
            print(f"📦 Materiales encontrados para lenguas: {ContentMaterial.objects.filter(subject__academic_year__degree__in=degrees).distinct().count()}")
            print(f"🛡️ Materiales protegidos (Paris): {len(protected_material_ids)}")
            print(f"🗑️ Materiales a eliminar: {count}")

            if count > 0:
                # El borrado de ContentMaterial no afecta a las asignaturas (es M2M)
                materials_to_delete.delete()
                print(f"✅ ÉXITO: {count} contenidos purgados.")
            else:
                print("ℹ️ No hay contenidos que purgar.")

            # 4. Saneamiento de Flags en Asignaturas
            # Ponemos a False el flag 'has_public_content' en las asignaturas de estos grados 
            # (excepto si conservan algún material protegido)
            subjects = Subject.objects.filter(academic_year__degree__in=degrees)
            for s in subjects:
                if not s.content_materials.exists():
                    s.has_public_content = False
                    s.save()

        print("-" * 60)
        print("🏁 PURGA COMPLETADA. El directorio ahora debería mostrar 'Solicitar Contenido'.")
