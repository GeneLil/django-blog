from django import forms
from .Models import Post, Tag, Comment, UserProfile
from datetime import date


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'image', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', 'id': 'title'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '', 'id': 'body'}),
            'tags': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input', 'value': ''})
        }
        

class NewTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', 'id': 'title'}),         
        }
        

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '', 'id': 'body'}),
        }
    
        
class DateInput(forms.DateInput):
    input_type = 'date'
            
        
class UserProfileForm(forms.ModelForm):
    
    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data.get('dob')
        if dob > date.today():
            self.add_error('dob', 'Date of birth cannot be in future')
    
    class Meta:
        model = UserProfile
        fields = ['avatar', 'dob', 'email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '', 'id': 'email'}),
            'dob': DateInput(attrs={'class': 'form-control', 'placeholder': '', 'id': 'dob'})
        }