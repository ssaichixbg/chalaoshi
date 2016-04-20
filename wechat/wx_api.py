import json
import time
import urllib

from django.http import *
from django.shortcuts import  render_to_response
from django.views.decorators.csrf import csrf_exempt

import weilib.lib
from weilib.lib import generate_js_signature,get_qrcode

try:
    from main_app.localsettings import TOKEN,APP_ID,APP_SEC
except ImportError:
    from main_app.settings import TOKEN,APP_ID,APP_SEC


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