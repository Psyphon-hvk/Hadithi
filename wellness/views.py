from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import BreathingExercise, JournalEntry, MindfulnessLog, MindfulnessSession


@login_required
def journal_list(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        body = request.POST.get("body", "").strip()
        mood = request.POST.get("mood", "").strip()
        if body:
            JournalEntry.objects.create(user=request.user, title=title, body=body, mood=mood)
            return redirect("wellness:journal")
    entries = JournalEntry.objects.filter(user=request.user)
    return render(request, "wellness/journal.html", {"entries": entries})


def breathing_list(request):
    exercises = BreathingExercise.objects.all()
    return render(request, "wellness/breathing.html", {"exercises": exercises})


def mindfulness_list(request):
    sessions = MindfulnessSession.objects.all()
    return render(request, "wellness/mindfulness.html", {"sessions": sessions})


@login_required
def mindfulness_complete(request, pk):
    session = get_object_or_404(MindfulnessSession, pk=pk)
    MindfulnessLog.objects.create(user=request.user, session=session)
    return redirect("wellness:mindfulness")


import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import anthropic

client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are a supportive reflection assistant inside a personal journaling app.
The user has just written about something on their mind. Respond with a short JSON object only:

{
  "reassurance": "1-2 warm, validating sentences. No clichés, no diagnosis, no clinical labels.",
  "options": ["2-4 short, concrete, non-clinical things they could try or consider"],
  "crisis": false
}

Rules:
- Never diagnose or name a mental health condition.
- Never give specific medication, dosage, or self-harm-method-adjacent information.
- If the text suggests the person may be in crisis, at risk of harming themselves or others,
  or in acute danger, set "crisis": true, keep "options" empty, and make "reassurance" a brief,
  calm, stabilizing message that encourages contacting a crisis line or trusted person immediately.
- Keep total output under 120 words.
- Output ONLY the JSON object, nothing else."""

@login_required
@require_POST
def ai_reflect(request):
    data = json.loads(request.body)
    text = (data.get("text") or "").strip()
    if not text:
        return JsonResponse({"error": "No text provided"}, status=400)

    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=400,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": text}],
    )

    raw = "".join(b.text for b in resp.content if b.type == "text")
    try:
        parsed = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        parsed = {"reassurance": "Thanks for sharing that.", "options": [], "crisis": False}

    return JsonResponse(parsed)