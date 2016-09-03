import time
import datetime
import copy

from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now

from .models import *
from .cache import *
time_coefficients = [10,8,4,2,1]

def clear_rank_cache(request=None):
    colleges = College.objects.all()
    keys = [c.pk for c in colleges]
    keys.append(-1)

    for key in keys:
        hot_teacher_key = 'hot_teacher_%s' % str(key)
        delCache(hot_teacher_key)
        low_rate_teacher_key = 'low_rate_teacher_%s' % str(key)
        delCache(low_rate_teacher_key)
        high_rate_teacher_key = 'high_rate_teacher_%s' % str(key)
        delCache(high_rate_teacher_key)
    if request:
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
            dt1 = now() - datetime.timedelta(days=i)
            dt2 = now() - datetime.timedelta(days=i+1)

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
        time.sleep(0.1)

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
            teacher_rates.setdefault(pk,[])
            teacher_rates[pk].append(rate.rate)
        return teacher_rates

    html = '<table>'
    results = []
    rates = Rate.objects.all()
    teacher_rates = []
    for rate in rates:
        teacher_rates.append(rate.rate)
    teacher_ave = sum(teacher_rates) * 1.0 / len(teacher_rates)

    teacher_rates = devide_rate(rates)
    teachers = Teacher.objects.all()
    for teacher in teachers:
        rate_list = copy.copy(teacher_rates.get(teacher.pk,[]))
        count = len(rate_list)
        eff = max(1,int(count*0.2))

        if count >=5:
            rate_list = rate_list[eff:]
            rate_list = rate_list[:len(rate_list)-eff]
            ave_rate = sum(rate_list) * 1.0 / len(rate_list)
            rate = 1.0 * count / ( 2 + count) * ave_rate + \
                           2.0 / (2 + count) * teacher_ave
            teacher.rate = rate
            results.append((teacher.name, ave_rate, rate, count,teacher_rates.get(teacher.pk,[]) ))
        else:
            teacher.rate = 0

        teacher.save()
        time.sleep(0.1)

    html += '<h5>%.2f</h5>' % teacher_ave
    results.sort(key=lambda result: -result[1])
    for result in results:
        html += '<tr><td>%s</td><td>%.1f</td><td>%.1f</td><td>%d</td>i<td>%s</td></tr>' % (result[0], result[1],result[2], result[3], str(result[4]))

    html += '</table>'

    if request is None:
        return html

    return HttpResponse(html)

# def backup_db(request=""):
#     from sae.deferredjob import add, MySQLExport
#     job = MySQLExport('backup', time.strftime('%Y-%m-%d',time.localtime(time.time()))+'.sql.bz2')
#     add(job)
#     return HttpResponse('1')
