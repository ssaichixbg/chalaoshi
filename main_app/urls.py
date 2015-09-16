# coding:utf-8
from django.conf.urls import patterns, include, url, static
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
        url(r'^mmm/', include(admin.site.urls)),
)

urlpatterns += patterns('main_app.tasks',
        url(r'^task/cal_hot$', 'cal_hot'),
        url(r'^task/cal_rate$', 'cal_rate'),
        url(r'^task/backup_db', 'backup_db'),
)

urlpatterns += patterns('main_app.views',
        url(r'^upload_teachers','upload_teachers'),
        url(r'^search$','search'),
        url(r'^feedback$','feedback'),

        url(r'^teacher/(?P<tid>\d+)/$','teacher_detail'),
        url(r'^teacher/(?P<tid>\d+)/comment$','teacher_comment'),
        url(r'^teacher/(?P<tid>\d+)/rate$','teacher_rate'),

        url(r'^comment/(?P<cid>\d+)/rate$','comment_rate'),
        url(r'^$', 'home'),
)