import time
import datetime

from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt


from .models import *
from .cache import *
time_coefficients = [10,8,4,2,1]

def clear_rank_cache(request):
    hot_teacher_key = 'hot_teacher_%s' % str(-1)
    delCache(hot_teacher_key)
    high_rate_teacher_key = 'high_rate_teacher_%s' % str(-1)
    delCache(high_rate_teacher_key)
    return HttpResponse(0)
##
# offline calculation for hot of teachers
#
def cal_hot(request=None):
    html = '<table><tr><td>xm</td><td>hot</td><td>visit-0</td><td>visit-1</td><td>visit-2</td><td>visit-3</td><td>visit-4</td><td>comment</td></tr>'
    results = []
    teachers = Teacher.objects.all().order_by('-hot')
    for teacher in teachers:
        visit = 0
        comment = 0

        logOnTeachers = LogOnTeacher.objects.all()
        comments = Comment.objects.all()
        detail = []
        for i in range(0,5):
            time_coefficient = time_coefficients[i]
            dt1 = datetime.datetime.now() - datetime.timedelta(days=i)
            dt2 = datetime.datetime.now() - datetime.timedelta(days=i+1)

            logTs = logOnTeachers.filter(teacher=teacher,create_time__lt=dt1)
            cms = comments.filter(teacher=teacher,create_time__lt=dt1)
            if not i == 4:
                logTs = logTs.filter(create_time__gt=dt2)
                cms = cms.filter(create_time__gt=dt2)

            visit_count = logTs.count()
            comment_count = cms.count()
            detail.append(visit_count)

            visit += (visit_count*time_coefficient)
            comment += (comment_count*time_coefficient)

        hot = visit + comment * 10

        teacher.hot = hot
        teacher.save()
        results.append((teacher.name, hot,detail,comment))

    if request is None:
        return

    results.sort(key=lambda result: -result[1])
    for result in results:
        html += '<tr><td>%s</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td></tr>' % (result[0], result[1],result[2][0],result[2][1],result[2][2],result[2][3],result[2][4],result[3])

    html += '</table>'
    return HttpResponse(html)

##
# offline calculation for rate of teachers
#
def cal_rate(request=None):
    def devide_rate(rates):
        teacher_rates = {}
        for rate in rates:
            pk = rate.teacher_id
            if not teacher_rates.has_key(pk):
                teacher_rates[pk] = []
            teacher_rates[pk].append(rate.rate)
        return teacher_rates

    html = '<table>'
    results = []
    rates = Rate.objects.all()
    teacher_rates = []
    for rate in rates:
        teacher_rates.append(rate.rate)
    teacher_ave = sum(teacher_rates) / len(teacher_rates)

    teacher_rates = devide_rate(rates)
    teachers = Teacher.objects.all()
    for teacher in teachers:
        rate_list = teacher_rates[teacher.pk]
        count = len(rate_list)
        eff = max(1,int(count*0.2))

        if count >=5:
            rate_list = rate_list[eff:]
            rate_list = rate_list[:len(rate_list)-eff]
            ave_rate = sum(rate_list) / len(rate_list)
            rate = count / ( 5 + count) * ave_rate + \
                           5 / (5 + count) * teacher_ave
            #teacher.save()
            results.append((teacher.name, teacher.rate,rate,count, ))
        else:
            teacher.rate = 0

        #teacher.save()
    results.sort(key=lambda result: -result[1])
    for result in results:
        html += '<tr><td>%s</td><td>%.1f</td><td>%.1f</td><td>%d</td></tr>' % (result[0], result[1],result[2], result[3])

    html += '</table>'

    if request is None:
        return html

    return HttpResponse(html)

# def backup_db(request=""):
#     from sae.deferredjob import add, MySQLExport
#     job = MySQLExport('backup', time.strftime('%Y-%m-%d',time.localtime(time.time()))+'.sql.bz2')
#     add(job)
#     return HttpResponse('1')