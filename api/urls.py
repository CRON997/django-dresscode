from django.urls import path

from api.views.main import CategoryApiView, ProductApiView, CategoryDetailApiView, ProductDetailApiView

urlpatterns = [
    path('categories/', CategoryApiView.as_view(), name='categories-list'),
    path('products/', ProductApiView.as_view(), name='products-list'),
    path('category/<int:pk>/', CategoryDetailApiView.as_view(), name='category-by-id'),
    path('delete/category/<int:pk>/', CategoryDetailApiView.as_view(), name='delete-category-by-id'),
    path('product/<int:pk>/', ProductDetailApiView.as_view(), name='product-by-id'),
]
