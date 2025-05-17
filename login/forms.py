from django import forms
from django.contrib.auth.models import User
from login.models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    class Meta:
        model = UserProfile
        fields = ['full_name', 'phone_number', 'date_of_birth', 'address', 'profile_picture']
