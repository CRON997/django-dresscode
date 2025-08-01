from django.contrib import admin

from .models import Category, Product, Size, ProductSize


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'available', 'created_at', 'updated', 'original_price',
                    'status_discount', 'percent']
    list_filter = ['available', 'created_at', 'updated', 'category', 'status_discount']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('original_price',)
    inlines = [ProductSizeInline]


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name']
