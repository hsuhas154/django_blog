from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Profile 

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User 
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User 
        fields = ['username', 'email'] 

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile 
        fields = ['image']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        UserModel = get_user_model()
        if username and password:
            try:
                if '@' in username:
                    user_temp = UserModel.objects.get(email=username)
                else:
                    user_temp = UserModel.objects.get(username=username)
                self.user_cache = user_temp
            except UserModel.DoesNotExist:
                raise forms.ValidationError("Invalid username or email")
            if not self.user_cache.check_password(password):
                raise forms.ValidationError("Invalid password")
        return self.cleaned_data
