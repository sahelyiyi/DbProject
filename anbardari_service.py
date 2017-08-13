#!/usr/bin/env python2
import os
import subprocess
import sys

from jinja2.exceptions import TemplateNotFound

from settings import BASE_DIR, GUNICORN_LOG_FILE_NAME, GUNICORN_PORT, GUNICORN_SOCKET_FILE_NAME, \
    GUNICORN_TEMPLATE_FILE_NAME, LOG_DIR, SERVICE_WORKERS, DOCKER_TEMPLATES_ENV, DOCKER_TEMPLATES_DIR

PID_FILE_PATH = os.path.join('/tmp', GUNICORN_SOCKET_FILE_NAME)
LOG_FILE_PATH = os.path.join(LOG_DIR, GUNICORN_LOG_FILE_NAME)
TEMPLATE_FILE_PATH = os.path.join(DOCKER_TEMPLATES_DIR, GUNICORN_TEMPLATE_FILE_NAME)
CONFIG_FILE_PATH = os.path.join('/tmp', GUNICORN_TEMPLATE_FILE_NAME)


def start_gunicorn():
    try:
        with open(PID_FILE_PATH, 'r') as pid_file:
            pid = int(pid_file.read())
            print 'Anbardari service already running with pid=%d' % pid
    except (IOError, ValueError):
        try:
            template = DOCKER_TEMPLATES_ENV.get_template(GUNICORN_TEMPLATE_FILE_NAME)
        except TemplateNotFound:
            print 'Template %s not found' % TEMPLATE_FILE_PATH
            return
        try:
            with open(CONFIG_FILE_PATH, 'w') as output_file:
                output_file.write(
                    template.render(
                        base_dir=BASE_DIR,
                        service_workers=SERVICE_WORKERS,
                        port=GUNICORN_PORT,
                    )
                )
        except IOError as error:
            print str(error)
            return

        result = subprocess.call(' '.join([
            'gunicorn',
            'wsgi:application',
            '--config=%s' % CONFIG_FILE_PATH,
            '--pid=%s' % PID_FILE_PATH,
            '--name=anbardari_gunicorn',
            '--user=root',
            '--group=root',
            '--log-level=info',
        ]), shell=True)
        if result:
            print 'Starting anbardari gunicorn failed'
            return
        print 'Successfully started anbardari service'


def stop_gunicorn():
    try:
        with open(PID_FILE_PATH, 'r') as pidfile:
            pid = int(pidfile.read())
            result = subprocess.call('kill -9 %d' % pid, shell=True)
            if result:
                print 'Could not stop anbardari service with pid=%d' % pid
                os.remove(PID_FILE_PATH)
                return
            try:
                os.remove(PID_FILE_PATH)
            except OSError:
                print 'Could not remove PID file %s: Permission denied or file does not exist' % PID_FILE_PATH
            print 'Stopped anbardari service with pid=%d' % pid
    except (IOError, ValueError):
        print 'anbardari service already stopped'


def restart_gunicorn():
    stop_gunicorn()
    start_gunicorn()


def configure():
    pass


methods = {
    'start': start_gunicorn,
    'stop': stop_gunicorn,
    'restart': restart_gunicorn,
    'configure': configure
}

if sys.argv[1] in methods:
    methods[sys.argv[1]](*sys.argv[2:])
else:
    print 'Invalid method'
