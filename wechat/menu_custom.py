#coding=utf-8
from weilib.lib import create_menu,MButton,get_token
def create_btns():
    btn1 = MButton(u'查成绩')
    btn2 = MButton('查课程')
    btn3 = MButton(u'学习资料')
    btn4 = MButton(u'\ue00e查老师')
    m_list = [btn1, btn3, btn4]

    #btn1.make_click(key="123")
    #btn1.add_button(MButton('发Offer', url='http://weixin2py.gg-workshop.com/recent/'))
    btn1.add_button(MButton('成绩速查', key='GPA_BRIEF'))
    btn1.add_button(MButton('成绩统计', key='GPA_CAL'))
    btn1.add_button(MButton('15-16成绩单', key='GPA_PAPER'))
    btn1.add_button(MButton('GPA的算法', key='HELP_GPA'))

    #btn2.add_button(MButton('按课程名称', key='COURSE'))
    #btn2.add_button(MButton('按类别', key=''))
    #btn2.add_button(MButton('我来组织',key='CREATE_ACTIVITY'))
    #btn2.make_click(key='COURSE')

    btn3.add_button(MButton('理工科类', key='DOC_SCIENC'))
    btn3.add_button(MButton('社科类', key='DOC_SOC'))
    btn3.add_button(MButton('实验报告', key='DOC_OTHER'))
    btn3.add_button(MButton('体育健康手册', key='PE'))
    btn3.add_button(MButton('如何下载学习资料', key='HELP_DOWNLOAD'))

    btn4.make_click(key='CLS')


    #btn4.add_button(MButton('帮助', key='HELP_FUNCTION'))
    #btn4.make_view('http://chalaoshi.cn')
    return m_list

def post_menu(appid, appsecret):
    mlist = create_btns
    token = get_token(appid, appsecret)
    return create_menu(token, mlist)
