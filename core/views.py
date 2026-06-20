from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Sum, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
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
        s = subjects.annotate(total_seconds=Sum(
            "studysession__duration",
            filter=Q(studysession__start_time__date=today)
        ))

        context["subjects"] = subjects
        context["sessions"] = sessions
        context["total_today"] = total_today
        context["streak"] = streak
        context["chart_labels"] = json.dumps([
            sub.name for sub in s
        ])
        context["chart_data"] = json.dumps([
            sub.total_seconds for sub in s
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

class StartSessionView(LoginRequiredMixin, View):
    def post(self, request, subject_id):
        subject = get_object_or_404(Subject, id=subject_id, user=request.user)

        s = StudySession.objects.filter(
            user=request.user,
            end_time__isnull=True
        )

        if s:
            s = s.first()
            s.end_time = timezone.now()
            duration = (s.end_time - s.start_time).total_seconds()
            s.duration = int(duration)
            s.save()
        session = StudySession.objects.create(
            user=request.user,
            subject=subject,
            start_time=timezone.now()
        )

        return JsonResponse({
            "success": True,
            "session_id": session.id,
            "start_time": session.start_time.timestamp(),
            "subject": subject.name
        })

from .utils import update_streak
class StopSessionView(LoginRequiredMixin, View):
    def post(self, request):
        session = StudySession.objects.filter(
            user=request.user,
            end_time__isnull=True
        ).first()

        if not session:
            return JsonResponse({
                "success": False,
                "message": "No active session"
            })

        session.end_time = timezone.now()
        duration = (session.end_time - session.start_time).total_seconds()
        session.duration = int(duration)
        session.save()
        update_streak(request.user)
        return JsonResponse({
            "success": True,
            "duration": session.duration,
            "message": "Session stoped"
        })
