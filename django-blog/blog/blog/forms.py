"""Module for forms"""
from datetime import date
from django import forms
from .models import Post, Tag, Comment, UserProfile


class NewPostForm(forms.ModelForm):
    """Class for new post form"""
    class Meta:
        """Meta class for new post form"""
        model = Post
        fields = ['title', 'body', 'image', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': '',
                                            'id': 'title'}),
            'body': forms.Textarea(attrs={'class': 'form-control',
                                          'placeholder': '', 
                                          'id': 'body'}),
            'tags': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input', 
                                                        'value': ''})
        }


class NewTagForm(forms.ModelForm):
    """Class for new tag form"""
    class Meta:
        """Meta class for new tag form"""
        model = Tag
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': '',
                                            'id': 'title'}),         
        }


class NewCommentForm(forms.ModelForm):
    """Class for new comment form"""
    class Meta:
        """Meta class for new comment form"""
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control',
                                          'placeholder': '',
                                          'id': 'body'}),
        }


class DateInput(forms.DateInput):
    """Custom class for date input"""
    input_type = 'date'


class UserProfileForm(forms.ModelForm):
    """Class for user profile form"""

    def clean(self):
        """Overriding clean method for user profile"""
        cleaned_data = super().clean()
        dob = cleaned_data.get('dob')
        if dob is not None and dob > date.today():
            self.add_error('dob', 'Date of birth cannot be in future')

    class Meta:
        """Meta class for user profile form"""
        model = UserProfile
        fields = ['avatar', 'dob', 'email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'placeholder': '',
                                             'id': 'email'}),
            'dob': DateInput(attrs={'class': 'form-control', 
                                    'placeholder': '',
                                    'id': 'dob'})
        }
        