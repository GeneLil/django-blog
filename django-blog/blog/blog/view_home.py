"""File for home view"""
from django.http import HttpRequest
from django.shortcuts import redirect


def home_view(request: HttpRequest):
    """View to resolve home url"""
    user = request.user
    if user.is_authenticated:
        return redirect('posts')
    return redirect('login')
    