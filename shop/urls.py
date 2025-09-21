from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.utils.translation import gettext_lazy as _
from debug_toolbar.toolbar import debug_toolbar_urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

api_patterns = [
    path("api/", include("api.urls")),
]

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version="v1",
        description="Документация для моего API",
        terms_of_service="https://example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Основные маршруты (с i18n)
main_patterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path(_("cart/"), include("apps.cart.urls", namespace="cart")),
    path("", include("apps.main.urls", namespace="main")),
    path("user/", include("apps.users.urls", namespace="users")),
    path("comments/", include("apps.comments.urls", namespace="comments")),
    path("orders/", include("apps.orders.urls", namespace="orders")),
    path("coupons/", include("apps.coupons.urls", namespace="coupons")),
    path("accounts/", include("allauth.urls")),
    path("rosetta/", include("rosetta.urls")),
)

# Swagger — без i18n
swagger_patterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]

# Объединяем
urlpatterns = api_patterns + main_patterns + swagger_patterns

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
