# /home/MiguelAeTxio/CampuStudiOnline/favorites_prototype/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseBadRequest
from .models import TestFolder

@login_required
def test_tree_view(request):
    root_folders = TestFolder.get_root_nodes().filter(user=request.user)
    context = {
        'nodes': root_folders
    }
    return render(request, 'favorites_prototype/test_tree.html', context)

@login_required
def folder_detail_view(request, folder_id):
    folder = get_object_or_404(TestFolder, id=folder_id, user=request.user)
    children = folder.get_children()
    ancestors = folder.get_ancestors()
    context = {
        'folder': folder,
        'nodes': children,
        'ancestors': ancestors,
    }
    return render(request, 'favorites_prototype/folder_detail.html', context)

@login_required
@require_http_methods(["POST"])
def create_folder_view(request):
    parent_id = request.POST.get('parent_id')
    folder_name = request.POST.get('folder_name')

    if not folder_name:
        return HttpResponseBadRequest("El nombre de la carpeta no puede estar vacío.")

    if parent_id:
        parent_folder = get_object_or_404(TestFolder, id=parent_id, user=request.user)
        parent_folder.add_child(name=folder_name, user=request.user)
        nodes = parent_folder.get_children()
    else:
        TestFolder.add_root(name=folder_name, user=request.user)
        nodes = TestFolder.get_root_nodes().filter(user=request.user)

    return render(request, 'favorites_prototype/_tree_nodes.html', {'nodes': nodes})

@login_required
@require_http_methods(["DELETE"])
def delete_folder_view(request, folder_id):
    folder = get_object_or_404(TestFolder, id=folder_id, user=request.user)
    folder.delete()
    return HttpResponse(status=200)

@login_required
def rename_folder_form_view(request, folder_id):
    folder = get_object_or_404(TestFolder, id=folder_id, user=request.user)
    return render(request, 'favorites_prototype/_rename_form.html', {'folder': folder})

@login_required
@require_http_methods(["POST"])
def rename_folder_view(request, folder_id):
    folder = get_object_or_404(TestFolder, id=folder_id, user=request.user)
    new_name = request.POST.get('new_folder_name')

    if not new_name:
        return HttpResponseBadRequest("El nuevo nombre no puede estar vacío.")

    folder.name = new_name
    folder.save()

    # Devolvemos el fragmento actualizado del nodo para que encaje en el nuevo span
    return HttpResponse(f'<a href="{folder.get_absolute_url()}">{folder.name}</a>')


