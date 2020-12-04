from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# TODO: Will need to add additional models to this file to represent details about posts, likes and followers