from django.db import models
from accounts.models import CustomUser
from .Post import Post


class Like(models.Model):
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    