import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse

from apps.main.models import Product, Size

from apps.coupons.models import Coupon


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending',),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled')
    )

    order_number = models.CharField(max_length=12, unique=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    address1 = models.CharField(max_length=50, blank=True, null=True)
    address2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', null=True)
    postal_code = models.CharField(max_length=10, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    coupon = models.ForeignKey(Coupon, related_name='orders', on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_order_number():
        return f"ORD-{uuid.uuid4().hex[:8].upper()}"

    def __str__(self):
        return f'Order:{self.id}'

    def get_absolute_url(self):
        return reverse('orders:order_detail', args=[self.order_number])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    size = models.ForeignKey(Size, on_delete=models.CASCADE)

    def get_total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return str(self.product.name)

    def get_total_cost(self):
        return self.price * self.quantity
