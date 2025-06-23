from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at', 'text']
