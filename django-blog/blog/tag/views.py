"""Module for tags view"""
import json
from django.views.generic import TemplateView
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from .models import Tag
from .forms import NewTagForm
from django.http import JsonResponse


def get_all_tags(request: HttpRequest):
    if request.user.is_authenticated:
        tags = Tag.objects.all()
        tags_response = []
        for tag in tags:
            tags_response.append({'id': tag.pk, 'title': tag.title})
        return JsonResponse({'tags': tags_response})
    return redirect('home')


class TagsView(TemplateView):
    """Class for tags view"""
    template_name = 'authorized/tags.html'

    def get(self, request: HttpRequest):
        """Get method for tags view"""
        if request.user.is_authenticated:            
            context = {
                'form': NewTagForm()
            }
            return render(request, template_name=self.template_name, context=context)
        return redirect('home')
    
    def post(self, request: HttpRequest):
        """Post method for new tag view"""        
        response = {}
        if request.user.is_authenticated:
            try:
                json_request = json.loads(request.body)
                title = json_request['tagTitle']
                tag = Tag.objects.create(title=title)
                tag.save()
                response = {'status': 1, 'message': 'Tag succesfully created'} 
            except:
                response = {'status': 0, 'message': 'Error during tag creation'} 
            return JsonResponse(response)
        return redirect('home')
    