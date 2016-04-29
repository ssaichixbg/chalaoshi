# coding:utf-8
from django.conf.urls import patterns, include, url, static
from django.contrib import admin
from django.conf import settings

from .views import *
urlpatterns = patterns('',
        url(r'^update_men/', update_menu_to_wechat),
        url(r'^wx_js_sign', wx_js_sign),
        url(r'^wx_userinfo_callback', wx_userinfo_callback),
        url(r'^.*', home),
)
