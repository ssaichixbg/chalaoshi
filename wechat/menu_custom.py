#coding=utf-8

from weilib.lib import create_menu,MButton,get_token
def create_btns(hostname):
    btn_search = MButton(u'\U0001F50D查老师', key='SEARCH')

    btn_rank = MButton(u'排行榜')
    btn_rank.add_button(MButton(u'\U0001F525热门老师', url=hostname + '/?from=mp_menu#0'))
    btn_rank.add_button(MButton(u'\U0001f51d高分榜', url=hostname + '/?from=mp_menu#1'))
    btn_rank.add_button(MButton(u'\U0001f31a低分榜', url=hostname + '/?from=mp_menu#2'))

    btn_home = MButton(u'\U0001F4C4网页版', url=hostname + '/?from=mp_menu')

    #btn1.make_click(url='http://chalaoshi.cn/?from=mp_menu')
    #btn1.add_button(MButton('发Offer', url='http://weixin2py.gg-workshop.com/recent/'))
    #btn1.add_button(MButton('成绩速查', key='GPA_BRIEF'))

    m_list = [btn_search, btn_rank, btn_home,]
    return m_list

def post_menu(appid, appsecret, hostname):
    mlist = create_btns(hostname)
    token = get_token(appid, appsecret)
    return create_menu(token, mlist)
