from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path(_('cart/'), include('cart.urls', namespace='cart')),
    path('', include('main.urls', namespace='main')),
    path('user/', include('users.urls', namespace='users')),
    path('comments/', include('comments.urls', namespace='comments')),
    # path('orders/', include('orders.urls', namespace='orders')),
    path('accounts/', include('allauth.urls')),
    path('rosetta/', include('rosetta.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
