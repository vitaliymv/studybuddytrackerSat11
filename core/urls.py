from django.urls import path
from .views import (
    RegistrationView,
    AddSubjectView,
    DashboardView,
    DeleteSubjectView,
    SubjectDetailView,
    StartSessionView,
    StopSessionView
)

urlpatterns = [
    path('register/', RegistrationView.as_view(), name="register"),
    path('', DashboardView.as_view(), name="dashboard"),
    path('subjects/add/', AddSubjectView.as_view(), name="add_subject"),
    path('subjects/<int:pk>/delete', DeleteSubjectView.as_view(), name="delete_subject"),
    path('subjects/<int:pk>/', SubjectDetailView.as_view(), name="subject_detail"),
    path("sessions/start/<int:subject_id>/", StartSessionView.as_view(), name="start_session"),
    path("sessions/stop/", StopSessionView.as_view(), name="stop_session")
]