#!/usr/bin/env python
#coding:utf-8
#tuwei/tests.py - test file of the lib
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.parse, urllib.error
import re
import csv
import http.cookiejar

from django.test import TestCase
from .models import *

cookieFileName = 'sdsas'
#httpHandler = urllib2.HTTPHandler(debuglevel=1)
#httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
cookie = http.cookiejar.LWPCookieJar(cookieFileName)
cookieProc = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(cookieProc)
urllib.request.install_opener(opener)


def search(key):
    url = 'http://www.cc98.org/queryresult.asp'
    data = urllib.parse.urlencode({'keyword':key})+'&sType=2&SearchDate=ALL&boardarea=0&serType=1'
    result = urllib.request.urlopen(url,data).read()
    pattern = re.compile(r'(?<=>)\d+(?=</font>个结果)')

    if not '没有找到您要查询的内容' in result:
        return int(pattern.findall(result)[0])
    else:
        return 0

def search_all_teachers():
    url = 'http://www.cc98.org/sign.asp'
    data = r'a=i&u=zhangy405&p=6bc6d4e740b65f95b2787eac4a6cfb2f&userhidden=2'
    result = urllib.request.urlopen(url,data).read()
    reader = csv.reader(open('teachers.csv','rb'))
    writer = csv.writer(open('teachers_hot.csv','wb'))

    for line in reader:
        teacher = line[1]
        s = search(teacher)
        writer.writerow((teacher,s))
        print((teacher,s))

def convert_teachers_name():
    teachers = Teacher.objects.all()
    for teacher in teachers:
        teacher.pinyin = ''
        teacher.save()
        print(('%s %s' % (teacher.name, teacher.pinyin)))


#class TeacherRateTests(TestCase):
#    def test_teacher_dianming_within_zero_and_one:
#    def test_teacher_rate:
#    def test_rate_:
