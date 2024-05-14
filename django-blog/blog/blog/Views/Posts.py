from django.http import HttpRequest
from django.views.generic import TemplateView
from django.shortcuts import render
from ..models import Post


class PostsView(TemplateView):
    all_posts__template = 'authorized/posts.html'
    post_details_template = 'authorized/post-details.html'
    
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}        
        if 'pk' in kwargs:
            post_id = kwargs['pk']
            post = Post.objects.get(pk=post_id)   
            user_can_edit_post = post.author.id == request.user.id     
            context = {
                'post': post,
                'tags': post.tags.all(),
                'can_edit_post': user_can_edit_post
            }
            return render(request, template_name=self.post_details_template, context=context)    
        
        posts = Post.objects.all()
        context = {
            'posts': posts
        }
        return render(request, template_name=self.all_posts__template, context=context)
