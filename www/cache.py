import pylibmc as memcache
from django.conf import settings

DISPLAY_DEBUG = settings.DEBUG#False
mc = memcache.Client(['127.0.0.1'])

def setCache(key,value,time=0):
    mc.set(settings.CACHE_DOMAIN + key,value,time)
    if settings.DEBUG and DISPLAY_DEBUG:
        print(('set cache for key', settings.CACHE_DOMAIN + key, value))

def delCache(key):
    if isinstance(key, list):
        key = [k + settings.CACHE_DOMAIN for k in key]
        mc.delete_many(key)
    else:
        mc.delete(settings.CACHE_DOMAIN + key)
    if settings.DEBUG and DISPLAY_DEBUG:
        print(('del cache for key ', settings.CACHE_DOMAIN + key))

def getCache(key):
    value = mc.get(settings.CACHE_DOMAIN + key)
    if settings.DEBUG and DISPLAY_DEBUG:
        print(('get cache for key ', settings.CACHE_DOMAIN + key, value))
    return value
