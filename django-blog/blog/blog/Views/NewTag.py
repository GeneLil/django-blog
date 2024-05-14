from ..forms import NewTagForm
from django.http import HttpRequest
from django.views.generic import TemplateView
from django.shortcuts import render, redirect


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
        