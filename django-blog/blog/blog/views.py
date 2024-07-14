"""File for ungrouped views"""
import json
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from post.models import Post
from tag.models import Tag, get_tags_titles


def home_view(request: HttpRequest):
    """View to resolve home url"""
    user = request.user
    if user.is_authenticated:
        return redirect('posts')
    return redirect('login')
    
    
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