from django.shortcuts import render, redirect, get_object_or_404

from main.models import Product
from .cart import Cart
from django.views.decorators.http import require_POST

from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    current_page = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)
    if request.htmx:
        return render(request, 'cart/count.html', )
    return redirect(current_page)


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'override': True})
    return render(request, 'cart/cart_detail.html', {'cart': cart})
