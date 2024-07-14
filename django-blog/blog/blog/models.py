"""Module for post model"""
from django.db import models
from accounts.models import CustomUser
from post.models import Post


class Like(models.Model):
    """Class for like model"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')


class UserProfile(models.Model):
    """Class for user profile model"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_profile')
    email = models.EmailField()
    dob = models.DateField()
    avatar = models.ImageField(upload_to='avatars')
    