from django.contrib import admin
from .models import Category, Product, ShoesSize, ClothingSize


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'available', 'created_at', 'updated', 'original_price',
                    'status_discount', 'percent']
    list_filter = ['available', 'created_at', 'updated', 'category', 'status_discount']  # для админки
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('original_price',)


@admin.register(ClothingSize)
class ClothingSizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']


@admin.register(ShoesSize)
class ClothingSizeAdmin(admin.ModelAdmin):
    list_display = ['name', ]
