from django.views.generic import TemplateView
from django.http import HttpRequest
from ..Models import Like, Post
from django.shortcuts import redirect


class LikeView(TemplateView):
    
    def post(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:            
            user_id = request.user
            post_id = kwargs['post_id']
            existing_like = Like.objects.filter(post_id=post_id).filter(user_id=user_id)
        
            if len(existing_like) > 0:
                existing_like.delete()
                return redirect(f'/posts/{post_id}')
            
            post = Post.objects.get(pk=post_id)
            like = Like(user=user_id, post=post)
            like.save()
            return redirect(f'/posts/{post_id}')
            