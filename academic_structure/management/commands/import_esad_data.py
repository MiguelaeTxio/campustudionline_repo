import json
import os
import hashlib
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import transaction
from academic_structure.models import University, Branch, Degree, AcademicYear, Subject, ContentHashFamily

class Command(BaseCommand):
    help = 'Importa datos de ESAD Córdoba (V3 - Final con nombre corregido)'

    def handle(self, *args, **options):
        json_path = os.path.join(settings.BASE_DIR, 'web_scrapping', 'esad_final_data_v3.json')
        
        if not os.path.exists(json_path):
            raise CommandError(f'Falta el archivo: {json_path}')

        self.stdout.write(self.style.NOTICE(f"--- Importando ESAD V3 ---"))
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        stats = {'s_created': 0}

        try:
            with transaction.atomic():
                # Universidad con el nombre solicitado para el Directorio Académico
                university, _ = University.objects.update_or_create(
                    code="ESAD-C",
                    defaults={
                        "name": "Institución Académica de Córdoba II",
                        "url": "https://esadcordoba.com/"
                    }
                )

                for item in data:
                    degree_name = item.get('degree')
                    branch_name = item.get('branch')
                    year_num = item.get('year')
                    subjects_list = item.get('subjects', [])

                    branch, _ = Branch.objects.get_or_create(university=university, name=branch_name)
                    
                    deg_code = f"ESAD-{hashlib.md5(degree_name.encode()).hexdigest()[:4].upper()}"
                    degree, _ = Degree.objects.update_or_create(
                        branch=branch, name=degree_name,
                        defaults={"code": deg_code, "degree_type": Degree.DegreeType.BACHELOR, "url": "https://esadcordoba.com/"}
                    )

                    academic_year, _ = AcademicYear.objects.get_or_create(degree=degree, year=year_num)

                    for subj_data in subjects_list:
                        subj_name = subj_data.get('name')
                        outline = subj_data.get('course_content_outline', [])
                        
                        if outline: content_source = outline[0][:5000]
                        else: content_source = f"{degree_name}-{subj_name}-{year_num}"
                        
                        content_hash = hashlib.sha256(content_source.encode('utf-8')).hexdigest()
                        hash_family, _ = ContentHashFamily.objects.get_or_create(hash=content_hash)

                        Subject.objects.create(
                            academic_year=academic_year,
                            name=subj_name,
                            subject_type=Subject.SubjectType.MANDATORY,
                            content_hash_family=hash_family,
                            learning_objectives=[],
                            course_content_outline=outline,
                            bibliography={}
                        )
                        stats['s_created'] += 1

        except Exception as e:
            raise CommandError(f"Error: {e}")

        self.stdout.write(self.style.SUCCESS(f"Finalizado. Asignaturas Creadas: {stats['s_created']}"))
