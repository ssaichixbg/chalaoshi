import json
import time
import urllib.request, urllib.parse, urllib.error

from django.http import *
from django.shortcuts import  render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import weilib.lib
from weilib.lib import generate_js_signature,get_qrcode

APP_ID = settings.WECHAT['APPID']
APP_SEC = settings.WECHAT['SECRET']

@csrf_exempt
def wx_js_sign(request):
    url = request.POST.get('url','')
    wx = generate_js_signature(APP_ID,APP_SEC,url)
    return HttpResponse(json.dumps(wx))

@csrf_exempt
def get_qrcode(request):
    scene_id = request.GET.get('scene_id','')
    qrcode_url = weilib.lib.get_qrcode(APP_ID,APP_SEC,scene_id)
    return HttpResponse(qrcode_url)
