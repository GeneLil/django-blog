from django.http import HttpRequest
from django.views.generic import TemplateView
from django.shortcuts import render
from ..Models import Post, Comment, Like
from ..forms import NewCommentForm


class PostsView(TemplateView):
    all_posts__template = 'authorized/posts.html'
    post_details_template = 'authorized/post-details.html'
    
    def post_details_context(self, request: HttpRequest, post_id: str):        
        post = Post.objects.get(pk=post_id)
        user_id = request.user.id
        user_can_edit_post = post.author.id == user_id     
        comments = Comment.objects.filter(post_id=post_id).order_by('-created_at')
        is_liked_by_user = Like.objects.filter(post_id=post_id).filter(user_id=user_id)
        return {
            'post': post,
            'tags': post.tags.all(),
            'can_edit_post': user_can_edit_post,
            'is_user_authenticated': request.user.is_authenticated,
            'add_comment_form': NewCommentForm(),
            'comments': comments,   
            'is_liked': True if is_liked_by_user else False,
        }
        
        
    def all_posts_context(self):
        posts = Post.objects.all()
        all_comments = Comment.objects.all()
        all_likes = Like.objects.all()        
        for post in posts:
            comments_for_post = all_comments.filter(post_id=post.id)
            likes_for_post = all_likes.filter(post_id=post.id)
            post.comments_quantity = len(comments_for_post)
            post.likes_quantity = len(likes_for_post)
        return {
            'posts': posts
        }
        
        
    def get(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:                  
            if 'pk' in kwargs:
                context = self.post_details_context(request, post_id=kwargs['pk'])
                return render(request, template_name=self.post_details_template, context=context)    
            
            context = self.all_posts_context()
            return render(request, template_name=self.all_posts__template, context=context)
