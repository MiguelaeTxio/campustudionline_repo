# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/contents/feeds.py
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.urls import reverse
from .models import ContentMaterial

class MetaCatalogFeedGenerator(Rss201rev2Feed):
    """
    Generador de RSS extendido con namespace de Google/Meta Commerce.
    Añade los campos requeridos para catálogos de productos (precio, imagen, disponibilidad).
    """
    def root_attributes(self):
        attrs = super().root_attributes()
        # Añadir el namespace necesario para los prefijos 'g:'
        attrs['xmlns:g'] = 'http://base.google.com/ns/1.0'
        return attrs

    def add_item_elements(self, handler, item):
        super().add_item_elements(handler, item)
        # Campos obligatorios de Meta/Google
        handler.addQuickElement(u"g:id", item['g_id'])
        handler.addQuickElement(u"g:title", item['title'])
        handler.addQuickElement(u"g:description", item['description'])
        handler.addQuickElement(u"g:brand", "CampuStudiOnline")
        handler.addQuickElement(u"g:condition", "new")
        handler.addQuickElement(u"g:availability", "in stock")
        handler.addQuickElement(u"g:price", "0.00 EUR")
        
        # Campos de imagen (Crítico para anuncios)
        if item.get('image_link'):
            handler.addQuickElement(u"g:image_link", item['image_link'])
            
        # Categorización
        if item.get('product_type'):
            handler.addQuickElement(u"g:product_type", item['product_type'])

class MetaCatalogFeed(Feed):
    feed_type = MetaCatalogFeedGenerator
    title = "CampuStudiOnline Course Catalog"
    link = "/contents/"
    description = "Catálogo oficial de cursos y materiales de estudio de CampuStudiOnline."

    def items(self):
        return ContentMaterial.objects.filter(is_public=True).select_related('master_category', 'sub_category').order_by('-updated_at')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.short_description

    def item_link(self, item):
        return reverse('contents:content_detail', args=[item.pk])
    
    def item_guid(self, item):
        return str(item.pk)

    def item_extra_kwargs(self, item):
        """
        Prepara los datos extra que el Generador consumirá para las etiquetas 'g:'.
        """
        # Construcción de URL absoluta para la imagen
        image_url = reverse('contents:generate_share_image', args=[item.pk])
        full_image_url = self.request.build_absolute_uri(image_url)
        
        # Construcción de la jerarquía de categorías
        category_path = "Education"
        if item.master_category:
            category_path += f" > {item.master_category.name}"
            if item.sub_category:
                category_path += f" > {item.sub_category.name}"

        return {
            'g_id': str(item.pk),
            'title': item.title,
            'description': item.short_description,
            'image_link': full_image_url,
            'product_type': category_path
        }
