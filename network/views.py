import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import *

import datetime

# Constants
NUM_POSTS_PER_PAGE = 10

def index(request):
    all_posts = Post.objects.all().order_by('-post_date')

    paginator = Paginator(all_posts, NUM_POSTS_PER_PAGE)
    page = request.GET.get('page')

    posts = paginator.get_page(page)

    #TODO: figure out way to convert timestamp to local time
    return render(request, "network/index.html", {
        "posts": posts
    })

def following(request):
    # Page should only be available to users who are signed in
    if not request.user.is_authenticated:
        return render(request, "network/index.html")

    else:
        followed_users = Following.objects.filter(following_user=request.user).values_list('followed_user', flat=True)
        following_posts = Post.objects.filter(author__in=followed_users).order_by('-post_date')

        paginator = Paginator(following_posts, NUM_POSTS_PER_PAGE)
        page = request.GET.get('page')

        posts = paginator.get_page(page)




        return render(request, "network/following.html", {
            "posts": posts
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
    desired_user_posts = Post.objects.filter(author=desired_user).order_by('-post_date')

    paginator = Paginator(desired_user_posts, NUM_POSTS_PER_PAGE)
    page = request.GET.get('page')

    posts = paginator.get_page(page)
    
    # If the user is not signed in
    if not request.user.is_authenticated:
        return render(request, "network/user_profile.html", {
            "desired_user": desired_user,
            "posts": posts
        })


    # Check if the logged in user is following the desired user already
    if Following.objects.filter(followed_user=desired_user, following_user=request.user).exists():
        is_following = True
    else:
        is_following = False


    return render(request, "network/user_profile.html", {
            "desired_user": desired_user,
            "posts": posts,
            "is_following": is_following
        })

@csrf_exempt
@login_required
def like_unlike(request):

    # Liking/unliking a post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get the post's id
    data = json.loads(request.body)
    post_id = data.get("post_id")
    # Get post object
    post = Post.objects.get(id=post_id)
    
    # Find out if user has liked the post already
    if Likes.objects.filter(liked_post=post, liking_user=request.user).exists():
        # User has already liked post
        # Delete Likes relation
        Likes.objects.filter(liked_post=post, liking_user=request.user).delete()
        # Decrease like attribute on post
        post.num_likes -= 1
        post.save()
        # Return message to JS function
        return JsonResponse({"message": "post unliked successfully"}, status=201)

    else:
        # User has not like post yet
        # Create a new Likes object
        likes = Likes(liked_post=post, liking_user=request.user)
        likes.save()
        # Increase like attribute on post
        post.num_likes += 1
        post.save()
        # Return message to JS function
        return JsonResponse({"message": "post liked successfully"}, status=201)
        

    
@csrf_exempt
@login_required
def follow_unfollow(request):
    # following/unfollowing a user must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get the desired user's username
    data = json.loads(request.body)
    desired_username = data.get("desired_username")
    # Get desired user object
    desired_user = User.objects.filter(username=desired_username).first()

    # Check if current_user is already following desired_user
    if Following.objects.filter(followed_user=desired_user, following_user=request.user).exists():
        # Already following
        # Delete Following relation
        Following.objects.filter(followed_user=desired_user, following_user=request.user).delete()
        # Decrease followers attribute on desired_user
        desired_user.num_followers -= 1
        desired_user.save()
        # Return message to JS function
        return JsonResponse({"message": "user unfollowed successfully"}, status=201)
    else:
        # Not following yet
        # Create a new Following relation
        following = Following(followed_user=desired_user, following_user=request.user)
        following.save()
        # Increase followers attribute on desired_user
        desired_user.num_followers += 1
        desired_user.save()
        # Return message to JS function
        return JsonResponse({"message": "user followed successfully"}, status=201)


@csrf_exempt
@login_required
def edit_post(request):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    data = json.loads(request.body)
    # Get post object
    post_id = data.get("post_id")
    post = Post.objects.get(id=post_id)
    # Get the new post content
    new_content = data.get("new_content")

    # Edit the post
    post.content = new_content
    try:
        post.save()
    except:
        return JsonResponse({"message": "unable to edit post"}, status=401)
    
    # Return message to JS function
    return JsonResponse({"message": "post edited successfully"}, status=201)