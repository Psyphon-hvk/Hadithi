from django.contrib import admin

from .models import Assessment, AssessmentQuestion, AssessmentResult, Comment, Story


class AssessmentQuestionInline(admin.TabularInline):
    model = AssessmentQuestion
    extra = 1


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ("name", "assessment_type", "is_active")
    inlines = [AssessmentQuestionInline]


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_anonymous", "is_approved", "created_at")
    list_filter = ("is_anonymous", "is_approved")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("story", "author", "created_at")


@admin.register(AssessmentResult)
class AssessmentResultAdmin(admin.ModelAdmin):
    list_display = ("user", "assessment", "score", "taken_at")
    list_filter = ("assessment",)
