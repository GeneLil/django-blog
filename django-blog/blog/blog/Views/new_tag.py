"""Module for new tag view"""
from django.http import HttpRequest
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from ..forms import NewTagForm


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
        form = NewTagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tags')
        