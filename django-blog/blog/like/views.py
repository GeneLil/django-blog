"""MOdule for Like view"""
from django.views.generic import TemplateView
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from .models import Like
from post.models import Post


class LikeView(TemplateView):
    """View for Like queries processing"""
    template_name = ''

    def get(self, request: HttpRequest):
        """Get query for checking if post is liked by user"""
        if request.user.is_authenticated:
            user = request.user
            post_id = request.GET.get('post_id')
            all_likes = Like.objects.all()
            likes_for_post = all_likes.filter(post_id=post_id)
            existing_like = Like.objects.filter(post_id=post_id).filter(user_id=user.pk)
            return JsonResponse({ 'post_id': post_id, 
                                 'total_likes': len(likes_for_post), 
                                 'is_liked': len(existing_like) > 0 })
        return redirect('home')

    def post(self, request: HttpRequest):
        """Post query for Like creation"""
        if request.user.is_authenticated:
            user = request.user
            post_id = request.POST.get('post_id')
            existing_like = Like.objects.filter(post_id=post_id).filter(user_id=user.pk)

            if len(existing_like) > 0:
                existing_like.delete()
                return JsonResponse({ 'post_id': post_id, 'is_liked': False })

            post = Post.objects.get(pk=post_id)
            like = Like(user=user, post=post)
            like.save()
            return JsonResponse({ 'post_id': post_id, 'is_liked': True })
        return redirect('home')
            