# coding:utf-8
from django.conf.urls import include, url, static
from django.contrib import admin
from django.conf import settings

import www.urls
import wechat.urls
admin.autodiscover()

urlpatterns = [
        url(r'^mmm/', include(admin.site.urls)),
        url(r'^wechat/', include(wechat.urls)),
        url(r'^', include(www.urls)),
] + static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
