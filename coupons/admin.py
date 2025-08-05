from django.contrib import admin

from users.views import register
from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to', 'discount', 'active']
    filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']
