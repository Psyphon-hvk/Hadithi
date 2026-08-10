from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Bookmark, Resource, ResourceCategory


def resource_list(request):
    resources = Resource.objects.filter(is_published=True).select_related("category")

    query = request.GET.get("q", "")
    category_slug = request.GET.get("category", "")
    resource_type = request.GET.get("type", "")

    if query:
        resources = resources.filter(
            Q(title__icontains=query) | Q(summary__icontains=query) | Q(tags__icontains=query)
        )
    if category_slug:
        resources = resources.filter(category__slug=category_slug)
    if resource_type:
        resources = resources.filter(resource_type=resource_type)

    context = {
        "resources": resources,
        "categories": ResourceCategory.objects.all(),
        "resource_types": Resource.ResourceType.choices,
        "query": query,
        "selected_category": category_slug,
        "selected_type": resource_type,
    }
    return render(request, "resources/list.html", context)


def resource_detail(request, slug):
    resource = get_object_or_404(Resource, slug=slug, is_published=True)
    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(user=request.user, resource=resource).exists()
    return render(request, "resources/detail.html", {"resource": resource, "is_bookmarked": is_bookmarked})


@login_required
def toggle_bookmark(request, slug):
    resource = get_object_or_404(Resource, slug=slug)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, resource=resource)
    if not created:
        bookmark.delete()
    return redirect("resources:detail", slug=slug)


@login_required
def my_bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related("resource")
    return render(request, "resources/bookmarks.html", {"bookmarks": bookmarks})


from django.contrib import messages
from .forms import ResourceSubmissionForm


@login_required
def submit_resource(request):
    if request.method == "POST":
        form = ResourceSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save()
            resource.created_by = request.user
            resource.save(update_fields=["created_by"])
            messages.success(request, "Thanks! Your resource was submitted and is pending review.")
            return redirect("resources:list")
    else:
        form = ResourceSubmissionForm()
    return render(request, "resources/submit.html", {"form": form})