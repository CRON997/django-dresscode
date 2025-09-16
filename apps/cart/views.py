from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.main.models import Size, Product
from .cart import Cart


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    current_page = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=product_id)

    size_id = request.POST.get('size_id')

    if not size_id or size_id == '':
        messages.error(request, 'Please select a size!')
        return redirect(current_page)

    try:
        size_id = int(size_id)
        size = get_object_or_404(Size, id=size_id)
    except (ValueError, TypeError):
        messages.error(request, 'Invalid size selected!')
        return redirect(current_page)

    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity <= 0:
            quantity = 1
    except (ValueError, TypeError):
        quantity = 1

    cart.add(product, size, quantity)
    messages.success(request, 'Товар добавлен в корзину!')

    return redirect(current_page)


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    size_id = request.POST.get('size_id')

    # Validate size_id
    if not size_id or size_id == '':
        messages.error(request, 'Invalid size!')
        return redirect('cart:cart_detail')

    try:
        size_id = int(size_id)
        size = get_object_or_404(Size, id=size_id)
    except (ValueError, TypeError):
        messages.error(request, 'Invalid size!')
        return redirect('cart:cart_detail')

    cart.remove(product, size)
    return redirect('cart:cart_detail')


@require_POST
def cart_remove_one_quan(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    size_id = request.POST.get('size_id')

    # Validate size_id
    if not size_id or size_id == '':
        messages.error(request, 'Invalid size!')
        return redirect('cart:cart_detail')

    try:
        size_id = int(size_id)
        size = get_object_or_404(Size, id=size_id)
    except (ValueError, TypeError):
        messages.error(request, 'Invalid size!')
        return redirect('cart:cart_detail')

    product_id_str = str(product.id)
    cart_key = f"{product_id_str}_{size.id}"

    if cart_key in cart.cart:
        if cart.cart[cart_key]['quantity'] > 1:
            cart.cart[cart_key]['quantity'] -= 1
            cart.save()
        else:
            cart.remove(product, size)

    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})
