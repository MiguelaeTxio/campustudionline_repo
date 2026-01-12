from django.core.management.base import BaseCommand
from django.db import transaction
from academic_structure.models import Degree, Subject
from contents.models import ContentMaterial, ContentCopy
from django.db.models import Q

class Command(BaseCommand):
    help = 'Purga contenidos de asignaturas Maior/Minor en la UGR protegiendo a Paris.'

    def handle(self, *args, **options):
        print("🔥 INICIANDO PURGA QUIRÚRGICA: MAIOR/MINOR UGR")
        print("=" * 60)
        
        PROTECTED_USER = "parislegend83@gmail.com"
        # Usamos icontains para los grados para ser flexibles con "Grado en..."
        LANGUAGE_KEYWORDS = ["Árabe", "Francés", "Francés", "Inglés", "Modernas", "Hispánica", "Clásica"]
        
        with transaction.atomic():
            # 1. Identificar Grados de Lenguas
            degrees = Degree.objects.filter(
                branch__university__code="UGR"
            ).filter(
                reduce(lambda x, y: x | y, [Q(name__icontains=k) for k in LANGUAGE_KEYWORDS])
            )

            # 2. Identificar Asignaturas Maior/Minor/Minus
            subjects = Subject.objects.filter(
                academic_year__degree__in=degrees
            ).filter(
                Q(name__icontains="Maior") | 
                Q(name__icontains="Minor") | 
                Q(name__icontains="Minus")
            )

            # 3. Obtener IDs protegidos de Paris
            protected_ids = ContentCopy.objects.filter(
                user__email=PROTECTED_USER
            ).values_list('original_content_id', flat=True)

            # 4. Localizar y eliminar materiales no protegidos
            materials_to_purge = ContentMaterial.objects.filter(
                subject__in=subjects
            ).exclude(
                id__in=protected_ids
            ).distinct()

            total_found = materials_to_purge.count()
            
            if total_found > 0:
                for mat in materials_to_purge:
                    print(f"   🗑️ Borrando material: {mat.title[:50]}...")
                
                materials_to_purge.delete()
                print(f"\n✅ ÉXITO: {total_found} materiales purgados.")
            else:
                print("ℹ️ No se han encontrado materiales Maior/Minor para purgar.")

            # 5. Sincronizar la UI (Flags de asignatura)
            for s in subjects:
                if not s.content_materials.exists():
                    s.has_public_content = False
                    s.save()
        
        print("-" * 60)
        print("🏁 PROCESO FINALIZADO.")

# Necesario para el reduce de los Q objects
from functools import reduce
