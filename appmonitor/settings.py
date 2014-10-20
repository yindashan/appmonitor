# -*- coding:utf-8 -*-
# Django settings for appmonitor project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG
HERE = os.path.dirname(os.path.dirname(__file__))
#print HERE
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'appmonitor',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'root',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    }
}
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(HERE, 'media').replace('\\','/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(HERE, 'static').replace('\\','/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(HERE,'static/develop/').replace('\\','/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'aup47ns$^=ec2uvcp6@i#a!w=6%h@%c690)=$980wpvy!q=ar6'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'appmonitor.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'appmonitor.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(HERE,'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'django.contrib.admin',
    'shownode',
    'showchart',
    'appitem',
    'monitoritem',
    'dynamicconfig',
    'log',
    'authority',
    'account',
    'role',
    'combinechart',
    'caseset',
    'checkresult',
    'servicegroup',
    'product',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,
#    'filters': {
#        'require_debug_false': {
#            '()': 'django.utils.log.RequireDebugFalse'
#        }
#    },
#    'handlers': {
#        'mail_admins': {
#            'level': 'ERROR',
#            'filters': ['require_debug_false'],
#            'class': 'django.utils.log.AdminEmailHandler'
#        }
#    },
#    'loggers': {
#        'django.request': {
#            'handlers': ['mail_admins'],
#            'level': 'ERROR',
#            'propagate': True,
#        },
#    }
#}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {

            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
            #'filters': ['special'],
        },
        'default': {
            'level':'DEBUG', 
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/appmonitor/all.log', #或者直接写路径：'c://logs/all.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
#        'request_handler': {
#            'level':'DEBUG',
#            'class':'logging.handlers.RotatingFileHandler',
#            'filename': os.path.join(HERE, 'logs','request.log'), #或者直接写路径：'filename':'c:/logs/request.log''  
#                        'maxBytes': 1024*1024*5, # 5 MB
#            'backupCount': 5,
#            'formatter':'standard',
#        },
#        'scprits_handler': {
#            'level':'DEBUG',
#            'class':'logging.handlers.RotatingFileHandler',
#            'filename': os.path.join(HERE, 'logs','script.log'), #或者直接写路径：'filename':'c:/logs/script.log'
#            'maxBytes': 1024*1024*5, # 5 MB
#            'backupCount': 5,
#            'formatter':'standard',
#        },
    },
    'loggers': {
        'django': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
#        'django.request': {
#            'handlers': ['request_handler'],
#            'level': 'DEBUG',
#            'propagate': False
#        },
#        'scripts': { # 脚本专用日志
#            'handlers': ['scprits_handler'],
#            'level': 'INFO',
#            'propagate': False
#        },
    }
}          

# The URL where requests are redirected for login, especially when using the login_required() decorator.
# 登录页URL 
LOGIN_URL = "/loginpage"

# 设置 用户关闭浏览器，则session失效
SESSION_EXPIRE_AT_BROWSER_CLOSE = "true"

# 会话ID在cookie中的名称
SESSION_COOKIE_NAME = "appmonitor_sessionid"

# CSRF token在cookie 中的名称
CSRF_COOKIE_NAME = "appmonitor_csrftoken"

# session 的失效时间 30天
SESSION_COOKIE_AGE = 2592000 

# session 引擎
#SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# 自定义的设置
# rrd 文件所在位置
PERFDATA_PATH = "/opt/pnp4nagios/var/perfdata"

# API 接口的返回结果存储目录
RET_RESULT_PATH = "/tmp/api_check"

# API 接口返回结果URL访问地址
RET_RESULT_URL = "http://localhost/api_check"




