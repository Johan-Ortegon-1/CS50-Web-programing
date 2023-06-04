from django.urls import include, path

from excercise import admin

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("explore", views.explore, name="explore"),
    path("request", views.request, name="request"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_routine", views.create_routine, name="create_routine"),
    path("<int:exercise_id>", views.exercise_detail, name="exercise"),
    path("edit", views.edit_routine, name="edit_routine"),
    path("api", views.apiOverview, name="api"),
    path("api_list/<int:pk>", views.apiList, name="api_list"),
    path("api_update_position/<int:pk>", views.apiUpdatePosition, name="api_update_position"),
    path("api_update_repetition/<int:pk>", views.apiUpdateRepetitions, name="api_update_repetitions"),
    path("api_delete/<int:pk>", views.apiDelete, name="api_delete")
]