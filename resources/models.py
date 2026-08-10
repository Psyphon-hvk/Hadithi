from django.conf import settings
from django.db import models
from django.urls import reverse


class ResourceCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon identifier, e.g. heroicon name")

    class Meta:
        verbose_name_plural = "Resource categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Resource(models.Model):
    class ResourceType(models.TextChoices):
        ARTICLE = "article", "Article"
        VIDEO = "video", "Video"
        PODCAST = "podcast", "Podcast"
        PDF_GUIDE = "pdf_guide", "PDF Guide"
        FAQ = "faq", "FAQ"

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE, related_name="resources")
    resource_type = models.CharField(max_length=20, choices=ResourceType.choices)
    summary = models.TextField(blank=True)
    body = models.TextField(blank=True, help_text="Article/FAQ body content")
    external_url = models.URLField(blank=True, help_text="For videos/podcasts hosted externally")
    file_upload = models.FileField(upload_to="resources/files/", blank=True, null=True)
    thumbnail = models.ImageField(upload_to="resources/thumbnails/", blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags")
    is_published = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="resources_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("resources:detail", args=[self.slug])

    @property
    def tag_list(self):
        return [t.strip() for t in self.tags.split(",") if t.strip()]


class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookmarks")
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name="bookmarked_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "resource")

    def __str__(self):
        return f"{self.user} bookmarked {self.resource}"
