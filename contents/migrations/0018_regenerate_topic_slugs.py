# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/contents/migrations/0018_regenerate_topic_slugs.py
from django.db import migrations
from django.utils.text import slugify
import uuid

def regenerate_slugs(apps, schema_editor):
    """
    Itera sobre todos los Topics existentes y regenera sus slugs
    utilizando la nueva lógica que incluye la jerarquía padre para
    garantizar la unicidad.
    """
    Topic = apps.get_model('contents', 'Topic')
    total_topics = Topic.objects.count()
    print(f"\n    -> Encontrados {total_topics} Topics para procesar.")

    for i, topic in enumerate(Topic.objects.all(), 1):
        root_category = None
        # Navegamos hacia arriba para encontrar la raíz
        current = topic
        while current.parent:
            current = current.parent
        root_category = current.main_category

        if root_category:
            # Nueva lógica de slug robusta
            base_slug = slugify(f"{root_category.discipline.slug}-{root_category.name}-{topic.name}")
        else:
            # Fallback para topics sin categoría raíz (no debería ocurrir)
            base_slug = slugify(topic.name)
        
        # Lógica para garantizar unicidad en caso de colisión durante la migración
        proposed_slug = base_slug
        while Topic.objects.filter(slug=proposed_slug).exclude(pk=topic.pk).exists():
            unique_suffix = uuid.uuid4().hex[:6]
            proposed_slug = f"{base_slug}-{unique_suffix}"
            
        topic.slug = proposed_slug
        topic.save(update_fields=['slug'])
        
        # Imprimimos el progreso para no perder la pista
        print(f"    -> ({i}/{total_topics}) Actualizado slug para Topic '{topic.name[:50]}...' a '{topic.slug}'")

    print("    -> Regeneración de slugs completada.")


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0017_alter_contentcopy_unique_together_and_more'),
    ]

    operations = [
        migrations.RunPython(regenerate_slugs, migrations.RunPython.noop),
    ]
