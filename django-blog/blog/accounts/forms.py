from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")
        
        
class CustomUserLoginForm(AuthenticationForm):    
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', 'id': 'login-name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholer': '', 'id': 'login-password'}))
    
    class Meta:
        model = CustomUser
        fields = ("username", "password")
            