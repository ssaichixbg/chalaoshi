#!/usr/bin/env python
# coding:utf-8
# tuwei/handlers.py - router handlers for tuwei
# ver 0.1 by winkidney 2014.05.10
import urllib,json
import socket

from django.db.models import Q

from weilib.lib import PTItem
from weilib.lib import text_response, pic_text_response

from chat_robot import robot

from .models import *


def robot_handler(recv_msg, *args, **kwargs):
    recv_content = recv_msg.content
    reply = robot.get_reply(recv_content,recv_msg.from_user_name)
    if len(reply) > 0:
        return text_response(recv_msg, reply)
    else:
        return text_response(recv_msg, """
您的留言我们已经收到:)
        """)
        
        
    