from django.conf import settings
from django.db import models


class Event(models.Model):
    class EventType(models.TextChoices):
        WEBINAR = "webinar", "Webinar"
        IN_PERSON = "in_person", "In-person Event"
        WORKSHOP = "workshop", "Workshop"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    event_type = models.CharField(max_length=20, choices=EventType.choices, default=EventType.WEBINAR)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    location_or_link = models.CharField(max_length=500, blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_time"]

    def __str__(self):
        return self.title


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="event_registrations")
    registered_at = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)

    class Meta:
        unique_together = ("event", "user")

    def __str__(self):
        return f"{self.user} -> {self.event}"


class PlatformEngagementSnapshot(models.Model):
    """Aggregated analytics snapshot for research-friendly dashboards (Phase 4)."""

    date = models.DateField(unique=True)
    total_users = models.PositiveIntegerField(default=0)
    active_users_7d = models.PositiveIntegerField(default=0)
    stories_posted = models.PositiveIntegerField(default=0)
    assessments_taken = models.PositiveIntegerField(default=0)
    resources_viewed = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Snapshot {self.date}"
