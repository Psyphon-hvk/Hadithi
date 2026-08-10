from django.contrib import admin

from .models import BreathingExercise, JournalEntry, MindfulnessLog, MindfulnessSession


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "mood", "created_at")


@admin.register(BreathingExercise)
class BreathingExerciseAdmin(admin.ModelAdmin):
    list_display = ("name", "inhale_seconds", "hold_seconds", "exhale_seconds", "cycles")


@admin.register(MindfulnessSession)
class MindfulnessSessionAdmin(admin.ModelAdmin):
    list_display = ("title", "duration_minutes")


@admin.register(MindfulnessLog)
class MindfulnessLogAdmin(admin.ModelAdmin):
    list_display = ("user", "session", "completed_at")
