from django import forms


class CartAddProduct(forms.Form):
    quantity = forms.ImageField(min_value=1, max_value=20, initial=1, widget=forms.NumberInput(attrs={'class': ''}))
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
