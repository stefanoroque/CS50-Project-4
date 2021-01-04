from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    num_following = models.IntegerField(default=0)
    num_followers = models.IntegerField(default=0)

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    # post_date uses server time so we will need to convert when displaying the post
    post_date = models.DateTimeField(default=timezone.now)
    num_likes = models.IntegerField(default=0)

class Following(models.Model):
    followed_user = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)

class Likes(models.Model):
    liked_post = models.ForeignKey(Post, related_name="liked", on_delete=models.CASCADE)
    liking_user = models.ForeignKey(User, related_name="liker", on_delete=models.CASCADE)