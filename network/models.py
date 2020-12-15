from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    num_following = models.IntegerField(default=0)
    num_followers = models.IntegerField(default=0)

# TODO: Will need to add additional models to this file to represent details about posts, likes and followers
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    # post_date uses server time so we will need to convert when displaying the post
    post_date = models.DateTimeField(default=timezone.now)
    num_likes = models.IntegerField(default=0)

class Following(models.Model):
    username = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_username = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)