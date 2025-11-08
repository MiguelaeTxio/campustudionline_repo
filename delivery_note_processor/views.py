# /home/MiguelAeTxio/CampuStudiOnline/delivery_note_processor/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.views.decorators.http import require_POST

from .forms import DeliveryNoteUploadForm, VehicleResolutionForm
from .tasks import process_delivery_note_image_task
from .models import DeliveryNote, Vehicle


def is_staff(user):
    return user.is_staff

class DeliveryNoteUploadView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Vista basada en clase para manejar la subida de albaranes,
    compatible con subidas tradicionales y peticiones AJAX.
    """
    model = DeliveryNote
    form_class = DeliveryNoteUploadForm
    template_name = 'delivery_note_processor/upload_form.html'
    
    def test_func(self):
        return is_staff(self.request.user)

    def form_valid(self, form):
        # El objeto se guarda aquí por el super()
        response = super().form_valid(form)
        
        # Encolamos la tarea asíncrona
        transaction.on_commit(lambda: process_delivery_note_image_task.delay(self.object.id))
        
        # Distinguimos entre peticiones AJAX y normales
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'redirect_url': self.get_success_url()
            })
        else:
            messages.success(
                self.request,
                f'El albarán (ID: {self.object.id}) se ha subido correctamente y su procesamiento ha sido encolado.'
            )
            return response

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Aplanamos los errores para un JSON simple
            error_list = [f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()]
            return JsonResponse({'success': False, 'error': '; '.join(error_list)}, status=400)
        else:
            messages.error(self.request, 'Hubo un error con el formulario. Por favor, revisa los datos.')
            return super().form_invalid(form)

    def get_success_url(self):
        # Para la respuesta JSON, necesitamos la URL real. Para la redirección normal, CreateView la usa internamente.
        return reverse_lazy('delivery_note_processor:delivery_note_list')


@login_required
@user_passes_test(is_staff)
def delivery_note_list(request):
    """
    Muestra una lista paginada de todos los albaranes procesados.
    """
    notes = DeliveryNote.objects.all().order_by('-uploaded_at')
    return render(request, 'delivery_note_processor/delivery_note_list.html', {'notes': notes})

@login_required
@user_passes_test(is_staff)
def delivery_note_detail(request, pk):
    """
    Muestra el detalle de un albarán y, si es necesario, el formulario de resolución.
    """
    note = get_object_or_404(DeliveryNote, pk=pk)
    resolution_form = None
    if note.status == 'needs_review':
        resolution_form = VehicleResolutionForm(extracted_code=note.extracted_vehicle_code)
        
    context = {
        'note': note,
        'resolution_form': resolution_form
    }
    return render(request, 'delivery_note_processor/delivery_note_detail.html', context)

@login_required
@user_passes_test(is_staff)
@require_POST
def resolve_vehicle_issue(request, pk):
    """
    Procesa el formulario de creación de un nuevo vehículo y lo asigna al albarán.
    """
    note = get_object_or_404(DeliveryNote, pk=pk, status='needs_review')
    form = VehicleResolutionForm(request.POST)

    if form.is_valid():
        try:
            # Usamos get_or_create para evitar race conditions si dos usuarios intentan crearlo a la vez.
            new_vehicle, created = Vehicle.objects.get_or_create(
                code=form.cleaned_data['code'],
                defaults={
                    'license_plate': form.cleaned_data['license_plate'],
                    'vehicle_type': form.cleaned_data['vehicle_type'],
                }
            )
            
            if created:
                messages.success(request, f"Vehículo '{new_vehicle.code}' creado con éxito.")
            else:
                messages.info(request, f"Se ha utilizado el vehículo existente '{new_vehicle.code}'.")

            note.vehicle = new_vehicle
            note.status = 'completed'
            note.save()
            
            messages.success(request, f"Albarán #{note.id} asignado correctamente al vehículo '{new_vehicle.code}'.")

        except Exception as e:
            messages.error(request, f"Error al crear el vehículo: {e}")

    else:
        # Si el formulario no es válido, lo cual es raro, mostramos los errores.
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"Error en el campo '{field}': {error}")

    return redirect('delivery_note_processor:delivery_note_detail', pk=note.pk)
