from django import forms
from .models import Tag


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
