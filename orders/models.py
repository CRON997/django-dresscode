from django.conf import settings
from django.db import models

from main.models import ClothingSize, Product, ShoesSize


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending',),
        ('processing', 'Proceessing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled')
    )

    PAYMENT_PROVIDED_CHOICES = (
        ('stripe', 'Stripe'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    address1 = models.CharField(max_length=50, blank=True, null=True)
    address2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_provider = models.CharField(max_length=20, blank=True, choices=PAYMENT_PROVIDED_CHOICES)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order:{self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    size = models.ForeignKey(ClothingSize, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    def get_total_cost(self):
        return self.price * self.quantity
