"""Module for new comment view"""
import json
from django.views.generic import TemplateView
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from .forms import NewCommentForm
from .models import Comment, Post, UserProfile


class CommentView(TemplateView):
    """View class for comment"""
    template_name = ''
    
    def get(self, request: HttpRequest):
        """Get method to get all comments"""
        if request.user.is_authenticated:            
            post_id = request.GET.get('post_id')
            comments = Comment.objects.filter(post_id=post_id).order_by('-created_at')
            serialized_comments = []
            for comment in comments:
                user_profile = UserProfile.objects.get(user_id=comment.author.pk)
                serialized_comments.append({
                    'id': comment.pk,
                    'username': user_profile.user.username,
                    'avatar_url': user_profile.avatar.url,
                    'created_at': comment.created_at,
                    'body': comment.body,
                })
            return JsonResponse({ 'comments': serialized_comments })
        return redirect('home')
                                            

    def post(self, request: HttpRequest):
        """Post method to create comment"""
        if request.user.is_authenticated:
            response = {}
            try:
                body = request.POST.get('body')
                post_id = request.POST.get('post_id')
                author = request.user
                post = Post.objects.get(pk=post_id)                
                comment = Comment(author=author, post=post, body=body)
                comment.save()
                user_profile = UserProfile.objects.get(user_id=author.pk)
                response = {
                    'id': comment.pk,
                    'username': user_profile.user.username,
                    'avatar_url': user_profile.avatar.url,
                    'created_at': comment.created_at,
                    'body': comment.body,
                }
            except:
                response = {'status': 0, 'message': 'Error: comment not added'} 
            return JsonResponse(response)
        return redirect('home')
    