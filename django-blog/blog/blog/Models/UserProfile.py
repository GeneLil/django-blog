from django.db import models
from accounts.models import CustomUser


class UserProfile(models.Model):
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_profile')
    email = models.EmailField()
    dob = models.DateField()
    avatar = models.ImageField(upload_to='avatars')
    