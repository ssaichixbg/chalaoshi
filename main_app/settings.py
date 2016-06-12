#coding:utf-8
"""
Django settings for techangel_admin project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
env = os.environ
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f_ra_qu7hb5@0q84n%w()m^$&iej+ccwck=l8esu7z3-8*z3tr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
if 'debug' in env:
    DEBUG = True

ALLOWED_HOSTS = ['chalaoshi.cn', 'www.chalaoshi.cn', 'ecs.chalaoshi.cn','localhost']

# Application definition

if DEBUG:
    import memcache_toolbar.panels.pylibmc

DEBUG_TOOLBAR_PATCH_SETTINGS = False

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel', 
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    #'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    #'debug_toolbar.panels.signals.SignalsPanel',
    #'debug_toolbar.panels.logging.LoggingPanel',
    #'debug_toolbar.panels.redirects.RedirectsPanel',
    'memcache_toolbar.panels.pylibmc.PylibmcPanel',
]

DEBUG_TOOLBAR_CONFIG = {"JQUERY_URL": "http://code.jquery.com/jquery-2.1.1.min.js"}

INTERNAL_IPS = ['101.231.69.134',] 

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django-datadog',
    'weilib',
    'main_app',
    'www',
    'wechat',
    'memcache_toolbar',
    #'debug_toolbar', # for debug,
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django-datadog.middleware.DatadogMiddleware'
)
#X_FRAME_OPTIONS = 'ALLOW-FROM http://www.zjustudy.com.cn'
ROOT_URLCONF = 'main_app.urls'
APPEND_SLASH = True

WSGI_APPLICATION = 'main_app.wsgi.application'


# Database & Cache
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = None
if 'PRODUCTION' in env:
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.mysql',
            'NAME':     env['mysql_chalaoshi_db'],
            'USER':     env['mysql_chalaoshi_user'],
            'PASSWORD': env['mysql_chalaoshi_password'],
            'HOST':     env['mysql_host'],
            'PORT':     env['mysql_port'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/tmp/mysql.sock',
            'NAME':     'cls',
            'USER':     'root',
            'PASSWORD': '',
            'PORT':     '',
        }
    }
    DEBUG = True
DATABASES['default']['OPTIONS'] = {'charset':'utf8mb4'} #add emoji support

CACHES = {
    'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
           'LOCATION': '127.0.0.1:11211',
         }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# MEDIA_ROOT = '/s/files/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':[
                os.path.join(BASE_DIR, 'templates'),
                '/usr/local/lib/python2.7/dist-packages/debug_toolbar/templates',
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors':[
                'django.contrib.auth.context_processors.auth',
            ],
        },
    },
]

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Email Config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
FROM_EMAIL = '自动发送<contact@zjustudy.com.cn>'
EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_PORT = '25'
EMAIL_HOST_USER = 'contact@zjustudy.com.cn'
EMAIL_HOST_PASSWORD = ''
if 'PRODUCTION' in env:
    EMAIL_HOST_PASSWORD = env['email_password_chalaoshi']
#EMAIL_USE_TLS = True

# Wechat Config
WECHAT = {}
if 'PRODUCTION' in env:
    WECHAT['APPID'] = env['wechat_chalaoshi_appid']
    WECHAT['SECRET'] = env['wechat_chalaoshi_secret']
    WECHAT['TOKEN'] = env['wechat_chalaoshi_token']

# Datadog Config
DATADOG_API_KEY = ''
DATADOG_APP_KEY = ''
DATADOG_APP_NAME = ''
if 'PRODUCTION' in env:
    DATADOG_API_KEY = env['datadog_api_key_chalaoshi'] 
    DATADOG_APP_KEY = env['datadog_app_key_chalaoshi']
    DATADOG_APP_NAME = env['datadog_app_name_chalaoshi']

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/chalaoshi/debug/django.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'request_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/chalaoshi/debug/django_request.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'scprits_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/chalaoshi/debug/script.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'error_handler': {
            'level':'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/chalaoshi/django_error.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['default','console','error_handler',],
            'level': 'DEBUG',
            'propagate': False
        },
        # 'django.request': {
        #     'handlers': ['request_handler'],
        #     'level': 'DEBUG',
        #     'propagate': False
        # },
        # 'scripts': { # 脚本专用日志
        #     'handlers': ['scprits_handler'],
        #     'level': 'INFO',
        #     'propagate': False
        # },
    }
}