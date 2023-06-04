from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.searchArticle, name="article"),
    path("searchMatches", views.searchMatches, name = "searchMatches"),
    path("createArticle", views.createArticle, name = "createArticle"),
    path("edit/<str:title>", views.editArticle, name="editArticle"),
    path("randomPage", views.randomPage, name = "randomPage")
]
