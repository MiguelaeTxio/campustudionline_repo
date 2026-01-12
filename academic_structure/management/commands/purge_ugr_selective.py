from django.core.management.base import BaseCommand
from django.db import transaction
from academic_structure.models import University, Degree, Subject
from contents.models import ContentCopy
from django.db.models import Q

class Command(BaseCommand):
    help = 'Purga asignaturas intrusas UGR, protegiendo EXCLUSIVAMENTE a Paris.'

    def handle(self, *args, **options):
        print("🔥 PURGA SELECTIVA UGR (Protección: parislegend83)")
        print("=" * 60)
        
        ugr = University.objects.filter(Q(code="UGR") | Q(name__icontains="Granada")).first()
        if not ugr:
            print("❌ No se encuentra la UGR.")
            return

        PROTECTED_EMAIL = "parislegend83@gmail.com"

        LANGUAGES = {
            'INGLÉS': ['inglés', 'inglesa', 'ingles', 'english'],
            'FRANCÉS': ['francés', 'francesa', 'frances', 'french'],
            'ALEMÁN': ['alemán', 'alemana', 'aleman', 'german'],
            'ITALIANO': ['italiano', 'italiana'],
            'ÁRABE': ['árabe', 'arabe'],
            'CHINO': ['chino', 'china'],
            'RUSO': ['ruso', 'rusa'],
            'PORTUGUÉS': ['portugués', 'portuguesa'],
            'HEBREO': ['hebreo'],
            'GRIEGO': ['griego', 'griega'],
            'LATÍN': ['latín', 'latin'],
        }

        degrees = Degree.objects.filter(
            branch__university=ugr
        ).filter(
            Q(name__icontains="Lengua") | 
            Q(name__icontains="Estudios") | 
            Q(name__icontains="Filología") |
            Q(name__icontains="Traducción") |
            Q(name__icontains="Maior")
        )

        deleted_count = 0
        preserved_count = 0

        with transaction.atomic():
            for degree in degrees:
                d_name_upper = degree.name.upper()
                
                # Identificar idioma oficial
                official_langs = []
                for lang, keywords in LANGUAGES.items():
                    for kw in keywords:
                        if kw.upper() in d_name_upper:
                            official_langs.append(lang)
                            break
                
                if not official_langs: continue 

                subjects = Subject.objects.filter(academic_year__degree=degree)
                
                for subj in subjects:
                    s_name_upper = subj.name.upper()
                    
                    # Check Seguridad (Idioma correcto)
                    is_safe_subject = False
                    for official_lang in official_langs:
                        for safe_kw in LANGUAGES[official_lang]:
                            if safe_kw.upper() in s_name_upper:
                                is_safe_subject = True
                                break
                    if is_safe_subject: continue

                    # Check Intrusión
                    is_intruder = False
                    for lang, keywords in LANGUAGES.items():
                        if lang not in official_langs:
                            for kw in keywords:
                                if f" {kw.upper()} " in f" {s_name_upper} " or s_name_upper.endswith(f" {kw.upper()}"):
                                    is_intruder = True
                                    break
                        if is_intruder: break
                    
                    if is_intruder:
                        # VERIFICACIÓN DE PROTECCIÓN
                        materials = subj.content_materials.all()
                        copies = ContentCopy.objects.filter(original_content__in=materials)
                        
                        emails = list(copies.values_list('user__email', flat=True))
                        
                        if PROTECTED_EMAIL in emails:
                            print(f"   🛡️ PROTEGIDO (Usuario VIP): {subj.name} en {degree.name}")
                            preserved_count += 1
                        else:
                            print(f"   🗑️ ELIMINANDO: {subj.name} ({len(emails)} copias descartables)")
                            subj.delete()
                            deleted_count += 1

        print("-" * 60)
        print(f"🏁 FINALIZADO.")
        print(f"   🗑️ Eliminadas: {deleted_count}")
        print(f"   🛡️ Preservadas: {preserved_count}")
