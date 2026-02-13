from django.urls import path
from . import views

app_name = 'assessment_v2'

urlpatterns = [
    path('create/', views.ExamCreateView.as_view(), name='exam_create'),
    path('generating/<uuid:uuid>/', views.ExamGeneratingView.as_view(), name='exam_generating'),
    path('status/<uuid:uuid>/', views.ExamStatusView.as_view(), name='exam_status'),
    path('take/<uuid:uuid>/', views.ExamTakeView.as_view(), name='take_exam'),
]
