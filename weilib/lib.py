# coding:utf-8
# weilib/lib.py - contains libs of weichat message
# and some tool function.
# read xml text and return a xml object
import datetime
import os
import json
import re
import hashlib
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.parse, urllib.error
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import Context, Template
from django.core.cache import cache

from .models import MsgLog

try:
    import pickle as pickle
except ImportError:
    import pickle

from .plugin.setting import plugin_text as PLUGINS

DEFAULT_TIMEOUT = 15 * 60

# basic info
re_msg_type = re.compile(r"<MsgType><!\[CDATA\[(.*?)\]\]></MsgType>")
re_msg_tuid = re.compile(r"<ToUserName><!\[CDATA\[(.*?)\]\]></ToUserName>")
re_msg_fuid = re.compile(r"<FromUserName><!\[CDATA\[(.*?)\]\]></FromUserName>")
re_msg_ctime = re.compile(r"<CreateTime>(.*?)</CreateTime>")
re_msg_id = re.compile(r"<MsgId>(.*?)</MsgId>")
re_media_id = re.compile(r"<MediaId><!\[CDATA\[(.*?)\]\]></MediaId>")
# text msg
re_text_content = re.compile(r"<Content><!\[CDATA\[(.*?)\]\]></Content>")


# img msg
re_img_url = re.compile(r"<PicUrl><!\[CDATA\[(.*?)\]\]></PicUrl>")
re_img_id = re.compile(r"")
# location msg
re_locx = re.compile(r"<Location_X>(.*?)</Location_X>")
re_locy = re.compile(r"<Location_Y>(.*?)</Location_Y>")
re_scale = re.compile(r"<Scale>(.*?)</Scale>")
re_label = re.compile(r"<Label><!\[CDATA\[(.*?)\]\]></Label>")

# link msg
re_title = re.compile(r"<Title><!\[CDATA\[(.*?)\]\]></Title>")
re_description = re.compile(
    r"<Description><!\[CDATA\[(.*?)\]\]></Description>")
re_url = re.compile(r"<Url><!\[CDATA\[(.*?)\]\]></Url>")

# event msg
re_event = re.compile(r"<Event><!\[CDATA\[(.*?)\]\]></Event>")
re_eventkey = re.compile(r"<EventKey><!\[CDATA\[(.*?)\]\]></EventKey>")


class GetMsg(object):

    """输入一个xml文本字符串对象，生成一个object并返回"""

    def get_info(self, regx, msg):
        result = re.findall(regx, msg)
        if result:
            return result[0]
        else:
            return ''

    def get_text_msg(self, msg):

        self.content = self.get_info(re_text_content, msg)
        self.log.content = self.content

    def get_img_msg(self, msg):
        """图片消息"""

        self.pic_url = self.get_info(re_img_url, msg)
        self.media_id = self.get_info(re_media_id, msg)

        self.log.pic_url = self.pic_url
        self.log.media_id = self.media_id

    def get_location_msg(self, msg):
        """地理位置消息"""

        self.location_x = self.get_info(re_locx, msg)
        self.location_y = self.get_info(re_locy, msg)
        self.scale = self.get_info(re_scale, msg)
        self.label = self.get_info(re_label, msg)

        self.log.content = '%s %s\n %s\n %s\n'% (self.location_x,self.location_y,self.scale,self.label)

    def get_link_msg(self, msg):
        """链接消息推送"""

        self.title = self.get_info(re_title, msg)
        self.description = self.get_info(re_description, msg)
        self.url = self.get_info(re_url, msg)

        self.log.content = '%s\n %s\n %s\n'% (self.title,self.description,self.url)

    def get_event_msg(self, msg):
        """事件推送"""
        self.event = self.get_info(re_event, msg)
        self.event_key = self.get_info(re_eventkey, msg)

        self.log.event = self.event
        self.log.event_key = self.event_key

    def __init__(self, msg):
        """genetate a message object
        """
        self.log = MsgLog()
        self.to_user_name = self.get_info(re_msg_tuid, msg)
        self.from_user_name = self.get_info(re_msg_fuid, msg)
        self.create_time = self.get_info(re_msg_ctime, msg)
        self.msg_type = self.get_info(re_msg_type, msg)
        self.msg_id = self.get_info(re_msg_id, msg)

        log = self.log
        log.to_user = self.to_user_name
        log.from_user = self.from_user_name
        log.msg_type = self.msg_type
        try:
            log.msg_id = self.msg_id
        finally:
            log.msg_id = 0

        msgtype = self.msg_type
        if msgtype == 'text':
            self.get_text_msg(msg)
        elif msgtype == 'image':
            self.get_img_msg(msg)
        elif msgtype == 'location':
            self.get_location_msg(msg)
        elif msgtype == 'link':
            self.get_link_msg(msg)
        elif msgtype == 'event':
            self.get_event_msg(msg)

        #log.save()


class WeiSession(object):

    """ Helper Class to store info by session ID(Default: OpenID),
        Because of its usage of pickle, some type of data can't be stored correctly.
    """

    def __init__(self, session_id):
        if not isinstance(session_id, (str, int)):
            raise TypeError("Argument openid [%s] must be a str/unicode/int object!")
        self.session_id = session_id
        self._get_session()

    def _get_session(self):
        session = cache.get(self.session_id)
        if not session:
            self.session = {}
        else:
            self.session = pickle.loads(session)

    def _save(self):
        session_storage = pickle.dumps(self.session)
        cache.set(self.session_id, session_storage, DEFAULT_TIMEOUT)

    def set_key(self, key, value):
        self.session[key] = value
        self._save()

    def get_key(self, key):
        return self.session.get(key)


# Message for response to user
class BaseReMsg(object):

    """Base returned message for client."""

    def __init__(self, to_user, from_user, ctime, func_flag=0):
        """
        Normal init by (to_user, from_user, ctime, func_flag).
        :param to_user: target openid
        :type to_user: str, unicode, int
        :param from_user: openid
        :type from_user: str, unicode, int
        :param ctime: the origin msg send time(unix timestamp).
        :param func_flag: weichat func_flag.
        :return:
        """
        self.to_user_name = from_user
        self.from_user_name = to_user
        self.create_time = int(ctime) + 1
        self.function_flag = func_flag


class TextMsg(BaseReMsg):

    """文字消息类"""

    def make_msg(self, content):
        self.content = content


class MusicMsg(BaseReMsg):

    """music message"""

    def make_msg(self, title, description, music_url, hq, media_id=0):
        self.title = title
        self.description = description
        self.music_url = music_url
        self.hq_music_url = hq
        self.media_id = media_id


class ImgMsg(BaseReMsg):

    """Image message"""

    def make_msg(self, media_id):
        self.media_id = media_id


class PicTextMsg(BaseReMsg):

    """图文消息类"""

    def __init__(self, to_user, from_user, ctime, func_flag=0):
        super(PicTextMsg, self).__init__(
            to_user, from_user, ctime, func_flag=0)
        self.articles = []

    def make_msg(self, article_count):

        self.article_count = article_count

    def new_item(self, title, description, pic_url, url):
        item = {'title': title,
                'description': description,
                'pic_url': pic_url,
                'url': url, }
        self.articles.append(item)


class PTItem(object):

    def __init__(self, title, description, pic_url, url):
        self.title = title
        self.description = description
        self.pic_url = pic_url
        self.url = url


class MButton(object):

    """ button class of the weichat meun"""

    def __init__(self, name, **kwargs):
        self.type = None
        self.key = None
        self.url = None
        self.sub_buttons = []
        self.name = name
        url = kwargs.get('url')
        key = kwargs.get('key')
        if url or key:
            if url:
                self.make_view(url)
            else:
                self.make_click(key)

    def make_click(self, key):
        self.type = 'click'
        self.key = key

    def make_view(self, url):
        self.type = 'view'
        self.url = url

    def add_button(self, button):
        if isinstance(button, MButton):
            self.sub_buttons.append(button)
        else:
            raise TypeError


def check_signature(request, token):
    """Verify if the author of received msg is tencent."""
    request_dict = request.GET
    if request_dict.get('signature') and request_dict.get('timestamp') \
            and request_dict.get('nonce') and request_dict.get('echostr'):
        signature = request_dict.get('signature')
        timestamp = request_dict.get('timestamp')
        nonce = request_dict.get('nonce')
        token = token
        tmplist = sorted([token, timestamp, nonce])
        newstr = ''.join(tmplist)
        sha1result = hashlib.sha1()
        sha1result.update(newstr)
        if sha1result.hexdigest() == str(signature):
            return True
        else:
            return False
    else:
        return False


def get_qrcode(appid, appsecret, scene_id):
    token = get_token(appid, appsecret)
    ticket_url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s' % (token)
    post = {
        'expire_seconds':60*60,
        'action_name':'QR_SCENE',
        'action_info':{
            'scene':int(scene_id),
        }
    }
    result = json.loads(urllib.request.urlopen(ticket_url,json.dumps(post)).read())
    if 'errcode' not in result:
        ticket = result['ticket']
        qrcode_url = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?%s' % (urllib.parse.urlencode({
            'ticket':ticket,
        }))
        return qrcode_url
    return json.dumps(result)

def generate_js_signature(appid, appsecret,url, noncestr):
    import time

    # get jsapi_ticket
    jsapi_ticket = cache.get(appid+'jsapi_ticket')
    last_update = cache.get(appid+'jsapi_ticket_time')
    if not jsapi_ticket or not last_update or (time.time() - last_update > 7000):
        token = get_token(appid, appsecret)
        ticket_url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%(token)s&type=jsapi'\
              % {'token': token}
        try:
            result = urllib.request.urlopen(ticket_url, timeout=20).read()
        except:
            return None
        result = re.findall(b'"ticket":"(.*?)"', result)
        if result:
            # save to cache
            cache.set(appid+'jsapi_ticket',result[0])
            cache.set(appid+'jsapi_ticket_time',time.time())
            jsapi_ticket = result[0]
        else:
            return None

    timestamp = int(time.time())
    sign = 'jsapi_ticket=%s&noncestr=%s&timestamp=%s&url=%s' \
            %(jsapi_ticket,noncestr,timestamp,url)
    sha1result = hashlib.sha1()
    sha1result.update(sign)
    sign = sha1result.hexdigest()

    return {
        'appId':appid,
        'timestamp':timestamp,
        'nonceStr':noncestr,
        'signature':sign,
        'url':url
    }

def get_token(appid, appsecret):
    """
    Get AccessToken by appid and appsecret.The result will be saved in cache for 7000s
    :param appid:
    :param appsecret:
    :return: AccessToekn.
    """
    import time
    cache_key = '%sAccessToeken' % appid
    cache_time_key = '%sAccessToeken_time' % appid

    last_update = cache.get(cache_time_key)
    if last_update and (time.time() - last_update) < 7000 and cache.get(cache_key):
        return cache.get(cache_key)

    url = """https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%(appid)s&secret=%(appsecret)s""" \
        % {'appid': appid, 'appsecret': appsecret}
    result = ''
    try:
        result = urllib.request.urlopen(url, timeout=20).read()
    except:
        return None
    result = re.findall(b'"access_token":"(.*?)"', result)
    if result:
        # save to cache
        cache.set(cache_key,result[0])
        cache.set(cache_time_key,time.time())
        return result[0]
    return None


def create_menu(access_token, menu_list):
    """
    Create WeiChat menu in WeiChat Client.
    :param access_token: access_token str
    :param menu_list:
    :return:
    """
    url = """ https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s""" \
        % access_token
    data = render_to_string('send/menu_create.json', {'menu_list': menu_list})

    endata = data.encode('utf-8')
    # open('tmp.json','w').write(endata)
    try:
        result = ""
        result = urllib.request.urlopen(url, endata, 20).read()
    except:
        return False
    return result
    result = re.findall('ok', result)
    if result:
        return True
    else:
        return False


def render_from_string(string, data):
    t = Template(string)
    return t.render(Context(data))


def text_response(recv_msg, content):
    msg = TextMsg(
        recv_msg.to_user_name, recv_msg.from_user_name, recv_msg.create_time)
    plugin_dict = {}
    for plugin in PLUGINS:
        result = plugin.processor(recv_msg)
        if isinstance(result, dict):
            plugin_dict.update(result)
    msg.make_msg(render_from_string(content, plugin_dict))
    return render_to_response('response/msg_text.xml',
                              {'msg': msg, }
                              )


def image_response(recv_msg, media_id):
    msg = ImgMsg(
        recv_msg.to_user_name, recv_msg.from_user_name, recv_msg.create_time)
    msg.make_msg(media_id)
    return render_to_response('response/msg_text.xml',
                              {'msg': msg, }
                              )


def pic_text_response(recv_msg, msg_item):
    msg = PicTextMsg(
        recv_msg.to_user_name, recv_msg.from_user_name, recv_msg.create_time)
    if isinstance(msg_item, PTItem):
        article_count = 1
        msg.new_item(
            msg_item.title, msg_item.description, msg_item.pic_url, msg_item.url)
    if isinstance(msg_item, list):
        article_count = len(msg_item)
        for item in msg_item:
            msg.new_item(item.title, item.description, item.pic_url, item.url)
    msg.make_msg(article_count)
    return render_to_response('response/msg_pic_text.xml',
                              {'msg': msg, }
                              )

def web_page_auth_url(appid,redirect_uri,scope=2):
    if scope == 1:
        scope = 'snsapi_base'
    else:
        scope = 'snsapi_userinfo'

    params = {
        'appid' : appid,
        'redirect_uri' : redirect_uri,
        'response_type' : 'code',
        'scope' : scope,
    }
    url = 'https://open.weixin.qq.com/connect/oauth2/authorize?' + urllib.parse.urlencode(params) + '#wechat_redirect'
    return url
# TODO:
#def get
