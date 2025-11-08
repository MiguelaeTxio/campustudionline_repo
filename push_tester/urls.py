from django.urls import path
from .views import PushTestView, ViewLogFileView

app_name = "push_tester"

urlpatterns = [
    path("", PushTestView.as_view(), name="test_page"),
    path("view-log/", ViewLogFileView.as_view(), name="view_log"),
]
