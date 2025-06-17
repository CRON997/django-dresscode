from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from django.utils.html import strip_tags
from django.core.validators import RegexValidator

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=66,
                             widget=forms.EmailInput(attrs={'class': 'input-box', 'placeholder': 'Enter your email'}))
    first_name = forms.CharField(required=True, max_length=50,
                                 widget=forms.TextInput(
                                     attrs={'class': 'input-box', 'placeholder': 'Enter first name'}))
    last_name = forms.CharField(required=True, max_length=50,
                                widget=forms.TextInput(attrs={'class': 'input-box', 'placeholder': 'Enter last name'}))
    password1 = forms.CharField(required=True,
                                widget=forms.TextInput(
                                    attrs={'class': 'input-box', 'placeholder': 'Enter your password'}))
    password2 = forms.CharField(required=True,
                                widget=forms.TextInput(
                                    attrs={'class': 'input-box', 'placeholder': 'Confirm your password'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = None
        if commit:
            user.save()
        return user


class CustomUserLoginForm(AuthenticationForm):
    email = forms.CharField(label='Email', widget=forms.EmailInput(
        attrs={'autofocus': True, 'class': 'input-box', 'placeholder': 'Your email'}))

    password = forms.CharField(label='Password', widget=forms.TextInput(
        attrs={'autofocus': True, 'class': 'input-box', 'placeholder': 'Your password'}))
