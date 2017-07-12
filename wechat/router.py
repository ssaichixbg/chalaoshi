#!/usr/bin/env python
# coding:utf-8
# tuwei/router.py - message router to generate response message
# ver 0.1 by winkidney 2014.05.10

import re

from .handlers import *
"""
参考信息：
消息类型：text ,event,event-CLICK,image, video, link , location,
"""
router_patterns = [
    # 消息类型  消息文字（非文字类型消息留空）  操作函数
    #('text', re.compile('^help$'), help_handler),
    #('image', re.compile('^.*$'), image_handler),
    #('text', re.compile('^红包$'), hongbao_handler),
    #('text', re.compile('^成绩统计$'), gpa_cal_test_handler),
    ('text', re.compile('^.+$'), search_handler),
    ('text', re.compile('^.+$'), robot_handler),
    #('event-CLICK', re.compile('^GPA_BRIEF$'), gpa_brief_handler),
]
