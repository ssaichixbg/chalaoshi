import pylibmc as memcache
from django.conf import settings

DISPLAY_DEBUG = True
mc = memcache.Client(['127.0.0.1'])

def setCache(key,value,time=0):
    mc.set(key,value,time)
    if settings.DEBUG and DISPLAY_DEBUG:
        print 'set cache for key', key, value

def delCache(key):
    mc.delete(key)
    if settings.DEBUG and DISPLAY_DEBUG:
        print 'del cache for key ', key

def getCache(key):
    value = mc.get(key)
    if settings.DEBUG and DISPLAY_DEBUG:
        print 'get cache for key ', key, value
    return value
