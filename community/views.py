from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from .models import Assessment, AssessmentResult, Comment, Story


def story_list(request):
    stories = Story.objects.filter(is_approved=True).select_related("author")
    return render(request, "community/story_list.html", {"stories": stories})


def story_detail(request, slug):
    story = get_object_or_404(Story, slug=slug, is_approved=True)
    if request.method == "POST" and request.user.is_authenticated:
        body = request.POST.get("body", "").strip()
        if body:
            Comment.objects.create(story=story, author=request.user, body=body)
            return redirect("community:story_detail", slug=slug)
    return render(request, "community/story_detail.html", {"story": story})


@login_required
def story_create(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        body = request.POST.get("body", "").strip()
        is_anonymous = bool(request.POST.get("is_anonymous"))
        if title and body:
            slug = slugify(title)[:50] or "story"
            unique_slug = slug
            counter = 1
            while Story.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{slug}-{counter}"
                counter += 1
            story = Story.objects.create(
                author=request.user, title=title, slug=unique_slug, body=body, is_anonymous=is_anonymous
            )
            return redirect("community:story_detail", slug=story.slug)
    return render(request, "community/story_form.html")


@login_required
def toggle_like(request, slug):
    story = get_object_or_404(Story, slug=slug)
    if request.user in story.likes.all():
        story.likes.remove(request.user)
    else:
        story.likes.add(request.user)
    return redirect("community:story_detail", slug=slug)


def assessment_list(request):
    assessments = Assessment.objects.filter(is_active=True)
    return render(request, "community/assessment_list.html", {"assessments": assessments})


@login_required
def assessment_take(request, pk):
    assessment = get_object_or_404(Assessment, pk=pk, is_active=True)
    questions = assessment.questions.all()

    if request.method == "POST":
        score = 0
        for question in questions:
            score += int(request.POST.get(f"q_{question.id}", 0))

        if score <= 4:
            recommendation = "Your responses suggest minimal concern. Keep practicing self-care."
        elif score <= 9:
            recommendation = "Your responses suggest mild concern. Consider exploring the wellness toolkit."
        elif score <= 14:
            recommendation = "Your responses suggest moderate concern. Consider talking to a peer or counselor."
        else:
            recommendation = "Your responses suggest significant concern. Please reach out to a mental health professional."

        result = AssessmentResult.objects.create(
            user=request.user, assessment=assessment, score=score, recommendation=recommendation
        )
        return render(request, "community/assessment_result.html", {"result": result})

    return render(request, "community/assessment_take.html", {"assessment": assessment, "questions": questions})


@login_required
def my_results(request):
    results = AssessmentResult.objects.filter(user=request.user).select_related("assessment")
    return render(request, "community/my_results.html", {"results": results})
