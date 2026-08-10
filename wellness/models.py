from django.conf import settings
from django.db import models


class JournalEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="journal_entries")
    title = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    mood = models.CharField(max_length=50, blank=True, help_text="e.g. calm, stressed, hopeful")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Journal entries"

    def __str__(self):
        return f"{self.user} - {self.created_at:%Y-%m-%d}"


class BreathingExercise(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    inhale_seconds = models.PositiveIntegerField(default=4)
    hold_seconds = models.PositiveIntegerField(default=4)
    exhale_seconds = models.PositiveIntegerField(default=4)
    cycles = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.name


class MindfulnessSession(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    audio_url = models.URLField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.title


class MindfulnessLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mindfulness_logs")
    session = models.ForeignKey(MindfulnessSession, on_delete=models.CASCADE, related_name="logs")
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} completed {self.session}"
