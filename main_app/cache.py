import pylibmc as memcache
from django.conf import settings

DISPLAY_DEBUG = False

def setCache(key,value,time=0):
    mc = memcache.Client()
    mc.set(key,value,time=time)
    if settings.DEBUG and DISPLAY_DEBUG:
        print 'set cache for key', key, value

def delCache(key):
    mc = memcache.Client()
    mc.delete(key)
    if settings.DEBUG and DISPLAY_DEBUG:
        print 'del cache for key ', key

def getCache(key):
    mc = memcache.Client()
    value = mc.get(key)
    if settings.DEBUG and DISPLAY_DEBUG:
        print 'get cache for key ', key, value
    return value