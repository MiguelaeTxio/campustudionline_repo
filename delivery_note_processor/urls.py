# /home/MiguelAeTxio/CampuStudiOnline/delivery_note_processor/urls.py
from django.urls import path
from . import views

app_name = 'delivery_note_processor'

urlpatterns = [
    path('', views.delivery_note_list, name='delivery_note_list'),
    path('upload/', views.DeliveryNoteUploadView.as_view(), name='upload_delivery_note'),
    path('detail/<int:pk>/', views.delivery_note_detail, name='delivery_note_detail'),
    path('resolve/<int:pk>/', views.resolve_vehicle_issue, name='resolve_vehicle_issue'),
]
