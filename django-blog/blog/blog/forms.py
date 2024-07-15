"""Module for forms"""
from django import forms
from post.models import Post



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
