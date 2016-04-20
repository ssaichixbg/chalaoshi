# coding:utf-8
# weilib/admin.py - basic models admin for weilib
from django.contrib import admin
from .models import (DBTextMsg, PatternT2T, DBImgTextMsg, PatternT2PT,
                     PatternE2PT, PatternE2T,MsgLog)

class MsgLogAdmin(admin.ModelAdmin):
    list_display = ('from_user','create_time','msg_type','content','event','event_key',)
    list_filter = ('event','msg_type','create_time',)


admin.site.register(PatternT2T)
admin.site.register(PatternT2PT)
admin.site.register(PatternE2PT)
admin.site.register(PatternE2T)
admin.site.register(DBTextMsg)
admin.site.register(DBImgTextMsg)
admin.site.register(MsgLog,MsgLogAdmin)
