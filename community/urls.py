from django.urls import path

from . import views

app_name = "community"

urlpatterns = [
    path("stories/", views.story_list, name="story_list"),
    path("stories/new/", views.story_create, name="story_create"),
    path("stories/<slug:slug>/", views.story_detail, name="story_detail"),
    path("stories/<slug:slug>/like/", views.toggle_like, name="toggle_like"),
    path("assessments/", views.assessment_list, name="assessment_list"),
    path("assessments/<int:pk>/take/", views.assessment_take, name="assessment_take"),
    path("assessments/my-results/", views.my_results, name="my_results"),
]
