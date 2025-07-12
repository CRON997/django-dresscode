from decimal import Decimal

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views import View

from cart.cart import Cart
from orders.forms import OrderForm
from orders.models import Order, OrderItem


# @method_decorator(login_required(login_url='users/login'), name='dispatch')
# class CheckOutView(View):
#     def get(self, request):
#         cart = Cart.objects.filter(user=request.user)
#
#         if cart.get_total_items == 0:
#             raise 'Cart is empty'
#
#         total_price = cart.get_total_price
#
#         form = (OrderForm
#                 (user=request.user))
#         context = {
#             'form': form,
#             'cart': cart,
#             'cart_items': cart.items.selected_related['product', 'product_size__size'],
#             'total_price': total_price
#         }
#
#         return render(request, 'orders/checkout.html', context=context)
#
#     def post(self, request):
#         cart = Cart.objects.filter(user=request.user)
#         payment_provider = request.POST.get('payment_provider')
#         if cart.get_total_items == 0:
#             raise 'Cart is empty'
def checkout_view(request):
    return render(request, 'orders/checkout.html')
