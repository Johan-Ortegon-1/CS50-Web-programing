
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("index_following", views.following_posts, name="index_following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:user_id>", views.profile, name="profile")
]
