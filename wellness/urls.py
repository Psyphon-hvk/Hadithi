from django.urls import path

from . import views

app_name = "wellness"

urlpatterns = [
    path("journal/", views.journal_list, name="journal"),
    path("breathing/", views.breathing_list, name="breathing"),
    path("mindfulness/", views.mindfulness_list, name="mindfulness"),
    path("mindfulness/<int:pk>/complete/", views.mindfulness_complete, name="mindfulness_complete"),
    path("journal/ai-reflect/", views.ai_reflect, name="ai_reflect"),
]
