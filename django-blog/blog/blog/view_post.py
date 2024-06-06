"""Module for posts view"""
from django.http import HttpRequest
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .models import Post, Comment, Like, get_tag_title, UserProfile, Tag
from .forms import NewCommentForm


def get_single_post_context(request: HttpRequest, post_id: str):
    """Getting single post"""
    post = Post.objects.get(pk=post_id)
    user_id = request.user.pk
    user_can_edit_post = post.author.pk == user_id
    comments = Comment.objects.filter(post_id=post_id).order_by('-created_at')
    for comment in comments:
        user_profile = UserProfile.objects.get(user_id=comment.author.pk)
        if user_profile is not None:            
            comment.author_avatar = user_profile.avatar
    is_liked_by_user = Like.objects.filter(post_id=post_id).filter(user_id=user_id)
    return {
        'post': post,
        'tags': post.tags.all(),
        'can_edit_post': user_can_edit_post,
        'is_user_authenticated': request.user.is_authenticated,
        'add_comment_form': NewCommentForm(),
        'comments': comments,   
        'is_liked': bool(is_liked_by_user),
    }

def get_all_posts_context(request: HttpRequest):
    """"Getting all posts"""
    user = request.user
    posts = Post.objects.all()
    all_comments = Comment.objects.all()
    all_likes = Like.objects.all()
    posts_liked_by_user = []
    for post in posts:
        comments_for_post = all_comments.filter(post_id=post.pk)
        likes_for_post = all_likes.filter(post_id=post.pk)
        for like in likes_for_post:
            if like.user.pk == user.pk:
                posts_liked_by_user.append(post)
        post.comments_quantity = len(comments_for_post)
        post.likes_quantity = len(likes_for_post)
        
    all_tags = Tag.objects.all()
    posts_by_tags = []
    for tag in all_tags:
        posts_by_tag_num = len(posts.filter(tags__title=tag.title))
        if posts_by_tag_num > 0:
            posts_by_tags.append([tag.pk, tag.title, posts_by_tag_num])
    
    return {
        'posts': posts,
        'posts_liked_by_user': posts_liked_by_user,
        'posts_by_tags': posts_by_tags
    }


class PostsView(TemplateView):
    """Class for posts view"""
    all_posts__template = 'authorized/posts.html'
    post_details_template = 'authorized/post-details.html'

    def get(self, request: HttpRequest, **kwargs):
        """Get method for posts"""
        if request.user.is_authenticated:
            if 'pk' in kwargs:
                context = get_single_post_context(request, post_id=kwargs['pk'])
                return render(request, template_name=self.post_details_template, context=context)

            context = get_all_posts_context(request)
            return render(request, template_name=self.all_posts__template, context=context)
        return redirect('')
