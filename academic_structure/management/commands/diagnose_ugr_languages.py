from django.core.management.base import BaseCommand
from academic_structure.models import University, Degree
from django.db.models import Q
from collections import Counter

class Command(BaseCommand):
    help = 'Diagnostica la mezcla de Maior/Minor en la UGR'

    def handle(self, *args, **options):
        print("🕵️ DIAGNÓSTICO DE CONTAMINACIÓN LINGÜÍSTICA - UGR")
        print("-" * 50)

        # 1. Localizar UGR
        ugr = University.objects.filter(Q(code="UGR") | Q(name__icontains="Granada")).first()
        if not ugr:
            print("❌ No se encuentra la UGR en la base de datos.")
            return

        # 2. Palabras clave de idiomas para detectar intrusiones
        LANGUAGES = {
            'INGLÉS': ['inglés', 'inglesa', 'ingles'],
            'FRANCÉS': ['francés', 'francesa', 'frances'],
            'ALEMÁN': ['alemán', 'alemana', 'aleman'],
            'ITALIANO': ['italiano', 'italiana'],
            'ÁRABE': ['árabe', 'arabe'],
            'CHINO': ['chino', 'china'],
            'RUSO': ['ruso', 'rusa'],
            'PORTUGUÉS': ['portugués', 'portuguesa'],
            'HEBREO': ['hebreo'],
            'GRIEGO': ['griego', 'griega'],
            'LATÍN': ['latín', 'latin'],
        }

        # 3. Buscar Grados sospechosos (Filologías, Lenguas, Estudios...)
        degrees = Degree.objects.filter(
            branch__university=ugr
        ).filter(
            Q(name__icontains="Lengua") | 
            Q(name__icontains="Estudios") | 
            Q(name__icontains="Filología") |
            Q(name__icontains="Traducción") |
            Q(name__icontains="Maior")
        )

        for degree in degrees:
            d_name_upper = degree.name.upper()
            
            # Identificar el idioma "oficial" del grado según su nombre
            official_langs = []
            for lang, keywords in LANGUAGES.items():
                for kw in keywords:
                    if kw.upper() in d_name_upper:
                        official_langs.append(lang)
                        break
            
            # Si no detectamos idioma en el título (ej: "Lenguas Modernas"), asumimos que puede tener todo
            # Pero si se llama "Estudios Franceses", no debería tener asignaturas de Árabe avanzado.
            
            subjects = degree.academic_years.all().values_list('subjects__name', flat=True)
            subjects = [s for s in subjects if s] # Filtrar Nones
            
            total_subjects = len(subjects)
            if total_subjects == 0: continue

            # Analizar asignaturas
            detected_langs = Counter()
            intruders = []

            for subj_name in subjects:
                s_upper = subj_name.upper()
                for lang, keywords in LANGUAGES.items():
                    # Si el idioma NO es oficial del grado, es un sospechoso
                    if lang not in official_langs:
                        for kw in keywords:
                            # Buscamos palabras completas para evitar falsos positivos
                            # (ej: "Latina" en "América Latina" vs "Lengua Latina")
                            if f" {kw.upper()} " in f" {s_upper} " or s_upper.endswith(f" {kw.upper()}"):
                                detected_langs[lang] += 1
                                intruders.append(f"[{lang}] {subj_name}")
                                break

            # REPORTE SI HAY CONTAMINACIÓN SIGNIFICATIVA
            has_contamination = sum(detected_langs.values()) > 0
            
            if has_contamination and official_langs: # Solo reportar si el grado tiene idioma definido
                print(f"\n🎓 TITULACIÓN: {degree.name}")
                print(f"   Idiomas Titulares: {', '.join(official_langs) if official_langs else 'Genérico'}")
                print(f"   Total Asignaturas: {total_subjects}")
                print(f"   ⚠️ INTRUSIONES DETECTADAS:")
                
                for lang, count in detected_langs.items():
                    print(f"      🔴 {lang}: {count} asignaturas")
                
                # Mostrar muestra de intrusos (primeros 3)
                print(f"      🔎 Ejemplos de intrusos:")
                for i in intruders[:5]:
                    print(f"         - {i}")

        print("-" * 50)
        print("🏁 Diagnóstico finalizado.")
