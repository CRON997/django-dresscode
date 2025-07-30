from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'first_name', "last_name")
    search_fields = ('email', 'first_name', "last_name")
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]
