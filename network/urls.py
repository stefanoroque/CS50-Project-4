
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("userProfile/<str:username>", views.profile, name="profile"),
    path("followUser/<str:username>", views.followUser, name="followUser"),
    path("unfollowUser/<str:username>", views.unfollowUser, name="unfollowUser"),
    path("following", views.following, name="following"),

    # API Routes
    path("like_unlike", views.like_unlike, name="like_unlike")
]
