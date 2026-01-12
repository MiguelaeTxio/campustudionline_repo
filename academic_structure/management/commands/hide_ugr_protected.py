from django.core.management.base import BaseCommand
from academic_structure.models import University, Degree, Subject
from contents.models import ContentCopy
from django.db.models import Q

class Command(BaseCommand):
    help = 'Oculta (Soft-Delete) las asignaturas protegidas de Paris.'

    def handle(self, *args, **options):
        print("👻 OCULTANDO ARTEFACTOS UGR (Paris)")
        print("=" * 60)
        
        ugr = University.objects.filter(Q(code="UGR") | Q(name__icontains="Granada")).first()
        PROTECTED_EMAIL = "parislegend83@gmail.com"

        # (Misma lógica de detección de idiomas...)
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

        degrees = Degree.objects.filter(branch__university=ugr).filter(
            Q(name__icontains="Lengua") | Q(name__icontains="Estudios") | 
            Q(name__icontains="Filología") | Q(name__icontains="Traducción") |
            Q(name__icontains="Maior")
        )

        for degree in degrees:
            d_name_upper = degree.name.upper()
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
                is_safe_subject = False
                for official_lang in official_langs:
                    for safe_kw in LANGUAGES[official_lang]:
                        if safe_kw.upper() in s_name_upper:
                            is_safe_subject = True
                            break
                if is_safe_subject: continue

                is_intruder = False
                for lang, keywords in LANGUAGES.items():
                    if lang not in official_langs:
                        for kw in keywords:
                            if f" {kw.upper()} " in f" {s_name_upper} " or s_name_upper.endswith(f" {kw.upper()}"):
                                is_intruder = True
                                break
                    if is_intruder: break
                
                if is_intruder:
                    # Verificar si es de Paris
                    materials = subj.content_materials.all()
                    copies = ContentCopy.objects.filter(original_content__in=materials)
                    emails = list(copies.values_list('user__email', flat=True))
                    
                    if PROTECTED_EMAIL in emails:
                        print(f"🔒 OCULTANDO: {subj.name} ({degree.name})")
                        
                        # 1. Ocultar Materiales
                        count = materials.update(is_public=False)
                        print(f"   -> {count} materiales marcados como privados.")
                        
                        # 2. Ocultar Asignatura del Árbol
                        subj.has_public_content = False
                        subj.save()
                        print(f"   -> Asignatura retirada del índice público.")
                        
                        # 3. EXTRAER DATOS PARA RE-SCRAPING
                        # Intentamos sacar la URL de algún sitio (si la guardamos)
                        # O imprimimos el nombre para búsqueda manual
                        print(f"   ℹ️ DATA PARA SCRAPER: Nombre='{subj.name}'")

        print("-" * 60)
