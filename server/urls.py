from django.conf import settings
from django.contrib import admin
from drf_yasg import openapi, views
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.permissions import AllowAny

schema_view = views.get_schema_view(
    public=True,
    permission_classes=[AllowAny],
    info=openapi.Info(
        title="Superb Eats",
        default_version="v1",
        description="Superb Eats",
        license=openapi.License(name="BSD License"),
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(
            name="Muhammad Muhammad Inuwa",
            url="https://github.com/mminuwaali",
            email="mminuwaali.coding@gmail.com",
        ),
    ),
)

api, url = ['account'], ['account']

urlpatterns = [
    path("admin/", admin.site.urls),
    path("stripe/", include("drf_stripe.urls")),
    *(path("", include(f"{i}.urls")) for i in url),
    *(path("api/", include(f"{i}.api")) for i in api),
    path("", schema_view.with_ui(), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc"), name="schema-redoc"),
]

if settings.DEBUG:
    urlpatterns += [
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
        *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    ]
