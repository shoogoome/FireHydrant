"""
Django settings for FireHydrant project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
from __future__ import absolute_import, unicode_literals
import os
import yaml
import pymysql
from kombu import Queue, Exchange
import corsheaders

# 获取配置文件路径
if os.getcwd() == '/':
    conf_dir = '/firehydrant/config.yml'
else:
    conf_dir = os.getcwd() + '/config.yml'
# 读取配置文件
fp = open(conf_dir, 'r')
__fire_config = yaml.load(fp.read())
fp.close()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o_3t^bx-ajyntcrw)cwti)^c6-wf2qa8t*durk89ukdds#mq(h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True



# ##################
#      Secerts
# ##################

__config_secerts = __fire_config.get('secerts', {})
server_secerts = __config_secerts.get('server', {})
HMAC_SALT = server_secerts.get('HMAC_SALT', '')
ACCOUNT_PASSWORD_SALT = server_secerts.get('ACCOUNT_PASSWORD_SALT', '')


# ##################
#      Celery
# ##################

__config_celery = __fire_config.get('celery', {})

FIRE_CELERY_BROKER_URL = __config_celery.get('BROKER_URL', '')
FIRE_CELERY_TASK_RESULT_EXPIRES = __config_celery.get('TASK_RESULT_EXPIRES', 300)
FIRE_CELERY_RESULT_BACKEND = __config_celery.get('RESULT_BACKEND', "amqp")
FIRE_CELERY_ACCEPT_CONTENT = __config_celery.get('ACCEPT_CONTENT', ['application/json'])
FIRE_CELERY_TASK_SERIALIZER = __config_celery.get('TASK_SERIALIZER', 'json')
FIRE_CELERY_RESULT_SERIALIZER = __config_celery.get('RESULT_SERIALIZER', 'json')
FIRE_CELERY_TIMEZONE = __config_celery.get('TIMEZONE', 'Asia/Shanghai')

FIRE_CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('pay_queue', Exchange('pay_queue'), routing_key='pay_queue'),
    Queue('server_workers', Exchange('server_workers'), routing_key='server_workers'),
)
FIRE_CELERY_ROUTES = {
    # 'wejudge.server.judge.tasks.process_judge_result': {'queue': 'judge_queue', 'routing_key': 'judge_queue'},
}


# ##################
#      LiuMa
# ##################

_config_liuma = __fire_config.get('liuma', {})
LIUMA_SYSTEM_TOKEN = _config_liuma.get('systen_token', '')


# ##################
#      DataBase
# ##################

pymysql.install_as_MySQLdb()

__config_db = __fire_config.get('databases', {})
DATABASES = {
    'default': __config_db.get('server', {})
}

# ##################
#      Redis
# ##################
__config_redis = __fire_config.get('redis', {})
config_redis_cluster = __fire_config.get('redis-cluster', {})
REDIS_CONFIG_PASSWORD = ''

# ##################
#      Cache
# ##################

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '{0}:{1}'.format(
            __config_redis.get('host', '127.0.0.1'),
            __config_redis.get('port', 6379)
        ),

        'OPTIONS': {
            'DB': 2,
            'PASSWORD': __config_redis.get('password', ''),
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 100,
                'timeout': 10,
            },
        },
    },
}



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # CORS
    'corsheaders',

    'server.account',
    'server.team',
    'server.task',
    'server.pay',
    'server.ranking',
    'server.resources',
    'server.practice',
    'server.faceU',
]

MIDDLEWARE = [
    # CORS
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'common.middlewares.error_handle.FireHydrantErrorHandleMiddleware',
]

ROOT_URLCONF = 'FireHydrant.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'FireHydrant.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# ##################
#      CORS
# ##################
ALLOWED_HOSTS = ['*']

CORS_ORIGIN_WHITELIST = (
    'http://localhost:8080',
    'http://localhost:8000'
)
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)
CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'cookie',
    'cookies',
    'Cookies',
    'Cookie',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = './data/static/'

#关闭浏览器进程session失效
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# #120分钟之后session失效
SESSION_COOKIE_AGE = 60 * 60 * 2
