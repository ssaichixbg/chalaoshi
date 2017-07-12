# coding:utf-8
# in folder 'core'
from django.contrib import admin
from .models import *

from .cache import *

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name','display',)
    actions = ('change_status_hidden',)
    list_filter = ('display',)

    def change_status_hidden(self, request, queryset):
        rows_updated = queryset.update(display=False)
        self.message_user(request, "%s college(s) successfully marked as hidden." % rows_updated)
    change_status_hidden.short_description = "Mark selected college as hidden"

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name','college','hot','rate',)
    ordering = ('-hot',)
    search_fields = ('name',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('create_time', 'teacher','content','status',)
    search_fields = ('teacher__name',)
    actions = ('change_status_del','change_status_viewed',)
   # admin.site.disable_action('delete_selected',)

    list_filter = ('status',)

    def change_status_del(self, request, queryset):
        rows_updated = queryset.update(status=-1)
        # del cache
        for comment in queryset:
            key = str('comment_%s'%comment.teacher.id)
            delCache(key)

        self.message_user(request, "%s comment(s) successfully marked as deleted." % rows_updated)
    change_status_del.short_description = "Mark selected comments as 'delete'"

    def change_status_viewed(self, request, queryset):
        rows_updated = queryset.update(status=1)
        self.message_user(request, "%s comment(s) successfully marked as deleted." % rows_updated)
    change_status_viewed.short_description = "Mark selected comments as viewed"


class RateAdmin(admin.ModelAdmin):
    list_display = ('create_time', 'teacher','rate','check_in',)


class LogOnSearchAdmin(admin.ModelAdmin):
    list_display = ('create_time','kw','uuid')


class LogOnTeacherAdmin(admin.ModelAdmin):
    list_display = ('create_time','teacher','url','uuid',)

class SNSVisitLogAdmin(admin.ModelAdmin):
    list_display = ('create_time','ip','source',)
    list_filter = ('create_time','source',)

class OpenIDAdmin(admin.ModelAdmin):
    list_display = ('create_time','openid','uuid',)

admin.site.register(SNSVisitLog, SNSVisitLogAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(College, CollegeAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Rate, RateAdmin)
admin.site.register(LogOnSearch, LogOnSearchAdmin)
admin.site.register(LogOnTeacher, LogOnTeacherAdmin)
admin.site.register(OpenID, OpenIDAdmin)
