# coding:utf-8
# weilib/models.py - database definition file of weilib
# by kidney 2014.05.12
from django.db import models

MSG_TYPES = (
    ('text', '文本消息'),
    ('event', '事件消息'),
    ('image', '图片消息'),
    ('location', '位置消息'),
    ('voice', '语音消息'),
    ('video', '视频消息'),
)
EVENTS = (
         ('subscribe', '关注事件'),
         ('unsubscribe', '取消关注事件'),
         ('SCAN', '扫描二维码'),
         ('LOCATION', '上报地理位置'),
         ('CLICK', '自定义菜单事件'),
         ('VIEW', '用户点击链接的跳转事件'),
)


class DBTextMsg(models.Model):

    """msg in database"""
    class Meta:
        verbose_name = u'回复管理(文字消息)'
        verbose_name_plural = u'回复管理(文字消息)'
    name = models.CharField(blank=True, max_length=50, verbose_name=u"消息名字",
                            help_text=u"可以为空，仅用来标识消息")
    content = models.TextField(blank=False, verbose_name=u"消息内容")

    def __unicode__(self):
        return u'%s %s' % (self.id, self.name)


class DBImgTextMsg(models.Model):

    """image_text msg in database"""
    class Meta:
        verbose_name = u'回复管理(图文消息)'
        verbose_name_plural = u'回复管理(图文消息)'
    name = models.CharField(blank=True, max_length=50, verbose_name=u"消息名称",
                            help_text=u"可以为空，仅用来标识消息")
    title = models.CharField(blank=True, max_length=255, verbose_name=u"消息标题")
    description = models.CharField(
        blank=True, max_length=255, verbose_name=u"消息描述")
    pic_url = models.URLField(blank=False, verbose_name=u"图片地址")
    url = models.URLField(blank=False, max_length=255, verbose_name=u"文章地址")

    def __unicode__(self):
        return u'%s %s' % (self.id, self.name)


class PatternE2T(models.Model):

    """text response pattern to user"""
    class Meta:
        verbose_name = u'回复规则管理(事件>文本消息)'
        verbose_name_plural = u'回复规则管理(事件>文本消息)'
    name = models.CharField(blank=True, max_length=50, verbose_name=u"规则命名",
                            help_text=u"可以为空，仅用来标识规则")
    type = models.CharField(max_length=20,
                            choices=MSG_TYPES, verbose_name=u"收到的消息类型（请保持默认）",
                            default='event',)
    event = models.CharField(max_length=30,
                             choices=EVENTS,
                             default='CLICK', verbose_name=u"事件类型",
                             help_text=u"除非收到的消息类型为“自定义菜单事件或者点击链接跳转事件，否则不要修改本字段”")
    event_key = models.CharField(blank=True, max_length=255,
                                 verbose_name=u"event_key或者自定义url",
                                 help_text=u'<strong>对于自定义菜单事件和自定义链接跳转事件这个是必填的！</strong>')
    handler = models.ForeignKey(DBTextMsg, verbose_name=u"回复消息")

    def __unicode__(self):
        return u'%s %s' % (self.id, self.name)


class PatternE2PT(models.Model):

    """text response pattern to user"""
    class Meta:
        verbose_name = u'回复规则管理（事件>图文消息回复）'
        verbose_name_plural = u'回复规则管理（事件>图文消息回复）'
    name = models.CharField(blank=True, max_length=50, verbose_name=u"规则命名",
                            help_text=u"可以为空，仅用来标识规则")
    type = models.CharField(max_length=20,
                            choices=MSG_TYPES,
                            default='event', verbose_name=u"用户消息类型（请保持默认）",
                            help_text=u"除非你清楚这个字段的含义，否则请不要随意更改")
    event = models.CharField(max_length=30,
                             choices=EVENTS,
                             default='CLICK', verbose_name=u"事件类型")
    event_key = models.CharField(blank=True, max_length=255,
                                 verbose_name=u"event_key或者自定义url",
                                 help_text='<strong>对于自定义菜单事件和自定义链接跳转事件这个是必填的！</strong>')
    handler = models.ManyToManyField(
        DBImgTextMsg, verbose_name=u"回复消息", help_text=u"最多允许五条，不然会出错")

    def __unicode__(self):
        return u'%s %s' % (self.id, self.name)


class PatternT2PT(models.Model):

    """image_text response pattern to user"""
    class Meta:
        verbose_name = u'回复规则管理(文本>图文消息)'
        verbose_name_plural = u'回复规则管理(文本>图文消息)'
    name = models.CharField(blank=True, max_length=50, verbose_name=u"规则命名",
                            help_text=u"可以为空，仅用来标识规则")
    type = models.CharField(max_length=20,
                            choices=MSG_TYPES,
                            default='text', verbose_name=u"用户消息类型（请保持默认）",
                            help_text=u"除非你清楚这个字段的含义，否则请不要随意更改")
    content = models.CharField(max_length=50, blank=True, verbose_name=u"需要匹配的消息",
                               help_text=u"使用正则表达式")
    handler = models.ManyToManyField(
        DBImgTextMsg, verbose_name=u"回复消息", help_text=u"最多允许五条，不然会出错")

    def __unicode__(self):
        return u'%s %s' % (self.id, self.name)


class PatternT2T(models.Model):

    """text response pattern to user"""
    class Meta:
        verbose_name = u'回复规则管理(文本>文本消息)'
        verbose_name_plural = u'回复规则管理(文本>文本消息)'
    name = models.CharField(blank=True, max_length=50, verbose_name="规则命名",
                            help_text=u"可以为空，仅用来标识规则")
    type = models.CharField(max_length=20,
                            choices=MSG_TYPES,
                            default='text', verbose_name=u"用户消息类型（请保持默认）",
                            help_text=u"除非你清楚这个字段的含义，否则请不要随意更改")
    content = models.CharField(max_length=100, blank=True, verbose_name=u"收到的消息",
                               help_text=u"使用正则表达式")
    handler = models.ForeignKey(DBTextMsg, verbose_name=u"响应的消息内容")

    def __unicode__(self):
        return u'%s %s' % (self.id, self.name)


class MsgLog(models.Model):
    class Meta:
        verbose_name = u'消息记录'
        verbose_name_plural = u'消息记录'

    to_user  = models.CharField(max_length=100)
    from_user  = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)
    msg_type = models.CharField(choices=MSG_TYPES,max_length=50,default='')
    content = models.TextField(default='')
    msg_id = models.BigIntegerField(default=0)
    media_id = models.CharField(max_length=100,default='')
    pic_url = models.CharField(max_length=250,default='')
    media_format = models.CharField(max_length=50,default='')
    recongnition = models.TextField(default='')
    thumb_media_id = models.CharField(max_length=100,default='')
    event = models.CharField(max_length=50,default='')
    event_key = models.CharField(max_length=50,default='')
    ticket = models.CharField(max_length=50,default='')

    def __unicode__(self):
        return u'%s %s' % (self.id, self.to_user)


class WeixinGroup(models.Model):
    class Meta:
        verbose_name = u'用户分组'
        verbose_name_plural = u'用户分组'

    name = models.CharField(max_length=30, blank=True, verbose_name=u'组名')
    group_id = models.BigIntegerField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s %s' % (self.group_id, self.name)


class WeixinUser(models.Model):
    class Meta:
        verbose_name = u'用户分组'
        verbose_name_plural = u'用户分组'

    nickname = models.CharField(max_length=30, blank=True, verbose_name=u'昵称')
    openid = models.CharField(max_length=40, unique=True, verbose_name=u'OpenID')
    group = models.ForeignKey(WeixinGroup)

    def __unicode__(self):
        return u"%s %s" % (self.id, self.openid)

