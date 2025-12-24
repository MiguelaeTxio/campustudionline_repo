from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from .models import AcademicEvent
from .forms import AcademicEventForm

class AcademicEventCreateView(LoginRequiredMixin, CreateView):
    model = AcademicEvent
    form_class = AcademicEventForm
    template_name = 'schedule/event_form.html'
    success_url = reverse_lazy('schedule:calendar_view')

    def get_initial(self):
        initial = super().get_initial()
        # Pre-rellenar fecha si viene por GET
        start_param = self.request.GET.get('start_time')
        if start_param:
            initial['start_time'] = start_param
            initial['end_time'] = start_param 
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class AcademicEventUpdateView(LoginRequiredMixin, UpdateView):
    model = AcademicEvent
    form_class = AcademicEventForm
    template_name = 'schedule/event_form.html'
    success_url = reverse_lazy('schedule:calendar_view')
    
    def get_queryset(self):
        return self.request.user.academic_events.all()

class AcademicEventDeleteView(LoginRequiredMixin, DeleteView):
    model = AcademicEvent
    template_name = 'schedule/event_confirm_delete.html'
    success_url = reverse_lazy('schedule:calendar_view')
    
    def get_queryset(self):
        return self.request.user.academic_events.all()

@login_required
def api_events_feed(request):
    start_str = request.GET.get('start')
    end_str = request.GET.get('end')
    
    events_query = AcademicEvent.objects.filter(user=request.user)
    
    if start_str and end_str:
        start_date = parse_datetime(start_str)
        end_date = parse_datetime(end_str)
        if start_date and end_date:
            events_query = events_query.filter(start_time__gte=start_date, start_time__lte=end_date)
    
    events_data = []
    COLOR_MAP = {
        'EX': '#dc3545', 'CL': '#0d6efd', 'PR': '#198754',
        'DL': '#ffc107', 'TU': '#0dcaf0', 'ST': '#6c757d', 'PE': '#6610f2'
    }

    for event in events_query:
        color = COLOR_MAP.get(event.event_type, '#3788d8')
        events_data.append({
            'id': event.id,
            'title': f"[{event.get_event_type_display()}] {event.title}",
            'start': event.start_time.isoformat(),
            'end': event.end_time.isoformat() if event.end_time else None,
            'allDay': event.is_all_day,
            'backgroundColor': color,
            'borderColor': color,
            'extendedProps': {
                'location': event.location,
                'description': event.description,
                'subject': event.subject.name if event.subject else None
            }
        })
    return JsonResponse(events_data, safe=False)

@login_required
def calendar_view(request):
    return render(request, 'schedule/calendar_main.html')
