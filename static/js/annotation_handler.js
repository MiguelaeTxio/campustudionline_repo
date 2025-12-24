// /home/MiguelAeTxio/CampuStudiOnline/static/js/annotation_handler.js

const config = window.annotationConfig;
const editableContent = document.getElementById('material-content');
const floatingToolbar = document.getElementById('floating-toolbar');
const noteModalElement = document.getElementById('noteModal');
const noteModal = noteModalElement ? new bootstrap.Modal(noteModalElement) : null;
const noteTextInput = document.getElementById('note-text-input');
const saveNoteButton = document.getElementById('save-note-button');
const annotationsListContainer = document.getElementById('annotations-list');
const saveCopyButton = document.getElementById('btn-save-copy');
const copyForm = document.getElementById('form-copy');
const hiddenContentInput = document.getElementById('hidden_html_content_input');
const isPublicCheckbox = document.getElementById('visible_is_public_checkbox');
const hiddenIsPublicInput = document.getElementById('hidden_is_public_input');

const initializePopovers = () => {
    const oldPopovers = document.querySelectorAll('[data-bs-toggle="popover"]');
    oldPopovers.forEach(el => {
        const popoverInstance = bootstrap.Popover.getInstance(el);
        if (popoverInstance) { popoverInstance.dispose(); }
    });
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
};

const getXPathForElement = (element, relativeTo) => {
    if (element.nodeType === Node.TEXT_NODE) {
        let parent = element.parentNode;
        let xpath = getXPathForElement(parent, relativeTo) + '/text()';
        let childNodes = parent.childNodes;
        let textNodeIndex = 0;
        let found = false;
        for (let i = 0; i < childNodes.length; i++) {
            if (childNodes[i].nodeType === Node.TEXT_NODE) {
                textNodeIndex++;
                if (childNodes[i] === element) { found = true; break; }
            }
        }
        if (found && textNodeIndex > 0) { return xpath + '[' + textNodeIndex + ']'; }
        return xpath + '[1]';
    }
    const parts = [];
    while (element && element.nodeType === Node.ELEMENT_NODE && element !== relativeTo) {
        let part = element.tagName.toLowerCase();
        let index = 1;
        let prevSibling = element.previousSibling;
        while (prevSibling) {
            if (prevSibling.nodeType === Node.ELEMENT_NODE && prevSibling.tagName === element.tagName) { index++; }
            prevSibling = prevSibling.previousSibling;
        }
        part += `[${index}]`;
        parts.unshift(part);
        element = element.parentNode;
    }
    return './' + parts.join('/');
};

if (editableContent) {
    let selectedRange = null;

    const showToast = (message, type = 'info') => {
        const container = document.getElementById('toast-container');
        if (!container) { console.error("Toast container not found!"); return; }
        const toastId = `toast-${Date.now()}`;
        const bgClass = type === 'error' ? 'bg-danger' : (type === 'success' ? 'bg-success' : 'bg-info');
        const toastHtml = `
            <div id="${toastId}" class="toast align-items-center text-white ${bgClass} border-0" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">${message}</div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>`;
        container.insertAdjacentHTML('beforeend', toastHtml);
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement, { delay: 3000 });
        toast.show();
        toastElement.addEventListener('hidden.bs.toast', () => toastElement.remove());
    };

    editableContent.addEventListener('keydown', (event) => {
        if (event.ctrlKey || event.metaKey || event.altKey || event.shiftKey) {
            if ((event.ctrlKey || event.metaKey) && ['v', 'x'].includes(event.key.toLowerCase())) {
                event.preventDefault();
                showToast('Pegar o cortar contenido está deshabilitado.', 'warning');
            }
            return;
        }
        const allowedKeys = ['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End', 'PageUp', 'PageDown', 'Escape', 'Tab'];
        if (allowedKeys.includes(event.key)) return;
        event.preventDefault();
        if (!document.querySelector('.toast.show')) {
             showToast('La edición directa está desactivada. Usa las herramientas.', 'info');
        }
    });

    editableContent.addEventListener('click', function(e) {
        const link = e.target.closest('a:not(.annotation-link)');
        if (link) { e.preventDefault(); window.location.href = link.href; }
    });

    document.addEventListener('selectionchange', () => {
        const selection = window.getSelection();
        if (!selection.isCollapsed && editableContent.contains(selection.anchorNode)) {
            const range = selection.getRangeAt(0);
            const rect = range.getBoundingClientRect();
            floatingToolbar.style.left = `${rect.left + rect.width / 2}px`;
            floatingToolbar.style.bottom = `${window.innerHeight - rect.top + 10}px`;
            floatingToolbar.classList.add('visible');
        } else {
            floatingToolbar.classList.remove('visible');
        }
    });

    const createAnnotation = (type) => {
        const selection = window.getSelection();
        if (selection.isCollapsed) { showToast('Por favor, selecciona texto primero.', 'warning'); return; }
        selectedRange = selection.getRangeAt(0).cloneRange();
        if (type === 'note') {
            if (noteModal) { noteTextInput.value = ''; noteModal.show(); }
        } else {
            const color = document.getElementById('floating-annotation-color').value;
            saveAnnotation(type, '', color);
        }
    };

    const handleSaveNote = () => {
        const content = noteTextInput.value.trim();
        if (!content) { showToast('El contenido de la nota no puede estar vacío.', 'warning'); return; }
        const color = document.getElementById('floating-annotation-color').value;
        saveAnnotation('note', content, color);
        if(noteModal) noteModal.hide();
    };

    const saveAnnotation = (type, content, color) => {
        if (!selectedRange) { showToast('No se ha guardado una selección válida.', 'error'); return; }
        const formData = new FormData();
        formData.append('annotation_type', type);
        formData.append('content', content);
        formData.append('color', color);
        formData.append('selected_text', selectedRange.toString().trim());
        formData.append('start_container_xpath', getXPathForElement(selectedRange.startContainer, editableContent));
        formData.append('start_offset', selectedRange.startOffset);
        formData.append('end_container_xpath', getXPathForElement(selectedRange.endContainer, editableContent));
        formData.append('end_offset', selectedRange.endOffset);

        fetch(config.createAnnotationUrl, {
            method: 'POST', headers: { 'X-CSRFToken': config.csrfToken }, body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                editableContent.innerHTML = data.content_html;
                addAnnotationToList(data.annotation);
                showToast('Anotación creada con éxito', 'success');
                initializePopovers();
            } else { throw new Error(data.message || 'Error desconocido del servidor.'); }
        })
        .catch(error => { showToast(`Error al guardar: ${error.message}`, 'error'); })
        .finally(() => { selectedRange = null; });
    };

    const deleteAnnotation = (annotationId) => {
        if (!confirm('¿Estás seguro de que quieres eliminar esta anotación?')) return;
        const url = config.deleteAnnotationUrlBase.replace('00000000-0000-0000-0000-000000000000', annotationId);
        fetch(url, {
            method: 'POST', headers: { 'X-CSRFToken': config.csrfToken }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                editableContent.innerHTML = data.content_html;
                document.getElementById(`li-annotation-${annotationId}`)?.parentElement.remove();
                if (annotationsListContainer.children.length === 1 && annotationsListContainer.firstElementChild.tagName !== 'A') {
                     annotationsListContainer.innerHTML = '<p class="text-muted">No tienes anotaciones en este material.</p>';
                }
                showToast('Anotación eliminada', 'success');
                initializePopovers();
            } else { throw new Error(data.message || 'Error al eliminar'); }
        })
        .catch(error => { showToast(`Error al eliminar: ${error.message}`, 'error'); });
    };

    const saveMainContent = (e) => {
        e.preventDefault();
        const button = e.currentTarget;
        button.disabled = true;
        button.innerHTML = `<i class="fas fa-spinner fa-spin me-1"></i> Guardando...`;
        if(hiddenContentInput) hiddenContentInput.value = editableContent.innerHTML;
        if(hiddenIsPublicInput) hiddenIsPublicInput.checked = isPublicCheckbox.checked;
        const formData = new FormData(copyForm);
        fetch(copyForm.action, {
            method: 'POST', body: formData, headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') { showToast('Cambios guardados correctamente.', 'success'); } 
            else { throw new Error(data.message || 'Error al guardar los cambios.'); }
        })
        .catch(error => { showToast(`Error: ${error.message}`, 'error'); })
        .finally(() => {
            button.disabled = false;
            button.innerHTML = `<i class="fas fa-save me-1"></i> Guardar Cambios`;
        });
    };

    const addAnnotationToList = (annotation) => {
        const noAnnotationsMsg = annotationsListContainer.querySelector('p.text-muted');
        if (noAnnotationsMsg) noAnnotationsMsg.remove();
        
        const existingLi = document.getElementById(`li-annotation-${annotation.id}`);
        if(existingLi) existingLi.parentElement.remove();

        let typeClass = 'bg-secondary text-white';
        let style = '';
        if (annotation.annotation_type === 'highlight') { typeClass = 'bg-warning text-dark'; style = `background-color: ${annotation.color};`; } 
        else if (annotation.annotation_type === 'note') { typeClass = 'bg-info text-dark'; style = `border-bottom: 2px dotted ${annotation.color};`; } 
        else if (annotation.annotation_type === 'mark') { typeClass = 'bg-danger text-white'; style = `color: ${annotation.color}; font-weight:bold;`; }
        
        let contentHtml = annotation.annotation_type === 'note' && annotation.selected_text ? `<em>Referencia: "${annotation.selected_text.substring(0, 50)}..."</em><br>${annotation.content}` : (annotation.selected_text || annotation.content);
        const date = new Date(annotation.created_at).toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit', year: '2-digit', hour: '2-digit', minute: '2-digit' });
        
        const newAnnotationHTML = `
            <a href="#annotation-${annotation.id}" class="annotation-link" data-annotation-id="${annotation.id}">
                <div class="annotation-item" id="li-annotation-${annotation.id}">
                    <div class="annotation-header d-flex justify-content-between align-items-center">
                        <span class="annotation-type badge ${typeClass}">${annotation.annotation_type_display}</span>
                        <div>
                            <small class="text-muted me-2">${date}</small>
                            <button class="btn-delete-annotation btn btn-sm btn-link text-danger p-0" data-id="${annotation.id}" title="Eliminar anotación"><i class="fas fa-trash"></i></button>
                        </div>
                    </div>
                    <div class="annotation-content" style="${style}">${contentHtml}</div>
                </div>
            </a>`;
        annotationsListContainer.insertAdjacentHTML('beforeend', newAnnotationHTML);
    };

    document.addEventListener('DOMContentLoaded', initializePopovers);
    document.getElementById('floating-btn-highlight').addEventListener('click', () => createAnnotation('highlight'));
    document.getElementById('floating-btn-note').addEventListener('click', () => createAnnotation('note'));
    document.getElementById('floating-btn-mark').addEventListener('click', () => createAnnotation('mark'));
    if (saveNoteButton) saveNoteButton.addEventListener('click', handleSaveNote);
    
    annotationsListContainer.addEventListener('click', e => {
        const deleteButton = e.target.closest('.btn-delete-annotation');
        if (deleteButton) {
            e.preventDefault();
            e.stopPropagation();
            deleteAnnotation(deleteButton.dataset.id);
        }
    });

    if (saveCopyButton) saveCopyButton.addEventListener('click', saveMainContent);
    initializePopovers();
}
