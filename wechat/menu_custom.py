#coding=utf-8
from weilib.lib import create_menu,MButton,get_token
def create_btns():
    btn1 = MButton(u'\ue00e进入查老师', url='http://chalaoshi.cn/?from=mp_menu')
    m_list = [btn1, ]

    #btn1.make_click(url='http://chalaoshi.cn/?from=mp_menu')
    #btn1.add_button(MButton('发Offer', url='http://weixin2py.gg-workshop.com/recent/'))
    #btn1.add_button(MButton('成绩速查', key='GPA_BRIEF'))
    return m_list

def post_menu(appid, appsecret):
    mlist = create_btns
    token = get_token(appid, appsecret)
    return create_menu(token, mlist)
