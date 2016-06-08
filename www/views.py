# coding:utf-8
import json
import time
import urllib
import urllib2

from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .models import *

# minimum count of rate needed for display
MIN_COUNT = 4

def before(func):
    def generate_uuid(ip):
        import time
        uuid = ip.replace('.','')
        uuid += '%d' % int(time.time()/50)
        return uuid[:15]
    
    def test_ua(request):
        # test ua
        ua_mobiles = [
            'ipad',
            'iphone',
            'midp',
            'ucweb',
            'windows phone',
            'windows mobile',
            'android',
        ]
        ua = request.META.get('HTTP_USER_AGENT', ' ').lower()
        
        request.ua_is_spider = ('spider' in ua)
        request.ua_is_wx = ('micromessenger' in ua)
        request.ua_is_mobile = False
        request.ua_is_pc = False
        for ua_mobile in ua_mobiles:
            if ua_mobile in ua:
                request.ua_is_mobile = True
                break
        request.ua_is_pc = not request.ua_is_spider and not request.ua_is_wx and not request.ua_is_mobile

        return

    def wx_js_sign(url):
        data = urllib.urlencode({
            'url':url,
        })
        wx = {}
        try:
            wx = json.loads(urllib2.urlopen('http://chalaoshi.cn/wechat/wx_js_sign',data,timeout=1).read())
        except Exception, e:
            raise e
        return wx

    def test(request,*args, **kwargs):
        # redirect
        if request.get_host() == 'www.chalaoshi.cn':
            return HttpResponsePermanentRedirect('http://chalaoshi.cn'+request.get_full_path())

        test_ua(request)
        if request.ua_is_pc:
            copyright = True
            return render_to_response('pc.html',locals())

        # add uuid
        uuid = -1
        ip = request.META['REMOTE_ADDR']
        
        if not 'uuid' in request.session and 'uuid' in request.COOKIES:
            request.session['uuid'] = request.COOKIES['uuid']
        
        if not 'uuid' in request.session:
             uuid = generate_uuid(ip)
             request.session['uuid'] = uuid
        else:
            uuid = request.session['uuid']
            try:
                uuid = int(uuid)
            except:
                uuid = generate_uuid(ip)
        
        # check new openid
        redirect = request.GET.get('redirect','')
        if redirect == 'openid_callback':
           pass
            
        # SNS visit log
        fr = request.GET.get('from','')
        if not fr == '':
            # save visit log if from SNS
            log = SNSVisitLog()
            log.ip = request.META['REMOTE_ADDR']
            log.source = fr
            log.path = request.get_full_path()
            log.uuid = uuid
            log.save()

        # add wx js signature
        request.wx = wx_js_sign('http://'+request.get_host()+request.get_full_path())
        
        # redirect to OpenID url
        response = None
        if 'openid' not in request.session and request.ua_is_wx:
            from urllib import quote
            callback_url = quote('http://chalaoshi.cn/wechat/wx_userinfo_callback')
            request.session['redirect'] = 'http://'+request.get_host()+request.get_full_path()
            response = HttpResponseRedirect('https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=%s#wechat_redirect' % (settings.WECHAT['APPID'], callback_url, settings.WECHAT['TOKEN']))
        else:
            if request.ua_is_wx:
                oid = OpenID.get_or_create(request.session['openid'], uuid)
                request.session['uuid'] = oid.uuid

            response = func(request,*args, **kwargs)
            response.set_cookie('uuid','',expires=-1)
        
        return response
    return test

@before
def home(request):
    def get_college_id():
        college_id = request.session.get('college',-1)
        if request.method == 'POST':
            college_id = request.POST.get('college',-1)
        try:
            college_id = int(college_id)
        except:
            college_id = -1
        return college_id

    college_id = get_college_id()
    hot_teachers = Teacher.get_hot(8,college_id)
    high_teachers = Teacher.get_high_rate(8,college_id)

    if request.ua_is_spider:
        spider = True
        hot_teachers = Teacher.objects.all().order_by('-hot')

    colleges = College.getAll()
    copyright = True
    help = True

    keywords = request.GET.getlist('q',[])
    search_url = ''
    if len(keywords) > 0:
        for keyword in keywords:
            search_url += 'q=%s&' % urllib.quote(keyword.encode('UTF-8'))

    request.session['college'] = college_id

    # wechat share
    request.share = {
        'desc':'在这里，一切都是匿名的，您可以畅所欲言。期末选课必备神器！',
        'title':'查老师 - 浙江大学非官方匿名教评系统',
    }
    response = render_to_response('home.html',locals())
    return response

@before
def search(request):
    query = request.GET.getlist('q',[])
    teachers = []
    keyword = None
    if len(query) > 1:
        teachers = Teacher.search(query)
    else:
        keyword = request.GET.get('q','').replace(' ','').replace('\'','').replace(u'\u2006','')
        teachers = Teacher.search(keyword.encode('utf-8'))

    for teacher in teachers:
        (count, rate, check_in) = Rate.get_rate(teacher)
        if count > MIN_COUNT:
            teacher.rate = '%.1f' % rate
        else:
            teacher.rate = 'N/A'

    # add log if not empty
    if len(teachers) > 0 and keyword is not None:
        LogOnSearch.add_log(keyword,request.session['uuid'])
    return render_to_response('search_list.html',locals())

@before
def teacher_detail(request,tid):
    order_by = request.GET.get('order_by','rate')

    def get_comments(teacher):
        if isinstance(teacher, Teacher):
            comments = Comment.get_comments(teacher)
            if not comments:
                return

            (likes, dislikes) = RateOnComment.get_comment_pks(request.session['uuid'])
            for comment in comments:
                comment.rate = RateOnComment.get_rate(comment)
                if comment.pk in likes:
                    comment.like = True
                elif comment.pk in dislikes:
                    comment.dislike = True

            if order_by == 'rate':
                comments = sorted(comments, key=lambda comment: -comment.rate)
            elif order_by == 'time':
                comments = sorted(comments, key=lambda comment: -int(comment.edit_time.strftime('%Y%m%d%H%M')))
            return comments

    teacher = Teacher.objects.all().filter(pk=int(tid))
    if not teacher:
        return HttpResponseNotFound()
    teacher = teacher[0]

    comments = get_comments(teacher)
    (count, rate, check_in) = Rate.get_rate(teacher)
    not_empty = False
    if count <= MIN_COUNT:
        rate = 'N/A'
    else:
        check_in = float(check_in ) / count * 100
        if not settings.DEBUG:
            rate = min(10.0,rate)
            check_in = min(100.0,check_in)
        rate = '%.2f' % rate
        check_in = '%.1f' % check_in#(float(check_in ) / count * 100)
        not_empty = True

    # Get teacher's gpa from zjustudy
    teacher.gpa = urllib2.urlopen('http://chalaoshi.sinaapp.com/course/list?'+urllib.urlencode({'teacher':teacher.name.encode('UTF-8')})).read()
    # If the user has already rated
    rated = Rate.is_rated(teacher, request.session['uuid'])
    # Add log
    LogOnTeacher.add_log(teacher,request.get_full_path(),request.session['uuid'])
    college= teacher.college

    # wechat share
    desc = '%s老师尚未收到足够评分,快来评价吧吧!' %teacher.name
    title = '快来评价%s老师吧! - 查老师' % teacher.name

    if count > MIN_COUNT:
        desc = '%d人评价 %s分 有%s%%的人认为老师点名 ' % (count, rate, check_in)
        title = '听%s老师(%s分)的课是怎样的一种体验 - 查老师' % (teacher.name, rate)
        if comments:
            desc += str(comments[0].content)

    request.share = {
        'desc': desc,
        'title': title
    }

    response = render_to_response('teacher_detail.html',locals())
    return response

@before
def teacher_comment(request,tid):
    method = request.method

    if method == 'GET':
        return render_to_response('teacher_comment.html',locals())
    elif method == 'POST':
        teacher = Teacher.objects.all().filter(pk=int(tid))
        if not teacher:
            return HttpResponseNotFound()
        teacher = teacher[0]

        POST = request.POST
        text = POST.get('comment','')
        uuid = int(request.session['uuid'])
        if len(text) > 0:
            Comment.add_comment(teacher,text,uuid)

        return HttpResponseRedirect('./')

@before
def teacher_rate(request,tid):
    method = request.method

    if method == 'GET':
        return render_to_response('teacher_rate.html',locals())
    elif method == 'POST':
        teacher = Teacher.objects.all().filter(pk=int(tid))
        if not teacher:
            return HttpResponseNotFound()

        teacher = teacher[0]
        POST = request.POST
        rate = POST.get('rate')
        check_in = POST.get('check_in')

        #try:
        rate = int(rate)
        check_in = int(check_in)
        uuid = int(request.session['uuid'])
        Rate.add_rate(teacher, rate, check_in, uuid)
        #except :
            #assert False

        return HttpResponseRedirect('./comment')
    else:
        return HttpResponseNotFound()

@before
def comment_rate(request, cid):
    comment = Comment.objects.all().filter(pk=int(cid))
    t = request.GET.get('type', '')

    if comment.exists() and t in ['like','dislike']:
        if t == 'like':
            rate_num = 1
        else:
            rate_num = -1
        uuid = int(request.session['uuid'])

        RateOnComment.add_rate(comment[0],rate_num,uuid)

        return HttpResponse('1')
    else:
        return HttpResponseNotFound()

@before
def comment_report(request, cid):
    comment = Comment.objects.all().filter(pk=int(cid))
    if comment.exists():
        comment = comment[0]
        comment.status = 2
        comment.save()
        return HttpResponse('1')
    else:
        return HttpResponseNotFound()

# def upload_teachers():
#     import csv
#     f = open('teachers.csv')
#     reader = csv.reader(f)
#     school = '浙江大学'
#     (school,new) = School.objects.get_or_create(name=school)
#     i = 0
#     for line in reader:
#         college = line[0]
#         teacher = line[1]
#         if len(college) > 0 and len(teacher) > 0:
#             (college,new)  = College.objects.get_or_create(name=college,school=school)
#             t = Teacher.objects.all().filter(name=teacher)
#             if not t.exists():
#                 (teacher,new) = Teacher.objects.get_or_create(name=teacher,college=college)
#
#         i+=1
#     return i

def upload_teachers(request):
    if request.method == 'GET':
        return HttpResponse("""
<form enctype="multipart/form-data" method="POST" action="">
   <input type="file" name="file" />
   <br />
   <input type="submit" value="上传文件" />
</form>

        """)
    else:
        import csv
        f = request.FILES['file']
        reader = csv.reader(f)
        school = '浙江大学'
        (school,new) = School.objects.get_or_create(name=school)
        i = 0
        for line in reader:
            college = line[0]
            teacher = line[1]
            if len(college) > 0 and len(teacher) > 0:
                (college,new)  = College.objects.get_or_create(name=college,school=school)
                (teacher,new) = Teacher.objects.get_or_create(name=teacher,college=college)

            i+=1
        return HttpResponse(i)

def feedback(request):
    if request.method == 'GET':
        return render_to_response('feedback.html')
    else:
        from django.core.mail import EmailMessage

        POST = request.POST
        content = '<h3>%s</h3><p>%s</p>' % (POST.get('contact',''),POST.get('comment',''))
        msg = EmailMessage('网站意见反馈',content,'contact@zjustudy.com.cn',('contact@zjustudy.com.cn',))
        msg.content_subtype = 'html'
        msg.send()

        return HttpResponseRedirect('/')

def clear_session(request):
    request.session.pop('uuid')
    request.session.pop('openid')
    return HttpResponse('Done')

@before
def robot_txt(request):
    if request.ua_is_spider:
        return HttpResponse("""
        User-agent: *
        Disallow: /static/
        """)
    else :
        return HttpResponse('')

def to_static_img(request, file):
    return HttpResponsePermanentRedirect('/static/img/' + file)
