from django import forms
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First name')
    last_name = forms.CharField(max_length=30, label='Last name')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'image', 'about_me', 
            'phone','address', 'city',
            'country',
            'facebook',
            'instagram',
            'twitter']

class ProfileArtisanUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'skill', 'proficiency', 'experience',
            'efficiency', 'time_conscious','standout']

# class ChatForm(forms.ModelForm):
#     class Meta:
#         model = Chat
#         fields = ['sender', 'receiver', 'message']
