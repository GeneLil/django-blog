from datetime import datetime
from django.http import HttpRequest
from django.views.generic import TemplateView
from ..models import Post
from ..forms import NewPostForm
from django.shortcuts import render, redirect


class SinglePostView(TemplateView):
    new_post_template = 'authorized/new-post.html'
    edit_post_template = 'authorized/edit-post.html'
    
    @staticmethod
    def make_short_description(body: str):
        return body.rsplit('.', 1)[0] + '.'
    
    def create_post(self, request: HttpRequest, form: NewPostForm):
        title = form.cleaned_data.get('title') 
        body = form.cleaned_data.get('body') 
        short_description = self.make_short_description(body[:400])
        image = form.cleaned_data.get('image') 
        author = request.user                
        tags = form.cleaned_data.get('tags')        
        post = Post(title=title, body=body, short_description=short_description,
                    image=image,
                    author=author)
        post.save()
        post.tags.set(tags)
    
    def update_post(self, request: HttpRequest, form: NewPostForm, primary_key: str):              
        post = Post.objects.get(pk=primary_key)  
        body = form.cleaned_data.get('body')      
        post.title = form.cleaned_data.get('title') 
        post.body = body
        post.short_description = self.make_short_description(body[:400])
        post.image = form.cleaned_data.get('image') 
        tags = form.cleaned_data.get('tags')        
        post.modified_at = datetime.now()        
        post.save()
        post.tags.set(tags)
        
        
    def get(self, request: HttpRequest, *args, **kwargs):        
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
    
    def post(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            form = NewPostForm(request.POST, request.FILES)            
            if form.is_valid():                
                if 'pk' in kwargs:
                    primary_key = kwargs['pk']                    
                    self.update_post(request, form, primary_key=primary_key)
                else:                                
                    self.create_post(request, form)
            return redirect('posts')      
    
