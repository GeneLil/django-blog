from django import forms
from .models import Comment


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
