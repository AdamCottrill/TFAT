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
from django.urls import include, path
from django.contrib import admin

from tfat import urls as tfat_urls
from tfat.views import tags_recovered_this_year

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("myusers.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("tfat/", include(tfat_urls, namespace="tfat")),
    #    path("common/", include("common.urls")),
    path("", tags_recovered_this_year, name="home"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
