#!/usr/bin/env python
# coding:utf-8
# tuwei/handlers.py - router handlers for tuwei
# ver 0.1 by winkidney 2014.05.10
import urllib,json
import socket

from django.db.models import Q
from django.conf import settings

from weilib.lib import PTItem
from weilib.lib import text_response, pic_text_response

from chat_robot import robot
from www.models import Teacher

from .models import *

HOST = settings.HOST_NAME

def search_handler(recv_msg):
    def search_teacher():
        recv_content = recv_msg.content
        teachers = Teacher.search(recv_content)
        items = [PTItem(t.name,t.name,'', HOST + '/teacher/%d/' % t.pk) for t in teachers]
        return items

    def search_course():
        pass


    result = search_teacher()

    if not result:
        result = search_course()

    if not result:
        return

    headerItem = PTItem('查询结果（最多显示10个结果）', '', '', HOST + '/')
    result.insert(0, headerItem)

    return pic_text_response(recv_msg,result[:10])

def robot_handler(recv_msg, *args, **kwargs):
    recv_content = recv_msg.content
    reply = robot.get_reply(recv_content,recv_msg.from_user_name)
    if len(reply) > 0:
        return text_response(recv_msg, reply)
    else:
        return text_response(recv_msg, """
您的留言我们已经收到:)
        """)
        
        
    