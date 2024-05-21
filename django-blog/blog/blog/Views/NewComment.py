from django.views.generic import TemplateView
from django.http import HttpRequest
from ..forms import NewCommentForm
from ..Models import Comment, Post
from django.shortcuts import redirect


class NewCommentView(TemplateView):
    
    def post(self, request: HttpRequest, *args, **kwargs):
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
            