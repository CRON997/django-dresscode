from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.html import strip_tags

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


class CustomUserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50,
                                 widget=forms.TextInput(
                                     attrs={'class': ""}))
    last_name = forms.CharField(max_length=50,
                                widget=forms.TextInput(
                                    attrs={'class': ""}))
    email = forms.EmailField(max_length=66,
                             widget=forms.EmailInput(
                                 attrs={'class': ""}))
    address1 = forms.CharField(max_length=66,
                               widget=forms.TextInput(
                                   attrs={'class': ''}))
    address2 = forms.CharField(max_length=66,
                               widget=forms.TextInput(
                                   attrs={'class': ''}))
    city = forms.CharField(max_length=66,
                           widget=forms.TextInput(
                               attrs={'class': ''}))
    phone = forms.CharField(max_length=66,
                            widget=forms.TextInput(
                                attrs={'class': ''}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'address1', 'address2', 'city', 'phone')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Use')

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('email'):
            cleaned_data['email'] = self.instance.email

            for field in ['first_name', 'last_name', 'address1', 'address2', 'city', 'phone']:
                if cleaned_data.get(field):
                    cleaned_data[field] = strip_tags(cleaned_data[field])
                return cleaned_data
