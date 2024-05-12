from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Post, Tag
from .forms import NewPostForm, NewTagForm
from django.shortcuts import redirect


class PostsView(TemplateView):
    template_name = 'authorized/posts.html'
    
    def get(self, request: HttpRequest):
        print("GET QUERY")
        context = {}
        posts = Post.objects.all()
        print("POSTS:", posts)
        context = {
            'posts': posts
        }
        return render(request, template_name=self.template_name, context=context)
    
    def post(self, request: HttpRequest):
        pass


class NewPostView(TemplateView):
    template_name = 'authorized/new-post.html'
    
    @staticmethod
    def make_short_description(body: str):
        return body.rsplit('.', 1)[0] + '.'
        
    
    def get(self, request: HttpRequest):        
        context = {
            'form': NewPostForm()
        }
        return render(request, template_name=self.template_name, context=context)
    
    def post(self, request: HttpRequest):
        if request.user.is_authenticated:
            form = NewPostForm(request.POST, request.FILES)            
            
            if form.is_valid():
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
                print("SUCCESS")
                return redirect('posts')
        # return render(request, template_name='authorized/posts/new.html')           


class TagsView(TemplateView):
    template_name = 'authorized/tags.html'
    
    def get(self, request: HttpRequest):
        context = {}
        tags = Tag.objects.all()
        context = {
            'tags': tags
        }
        return render(request, template_name=self.template_name, context=context)


class NewTagView(TemplateView):
    template_name = 'authorized/new-tag.html'
    
    def get(self, request: HttpRequest):
        context = {
            'form': NewTagForm()
        }
        return render(request, template_name=self.template_name, context=context)
    
    def post(self, request: HttpRequest):
        form = NewTagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tags')      
