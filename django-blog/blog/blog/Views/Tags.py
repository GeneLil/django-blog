"""Module for tags view"""
from django.views.generic import TemplateView
from django.http import HttpRequest
from django.shortcuts import render
from ..models import Tag


class TagsView(TemplateView):
    """Class for tags view"""
    template_name = 'authorized/tags.html'

    def get(self, request: HttpRequest):
        """Get method for tags view"""
        context = {}
        tags = Tag.objects.all()
        context = {
            'tags': tags
        }
        return render(request, template_name=self.template_name, context=context)
    