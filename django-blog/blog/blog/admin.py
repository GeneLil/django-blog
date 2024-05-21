from django.contrib import admin
from .Models import Post, Tag, Comment, Like, UserProfile


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    
    list_display = ['title']
    
    class Meta:
        model = Tag

        
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    
    list_display = ['title', 'short_description', 'body', 'author', 'created_at', 'image', 'serialized_liked_by', 'serialized_tags']
    
    class Meta:
        model = Post
        

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    
    list_display = ['body', 'created_at', 'post', 'author']
    
    class Meta:
        model = Comment
    

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    
    list_display = ['user_id', 'post_id']
    
    class Meta:
        model = Like
        

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    
    list_display = ['user_id', 'avatar', 'dob', 'email']
    
    class Meta:
        model = UserProfile
        