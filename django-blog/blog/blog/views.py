from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def articles_view(request: HttpRequest):
    """Articles page view"""    
    return render(request, 'authorized/articles.html')
