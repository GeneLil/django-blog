"""Module for posts view"""
import json
from typing import List
from django.http import HttpRequest
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..models import Post, Comment, Like
from ..models.tag import get_tag_title
from ..forms import NewCommentForm


def get_tags_titles(tags):
    """Getting list of tags titles"""
    tags_titles = []
    for tag in tags.all():
        tags_titles.append(get_tag_title(tag))
    return tags_titles


def get_posts_by_tag_search(request: HttpRequest):
    """Get posts by list of tags"""
    json_request = json.loads(request.body)
    tag_search_input = json_request['tagTitle']
    posts_with_found_tags: List[Post] = []
    all_posts = Post.objects.all()
    for post in all_posts:
        for tag in post.tags.all():
            if str.lower(tag_search_input).strip() in str.lower(get_tag_title(tag)).strip():
                posts_with_found_tags.append(post)
                break

    serialized_posts = []
    for post in posts_with_found_tags:
        serialized_posts.append({
            'id': post.pk,
            'title': post.title,
            'tags': get_tags_titles(post.tags)
        })
    return JsonResponse({ 'posts': serialized_posts }) 


def get_single_post_context(request: HttpRequest, post_id: str):
        """Getting single post"""
        post = Post.objects.get(pk=post_id)
        user_id = request.user.pk
        user_can_edit_post = post.author.pk == user_id
        comments = Comment.objects.filter(post_id=post_id).order_by('-created_at')
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
    return {
        'posts': posts,
        'posts_liked_by_user': posts_liked_by_user
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
