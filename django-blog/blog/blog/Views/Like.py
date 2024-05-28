"""MOdule for Like view"""
from django.views.generic import TemplateView
from django.http import HttpRequest
from django.shortcuts import redirect
from ..models import Like, Post


class LikeView(TemplateView):
    """View for Like queries processing"""
    template_name = ''

    def post(self, request: HttpRequest, **kwargs):
        """Post query for Like creation"""
        if request.user.is_authenticated:
            user = request.user
            post_id = kwargs['post_id']
            existing_like = Like.objects.filter(post_id=post_id).filter(user_id=user.pk)

            if len(existing_like) > 0:
                existing_like.delete()
                return redirect(f'/posts/{post_id}')

            post = Post.objects.get(pk=post_id)
            like = Like(user=user, post=post)
            like.save()
            return redirect(f'/posts/{post_id}')
        return redirect('')
            