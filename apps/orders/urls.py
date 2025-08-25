from django.urls import path
from .views import order_create, order_success, order_detail, admin_order_pdf
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', order_create, name='order_create'),
    path('completed/', order_success, name='order_success'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
    path('admin/order/<uuid:order_number/pdf', admin_order_pdf, name='admin_order_pdf'),
]
