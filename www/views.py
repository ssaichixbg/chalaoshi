# coding:utf-8
import json
import time
import urllib
import urllib2

from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from .models import *



# minimum count of rate needed for display
MIN_COUNT = 1

def before(func):
    def generate_uuid(ip):
        import time
        uuid = ip.replace('.','')
        uuid += '%d' % int(time.time()/50)
        return uuid[:15]
    def test_ua(ua):
        # test ua
        ua_alloweds = [
            'spider',
            'ipad',
            'iphone',
            'midp',
            'ucweb',
            'windows phone',
            'windows mobile',
            'android',
            'micromessenger',
        ]
        for ua_allowed in ua_alloweds:
            if ua_allowed in ua:
                return True
        return False

    def wx_js_sign(url):
        data = urllib.urlencode({
            'url':url,
        })
        wx = {}
        try:
            wx = json.loads(urllib2.urlopen('http://chalaoshi.sinaapp.com/wx_js_sign',data,timeout=1).read())
        except:
            pass
        return wx

    def test(request,*args, **kwargs):
        # redirect
        if request.get_host() == 'www.chalaoshi.cn':
            return HttpResponsePermanentRedirect('http://chalaoshi.cn'+request.get_full_path())

        ua = request.META.get('HTTP_USER_AGENT', None).lower()
        if not (test_ua(ua)):
            copyright = True
            return render_to_response('pc.html',locals())

        # add uuid
        mc = sae.kvdb.KVClient()
        uuid = ''
        ip = ip = request.META['REMOTE_ADDR']

        if not 'uuid' in request.COOKIES:
             uuid = generate_uuid(ip)
             request.COOKIES['uuid'] = uuid
             mc.set('v2'+uuid,1)
        else:
             uuid = request.COOKIES['uuid']

        if not mc.get('v2'+uuid):
             uuid = generate_uuid(ip)
             request.COOKIES['uuid'] = uuid
             mc.set('v2'+uuid,1)

        # SNS visit log
        fr = request.GET.get('from','')
        if not fr == '':
            # save visit log if from SNS
            log = SNSVisitLog()
            log.ip = request.META['REMOTE_ADDR']
            log.source = fr
            log.uuid = uuid
            log.save()

        # add wx js signature
        request.wx = wx_js_sign('http://'+request.get_host()+request.get_full_path())
        response = func(request,*args, **kwargs)
        response.set_cookie('uuid',request.COOKIES['uuid'][:15],expires=60*60*24*365*10)
        return response
    return test

@before
def home(request):
    def get_college_id(request):
        college_id = request.COOKIES.get('college',-1)
        if request.method == 'POST':
            college_id = request.POST.get('college',-1)
        try:
            college_id = int(college_id)
        except:
            college_id = -1
        return college_id

    college_id = get_college_id(request)
    hot_teachers = Teacher.get_hot(8,college_id)
    high_teachers = Teacher.get_high_rate(8,college_id)

    spider = False
    if 'spider' in request.META.get('HTTP_USER_AGENT', None).lower():
        spider = True
        hot_teachers = Teacher.objects.all().order_by('-hot')

    colleges = College.getAll()
    copyright = True
    help = True

    response = render_to_response('home.html',locals())
    response.set_cookie('college',college_id,expires=60*60*24*365*10)
    return response

@before
def search(request):
    keyword = request.GET.get('q','').replace(' ','').replace('\'','').replace(u'\u2006','')

    teachers = Teacher.search(keyword.encode('utf-8'))

    for teacher in teachers:
        (count, rate, check_in) = Rate.get_rate(teacher)
        if count > MIN_COUNT:
            teacher.rate = '%.1f' % rate
        else:
            teacher.rate = 'N/A'

    # add log if not empty
    if len(teachers) > 0:
        LogOnSearch.add_log(keyword,request.COOKIES['uuid'])
    return render_to_response('search_list.html',locals())

@before
def teacher_detail(request,tid):
    def get_comments(teacher):
        if isinstance(teacher, Teacher):
            comments = Comment.get_comments(teacher)
            if not comments:
                return

            (likes, dislikes) = RateOnComment.get_comment_pks(request.COOKIES['uuid'])
            for comment in comments:
                comment.rate = RateOnComment.get_rate(comment)
                if comment.pk in likes:
                    comment.like = True
                elif comment.pk in dislikes:
                    comment.dislike = True

            comments = sorted(comments, key=lambda comment: -comment.rate)
            return comments

    teacher = Teacher.objects.all().filter(pk=int(tid))
    if teacher is None:
        return HttpResponseNotFound()
    teacher = teacher[0]

    comments = get_comments(teacher)
    (count, rate, check_in) = Rate.get_rate(teacher)
    not_empty = False
    if count <= MIN_COUNT:
        rate = 'N/A'
    else:
        rate = '%.2f' % rate
        check_in = '%.1f' % check_in
        not_empty = True

    # Get teacher's gpa from zjustudy
    teacher.gpa = urllib2.urlopen('http://chalaoshi.sinaapp.com/course/list?'+urllib.urlencode({'teacher':teacher.name.encode('UTF-8')})).read()
    # If the user has already rated
    rated = Rate.is_rated(teacher, request.COOKIES['uuid'])
    # Add log
    LogOnTeacher.add_log(teacher,request.get_full_path(),request.COOKIES['uuid'])
    college= teacher.college
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
        uuid = int(request.COOKIES['uuid'])
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
        uuid = int(request.COOKIES['uuid'])
        Rate.add_rate(teacher, rate, check_in, uuid)
        #except :
            #assert False

        return HttpResponseRedirect('./comment')
    else:
        return HttpResponseNotFound()

@before
def comment_rate(request,cid):
    comment = Comment.objects.all().filter(pk=int(cid))
    t = request.GET.get('type', '')

    if comment.exists() and t in ['like','dislike']:
        if t == 'like':
            rate_num = 1
        else:
            rate_num = -1
        uuid = int(request.COOKIES['uuid'])

        RateOnComment.add_rate(comment[0],rate_num,uuid)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

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
        from django.conf import settings

        POST = request.POST
        content = '<h3>%s</h3><p>%s</p>' % (POST.get('contact',''),POST.get('comment',''))
        msg = EmailMessage('网站意见反馈',content,'contact@zjustudy.com.cn',('contact@zjustudy.com.cn',))
        msg.content_subtype = 'html'
        msg.send()

        return HttpResponseRedirect('/')