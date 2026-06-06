from django.urls import path
from .views import (
    RegistrationView,
    AddSubjectView,
    DashboardView,
    DeleteSubjectView,
    SubjectDetailView
)

urlpatterns = [
    path('register/', RegistrationView.as_view(), name="register"),
    path('', DashboardView.as_view(), name="dashboard"),
    path('subjects/add/', AddSubjectView.as_view(), name="add_subject"),
    path('subjects/<int:pk>/delete', DeleteSubjectView.as_view(), name="delete_subject"),
    path('subjects/<int:pk>/', SubjectDetailView.as_view(), name="subject_detail")
]