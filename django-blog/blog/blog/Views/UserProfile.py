from django.views.generic import TemplateView
from django.http import HttpRequest
from ..forms import UserProfileForm
from ..Models import UserProfile
from django.shortcuts import render, redirect


class UserProfileView(TemplateView):
    template_name = 'authorized/user-profile.html'
    
    def get_form_data(self, form: UserProfileForm):
        email = form.cleaned_data.get('email')
        dob = form.cleaned_data.get('dob')
        avatar = form.cleaned_data.get('avatar')      
        return email, dob, avatar
    
    def create_profile(self, request: HttpRequest, form: UserProfileForm):                                       
        user = request.user     
        username = request.POST.get('username')        
        user.username = username
        user.save()
        email, dob, avatar = self.get_form_data(form)                                
        user_profile = UserProfile(user=user, email=email, dob=dob, avatar=avatar)
        user_profile.save()
             
    def update_profile(self, request: HttpRequest, form: UserProfileForm):                 
        user = request.user         
        user_profile = UserProfile.objects.get(user_id=user.id)
        username = request.POST.get('username')
        user.username = username
        user.save() 
        user_profile.user = user
        email, dob, avatar = self.get_form_data(form)                                
        user_profile.avatar = avatar
        user_profile.dob = dob
        user_profile.email = email
        user_profile.save()        
    
    def post(self, request: HttpRequest):        
        user = request.user
        form = UserProfileForm(request.POST, request.FILES)
        if user.is_authenticated:
            if form.is_valid():                
                try: 
                    user_profile = UserProfile.objects.get(user_id=user.id)                    
                    if user_profile is not None:
                        self.update_profile(request, form)
                        return redirect('posts')
                except UserProfile.DoesNotExist:                                    
                    self.create_profile(request, form)                                
                    return redirect('posts')
            else:                
                user_profile = UserProfile.objects.get(user_id=user.id)              
                
                context = {
                    'form': form,
                    'user': user,
                    'avatar_url': user_profile.avatar.url,                    
                } 
                return render(request, template_name=self.template_name, context=context)          
                
    
    def get(self, request: HttpRequest):
        context = {}
        user = request.user        
        try:
            user_profile = UserProfile.objects.get(user_id=user.id)                        
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
    