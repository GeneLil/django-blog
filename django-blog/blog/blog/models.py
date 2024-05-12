from django.db import models
from accounts.models import CustomUser


class Tag(models.Model):
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title


class Post(models.Model):
    
    title = models.CharField(max_length=255)
    short_description = models.TextField(blank=True)
    body = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="media")
    liked_by = models.ManyToManyField(CustomUser, related_name='liked_by')
    tags = models.ManyToManyField(Tag, related_name='tags')
    
    def serialized_tags(self):
        tags_names = []
        for tag in self.tags.all():
            tags_names.append(tag.title)
        return tags_names
            
    def serialized_liked_by(self):
        users_names = []
        print("LIKED BY", self.liked_by)
        if self.liked_by is not None:
            for user in self.liked_by.all():
                users_names.append(user.username)
        return users_names
            