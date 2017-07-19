#coding:utf-8

import os
env = os.environ
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True

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
    'raven.contrib.django.raven_compat',
    'weilib',
    'main_app',
    'www',
    'wechat',
    'memcache_toolbar',
    'debug_toolbar',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'NAME': 'cls',
        'USER': 'root',
        'PASSWORD': '123456',
        'PORT': '',
        'OPTIONS': {
            'charset':'utf8mb4', #add emoji support
        }
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':[
                os.path.join(BASE_DIR, 'templates'),
                #'/usr/local/lib/python2.7/dist-packages/debug_toolbar/templates',
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


# Email Config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
FROM_EMAIL = '自动发送<contact@zjustudy.com.cn>'
EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_PORT = '25'
EMAIL_HOST_USER = 'contact@zjustudy.com.cn'
EMAIL_HOST_PASSWORD = ''
#EMAIL_USE_TLS = True

# Wechat Config
WECHAT = {
    'APPID':'',
    'SECRET':'',
    'TOKEN': '',
    'FAKE_OPENID': False,
}

# Datadog Config
DATADOG_API_KEY = ''
DATADOG_APP_KEY = ''
DATADOG_APP_NAME = ''

CACHE_DOMAIN = 'cls'

HOST_NAME = 'https://chalaoshi.cn'

import raven

RAVEN_CONFIG = {
    'dsn': '',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
}

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
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/chalaoshi/debug/django.log',
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/chalaoshi/debug/django_request.log',
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'scripts_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/chalaoshi/debug/script.log',
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'error_handler': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/chalaoshi/django_error.log',
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['default', 'console', 'error_handler', ],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.request': {
            'handlers': ['request_handler', ],
            'level': 'DEBUG',
            'propagate': False
        },
        'scripts': {
            'handlers': ['scripts_handler', ],
            'level': 'INFO',
            'propagate': False
        },
    }
}