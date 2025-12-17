from django.urls import path
from . import views

app_name = 'universia'

urlpatterns = [
    path('api/chat/', views.chat_api, name='chat_api'),
    path('api/history/', views.get_history_api, name='history_api'),
]
