from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import *

import datetime

def index(request):
    all_posts = Post.objects.all()
    #TODO: figure out way to convert timestamp to local time
    return render(request, "network/index.html", {
        "all_posts": all_posts.order_by('-post_date')
    })

def following(request):
    # Page should only be available to users who are signed in
    if not request.user.is_authenticated:
        return render(request, "network/index.html")

    else:
        followed_users = Following.objects.filter(following_user=request.user).values_list('followed_user', flat=True)
        following_posts = Post.objects.filter(author__in=followed_users)

        return render(request, "network/following.html", {
            "following_posts": following_posts.order_by('-post_date')
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def new_post(request):
    if request.method == "POST":
        author = request.user
        content = request.POST["content"]

        # Attempt to create new post
        try:
            post = Post(author=author, content=content)
            # Save post to database
            post.save()

        except:
            return render(request, "network/index.html", {
                "message": "Sorry, we are unable to create your post at this time."
            })
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/index.html")

def profile(request, username):
    # Fetch the user object so it can be passed into the template
    desired_user = User.objects.filter(username=username).first()
    desired_user_posts = Post.objects.filter(author=desired_user)
    
    # If the user is not signed in
    if not request.user.is_authenticated:
        return render(request, "network/user_profile.html", {
            "desired_user": desired_user,
            "desired_user_posts": desired_user_posts.order_by('-post_date')
        })


    # Check if the logged in user is following the desired user already
    if Following.objects.filter(followed_user=desired_user, following_user=request.user).exists():
        is_following = True
    else:
        is_following = False


    return render(request, "network/user_profile.html", {
            "desired_user": desired_user,
            "desired_user_posts": desired_user_posts.order_by('-post_date'),
            "is_following": is_following
        })


"""
There HAS to be a better way to handle following/unfollowing users.
However, I will leave if for now so that I can progress with the project
TODO
"""
def followUser(request, username):
    # Fetch the object of the user being followed
    followed_user = User.objects.filter(username=username).first()
    followed_user_posts = Post.objects.filter(author=followed_user)

    following_user = request.user
    
    # Create new relation
    relation = Following(followed_user=followed_user, following_user=following_user)
    relation.save()

    # Update num_following and num_followers attributes of users
    followed_user.num_followers += 1
    followed_user.save()
    following_user.num_following += 1
    following_user.save()
   

    return render(request, "network/user_profile.html", {
            "desired_user": followed_user,
            "desired_user_posts": followed_user_posts.order_by('-post_date'),
            "is_following": True
        })


def unfollowUser(request, username):
    # Fetch the object of the user being followed
    followed_user = User.objects.filter(username=username).first()
    followed_user_posts = Post.objects.filter(author=followed_user)

    following_user = request.user
    
    # Delete relation
    Following.objects.filter(followed_user=followed_user, following_user=following_user).delete()

    # Update num_following and num_followers attributes of users
    followed_user.num_followers -= 1
    followed_user.save()
    following_user.num_following -= 1
    following_user.save()
   

    return render(request, "network/user_profile.html", {
            "desired_user": followed_user,
            "desired_user_posts": followed_user_posts.order_by('-post_date'),
            "is_following": False
        })