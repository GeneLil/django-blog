"""Module for new comment view"""
from django.views.generic import TemplateView
from django.http import HttpRequest
from django.shortcuts import redirect
from ..forms import NewCommentForm
from ..models import Comment, Post


class NewCommentView(TemplateView):
    """View class for comment"""

    def post(self, request: HttpRequest, **kwargs):
        """Post method to create comment"""
        if request.user.is_authenticated:
            if 'post_id' in kwargs:
                post_id = kwargs['post_id']
                form = NewCommentForm(request.POST)
                if form.is_valid():
                    author = request.user
                    post = Post.objects.get(pk=post_id)
                    body = form.cleaned_data.get('body')
                    comment = Comment(author=author, post=post, body=body)
                    comment.save()
                    return redirect(f'/posts/{post_id}')
        return redirect('')
    