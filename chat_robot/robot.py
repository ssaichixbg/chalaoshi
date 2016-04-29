#!coding=utf-8
import urllib2
import urllib
import json


def get_reply(content,openId=''):
    try:
        # params = {
        #     'para': content,
        # }
        # response = urllib2.urlopen('http://www.xiaohuangji.com/ajax.php', data=urllib.urlencode(params))
        params = {
            'key': 'e49b7f8beae66073faed68da3fc12a4e',
            'info': content,
            'userid':openId,

        }
        response = urllib2.urlopen('http://www.tuling123.com/openapi/api?'+urllib.urlencode(params))
        dic = json.loads(response.read())
        return dic['text'].replace('<br>','\n')
    except:
        return ""

if __name__ == '__main__':
    print get_reply('hi')
