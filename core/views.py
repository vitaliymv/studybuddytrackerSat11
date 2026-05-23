from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.utils import timezone
from .forms import RegistrationForm
from .models import Subject, StudySession, Streak
import json

class RegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()

        subjects = Subject.objects.filter(user=self.request.user)
        sessions = StudySession.objects.filter(
            user=self.request.user,
            start_time__date=today
        )
        total_today = sum(session.duration for session in sessions)
        streak, _ = Streak.objects.get_or_create(
            user=self.request.user
        )

        context["subjects"] = subjects
        context["sessions"] = sessions
        context["total_today"] = total_today
        context["streak"] = streak
        context["chart_labels"] = json.dumps([
            s.subject.name for s in sessions
        ])
        context["chart_data"] = json.dumps([
            s.duration for s in sessions
        ])
        return context

