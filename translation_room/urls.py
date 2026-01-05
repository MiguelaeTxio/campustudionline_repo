from django.urls import path
from .views import TranslationHomeView, TranslationStreamView

app_name = 'translation_room'

urlpatterns = [
    path('', TranslationHomeView.as_view(), name='home'),
    path('stream/', TranslationStreamView.as_view(), name='stream'),
]
