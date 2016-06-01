# coding:utf-8

import json

from django.db import models
from django.db.models import Q

from .cache import *

COMMENT_STATUS = (
    (0,'未审核'),
    (1,'已审核'),
    (-1,'删除'),
)

MIN_RATE_COUNT = 5
# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class College(models.Model):
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School)
    display = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    def __getattribute__(self, item):
        def get_school():
            key = 'school_%s' % self.school_id
            school = getCache(key)
            if school:
                return school
            school = models.Model.__getattribute__(self,'school')
            setCache(key, school)
            return school

        if item == 'school':
            return get_school()

        return super(College, self).__getattribute__(item)

    @staticmethod
    def getAll():
        key = 'college_list'
        #delCache(key)
        if getCache(key):
            return getCache(key)

        from tools import convert2PY
        colleges = list(College.objects.all().filter(display=True).order_by('name'))
        for college in colleges:
            college.pinyin = convert2PY(college.name[:1])
            college.name = college.name
        colleges = sorted(colleges, key=lambda college: college.pinyin)
        setCache(key,colleges)

        return colleges


class Teacher(models.Model):
    
    name = models.CharField(max_length=100)
    college = models.ForeignKey(College)
    hot = models.IntegerField(default=0)
    rate = models.FloatField(default=0.0)

    pinyin = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        from tools import convert2PY
        if not self.pinyin or len(self.pinyin) == 0:
            self.pinyin = convert2PY(self.name)
        rate_distribution_key = 'rate_distribution'
        delCache(rate_distribution_key)
        super(Teacher, self).save(*args, **kwargs)

    def __getattribute__(self, item):
        def get_college():
            key = 'college_%s' % self.college_id
            college = getCache(key)
            if college:
                return college
            college = models.Model.__getattribute__(self, 'college')
            setCache(key, college)
            return college

        if item == 'college':
            return get_college()

        return models.Model.__getattribute__(self, item)

    @staticmethod
    def get_hot(n,cid):
        import random
        teachers = Teacher.objects.all()
        key = 'hot_teacher_%s' % str(cid)

        cached_teachers = getCache(key)
        if int(cid) >= 0:
            if not cached_teachers:
                teachers = list(teachers.filter(college=cid).order_by('-hot')[:30])
                setCache(key,teachers,3600*4)
            else:
                teachers = cached_teachers
            return teachers[:n]


        else:
            if not cached_teachers:
                teachers = list(teachers.order_by('-hot')[:30])
                setCache(key,teachers,3600*4)
            else:
                teachers = cached_teachers

            teachers_top = teachers[0:5]
            teachers_middle = teachers[5:15]
            teachers_bottom = teachers[15:30]

            teachers = random.sample(teachers_top,n/3)
            teachers += random.sample(teachers_middle,n/3)
            teachers += random.sample(teachers_bottom,n - n/3*2)

            return teachers

    @staticmethod
    def get_high_rate(n,cid):
        import random
        teachers = Teacher.objects.all()
        key = 'high_rate_teacher_%s' % str(cid)

        cached_teachers = getCache(key)
        if int(cid) >= 0:
            if not cached_teachers:
                teachers = list(teachers.filter(college=cid).order_by('-rate')[:30])
                setCache(key,teachers,3600*4)
            else:
                teachers = cached_teachers
            return teachers[:n]

        else:
            if not cached_teachers:
                teachers = list(teachers.order_by('-rate')[:30])
                setCache(key,teachers,3600*4)
            else:
                teachers = cached_teachers

            teachers_top = teachers[0:5]
            teachers_middle = teachers[5:15]
            teachers_bottom = teachers[15:30]

            teachers = random.sample(teachers_top,n/3)
            teachers += random.sample(teachers_middle,n/3)
            teachers += random.sample(teachers_bottom,n - n/3*2)

            return sorted(teachers,lambda x,y:-cmp(x.rate, y.rate))

    @staticmethod
    def get_low_rate(n):
        teachers = Teacher.objects.all().order_by('rate')[:n]
        return teachers


    @staticmethod
    def search(kw):
        teachers = []
        if kw == '':
            teachers = Teacher.objects.all()
        elif isinstance(kw, list):
            q = Q(pk=-1)
            for w in kw:
                q = Q(name=w) | q
            teachers = Teacher.objects.all().filter(q)
            teachers = teachers.order_by('-hot')[:40]
        else:
            teachers = Teacher.objects.all().filter(Q(name__contains=kw) | Q(pinyin__startswith=kw))
            teachers = teachers.order_by('-hot')[:20]

        key = str('search_teacher_%s'%kw)

        #if getCache(key):
        #    return getCache(key)
        #else:
        teachers = list(teachers)
        #    setCache(key,teachers,60*60*24)
        return teachers
    
    @staticmethod
    def get_teacher_rate_distribution():
        rate_distribution_key = 'rate_distribution'
        result = getCache(rate_distribution_key)

        if result is not None:
            return result

        teachers = Teacher.objects.all().only('rate')
        distribution = {}
        for t in teachers:
            index = int(t.rate)
            distribution.setdefault(index,0)
            distribution[index] += 1
        
        setCache(rate_distribution_key, distribution)
        return distribution

    def __unicode__(self):
        return self.name


class Comment(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)

    teacher = models.ForeignKey(Teacher)
    uuid = models.BigIntegerField()

    content = models.TextField()

    status = models.IntegerField(choices=COMMENT_STATUS, default=0)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Comment, self).save(force_insert, force_update, using,
             update_fields)

        # del cache
        key = str('comment_%s' % self.teacher.id)
        delCache(key)

    def __getattribute__(self, item):
        def get_teacher():
            key = 'teacher_%s' % self.teacher_id
            teacher = getCache(key)
            if teacher:
                return teacher
            teacher = models.Model.__getattribute__(self, 'teacher')
            setCache(key, teacher)
            return teacher

        if item == 'teacher':
            return get_teacher()

        return models.Model.__getattribute__(self, item)

    @staticmethod
    def add_comment(teacher, text, uuid):
        if isinstance(teacher, Teacher):
            comment = Comment.objects.all().filter(teacher=teacher,uuid=uuid)
            if not comment.exists():
                comment = Comment()
            else:
                comment = comment[0]

            comment.teacher = teacher
            comment.uuid = uuid
            comment.content = text
            comment.save()

            return comment

    @staticmethod
    def get_comments(teacher):
        if isinstance(teacher, Teacher):
            # get cache first
            key = str('comment_%s' % teacher.id)
            comments = getCache(key)
            if comments is not None:
                return comments
            # cache missed
            comments = list(Comment.objects.all().filter(teacher=teacher,status__gte=0))
            setCache(key,comments)
            return comments


    def __unicode__(self):
        return '%s %d' % (self.teacher.name,self.uuid)


class RateOnComment(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)

    comment = models.ForeignKey(Comment)
    uuid = models.BigIntegerField()

    rate = models.IntegerField()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(RateOnComment, self).save(force_insert, force_update, using,
             update_fields)

        # del cache
        roc_key = 'rate_on_comment_%s' % self.comment.id
        delCache(roc_key)

        # add cache
        roc_uuid_key = 'rate_on_comment_uuid_%s' % self.uuid
        rates = RateOnComment.objects.all().filter(uuid=self.uuid)
        setCache(roc_uuid_key, rates)

    @staticmethod
    def get_rate(comment):
        if isinstance(comment, Comment):
            key = 'rate_on_comment_%s' % comment.id
            # get cache first
            s = getCache(key)
            if s is not None:
                return s

            # cache missed
            rates = list(RateOnComment.objects.all().filter(comment=comment))
            s = 0
            for rate in rates:
                s += rate.rate
            setCache(key, s)
            return s

    @staticmethod
    def add_rate(comment,rate,uuid):
        if isinstance(comment, Comment):
            roc = RateOnComment.objects.all().filter(comment=comment,uuid=uuid)
            if roc:
                roc = roc[0]
            else:
                roc = RateOnComment()
            roc.comment = comment
            roc.rate = rate
            roc.uuid = uuid
            roc.save()

    @staticmethod
    def get_comment_pks(uuid):
        key = 'rate_on_comment_uuid_%s' % uuid
        rates = getCache(key)
        if rates is None:
            rates = []

        likes = []
        dislikes = []
        for rate in rates:
            if rate.rate > 0:
                likes.append(rate.comment.pk)
            else:
                dislikes.append(rate.comment.pk)
        return likes, dislikes


class Rate(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)

    teacher = models.ForeignKey(Teacher,related_name='teacher+')
    uuid = models.BigIntegerField()

    rate = models.IntegerField()
    check_in = models.IntegerField()


    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Rate, self).save(force_insert, force_update, using,
             update_fields)

        # Del cache
        rate_key = 'rate_%s' % self.teacher.id
        delCache(rate_key)

        is_rate_key = 'is_rate_%s_%s' % (self.teacher_id, self.uuid)
        delCache(is_rate_key)

    @staticmethod
    def is_rated(teacher, uuid):
        key = 'is_rate_%s_%s' % (teacher.id, uuid)
        rated = getCache(key)
        if rated is not None:
            return rated

        # Cache missed
        rated = Rate.objects.all().filter(teacher=teacher,uuid=uuid).exists()
        setCache(key, rated)
        return rated

    @staticmethod
    def get_rate(teacher):
        if isinstance(teacher, Teacher):
            key = 'rate_%s' % teacher.id
            # get cache first
            result = getCache(key)
            if result is not None:
                return result

            # cache missed
            rates = list(Rate.objects.all().filter(teacher=teacher))
            check_in_list = []
            for rate in rates:
                check_in_list.append(rate.check_in)

            count = len(check_in_list)
            rate = teacher.rate
            check_in = sum(check_in_list)

            result = (count, rate, check_in)
            setCache(key, result)
            return result
        else:
            assert False

    @staticmethod
    def add_rate(teacher, rate_num, check_in, uuid):
        if isinstance(teacher, Teacher):
            if 0 <= check_in <= 1 and 1<= rate_num <= 10 and not uuid == '':
                rate = Rate.objects.all().filter(teacher=teacher,uuid=uuid)
                if not rate.exists():
                    rate = Rate()
                else:
                    rate = rate[0]

                rate.teacher = teacher
                rate.uuid = uuid
                rate.rate = rate_num
                rate.check_in = check_in
                rate.save()

                #del cache
                key = 'rate_%s' % teacher.id
                delCache(key)
                return rate
    
    def __unicode__(self):
        return '%s %d' % (self.teacher.name,self.uuid)


class LogOnSearch(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)

    uuid = models.BigIntegerField()
    kw = models.CharField(max_length=50)

    @staticmethod
    def add_log(keyword,uuid):
        log = LogOnSearch()
        log.uuid = uuid
        log.kw = keyword
        log.save()

class LogOnTeacher(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)

    uuid = models.BigIntegerField()
    teacher = models.ForeignKey(Teacher)
    url = models.URLField()

    @staticmethod
    def add_log(teacher,url,uuid):
        log = LogOnTeacher()
        log.uuid = uuid
        log.teacher = teacher
        log.url = url
        log.save()

class OpenID(models.Model):
    '''This model is to translate OpenID in wechat to uuid'''
    create_time = models.DateTimeField(auto_now_add=True)
    openid = models.CharField(max_length=100)
    uuid = models.BigIntegerField(default=0)
    
    @staticmethod
    def get_or_create(openid, uuid=''):
        if not isinstance(uuid, int):
            try:
                uuid = int(uuid)
            except:
                uuid = 0

        oid = OpenID.objects.all().filter(openid=openid)
        if not oid.exists():
            if uuid == '':
                return
            oid = OpenID()
            oid.openid = openid
            oid.uuid = uuid
            oid.save()
        else:
            oid = oid[0]
        return oid

class SNSVisitLog(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)

    ip = models.CharField(max_length=50)
    source = models.CharField(max_length=100)
    uuid = models.BigIntegerField()
    path = models.CharField(max_length=200)
