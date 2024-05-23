"""Module for like model"""
from django.db import models
from accounts.models import CustomUser
from .post import Post


class Like(models.Model):
    """Class for like model"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    