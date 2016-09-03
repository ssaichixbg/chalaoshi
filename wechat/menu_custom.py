#coding=utf-8

from weilib.lib import create_menu,MButton,get_token
def create_btns(hostname):
    btn1 = MButton(u'搜索', key='SEARCH')

    btn2 = MButton(u'排行榜')
    btn2.add_button(MButton(u'热门老师', url=''))
    btn2.add_button(MButton(u'高分榜', url=''))
    btn2.add_button(MButton(u'低分榜', url=''))

    btn3 = MButton(u'\ue00e进入查老师', url=hostname + '/?from=mp_menu')

    #btn1.make_click(url='http://chalaoshi.cn/?from=mp_menu')
    #btn1.add_button(MButton('发Offer', url='http://weixin2py.gg-workshop.com/recent/'))
    #btn1.add_button(MButton('成绩速查', key='GPA_BRIEF'))

    m_list = [btn1, btn2, btn3 ]
    return m_list

def post_menu(appid, appsecret, hostname):
    mlist = create_btns(hostname)
    token = get_token(appid, appsecret)
    return create_menu(token, mlist)
