from django.urls import path

from . import views
from .views import CatalogView, Search

app_name = 'main'

urlpatterns = [
    path('about-store/', views.about, name='about'),
    path('', CatalogView.as_view(), name='product_list'),
    path('search/', Search.as_view(), name='search'),
    path('<slug:category_slug>/', CatalogView.as_view(), name='product_list_by_category'),
    path('<int:id>/<slug:slug>', views.product_detail, name='product_detail'),
]
