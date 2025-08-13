from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


def order_pdf(obj):
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')


order_pdf.short_description = 'Invoice'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email', 'status', 'created_at', 'updated_at', 'total_price', order_pdf)
    list_filter = ('status', 'first_name', "last_name")
    search_fields = ('email', 'first_name', "last_name")
    readonly_fields = ('created_at', 'updated_at', 'total_price')
    inlines = [OrderItemInline]
