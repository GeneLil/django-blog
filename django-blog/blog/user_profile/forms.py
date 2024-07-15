from datetime import date
from django import forms
from .models import UserProfile


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
        