from random import choices

from django import forms
from .models import Order

CITY_CHOICE = [
    ('kyiv', 'Kyiv'),
    ('kharkiv', 'Kharkiv'),
    ('lviv', 'Lviv')
]

COUNTRY_PHONE_CODE_CHOICE = [
    ('+380', 'Ukraine')
]

COUNTRY_CHOICE = [
    ('ukraine', 'Ukraine'),
    ('poland', 'Poland'),
]


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
    city = forms.ChoiceField(choices=CITY_CHOICE,
                             widget=forms.Select(attrs={'class': 'form-input', "placeholder": 'City'}))
    phone = forms.ChoiceField(choices=COUNTRY_PHONE_CODE_CHOICE, widget=forms.Select(attrs={
        'class': 'form-input', "placeholder": 'Phone',
    }))
    postal_code = forms.CharField(max_length=10, widget=forms.TextInput(attrs={
        'class': 'form-input', "placeholder": 'Postal code',
    }))

    # country = forms.ChoiceField(choices=COUNTRY_CHOICE,
    #                             widget=forms.Select(attrs={'class': 'form-input', "placeholder": 'Country'}))

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address1', 'city', 'phone', 'postal_code']
