from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate

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
                                widget=forms.PasswordInput(
                                    attrs={'class': 'input-box', 'placeholder': 'Enter your password'}))
    password2 = forms.CharField(required=True,
                                widget=forms.PasswordInput(
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
    username = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'autofocus': True, 'class': '', 'placeholder': 'Enter your email'}))

    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'autofocus': True, 'class': '', 'placeholder': 'Enter your password'}))

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('Invalid email or password')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('This account is inactive')
        return self.cleaned_data
