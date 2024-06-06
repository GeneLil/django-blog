"""File for posts by tag class"""
import json
from django.http import HttpRequest
from django.views.generic import TemplateView
from django.http import JsonResponse
from .models import Post, get_tag_title, Tag
from django.shortcuts import render, redirect


def get_tags_titles(tags):
    """Getting list of tags titles"""
    tags_titles = []
    for tag in tags.all():
        tags_titles.append(get_tag_title(tag))
    return tags_titles


class PostsByTag(TemplateView):
    """Class to process posts by tag queries"""
    template_name = 'authorized/posts-by-tag.html'
    
    def get(self, request: HttpRequest,  **kwargs):
        """Get all posts by tags"""        
        if 'pk' in kwargs:
            tag_title = Tag.objects.get(pk=kwargs['pk']).title
            posts = Post.objects.filter(tags__title=tag_title)
            context = {
            'posts': posts,
            'title': tag_title
            }
            return render(request, template_name=self.template_name, context=context)
        return redirect('posts')
            
    def post(self, request: HttpRequest):        
        """Search posts by tag title"""
        json_request = json.loads(request.body)
        tag_search_input = json_request['tagTitle']    
        
        serialized_posts = []
        found_posts = Post.objects.filter(tags__title__icontains=str.lower(tag_search_input).strip())
        for post in found_posts:
            serialized_posts.append({
                'id': post.pk,
                'title': post.title,
                'tags': get_tags_titles(post.tags)
            })
        return JsonResponse({ 'posts': serialized_posts })