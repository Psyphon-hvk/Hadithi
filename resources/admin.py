from django.contrib import admin

from .models import Bookmark, Resource, ResourceCategory


@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.action(description="Publish selected resources")
def publish_resources(modeladmin, request, queryset):
    queryset.update(is_published=True)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "resource_type", "is_published", "created_by", "created_at")
    list_filter = ("resource_type", "category", "is_published")
    search_fields = ("title", "summary", "tags")
    prepopulated_fields = {"slug": ("title",)}
    actions = [publish_resources]


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("user", "resource", "created_at")