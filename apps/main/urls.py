from django.urls import path

from shop.urls import router
from . import views
from .views import CatalogView, Search, CategoryApiView, ProductApiView

app_name = 'main'

router.register(r'products/cats', CategoryApiView)
router.register(r'products', ProductApiView)

urlpatterns = [
    path('about-store/', views.about, name='about'),
    path('', CatalogView.as_view(), name='product_list'),
    path('search/', Search.as_view(), name='search'),
    path('<slug:category_slug>/', CatalogView.as_view(), name='product_list_by_category'),
    path('<int:id>/<slug:slug>', views.product_detail, name='product_detail'),

]
