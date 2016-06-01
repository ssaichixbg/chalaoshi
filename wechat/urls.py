# coding:utf-8
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings

from .views import *
urlpatterns = [
        url(r'^update_menu', update_menu_to_wechat),
        url(r'^wx_js_sign', wx_js_sign),
        url(r'^wx_userinfo_callback', wx_userinfo_callback),
        url(r'^.*', home),
]
