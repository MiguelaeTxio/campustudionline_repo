from django.core.management.base import BaseCommand
from academic_structure.models import University, Degree, Subject
from contents.models import ContentCopy
from django.db.models import Q

class Command(BaseCommand):
    help = 'Audita el impacto en usuarios antes de purgar la UGR.'

    def handle(self, *args, **options):
        print("🕵️ AUDITORÍA DE IMPACTO EN USUARIOS - UGR")
        print("=" * 60)
        
        ugr = University.objects.filter(Q(code="UGR") | Q(name__icontains="Granada")).first()
        if not ugr:
            print("❌ No se encuentra la UGR.")
            return

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

        safe_to_purge_count = 0
        blocked_count = 0
        
        # Lista de afectados: (Asignatura, Titulacion, [Emails])
        impact_report = []

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
                
                # Check Seguridad (Es del idioma correcto?)
                is_safe_subject = False
                for official_lang in official_langs:
                    for safe_kw in LANGUAGES[official_lang]:
                        if safe_kw.upper() in s_name_upper:
                            is_safe_subject = True
                            break
                if is_safe_subject: continue

                # Check Intrusión (Es de otro idioma?)
                is_intruder = False
                detected_lang = None
                for lang, keywords in LANGUAGES.items():
                    if lang not in official_langs:
                        for kw in keywords:
                            if f" {kw.upper()} " in f" {s_name_upper} " or s_name_upper.endswith(f" {kw.upper()}"):
                                is_intruder = True
                                detected_lang = lang
                                break
                    if is_intruder: break
                
                if is_intruder:
                    # ANÁLISIS DE IMPACTO
                    # 1. Buscar materiales asociados a esta asignatura
                    materials = subj.content_materials.all()
                    
                    # 2. Buscar copias de esos materiales
                    copies = ContentCopy.objects.filter(original_content__in=materials)
                    
                    if copies.exists():
                        # BLOQUEADO: Hay usuarios
                        users_affected = list(copies.values_list('user__email', flat=True).distinct())
                        impact_report.append({
                            'degree': degree.name,
                            'subject': subj.name,
                            'lang': detected_lang,
                            'users': users_affected
                        })
                        blocked_count += 1
                        # print(f"   🔴 BLOQUEADO: {subj.name} ({len(users_affected)} usuarios)")
                    else:
                        # SEGURO: No hay copias
                        safe_to_purge_count += 1
                        # print(f"   🟢 LIMPIO: {subj.name}")

        print("\n📊 RESUMEN DE IMPACTO")
        print(f"   🟢 Asignaturas intrusas SIN USO (Seguras de borrar): {safe_to_purge_count}")
        print(f"   🔴 Asignaturas intrusas CON USO (Conflictivas):      {blocked_count}")
        
        if blocked_count > 0:
            print("\n🚨 DETALLE DE CONFLICTOS (Usuarios Afectados):")
            for item in impact_report:
                print(f"   - [{item['degree']}] {item['subject']} ({item['lang']})")
                print(f"     emails: {', '.join(item['users'])}")
        else:
            print("\n✅ VÍA LIBRE: Ningún usuario se verá afectado por la purga.")

        print("-" * 60)
