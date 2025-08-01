from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(_('name'), max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категорія'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('main:product_list_by_category', args=[self.slug])


class Size(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}'


class ProductSize(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product_sizes')
    size = models.ForeignKey('Size', on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.size.name} ({self.stock} in stock ) for {self.product.name}"


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='product/%Y/%m/%d', blank=True)  # blank значит не обезательное добавление
    description = models.TextField(_('description'), blank=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)  # decimal_places максимальное кол-во чискл после запятой
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  # будет автоматичесски добавляться
    updated = models.DateTimeField(auto_now=True)

    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                         help_text='Исходная цена до скидки (заполняется автоматически при наличии скидки)')
    status_discount = models.BooleanField(default=False)
    percent = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True,
                                  help_text='Процент скидки от 1-100%')

    def get_discount_price(self):
        if self.original_price:
            discount = (self.original_price / Decimal(100)) * Decimal(self.percent)
            return self.original_price - discount
        return self.price

    def save(self, *args, **kwargs):
        if self.status_discount and self.percent:
            if not self.original_price:
                self.original_price = self.price
            self.price = self.get_discount_price()
        else:
            if self.original_price:
                self.price = self.original_price
                self.original_price = None
            self.percent = 0
            self.status_discount = False
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('name', 'status_discount',)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('main:product_detail', args=[self.id, self.slug])
