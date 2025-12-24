from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('', views.calendar_view, name='calendar_view'),
    path('api/feed/', views.api_events_feed, name='api_events_feed'),
    path('create/', views.AcademicEventCreateView.as_view(), name='event_create'),
    path('update/<int:pk>/', views.AcademicEventUpdateView.as_view(), name='event_update'),
    path('delete/<int:pk>/', views.AcademicEventDeleteView.as_view(), name='event_delete'),
]
