from django.db import models
from accounts.models import CustomUser
from .Post import Post


class Comment(models.Model):
    
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    