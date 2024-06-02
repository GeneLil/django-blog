"""Module for single post view"""
from datetime import datetime
from django.http import HttpRequest
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .models import Post
from .forms import NewPostForm


def make_short_description(body: str):
    """Make short description from body"""
    return body.rsplit('.', 1)[0] + '.'

def create_post(request: HttpRequest, form: NewPostForm):
    """Method for creating post"""
    title = form.cleaned_data.get('title')
    body = form.cleaned_data.get('body')
    short_description = ''
    if body is not None:
        short_description = make_short_description(body[:400])
    image = form.cleaned_data.get('image')
    author = request.user
    tags = form.cleaned_data.get('tags')
    post = Post(title=title, body=body, short_description=short_description,
                image=image,
                author=author)
    post.save()
    post.tags.set(tags)

def update_post(form: NewPostForm, primary_key: str):
    """Method for updating post"""
    post = Post.objects.get(pk=primary_key)
    body = form.cleaned_data.get('body')
    post.title = form.cleaned_data.get('title')
    post.body = body
    post.short_description = make_short_description(body[:400])
    post.image = form.cleaned_data.get('image')
    tags = form.cleaned_data.get('tags')
    post.modified_at = datetime.now()
    post.save()
    post.tags.set(tags)


class SinglePostView(TemplateView):
    """Class for single post view"""
    new_post_template = 'authorized/new-post.html'
    edit_post_template = 'authorized/edit-post.html'

    def get(self, request: HttpRequest, **kwargs):
        """Get method for single post"""
        context = {}
        if 'pk' in kwargs:
            post_id = kwargs['pk']
            post = Post.objects.get(pk=post_id)
            context = {
                'form': NewPostForm(instance=post),
                'isEditing': True,                
            }
            return render(request, template_name=self.edit_post_template, context=context)

        context = {
            'form': NewPostForm()
        }
        return render(request, template_name=self.new_post_template, context=context)

    def post(self, request: HttpRequest, **kwargs):
        """Post method for single post"""
        if request.user.is_authenticated:
            form = NewPostForm(request.POST, request.FILES)
            if 'pk' in kwargs:                
                if form.is_valid():                                     
                    primary_key = kwargs['pk']
                    update_post(form, primary_key=primary_key)
                    return redirect('posts')
                else:
                    return render(request, template_name=self.edit_post_template, context={'form': form})
            else:                
                if form.is_valid():                                     
                    create_post(request, form)
                    return redirect('posts')
                else:
                    return render(request, template_name=self.edit_post_template, context={'form': form})
        return redirect('')
