from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False, help_text='显示名称')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'address')

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='显示名称')
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('first_name', 'email') 