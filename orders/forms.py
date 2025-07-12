from django import forms
from django.utils.html import strip_tags

from .models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-group', "placeholder": 'First name',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-group', "placeholder": 'Last name',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-group', "placeholder": 'First name',
    }))
    address1 = forms.CharField(required=False, max_length=250, widget=forms.TextInput(attrs={
        'class': 'form-group', "placeholder": 'Address 1',
    }))
    address2 = forms.CharField(required=False, max_length=250, widget=forms.TextInput(attrs={
        'class': 'form-group', "placeholder": 'Address 2',
    }))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-group', "placeholder": 'City',
    }))
    phone = forms.CharField(max_length=10, widget=forms.TextInput(attrs={
        'class': 'form-group', "placeholder": 'Phone',
    }))

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.first_name
            self.fields['email'].initial = user.email

    def clean(self):
        cleaned_data = super().clean()
        for field in ['first_name', 'last_name', 'email',
                      ' address1', ' address2', 'city', 'phone']:
            if cleaned_data.get(field):
                cleaned_data[field] = strip_tags(cleaned_data[field])
        return cleaned_data
