from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from apps.coupons.forms import CouponApplyForm
from apps.main.models import Size
from .models import OrderItem, Order
from .forms import OrderCreateForm
from apps.cart.cart import Cart
import stripe
from django.http import HttpResponse
import weasyprint

from .tasks import payment_completed

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


def order_create(request):
    cart = Cart(request)
    total_price = cart.get_total_price_after_discount()

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
                total_price=total_price,
            )
            order.save()
            payment_completed(order.id)

        for item in cart:
            size_instance = Size.objects.get(name=item['size']['name'])
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
                            'unit_amount': int(item['price'] * 100),
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
        'city': request.user.city,
        'phone': request.user.phone,
        'postal_code': request.user.postal_code
    })

    coupon_form = CouponApplyForm()

    return render(request, 'orders/create.html', {
        'form': form,
        'cart': cart,
        'total_price': total_price,
        'coupon_form': coupon_form
    })


def order_success(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'orders/order_success.html')


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/pdf.html', {'order': order})
    response = HttpResponse(content_type='applications/pdf')
    response['Content-Disposition'] = f'filename-order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response)
    return response
