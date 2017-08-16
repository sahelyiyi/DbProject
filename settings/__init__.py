import json
import os

import jinja2


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_DIR = os.path.join(BASE_DIR, 'settings')

with open(os.path.join(SETTINGS_DIR, 'settings.json'), 'r') as settings_file:
    SETTINGS_DICT = json.loads(settings_file.read())

with open(os.path.join(SETTINGS_DIR, 'docker-settings.json'), 'r') as docker_settings_file:
    DOCKER_SETTINGS_DICT = json.loads(docker_settings_file.read())

ALLOWED_HOSTS = ['*']
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'secret')
DEBUG = SETTINGS_DICT['debug']

INSTALLED_APPS = [
    'anbardari',
]


ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            '%s/templates' % BASE_DIR,
        ],
    },
]

TIME_ZONE = 'Asia/Tehran'
LANGUAGE_CODE = 'fa-IR'
LANGUAGES = (
    ('fa', 'Persian'),
    ('en', 'English'),
)
USE_I18N = True
USE_L10N = True
USE_TZ = False

DOCKER_TEMPLATES_DIR = os.path.join(BASE_DIR, 'docker', 'templates')
DOCKER_TEMPLATES_ENV = jinja2.Environment(keep_trailing_newline=True, loader=jinja2.FileSystemLoader(DOCKER_TEMPLATES_DIR))

NGINX_LOG_DIR = os.path.join(BASE_DIR, 'nginx_logs')
NGINX_TEMPLATE_FILE_NAME = 'nginx'
NGINX_PORT = SETTINGS_DICT['nginx_port'] if 'nginx_port' in SETTINGS_DICT else None
NGINX_SERVER_NAME = SETTINGS_DICT['nginx_server_name'] if 'nginx_server_name' in SETTINGS_DICT else None
SHARED_DIR_OUTSIDE_CONTAINER = os.path.join(BASE_DIR, DOCKER_SETTINGS_DICT['shared_dir'])
SHARED_DIR_INSIDE_CONTAINER = '/shared_dir'

GUNICORN_PID_FILE_NAME = 'gunicorn.pid'
GUNICORN_LOG_FILE_NAME = 'gunicorn.log'
GUNICORN_TEMPLATE_FILE_NAME = 'gunicorn.conf'
GUNICORN_PORT = SETTINGS_DICT['gunicorn_port']
GUNICORN_SOCKET_FILE_NAME = 'gunicorn.sock'
SERVICE_WORKERS = SETTINGS_DICT['service_workers']

LOG_DIR = os.path.join(BASE_DIR, 'logs')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)3.3s %(asctime)22.22s %(process)7d [%(name)s:%(funcName)s] %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'stream': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        'info-file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'info.log'),
            'formatter': 'verbose',
        },
        'error-file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'error.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['info-file'] if DEBUG else ['error-file', 'stream'],
            'level': 'INFO' if DEBUG else 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['info-file'] if DEBUG else ['error-file', 'stream'],
            'level': 'INFO' if DEBUG else 'ERROR',
            'propagate': False,
        },
        '': {  # root logger, parent of all
            'handlers': ['info-file'] if DEBUG is True else ['error-file', 'stream'],
            'level': 'INFO' if DEBUG is True else 'ERROR',
            'propagate': False,
        },
    },
}

WSGI_APPLICATION = 'settings.wsgi:application'

