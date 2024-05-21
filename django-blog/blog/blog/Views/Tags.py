from ..Models import Tag
from django.views.generic import TemplateView
from django.http import HttpRequest
from django.shortcuts import render


class TagsView(TemplateView):
    template_name = 'authorized/tags.html'
    
    def get(self, request: HttpRequest):
        context = {}
        tags = Tag.objects.all()
        context = {
            'tags': tags
        }
        return render(request, template_name=self.template_name, context=context)