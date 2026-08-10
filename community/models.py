from django.conf import settings
from django.db import models
from django.urls import reverse


class Story(models.Model):
    """HADITHI Stories - anonymous or named peer storytelling."""

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="stories")
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    body = models.TextField()
    is_anonymous = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True, help_text="Moderation flag for admins")
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_stories", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("community:story_detail", args=[self.slug])

    @property
    def display_author(self):
        return "Anonymous" if self.is_anonymous else str(self.author)


class Comment(models.Model):
    """Peer support discussion thread on a story."""

    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.author} on {self.story}"


class Assessment(models.Model):
    """Self-assessment tool definitions, e.g. PHQ-9, GAD-7, burnout index."""

    class AssessmentType(models.TextChoices):
        PHQ9 = "phq9", "PHQ-9 (Depression)"
        GAD7 = "gad7", "GAD-7 (Anxiety)"
        BURNOUT = "burnout", "Burnout Index"
        OTHER = "other", "Other"

    name = models.CharField(max_length=120)
    assessment_type = models.CharField(max_length=20, choices=AssessmentType.choices)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class AssessmentQuestion(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name="questions")
    order = models.PositiveIntegerField(default=0)
    text = models.CharField(max_length=500)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Q{self.order}: {self.text[:50]}"


class AssessmentResult(models.Model):
    """Stores a user's personal results and recommendation."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assessment_results")
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name="results")
    score = models.PositiveIntegerField()
    recommendation = models.TextField(blank=True)
    taken_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-taken_at"]

    def __str__(self):
        return f"{self.user} - {self.assessment} ({self.score})"
