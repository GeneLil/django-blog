from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomUserLoginForm


# Create your views here.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    
    
class CustomLoginView(LoginView):
    form_class = CustomUserLoginForm
    success_url = reverse_lazy("posts")
    template_name = "registration/login.html"
    