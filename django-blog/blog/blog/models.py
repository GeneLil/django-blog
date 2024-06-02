"""Module for post model"""
from django.db import models
from accounts.models import CustomUser


class Tag(models.Model):
    """Class for tag model"""
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


def get_tag_title(tag: Tag):
    """Getting tag title from tag"""
    return Tag.objects.get(id=tag.pk).title


class Post(models.Model):
    """Class for post model"""
    title = models.CharField(max_length=255)
    short_description = models.TextField(blank=True)
    body = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=False, null=True)
    image = models.ImageField(upload_to="media")
    liked_by = models.ManyToManyField(CustomUser, related_name='liked_by')
    tags = models.ManyToManyField(Tag, related_name='posts')

    def __str__(self):
        return str(self.pk)

    def get_tags_names(self):
        """Getting tags titles from tags"""
        tags_names = []
        for tag in self.tags.all():
            tags_names.append(tag.title)
        return tags_names

    def serialized_liked_by(self):
        """Getting user names from post likes"""
        users_names = []
        if self.liked_by is not None:
            for user in self.liked_by.all():
                users_names.append(user.username)
        return users_names


class Comment(models.Model):
    """Class for comment model"""
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    body = models.TextField()


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
    