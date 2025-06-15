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

    status_discount = models.BooleanField(default=False)
    percent = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True,
                                  help_text='Процент скидки от 1-100%')

    def get_discount_price(self):
        if self.status_discount and self.percent > 0:
            discount = (self.price * Decimal(self.percent) / Decimal(100))
            return self.price - discount
        return 0

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('main:product_detail', args=[self.id, self.slug])
