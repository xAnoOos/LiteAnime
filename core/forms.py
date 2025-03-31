from django import forms
from django.contrib.auth.models import User
from .models import Thread, Comment, Profile
from django.core.exceptions import ValidationError
import re



class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if len(password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long.")
        if not re.search(r'\d', password):
            raise forms.ValidationError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError("Password must contain at least one special character.")
        
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # تأكد من تشفير الباسورد
        if commit:
            user.save()
        return user

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
