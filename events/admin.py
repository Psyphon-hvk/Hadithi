from django.contrib import admin

from .models import Event, EventRegistration, PlatformEngagementSnapshot


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "event_type", "start_time", "is_published")
    list_filter = ("event_type", "is_published")


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "registered_at", "attended")


@admin.register(PlatformEngagementSnapshot)
class PlatformEngagementSnapshotAdmin(admin.ModelAdmin):
    list_display = ("date", "total_users", "active_users_7d", "stories_posted", "assessments_taken", "resources_viewed")
