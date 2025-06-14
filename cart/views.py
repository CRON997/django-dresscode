from django.shortcuts import render, redirect, get_object_or_404
from main.models import Product
from .cart import Cart
from django.views.decorators.http import require_POST


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item
