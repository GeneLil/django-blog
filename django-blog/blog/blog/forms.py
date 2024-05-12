from django.forms import ModelForm, TextInput, Textarea, CheckboxSelectMultiple
from .views import Post, Tag


class NewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'image', 'tags']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': '', 'id': 'title'}),
            'body': Textarea(attrs={'class': 'form-control', 'placeholder': '', 'id': 'body'}),
            'tags': CheckboxSelectMultiple(attrs={'class': 'form-check-input', 'value': ''})
        }
        

class NewTagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['title']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': '', 'id': 'title'}),         
        }