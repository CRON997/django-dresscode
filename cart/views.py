from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from main.models import Product, ClothingSize, ShoesSize

from .cart import Cart
from .forms import CartAddProductForm

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    current_page = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=product_id)

    # Проверяем, нужен ли размер для этого товара
    size_required = product.clothing_sizes.exists() or product.shoes_sizes.exists()
    size_id = request.POST.get('size_id')

    size = None
    if size_required:
        if not size_id:
            messages.error(request, 'Пожалуйста, выберите размер.')
            if request.htmx:
                return JsonResponse({'error': 'Размер не выбран'}, status=400)
            return redirect(current_page)

        # Определяем модель размера
        size_model = ClothingSize if product.clothing_sizes.exists() else ShoesSize
        size = get_object_or_404(size_model, id=size_id)

    cart.add(product, size)
    messages.success(request, 'Товар добавлен в корзину!')

    if request.htmx:
        return render(request, 'cart/partial/count.html')
    return redirect(current_page)


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    size_id = request.POST.get('size_id')

    size = None
    if size_id:
        # Определяем модель размера
        size_model = ClothingSize if product.clothing_sizes.exists() else ShoesSize
        size = get_object_or_404(size_model, id=size_id)

    cart.remove(product, size)
    return redirect('cart:cart_detail')


@require_POST
def cart_remove_one_quan(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    size_id = request.POST.get('size_id')

    size = None
    if size_id:
        size_model = ClothingSize if product.clothing_sizes.exists() else ShoesSize
        size = get_object_or_404(size_model, id=size_id)

    # Уменьшаем количество на 1
    product_id_str = str(product.id)
    cart_key = f"{product_id_str}_{size.id}" if size else product_id_str

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
