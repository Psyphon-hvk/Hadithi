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


"""
TEMPORARY debug view — add this to core/views.py (or any app's views.py),
wire it up in urls.py, check the output, then DELETE both once you're done.
Do not leave this in a production app long-term — it exposes filesystem info.
"""

import os
from django.conf import settings
from django.http import JsonResponse


def debug_media(request):
    resources_path = os.path.join(settings.MEDIA_ROOT, "resources", "files")

    files_found = []
    if os.path.exists(resources_path):
        files_found = os.listdir(resources_path)

    media_root_exists = os.path.exists(settings.MEDIA_ROOT)

    return JsonResponse({
        "DEBUG": settings.DEBUG,
        "MEDIA_ROOT": str(settings.MEDIA_ROOT),
        "MEDIA_URL": settings.MEDIA_URL,
        "media_root_exists": media_root_exists,
        "resources_files_path": resources_path,
        "resources_files_path_exists": os.path.exists(resources_path),
        "files_found": files_found,
        "cwd": os.getcwd(),
    })