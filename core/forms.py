from django import forms
from django.contrib.auth.models import User
from .models import Thread, Comment, Profile
from django.core.exceptions import ValidationError
import re



class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        help_text="Password must be at least 6 characters and include a number and a special character."
    )
    password_confirm = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password', '').strip()

        if len(password) < 6:
            raise ValidationError("Password must be at least 6 characters long.")

        if not re.search(r'\d', password):
            raise ValidationError("Password must include at least one number.")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("Password must include at least one special character.")

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password', '').strip()
        password_confirm = cleaned_data.get('password_confirm', '').strip()
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match")
        return cleaned_data

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'content', 'image']  
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter thread title'}),
            'content': forms.Textarea(attrs={'placeholder': 'Share your thoughts...'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
