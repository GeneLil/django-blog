from django.http import HttpRequest
from django.views.generic import TemplateView
from django.shortcuts import render
from ..Models import Post, Comment, Like, Tag
from ..Models.Tag import get_tag_title
from ..forms import NewCommentForm
from django.http import JsonResponse
import json
from django.core import serializers
from typing import List


def get_tags_titles(tags):
    tags_titles = []
    for tag in tags.all():
        tags_titles.append(get_tag_title(tag))
    return tags_titles


def get_posts_by_tags(request: HttpRequest):
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


class PostsView(TemplateView):
    all_posts__template = 'authorized/posts.html'
    post_details_template = 'authorized/post-details.html'
    
    def get_single_post(self, request: HttpRequest, post_id: str):        
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
        
        
    def get_all_posts(self):
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
                context = self.get_single_post(request, post_id=kwargs['pk'])
                return render(request, template_name=self.post_details_template, context=context)    
            
            context = self.get_all_posts()
            return render(request, template_name=self.all_posts__template, context=context)
