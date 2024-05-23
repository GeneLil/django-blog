"""Module for user profile view"""
from django.views.generic import TemplateView
from django.http import HttpRequest
from django.shortcuts import render, redirect
from ..forms import UserProfileForm
from ..models import UserProfile


def get_form_data(form: UserProfileForm):
    """Getting form data"""
    email = form.cleaned_data.get('email')
    dob = form.cleaned_data.get('dob')
    avatar = form.cleaned_data.get('avatar')
    return email, dob, avatar

def create_profile(request: HttpRequest, form: UserProfileForm):
    """Create profile method"""
    user = request.user
    username = request.POST.get('username')
    user.username = username
    user.save()
    email, dob, avatar = get_form_data(form)                                
    user_profile = UserProfile(user=user, email=email, dob=dob, avatar=avatar)
    user_profile.save()

def update_profile(request: HttpRequest, form: UserProfileForm):
    """Update profile method"""
    user = request.user
    user_profile = UserProfile.objects.get(user_id=user.pk)
    username = request.POST.get('username')
    user.username = username
    user.save()
    user_profile.user = user
    email, dob, avatar = get_form_data(form)
    user_profile.avatar = avatar
    user_profile.dob = dob
    user_profile.email = email
    user_profile.save()


class UserProfileView(TemplateView):
    """Class for user profile view"""
    template_name = 'authorized/user-profile.html'

    def post(self, request: HttpRequest):
        """Post method for user profile"""
        user = request.user
        form = UserProfileForm(request.POST, request.FILES)
        if user.is_authenticated:
            if form.is_valid():
                try:
                    user_profile = UserProfile.objects.get(user_id=user.pk)
                    if user_profile is not None:
                        update_profile(request, form)
                        return redirect('posts')
                except UserProfile.DoesNotExist:         
                    create_profile(request, form)
                    return redirect('posts')
            else:
                user_profile = UserProfile.objects.get(user_id=user.pk)

                context = {
                    'form': form,
                    'user': user,
                    'avatar_url': user_profile.avatar.url,                    
                }
                return render(request, template_name=self.template_name, context=context)
        return redirect('')

    def get(self, request: HttpRequest):
        """Get method for user profile"""
        context = {}
        user = request.user
        try:
            user_profile = UserProfile.objects.get(user_id=user.pk)
            form = UserProfileForm(instance=user_profile)
            context = {
                'form': form,
                'avatar_url': user_profile.avatar.url,
                'user': user,                
            }
        except UserProfile.DoesNotExist:
            form = UserProfileForm()
            context = {
                'form': form,
                'user': user,                
            }
        return render(request, template_name=self.template_name, context=context)
    