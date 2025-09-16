from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from debug_toolbar.toolbar import debug_toolbar_urls

api_patterns = [
    path('api/', include('api.urls')),
]

# Основные маршруты С обработкой языков
main_patterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path(_('cart/'), include('apps.cart.urls', namespace='cart')),
    path('', include('apps.main.urls', namespace='main')),
    path('user/', include('apps.users.urls', namespace='users')),
    path('comments/', include('apps.comments.urls', namespace='comments')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
    path('coupons/', include('apps.coupons.urls', namespace='coupons')),
    path('accounts/', include('allauth.urls')),
    path('rosetta/', include('rosetta.urls')),
)

# Объединяем паттерны
urlpatterns = api_patterns + main_patterns

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
