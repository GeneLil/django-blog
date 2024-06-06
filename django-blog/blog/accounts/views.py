from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomUserLoginForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpRequest


# Create your views here.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    
    
class CustomLoginView(LoginView):    
    form_class = CustomUserLoginForm
    success_url = reverse_lazy("posts")
    template_name = "registration/login.html"
    
    def get(self, request: HttpRequest):
        form = CustomUserLoginForm()
        context = {
            'form': form,
            'login_error': ''
        }
        return render(request, template_name=self.template_name, context=context)
    
    def post(self, request: HttpRequest):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('posts')
        else:
            form = CustomUserLoginForm(request.POST)
            context = {
                'form': form,
                'login_error': 'Invalid username or password'
            }
            return render(request, template_name=self.template_name, context=context)
                