from django.contrib import admin
from .models import StudySession, Streak

# Register your models here.

admin.site.register(StudySession)
admin.site.register(Streak)