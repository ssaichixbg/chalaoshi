# coding:utf-8
import json
import time
import urllib

from django.http import *
from django.shortcuts import  render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from weilib.router import base_router, db_router
from weilib.lib import GetMsg, check_signature,generate_js_signature
from weilib.handlers import default_handler

from .router import router_patterns
from .menu_custom import post_menu,create_btns
from .models import *

# router 必须是一个list实例
routers = [db_router, base_router]


def update_menu_to_wechat(request):
    rep = post_menu(settings.WECHAT.APPID, settings.WECHAT.SECRET)
    return render_to_response('send/menu_create.json', {'menu_list': create_btns()})


def test_ua(request):
    wx_ua = 'MicroMessenger'
    wp = 'Windows Phone'
    dnspod = 'DNSPod-Monitor'
    ua = request.META.get('HTTP_USER_AGENT',None)
    #if not (wx_ua in ua or wp in ua or dnspod in ua):
    #    return HttpResponsePermanentRedirect('http://weixin.qq.com')


@csrf_exempt
def wx_js_sign(request):
    url = request.POST.get('url','')
    wx = generate_js_signature(settings.WECHAT.APPID,APP_SEC,settings.WECHAT.SECRET)
    return HttpResponse(json.dumps(wx))


@csrf_exempt
def home(request):
    if not check_signature(request, settings.WECHAT.TOKEN):
        return HttpResponse('Hello World!')

    if request.method == 'GET':
        response = HttpResponse()
        response.write(request.GET.get('echostr'))
        return response

    if request.method == 'POST':
        recv_msg = GetMsg(request.body)
        for router in routers:
            result = router(recv_msg, router_patterns)
            if isinstance(result, HttpResponse):
                return result
        return default_handler(recv_msg)

    return HttpResponse('Hello World!')
