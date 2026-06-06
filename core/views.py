from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView, DeleteView
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
    template_name = "tracker/dashboard.html"

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

class AddSubjectView(LoginRequiredMixin, CreateView):
    model = Subject
    template_name = "tracker/add_subject.html"
    fields = ["name"]
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class SubjectDetailView(LoginRequiredMixin, DetailView):
    model = Subject
    template_name = "tracker/subject_detail.html"
    context_object_name = "subject"

    def get_queryset(self):
        return Subject.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sessions = StudySession.objects.filter(
            subject=self.object
        )
        total_time = sum(
            s.duration for s in sessions
        )
        context["sessions"] = sessions
        context["total_time"] = total_time
        return context

class DeleteSubjectView(LoginRequiredMixin, DeleteView):
    model = Subject
    success_url = reverse_lazy("dashboard")

    def get_queryset(self):
        return Subject.objects.filter(user=self.request.user)

