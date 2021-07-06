"""tfat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from tfat import urls as tfat_urls
from tfat.views import tags_recovered_this_year

tfat_schema_view = get_schema_view(
    openapi.Info(
        title="TFAT API",
        default_version="v1",
        description="API end points for TFAT - Tagged Fish Assessment Tool.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="adam.cottrill@ontario.ca"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("myusers.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("tfat/", include(tfat_urls, namespace="tfat")),
    path("tfat/api/v1/", include("tfat.api.urls", namespace="tfat_api")),
    path("common_api/", include("common.api.urls", namespace="common_api")),
    url(
        r"^tfat/api/swagger(?P<format>\.json|\.yaml)$",
        tfat_schema_view.without_ui(cache_timeout=0),
        name="tfat-schema-json",
    ),
    path(
        "tfat/api/swagger/",
        tfat_schema_view.with_ui("swagger", cache_timeout=0),
        name="tfat-swagger-ui",
    ),
    path(
        "tfat/api/redoc/",
        tfat_schema_view.with_ui("redoc", cache_timeout=0),
        name="tfat-redoc",
    ),
    path("", tags_recovered_this_year, name="home"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
