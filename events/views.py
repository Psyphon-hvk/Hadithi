from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Event, EventRegistration


def event_list(request):
    upcoming = Event.objects.filter(is_published=True, start_time__gte=timezone.now())
    past = Event.objects.filter(is_published=True, start_time__lt=timezone.now())
    return render(request, "events/list.html", {"upcoming": upcoming, "past": past})


@login_required
def event_register(request, pk):
    event = get_object_or_404(Event, pk=pk, is_published=True)
    EventRegistration.objects.get_or_create(event=event, user=request.user)
    return redirect("events:list")
