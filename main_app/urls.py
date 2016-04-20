# coding:utf-8
from django.conf.urls import patterns, include, url, static
from django.contrib import admin
from django.conf import settings

import www.urls
import wechat.urls
admin.autodiscover()

urlpatterns = patterns('',
        url(r'^mmm/', include(admin.site.urls)),
        url(r'^wechat/', include(wechat.urls)),
        url(r'^.*', include(www.urls)),
)