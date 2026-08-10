from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from community.models import Story
from events.models import Event
from resources.models import Resource


def home(request):
    return render(request, "core/home.html")


@login_required
def dashboard(request):
    context = {
        "recent_resources": Resource.objects.filter(is_published=True)[:5],
        "recent_stories": Story.objects.filter(is_approved=True)[:5],
        "upcoming_events": Event.objects.filter(is_published=True)[:5],
    }
    return render(request, "core/dashboard.html", context)
