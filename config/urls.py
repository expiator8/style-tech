from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", include("core.urls", namespace="core")),
    path("naver_products/", include("naver_products.urls", namespace="naver_products")),
    path(
        "instagram_products/",
        include("instagram_products.urls", namespace="instagram_products"),
    ),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
