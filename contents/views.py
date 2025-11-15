# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/contents/views.py
import logging
import yaml
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse, Http404, HttpResponseBadRequest
from django.views.decorators.http import require_POST, require_http_methods
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q, Exists, OuterRef # Importado para consultas complejas
import markdown
import bleach

from academic_structure.models import Subject # Importación necesaria
from .utils import generate_share_image_bytes
from .models import (
    ContentMaterial, KnowledgeArea, Discipline, MainCategory, Topic, FavoriteFolder
)
from .forms import (
    ContentMaterialForm, NEW_OPTION_ID_VALUE, NEW_OPTION_TEXT,
    PLACEHOLDER_OPTION_TEXT,
)

User = get_user_model()
logger = logging.getLogger(__name__)

# --- Configuración de Markdown y Bleach (sin cambios) ---
MARKDOWN_EXTENSIONS = [
    'markdown.extensions.fenced_code', 'markdown.extensions.codehilite', 'markdown.extensions.tables',
    'markdown.extensions.attr_list', 'markdown.extensions.toc', 'markdown.extensions.sane_lists',
    'markdown.extensions.nl2br', 'pymdownx.betterem', 'pymdownx.tilde', 'pymdownx.magiclink',
    'pymdownx.superfences', 'pymdownx.tasklist',
]
MARKDOWN_EXTENSION_CONFIGS = {
    'markdown.extensions.codehilite': {'css_class': 'highlight', 'guess_lang': False, 'noclasses': False},
}
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'del', 'ul', 'ol', 'li', 'a', 'img', 'hr',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'code', 'span', 'div',
    'blockquote', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'input',
    'details', 'summary'
]
ALLOWED_ATTRIBUTES = {
    '*': ['class', 'id', 'style'], 'a': ['href', 'title', 'target'],
    'img': ['src', 'alt', 'title', 'width', 'height'], 'input': ['type', 'checked', 'disabled'],
}

def markdown_to_html_internal(markdown_text):
    if not markdown_text: return ""
    html_output = markdown.markdown(markdown_text, extensions=MARKDOWN_EXTENSIONS, extension_configs=MARKDOWN_EXTENSION_CONFIGS)
    return bleach.clean(html_output, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)

def parse_yaml_front_matter(content_string):
    if not content_string:
        return {}, ''

    parts = content_string.split('---', 2)
    if len(parts) >= 3 and not parts[0].strip():
        yaml_block = parts[1]
        remaining_markdown = parts[2].lstrip('\n')
        try:
            metadata = yaml.safe_load(yaml_block) or {}
            if not isinstance(metadata, dict):
                metadata = {}
        except yaml.YAMLError as e:
            logger.error(f"Error al parsear YAML front matter: {e}")
            metadata = {}
        return metadata, remaining_markdown

    # Si no hay front matter, devolvemos metadata vacío y el texto completo
    return {}, content_string

# --- LÓGICA DE CARPETAS DE SISTEMA (CORREGIDA)---

def _ensure_system_folders(user):
    """
    Asegura la existencia de las carpetas inmutables "Mis Favoritos" y "Mis Publicaciones"
    en la raíz del árbol del usuario, utilizando la API correcta de treebeard.
    """
    
    # 1. Mis Publicaciones (PUB)
    try:
        pub_folder = FavoriteFolder.objects.get(user=user, folder_type=FavoriteFolder.FOLDER_TYPE_PUBLICATIONS)
    except FavoriteFolder.DoesNotExist:
        pub_folder = FavoriteFolder.add_root(
            user=user,
            name='Mis Publicaciones',
            folder_type=FavoriteFolder.FOLDER_TYPE_PUBLICATIONS
        )

    # 2. Mis Favoritos (FAV)
    try:
        fav_folder = FavoriteFolder.objects.get(user=user, folder_type=FavoriteFolder.FOLDER_TYPE_FAVORITES)
    except FavoriteFolder.DoesNotExist:
        fav_folder = FavoriteFolder.add_root(
            user=user,
            name='Mis Favoritos',
            folder_type=FavoriteFolder.FOLDER_TYPE_FAVORITES
        )

    # Treebeard ordena los nodos raíz por el campo 'path' que es alfabético
    # 'path' se genera automáticamente. Para asegurar el orden, recargamos y movemos si es necesario.
    all_roots = list(FavoriteFolder.get_root_nodes().filter(user=user))
    
    # Aseguramos que pub_folder y fav_folder están actualizados tras posibles creaciones/movimientos
    pub_folder = next((n for n in all_roots if n.folder_type == FavoriteFolder.FOLDER_TYPE_PUBLICATIONS), None)
    fav_folder = next((n for n in all_roots if n.folder_type == FavoriteFolder.FOLDER_TYPE_FAVORITES), None)

    # Lógica de reordenación robusta: si 'Mis Publicaciones' no es el primero, lo movemos al inicio.
    if all_roots and pub_folder and all_roots[0] != pub_folder:
         # Mover todos los demás nodos para que vayan después de pub_folder
         for node in all_roots:
             if node != pub_folder:
                 node.move(pub_folder, 'right')
    
    # Devolvemos la lista en el orden correcto para la plantilla
    return sorted(FavoriteFolder.get_root_nodes().filter(user=user), key=lambda n: n.path)


# --- VISTAS DEL NUEVO EXPLORADOR DE FAVORITOS (ARQUITECTURA PAIR) ---

@login_required
def personal_workspace_view(request):
    """
    Vista raíz del explorador personal. Muestra solo las carpetas de sistema (UX Atómica).
    """
    user = request.user
    
    # Asegurar que las carpetas de sistema existan (UX)
    root_nodes = _ensure_system_folders(user)

    # NOTA: Los materiales se listarán DENTRO de las carpetas de sistema, NO en esta vista raíz.
    
    context = {
        'nodes': root_nodes, # Debería contener al menos Mis Publicaciones y Mis Favoritos
    }
    return render(request, 'contents/personal_workspace.html', context)

@login_required
def favorite_folder_detail_view(request, folder_id):
    """
    Vista de detalle de una carpeta. Muestra subcarpetas y materiales (o publicaciones para la carpeta PUB).
    """
    user = request.user
    folder = get_object_or_404(FavoriteFolder, id=folder_id, user=user)
    children = folder.get_children()
    materials_in_folder = ContentMaterial.objects.none()

    if folder.folder_type == FavoriteFolder.FOLDER_TYPE_PUBLICATIONS:
        # Si es la carpeta de Mis Publicaciones, muestra los materiales creados por el usuario
        materials_in_folder = ContentMaterial.objects.filter(creator=user).order_by('-updated_at')
        if request.user.is_authenticated:
            materials_in_folder = materials_in_folder.annotate(
                is_favorite=Exists(
                    FavoriteFolder.objects.filter(user=request.user, materials__pk=OuterRef('pk'))
                )
            )
        # Para Mis Publicaciones, los ancestros son solo la raíz (y no se muestran)
        ancestors = []
    else:
        # Para Mis Favoritos o cualquier carpeta de usuario
        materials_in_folder = folder.materials.all().order_by('-updated_at')
        if request.user.is_authenticated:
            materials_in_folder = materials_in_folder.annotate(
                is_favorite=Exists(
                    FavoriteFolder.objects.filter(user=request.user, materials__pk=OuterRef('pk'))
                )
            )
        ancestors = folder.get_ancestors()
    
    # Obtener todas las carpetas raíz del usuario para el modal de "Mover"
    root_folders = FavoriteFolder.get_root_nodes().filter(user=user, folder_type=FavoriteFolder.FOLDER_TYPE_FAVORITES)

    context = {
        'folder': folder,
        'nodes': children,
        'ancestors': ancestors,
        'materials': materials_in_folder,
        'root_folders': root_folders, # Para el modal
        'current_folder_id': folder.id, # Para exclusión en el modal
    }
    return render(request, 'contents/favorite_folder_detail.html', context)

# --- VISTAS HTMX PARA CRUD DE CARPETAS ---

@login_required
@require_http_methods(["POST"])
def create_folder_htmx_view(request):
    parent_id = request.POST.get('parent_id')
    folder_name = request.POST.get('folder_name')

    if not folder_name:
        return HttpResponseBadRequest("El nombre de la carpeta no puede estar vacío.")

    if parent_id:
        parent_folder = get_object_or_404(FavoriteFolder, id=parent_id, user=request.user)
        
        # PROHIBIR CREAR CARPETAS DIRECTAMENTE DENTRO DE MIS PUBLICACIONES
        if parent_folder.folder_type == FavoriteFolder.FOLDER_TYPE_PUBLICATIONS:
            return HttpResponseBadRequest("Solo puedes crear subcarpetas dentro de 'Mis Favoritos'.")
            
        # Verificar que el nombre sea único en el mismo nivel (usando API de treebeard)
        if parent_folder.get_children().filter(name=folder_name).exists():
             return HttpResponseBadRequest("Ya existe una carpeta con este nombre en esta ubicación.")
        
        # SOLUCIÓN: Crear la instancia primero y pasarla al método `add_child`.
        new_folder_instance = FavoriteFolder(
            name=folder_name, 
            user=request.user, 
            folder_type=FavoriteFolder.FOLDER_TYPE_USER
        )
        parent_folder.add_child(instance=new_folder_instance)

        nodes = [new_folder_instance] # Devolvemos solo el nodo nuevo para 'beforeend'
    else:
        # No permitiremos la creación de más carpetas en la raíz
        return HttpResponseBadRequest("No se permite la creación de carpetas adicionales en la raíz.")

    response = render(request, 'contents/partials/_folder_nodes.html', {'nodes': nodes})
    response['HX-Trigger'] = 'newFolderCreated'
    return response

@login_required
@require_http_methods(["DELETE"])
def delete_folder_htmx_view(request, folder_id):
    folder = get_object_or_404(FavoriteFolder, id=folder_id, user=request.user)
    
    # PROHIBIR ELIMINAR CARPETAS DE SISTEMA
    if folder.is_system_folder:
        return HttpResponseBadRequest("No se puede eliminar una carpeta de sistema ('Mis Favoritos'/'Mis Publicaciones').")

    # Añadir lógica de verificación de vacío para que el FE pueda manejar el error 
    if folder.get_children().exists() or folder.materials.exists():
        return HttpResponseBadRequest("No se puede eliminar una carpeta que contiene subcarpetas o materiales.")
        
    folder.delete()
    
    # Devolver un 200 OK para que HTMX pueda actualizar
    return HttpResponse(status=200)

@login_required
def rename_folder_form_htmx_view(request, folder_id):
    folder = get_object_or_404(FavoriteFolder, id=folder_id, user=request.user)
    
    # PROHIBIR RENOMBRAR CARPETAS DE SISTEMA
    if folder.is_system_folder:
        return HttpResponseBadRequest("No se puede renombrar una carpeta de sistema ('Mis Favoritos'/'Mis Publicaciones').")
        
    return render(request, 'contents/partials/_rename_folder_form.html', {'folder': folder})

@login_required
@require_http_methods(["POST"])
def rename_folder_htmx_view(request, folder_id):
    folder = get_object_or_404(FavoriteFolder, id=folder_id, user=request.user)
    new_name = request.POST.get('new_folder_name')

    # PROHIBIR RENOMBRAR CARPETAS DE SISTEMA
    if folder.is_system_folder:
        return HttpResponseBadRequest("No se puede renombrar una carpeta de sistema ('Mis Favoritos'/'Mis Publicaciones').")
        
    if not new_name:
        return HttpResponseBadRequest("El nuevo nombre no puede estar vacío.")

    # Verificar unicidad del nombre en el mismo nivel (usando API de treebeard)
    if folder.get_siblings().filter(name=new_name).exists():
        return HttpResponseBadRequest("Ya existe una carpeta con este nombre en esta ubicación.")
        
    folder.name = new_name
    folder.save()
    
    # Devolvemos solo el nodo actualizado para que reemplace el formulario de renombrar
    return render(request, 'contents/partials/_folder_nodes.html', {'nodes': [folder]})


@login_required
@require_http_methods(["POST"])
def move_element_htmx_view(request):
    element_id = request.POST.get('element_id')
    element_type = request.POST.get('element_type')
    destination_folder_id = request.POST.get('destination_folder_id')
    user = request.user

    if not all([element_id, element_type, destination_folder_id]):
        return HttpResponseBadRequest("Faltan parámetros en la solicitud.")

    destination_folder = get_object_or_404(FavoriteFolder, id=destination_folder_id, user=user)

    if destination_folder.folder_type == FavoriteFolder.FOLDER_TYPE_PUBLICATIONS:
        return HttpResponseBadRequest("No se pueden mover elementos a la carpeta 'Mis Publicaciones'.")

    if element_type == 'material':
        material = get_object_or_404(ContentMaterial, id=element_id)
        # Quitar de todas las carpetas de favoritos del usuario y añadir a la nueva
        material.favorite_folders.remove(*(material.favorite_folders.filter(user=user)))
        destination_folder.materials.add(material)

    elif element_type == 'folder':
        folder_to_move = get_object_or_404(FavoriteFolder, id=element_id, user=user)

        # Validaciones de seguridad
        if folder_to_move.is_system_folder:
            return HttpResponseBadRequest("Las carpetas de sistema no se pueden mover.")
        if str(folder_to_move.id) == str(destination_folder.id):
            return HttpResponseBadRequest("No se puede mover una carpeta dentro de sí misma.")
        if destination_folder.is_descendant_of(folder_to_move):
            return HttpResponseBadRequest("No se puede mover una carpeta a una de sus propias subcarpetas.")

        folder_to_move.move(destination_folder, 'last-child')

    else:
        return HttpResponseBadRequest("Tipo de elemento no válido.")

    response = HttpResponse(status=204)
    response['HX-Refresh'] = 'true'
    return response

@login_required
@require_POST
def remove_material_from_folder_htmx_view(request, material_id, folder_id):
    material = get_object_or_404(ContentMaterial, id=material_id)
    folder = get_object_or_404(FavoriteFolder, id=folder_id, user=request.user)

    if folder.folder_type == FavoriteFolder.FOLDER_TYPE_PUBLICATIONS:
        return HttpResponseBadRequest("No se pueden eliminar materiales de 'Mis Publicaciones' de esta forma.")

    folder.materials.remove(material)

    # Si ya no está en ninguna carpeta de favoritos del usuario, quitamos la marca global
    if not material.favorite_folders.filter(user=request.user).exists():
        request.user.userprofile.favorite_content.remove(material)

    return HttpResponse(status=200) # 200 OK para que HTMX elimine el elemento del DOM

@login_required
@require_POST
def toggle_favorite_htmx_view(request, pk):
    material = get_object_or_404(ContentMaterial, pk=pk)
    user = request.user

    _ensure_system_folders(user)
    favorites_root = get_object_or_404(FavoriteFolder, user=user, folder_type=FavoriteFolder.FOLDER_TYPE_FAVORITES)

    is_currently_favorite = material.favorite_folders.filter(user=user).exists()

    if is_currently_favorite:
        material.favorite_folders.remove(*(material.favorite_folders.filter(user=user)))
        new_favorite_state = False
        message = "Material eliminado de tus favoritos."
    else:
        favorites_root.materials.add(material)
        new_favorite_state = True
        message = "Material añadido a 'Mis Favoritos'."

    return JsonResponse({
        'status': 'success',
        'is_favorite': new_favorite_state,
        'message': message
    })

@login_required
def get_folder_options_htmx_view(request):
    """
    Vista HTMX para obtener la lista de opciones de carpetas actualizada.
    Se usa para refrescar el contenido del modal de "Mover".
    """
    user = request.user
    current_folder_id = request.GET.get('current_folder_id')
    
    # Obtener todas las carpetas raíz del usuario para el modal de "Mover"
    root_folders = FavoriteFolder.get_root_nodes().filter(user=user, folder_type=FavoriteFolder.FOLDER_TYPE_FAVORITES)

    context = {
        'folders': root_folders,
        'current_folder_id': current_folder_id,
    }
    return render(request, 'contents/partials/_folder_tree_option.html', context)


# --- VISTAS DE CONTENIDO Y AJAX RESTANTES ---

def content_detail(request, pk, subject_pk=None):
    content_obj = get_object_or_404(ContentMaterial, pk=pk)
    
    subject_context = None
    if subject_pk:
        subject_context = get_object_or_404(Subject, pk=subject_pk)
        # Verificación de seguridad: Asegurarse de que el material pertenece a la asignatura.
        if not content_obj.subject.filter(pk=subject_pk).exists():
             raise Http404("Este material no pertenece a la asignatura especificada.")

    metadata, remaining_markdown = parse_yaml_front_matter(content_obj.markdown_content)
    rendered_html_content = markdown_to_html_internal(remaining_markdown)
    is_creator = request.user.is_authenticated and request.user == content_obj.creator
    
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = content_obj.favorite_folders.filter(user=request.user).exists()

    if not content_obj.is_public and not is_creator:
        messages.error(request, "No tienes permiso para acceder a este contenido privado.")
        return redirect("contents:personal_workspace")

    context = {
        "material": content_obj, "rendered_html_content": rendered_html_content,
        "metadata": metadata, "can_edit_delete": is_creator,
        "can_create_copy": content_obj.is_public or is_creator,
        "is_favorite": is_favorite,
        "subject": subject_context, # Se añade el contexto de la asignatura a la plantilla
        "show_preloader": True, "show_tour": True,
    }
    return render(request, "contents/content_detail.html", context)

@login_required
def create_content(request):
    user = request.user
    is_privileged_user = user.is_superuser or user.groups.filter(name__in=['Colaboradores', 'professors', 'rectors']).exists()
    public_count, private_count = 0, 0
    if not is_privileged_user:
        public_count = ContentMaterial.objects.filter(creator=user, is_public=True).count()
        private_count = ContentMaterial.objects.filter(creator=user, is_public=False).count()
        if request.method == "GET" and public_count >= 1 and private_count >= 1:
            messages.error(request, "Has alcanzado tu cuota máxima de creación de contenido (1 público y 1 privado).")
            return redirect("contents:personal_workspace")
    if request.method == "POST":
        form = ContentMaterialForm(request.POST)
        if form.is_valid():
            if not is_privileged_user:
                is_public_submission = form.cleaned_data.get('is_public', False)
                if is_public_submission and public_count >= 1:
                    form.add_error('is_public', "Ya has alcanzado tu cuota de 1 material público.")
                elif not is_public_submission and private_count >= 1:
                    form.add_error('is_public', "Ya has alcanzado tu cuota de 1 material privado.")
                else:
                    new_content = form.save(commit=False)
                    new_content.creator = request.user
                    new_content.save()
                    messages.success(request, f"¡El material '{new_content.title}' ha sido creado exitosamente!")
                    return redirect(new_content.get_absolute_url())
            else:
                new_content = form.save(commit=False)
                new_content.creator = request.user
                new_content.save()
                messages.success(request, f"¡El material '{new_content.title}' ha sido creado exitosamente!")
                return redirect(new_content.get_absolute_url())
    else:
        form = ContentMaterialForm()
    context = {
        "content_form": form, "page_title": "Crear Nuevo Material", "is_editing": False,
        "NEW_OPTION_ID_VALUE": NEW_OPTION_ID_VALUE, "NEW_OPTION_TEXT": NEW_OPTION_TEXT,
        "PLACEHOLDER_OPTION_TEXT": PLACEHOLDER_OPTION_TEXT,
    }
    return render(request, "contents/create_edit_content.html", context)

@login_required
def edit_content(request, pk):
    content_obj = get_object_or_404(ContentMaterial, pk=pk)
    if content_obj.creator != request.user:
        messages.error(request, "No tienes permiso para editar este material.")
        return redirect(content_obj.get_absolute_url())
    if request.method == "POST":
        form = ContentMaterialForm(request.POST, instance=content_obj)
        if form.is_valid():
            content_to_save = form.save()
            messages.success(request, f"El material '{content_to_save.title}' ha sido actualizado.")
            return redirect(content_to_save.get_absolute_url())
    else:
        form = ContentMaterialForm(instance=content_obj)
    context = {
        "content_form": form, "content_obj": content_obj, "page_title": "Editando Material",
        "is_editing": True, "NEW_OPTION_ID_VALUE": NEW_OPTION_ID_VALUE,
        "NEW_OPTION_TEXT": NEW_OPTION_TEXT, "PLACEHOLDER_OPTION_TEXT": PLACEHOLDER_OPTION_TEXT,
    }
    return render(request, "contents/create_edit_content.html", context)

@login_required
def delete_content(request, pk):
    content_obj = get_object_or_404(ContentMaterial, pk=pk)
    if content_obj.creator != request.user:
        messages.error(request, "No tienes permiso para eliminar este material.")
        return redirect(content_obj.get_absolute_url())
    if request.method == "POST":
        deleted_title = content_obj.title
        content_obj.delete()
        messages.success(request, f"El material '{deleted_title}' ha sido eliminado.")
        return redirect("contents:personal_workspace")
    return render(request, "contents/confirm_content_deletion.html", {"content_detail": content_obj})

def _options_to_json_response(queryset, include_create_new=True):
    options = [{"id": obj.pk, "text": str(obj)} for obj in queryset]
    return JsonResponse(options, safe=False)

def ajax_load_disciplines(request):
    area_id = request.GET.get("parent_id")
    queryset = Discipline.objects.filter(knowledge_area_id=area_id).order_by("name") if area_id else Discipline.objects.none()
    return _options_to_json_response(queryset)

def ajax_load_main_categories(request):
    discipline_id = request.GET.get("parent_id")
    queryset = MainCategory.objects.filter(discipline_id=discipline_id).order_by("name") if discipline_id else MainCategory.objects.none()
    return _options_to_json_response(queryset)

def ajax_load_topics(request):
    parent_model = request.GET.get("parent_model")
    parent_id = request.GET.get("parent_id")
    queryset = Topic.objects.none()
    if parent_id:
        if parent_model == "MainCategory":
            queryset = Topic.objects.filter(main_category_id=parent_id, parent__isnull=True).order_by("name")
        elif parent_model == "Topic":
            queryset = Topic.objects.filter(parent_id=parent_id).order_by("name")
    return _options_to_json_response(queryset)

def generate_share_image(request, pk):
    material = get_object_or_404(ContentMaterial, pk=pk)
    if not material.is_public and material.creator != request.user:
        raise Http404
    author_name = material.creator.get_full_name() or material.creator.username if material.creator else "Autor Anónimo"
    image_bytes = generate_share_image_bytes({"title": material.title, "author": author_name})
    if image_bytes:
        return HttpResponse(image_bytes, content_type="image/png")
    raise Http404()

def generate_default_share_image(request):
    image_bytes = generate_share_image_bytes()
    if image_bytes:
        return HttpResponse(image_bytes, content_type="image/png")
    raise Http404()
