# coding:utf-8
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings

from .views import *
from .tasks import *
admin.autodiscover()

urlpatterns = [
        #url(r'^task/cal_hot$', cal_hot, name='cal_hot'),
        #url(r'^task/cal_rate$', cal_rate, name='cal_rate'),
        #url(r'^task/backup_db', 'backup_db'),
        url(r'^task/clear_rank_cache', clear_rank_cache, name= 'clear_rank_cache'),
]

urlpatterns += [
        url(r'^test/clear_session',clear_session),
]

urlpatterns += [
        #url(r'^signin','signin'),
        url(r'^upload_teachers',upload_teachers),
        url(r'^search$',search),
        url(r'^feedback$',feedback),

        url(r'^teacher/(?P<tid>\d+)/$',teacher_detail, name='teacher_detail'),
        url(r'^teacher/(?P<tid>\d+)/comment_list$', teacher_comment_list, name='teacher_comment_list'),
        url(r'^teacher/(?P<tid>\d+)/comment$',teacher_comment, name='teacher_comment'),
        url(r'^teacher/(?P<tid>\d+)/rate$',teacher_rate, name='teacher_rate'),

        url(r'^comment/(?P<cid>\d+)/rate$',comment_rate),
        url(r'^comment/(?P<cid>\d+)/report', comment_report),
        
        url(r'robot.txt', robot_txt),
        #url(r'sitemap.xml', sitemap),
        url(r'(\w+\.\w+)$',to_static_img),
        url(r'^$', home),
]
