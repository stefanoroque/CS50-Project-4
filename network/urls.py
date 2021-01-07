
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("userProfile/<str:username>", views.profile, name="profile"),
    path("following", views.following, name="following"),

    # API Routes
    path("like_unlike", views.like_unlike, name="like_unlike"),
    path("follow_unfollow", views.follow_unfollow, name="follow_unfollow")
]
