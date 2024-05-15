from django.contrib import admin
from .models import Post, Tag, Comment


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
    