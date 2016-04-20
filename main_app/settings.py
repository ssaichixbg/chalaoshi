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
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f_ra_qu7hb5@0q84n%w()m^$&iej+ccwck=l8esu7z3-8*z3tr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['www.chalaoshi.cn', 'chalaoshi.cn','localhost']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main_app',
    #'www',
    'wechat',
    #'debug_toolbar',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
X_FRAME_OPTIONS = 'ALLOW-FROM http://www.zjustudy.com.cn'
ROOT_URLCONF = 'main_app.urls'
APPEND_SLASH = True

WSGI_APPLICATION = 'main_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = None
if 'PRODUCTION' in os.environ:
    env = os.environ
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

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
FROM_EMAIL = '自动发送<contact@zjustudy.com.cn>'
EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_PORT = '25'
EMAIL_HOST_USER = 'contact@zjustudy.com.cn'
EMAIL_HOST_PASSWORD = ''
#EMAIL_USE_TLS = True

WECHAT = {}
if 'PRODUCTION' in os.environ:
    WECHAT['APPID'] = env['wechat_chalaoshi_api']
    WECHAT['SECRET'] = env['wechat_chalaoshi_secret']
    WECHAT['TOKEN'] = env['wechat_chalaoshi_token']
