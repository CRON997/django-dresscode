from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib import messages

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

    if not cart.cart:
        messages.error(request, 'Your cart is empty!')
        return redirect('cart:cart_detail')

    total_price = cart.get_total_price_after_discount()

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            try:
                order = Order(
                    user=request.user,
                    first_name=form.cleaned_data.get('first_name'),
                    last_name=form.cleaned_data.get('last_name'),
                    email=form.cleaned_data.get('email'),
                    address1=form.cleaned_data.get('address1'),
                    phone=form.cleaned_data.get('phone'),
                    postal_code=form.cleaned_data.get('postal_code'),
                    total_price=total_price,
                    coupon=cart.coupon,
                    city=form.cleaned_data.get('city'),
                )
                order.save()

                for item in cart:
                    size_instance = None
                    if 'size' in item and item['size']:
                        size_instance = item['size']
                    elif 'size_id' in item and item['size_id']:
                        size_instance = Size.objects.get(id=item['size_id'])
                    elif 'size_name' in item and item['size_name']:
                        size_instance = Size.objects.get(name=item['size_name'])

                    if not size_instance:
                        messages.error(request, f'Size not found for product {item["product"].name}')
                        return redirect('cart:cart_detail')

                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        size=size_instance,
                        quantity=item['quantity'],
                        price=item['total_price']
                    )

                line_items = []
                for item in cart:
                    line_items.append({
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': f"{item['product'].name} - Size: {getattr(item.get('size'), 'name', item.get('size_name', 'N/A'))}",
                            },
                            'unit_amount': int(float(item['price']) * 100),  # Convert to cents
                        },
                        'quantity': item['quantity'],
                    })

                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url=request.build_absolute_uri('/orders/completed/'),
                    cancel_url=request.build_absolute_uri('/orders/create/'),
                    metadata={'order_id': order.id}  # Add order ID to metadata
                )

                payment_completed(order.id)  # Use .delay() if it's a Celery task

                return redirect(session.url, code=303)

            except Size.DoesNotExist:
                messages.error(request, 'One or more sizes in your cart are invalid.')
                return redirect('cart:cart_detail')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
                form = OrderCreateForm(request.POST)  # Keep form data
                coupon_form = CouponApplyForm()
                return render(request, 'orders/create.html', {
                    'form': form,
                    'cart': cart,
                    'total_price': total_price,
                    'coupon_form': coupon_form,
                    'error': str(e)
                })
        else:
            messages.error(request, 'Please correct the errors below.')

    # GET request or form validation failed
    form = OrderCreateForm(initial={
        'first_name': getattr(request.user, 'first_name', ''),
        'last_name': getattr(request.user, 'last_name', ''),
        'email': getattr(request.user, 'email', ''),
        'address1': getattr(request.user, 'address1', ''),
        'city': getattr(request.user, 'city', ''),
        'phone': getattr(request.user, 'phone', ''),
        'postal_code': getattr(request.user, 'postal_code', '')
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
    response = HttpResponse(content_type='application/pdf')  # Fixed typo: was 'applications/pdf'
    response['Content-Disposition'] = f'attachment; filename=order_{order.id}.pdf'  # Fixed format
    weasyprint.HTML(string=html).write_pdf(response)
    return response
