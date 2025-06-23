from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('add/<int:product_id>/<slug:product_slug>/', views.add_comment, name='add_comment'),
]
