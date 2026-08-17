from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable
)

from .models import Assessment, AssessmentQuestion, AssessmentResult, Comment, Story


class AssessmentQuestionInline(admin.TabularInline):
    model = AssessmentQuestion
    extra = 1


def export_stories_as_pdf(modeladmin, request, queryset):
    """
    Admin action: exports selected Stories, along with their full comment
    threads, as a single PDF report.
    """
    response = HttpResponse(content_type="application/pdf")
    filename = f"hadithi_stories_export_{timezone.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    doc = SimpleDocTemplate(
        response,
        pagesize=letter,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = ParagraphStyle(
        "StoryHeading", parent=styles["Heading2"], spaceBefore=6, spaceAfter=4,
    )
    meta_style = ParagraphStyle(
        "Meta", parent=styles["Normal"], textColor=colors.grey, fontSize=9, spaceAfter=8,
    )
    body_style = ParagraphStyle(
        "Body", parent=styles["Normal"], spaceAfter=10, leading=14,
    )
    comment_heading_style = ParagraphStyle(
        "CommentHeading", parent=styles["Heading3"], spaceBefore=10, spaceAfter=6,
    )
    comment_style = ParagraphStyle(
        "Comment", parent=styles["Normal"], leftIndent=14, spaceAfter=6, leading=13,
    )
    comment_meta_style = ParagraphStyle(
        "CommentMeta", parent=styles["Normal"], leftIndent=14, textColor=colors.grey,
        fontSize=8, spaceAfter=2,
    )

    elements = []

    elements.append(Paragraph("Hadithi — Stories & Conversations Export", title_style))
    elements.append(Paragraph(
        f"Generated {timezone.now().strftime('%d %b %Y, %H:%M')} · "
        f"{queryset.count()} storie(s) included",
        meta_style,
    ))
    elements.append(Spacer(1, 12))

    stories = queryset.order_by("-created_at").prefetch_related("comments__author")

    for index, story in enumerate(stories):
        if index > 0:
            elements.append(PageBreak())

        elements.append(Paragraph(story.title, heading_style))

        status = "Approved" if story.is_approved else "Pending moderation"
        elements.append(Paragraph(
            f"By: {story.display_author} &nbsp;|&nbsp; "
            f"Posted: {story.created_at.strftime('%d %b %Y, %H:%M')} &nbsp;|&nbsp; "
            f"Status: {status} &nbsp;|&nbsp; "
            f"Likes: {story.likes.count()}",
            meta_style,
        ))

        elements.append(HRFlowable(width="100%", color=colors.lightgrey, thickness=0.5))
        elements.append(Spacer(1, 6))

        # Story body — escape and preserve paragraph breaks
        for para in story.body.split("\n"):
            if para.strip():
                elements.append(Paragraph(para.strip(), body_style))

        comments = story.comments.all()
        elements.append(Paragraph(
            f"Conversation ({comments.count()} comment{'s' if comments.count() != 1 else ''})",
            comment_heading_style,
        ))

        if not comments:
            elements.append(Paragraph("No comments yet.", comment_meta_style))
        else:
            for comment in comments:
                elements.append(Paragraph(
                    f"{comment.author} · {comment.created_at.strftime('%d %b %Y, %H:%M')}",
                    comment_meta_style,
                ))
                for para in comment.body.split("\n"):
                    if para.strip():
                        elements.append(Paragraph(para.strip(), comment_style))

    doc.build(elements)
    return response


export_stories_as_pdf.short_description = "Download selected stories + conversations (PDF)"


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ("name", "assessment_type", "is_active")
    inlines = [AssessmentQuestionInline]


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_anonymous", "is_approved", "created_at")
    list_filter = ("is_anonymous", "is_approved")
    prepopulated_fields = {"slug": ("title",)}
    actions = [export_stories_as_pdf]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("story", "author", "created_at")


@admin.register(AssessmentResult)
class AssessmentResultAdmin(admin.ModelAdmin):
    list_display = ("user", "assessment", "score", "taken_at")
    list_filter = ("assessment",)