from django.conf import settings
from django.shortcuts import render, redirect

from main.models import ClothingSize
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
import stripe

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


def order_create(request):
    cart = Cart(request)
    total_price = sum(item['total_price'] for item in cart)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = Order(
                user=request.user,
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                email=form.cleaned_data.get('email'),
                address1=form.cleaned_data.get('address1'),
                phone=form.cleaned_data.get('phone'),
                postal_code=form.cleaned_data.get('postal_code'),
            )
            order.save()

        for item in cart:
            size_instance = item.get('size_object')
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                size=size_instance,
                quantity=item['quantity'],
                price=item['total_price']
            )
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': item['product'].name,
                            },
                            'unit_amount': int(item['total_price'] * 100),
                        },
                        'quantity': item['quantity'],
                    } for item in cart
                ],
                mode='payment',
                success_url='http://localhost:8000/orders/completed',
                cancel_url='http://localhost:8000/orders/create'
            )

            return redirect(session.url, code=303)
        except Exception as e:
            return render(request, 'orders/create.html', {
                'form': form,
                'cart': cart,
                'error': str(e)
            })
    form = OrderCreateForm(initial={
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'address1': request.user.address1,
        'phone': request.user.phone,
        'postal_code': request.user.postal_code
    })

    return render(request, 'orders/create.html', {
        'form': form,
        'cart': cart,
        'total_price': total_price,
    })


def order_success(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'orders/order_success.html')
