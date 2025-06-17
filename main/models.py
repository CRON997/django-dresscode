from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категорія'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('main:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='product/%Y/%m/%d', blank=True)  # blank значит не обезательное добавление
    description = models.TextField(blank=True)
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
        discount = (self.price / Decimal(100)) * Decimal(self.percent)
        return self.price - discount

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
