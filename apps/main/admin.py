from unfold.admin import ModelAdmin
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Product, Size, ProductSize, Brand


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['id', 'name', 'slug']
    list_display_links = ['id', 'name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'available', 'created_at', 'updated', 'original_price',
                    'status_discount', 'percent', 'image', 'product_image']
    list_display_links = ['id', 'name']
    list_filter = ['available', 'created_at', 'updated', 'category', 'status_discount']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('original_price', 'product_image')
    inlines = [ProductSizeInline]
    save_on_top = True

    @admin.display(description='Image of product')
    def product_image(self, product: Product):
        if product.image:
            return mark_safe(f"<img src='{product.image.url}' width=200>")
        return f'No image'


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name']
