from django.urls import path

from . import views

app_name = "resources"

urlpatterns = [
    path("", views.resource_list, name="list"),
    path("submit/", views.submit_resource, name="submit"),   # must come before <slug:slug>/
    path("bookmarks/", views.my_bookmarks, name="bookmarks"),
    path("<slug:slug>/", views.resource_detail, name="detail"),
    path("<slug:slug>/bookmark/", views.toggle_bookmark, name="toggle_bookmark"),
]