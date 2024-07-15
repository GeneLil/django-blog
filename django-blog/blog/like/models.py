from django.db import models
from post.models import Post
from accounts.models import CustomUser


class Like(models.Model):
    """Class for like model"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')