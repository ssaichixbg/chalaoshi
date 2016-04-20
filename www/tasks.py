import time
import datetime

from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt


from .models import *

time_coefficients = [10,8,4,2,1]

##
# offline calculation for hot of teachers
#
def cal_hot(request):
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

    results.sort(key=lambda result: -result[1])
    for result in results:
        html += '<tr><td>%s</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td></tr>' % (result[0], result[1],result[2][0],result[2][1],result[2][2],result[2][3],result[2][4],result[3])

    html += '</table>'
    return HttpResponse(html)

##
# offline calculation for rate of teachers
#
def cal_rate(request):
    html = '<table>'
    results = []
    teachers = Teacher.objects.all()
    for teacher in teachers:
        (count, rate, check_in) = Rate.get_rate(teacher)
        if count >=5:
            teacher.rate = rate
            teacher.save()
            results.append((teacher.name, rate,))
        else:
            teacher.rate = 0
            teacher.save()

    results.sort(key=lambda result: -result[1])
    for result in results:
        html += '<tr><td>%s</td><td>%.1f</td></tr>' % (result[0], result[1])

    html += '</table>'
    return HttpResponse(html)

def backup_db(request):
    from sae.deferredjob import add, MySQLExport
    job = MySQLExport('backup', time.strftime('%Y-%m-%d',time.localtime(time.time()))+'.sql.bz2')
    add(job)
    return HttpResponse('1')