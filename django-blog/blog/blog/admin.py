"""Module for admin panel"""
from django.contrib import admin
from comments.models import Comment
from post.models import Post
from .models import Like, UserProfile
from tag.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Class for admin section of tag"""
    list_display = ['title']

    class Meta:
        """Meta class for tag adminsection"""
        model = Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Class for admin section of post"""
    list_display = ['title', 'short_description', 'body',
                    'author', 'created_at', 'image', 
                    'serialized_liked_by', 'get_tags_names']

    class Meta:
        """Meta class for post adminsection"""
        model = Post


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Class for comment section of post"""
    list_display = ['body', 'created_at', 'post', 'author']

    class Meta:
        """Meta class for comment adminsection"""
        model = Comment


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """Class for like section of post"""
    list_display = ['user_id', 'post_id']

    class Meta:
        """Meta class for like adminsection"""
        model = Like


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Class for user profile section of post"""
    list_display = ['user_id', 'avatar', 'dob', 'email']

    class Meta:
        """Meta class for user profile adminsection"""
        model = UserProfile
        