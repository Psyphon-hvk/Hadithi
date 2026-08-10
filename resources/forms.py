from django import forms
from django.utils.text import slugify

from .models import Resource

INPUT_CLASSES = "w-full border rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-hadithi-500"


class ResourceSubmissionForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = [
            "title",
            "category",
            "resource_type",
            "summary",
            "body",
            "external_url",
            "file_upload",
            "thumbnail",
            "tags",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "category": forms.Select(attrs={"class": INPUT_CLASSES}),
            "resource_type": forms.Select(attrs={"class": INPUT_CLASSES}),
            "summary": forms.Textarea(attrs={"class": INPUT_CLASSES, "rows": 3}),
            "body": forms.Textarea(attrs={"class": INPUT_CLASSES, "rows": 8}),
            "external_url": forms.URLInput(attrs={"class": INPUT_CLASSES}),
            "file_upload": forms.ClearableFileInput(attrs={"class": "w-full text-sm"}),
            "thumbnail": forms.ClearableFileInput(attrs={"class": "w-full text-sm"}),
            "tags": forms.TextInput(attrs={"class": INPUT_CLASSES}),
        }

    def save(self, commit=True):
        resource = super().save(commit=False)
        base_slug = slugify(resource.title)
        slug = base_slug
        i = 1
        while Resource.objects.filter(slug=slug).exists():
            i += 1
            slug = f"{base_slug}-{i}"
        resource.slug = slug
        resource.is_published = False
        if commit:
            resource.save()
        return resource