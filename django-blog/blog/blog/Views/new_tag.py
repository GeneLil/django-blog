"""Module for new tag view"""
import json
from django.http import HttpRequest, JsonResponse
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from ..forms import NewTagForm
from ..models import Tag


class NewTagView(TemplateView):
    """Class for new tag view"""
    template_name = 'authorized/new-tag.html'

    def get(self, request: HttpRequest):
        """Get method for tag view"""
        context = {
            'form': NewTagForm()
        }
        return render(request, template_name=self.template_name, context=context)

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
        return redirect('')
        