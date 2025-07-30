from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input', "placeholder": 'First name',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input', "placeholder": 'Last name',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-input', "placeholder": 'Email',
    }))
    address1 = forms.CharField(required=False, max_length=250, widget=forms.TextInput(attrs={
        'class': 'form-input', "placeholder": 'Address 1',
    }))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-input', "placeholder": 'City',
    }))
    phone = forms.CharField(max_length=10, widget=forms.TextInput(attrs={
        'class': 'form-input', "placeholder": 'Phone',
    }))
    postal_code = forms.CharField(max_length=10, widget=forms.TextInput(attrs={
        'class': 'form-input', "placeholder": 'Postal code',
    }))

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address1', 'city', 'phone']
