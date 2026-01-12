import json
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
from academic_structure.models import University, Branch, Degree, AcademicYear, Subject

class Command(BaseCommand):
    help = 'Importación definitiva de lenguas UGR con preservación de contenidos.'

    def handle(self, *args, **options):
        json_path = '/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/data/ugr_languages_final.json'
        
        if not os.path.exists(json_path):
            self.stderr.write(self.style.ERROR(f'No se encuentra el archivo: {json_path}'))
            return

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.stdout.write(f"🚀 Iniciando importación de {len(data)} titulaciones UGR...")

        with transaction.atomic():
            # 1. Asegurar Institución y Rama
            uni, _ = University.objects.get_or_create(
                code="UGR",
                defaults={"name": "Institución Académica de Granada", "url": "https://www.ugr.es"}
            )
            
            branch, _ = Branch.objects.get_or_create(
                university=uni,
                name="Artes y Humanidades"
            )

            for degree_data in data:
                # 2. Asegurar Titulación
                degree_name = degree_data['degree_name']
                degree, _ = Degree.objects.get_or_create(
                    branch=branch,
                    name=degree_name,
                    defaults={"code": slugify(degree_name)[:10], "degree_type": "GR"}
                )

                # 3. Mapear Años Académicos
                year_map = {}
                for y in range(1, 5):
                    ay, _ = AcademicYear.objects.get_or_create(degree=degree, year=y)
                    year_map[y] = ay

                self.stdout.write(f"   🎓 Procesando: {degree_name}")
                
                subjects_list = degree_data.get('subjects', [])
                for s in subjects_list:
                    s_name = s['name']
                    s_year = s.get('year', 1)
                    s_sem = s.get('semester')
                    s_type = s.get('type', 'OP')

                    academic_year = year_map.get(s_year, year_map[1])

                    # 4. SUTURA DE ASIGNATURA
                    # Buscamos si ya existe por nombre en este grado (independientemente del año)
                    # para evitar duplicados al mover de curso.
                    subj_obj = Subject.objects.filter(
                        academic_year__degree=degree,
                        name=s_name
                    ).first()

                    if subj_obj:
                        # ACTUALIZACIÓN: Movemos de año/semestre si es necesario
                        subj_obj.academic_year = academic_year
                        subj_obj.semester = s_sem
                        subj_obj.subject_type = s_type
                        subj_obj.save()
                    else:
                        # CREACIÓN
                        Subject.objects.create(
                            academic_year=academic_year,
                            name=s_name,
                            subject_type=s_type,
                            semester=s_sem
                        )

        self.stdout.write(self.style.SUCCESS("✨ IMPORTACIÓN UGR FINALIZADA CORRECTAMENTE."))
