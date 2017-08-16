#!/usr/bin/env python2
import os
import re
import subprocess
import sys
from jinja2.exceptions import TemplateNotFound

from settings import BASE_DIR, DOCKER_TEMPLATES_ENV, DOCKER_TEMPLATES_DIR, NGINX_LOG_DIR, \
    DOCKER_SETTINGS_DICT, LOG_DIR, SHARED_DIR_OUTSIDE_CONTAINER, NGINX_TEMPLATE_FILE_NAME, NGINX_PORT, \
    NGINX_SERVER_NAME, DEBUG, GUNICORN_SOCKET_FILE_NAME, GUNICORN_PORT


# TODO some functions in this file should be utilities inside DockerMan


TEMPLATE_FILE_PATH = os.path.join(DOCKER_TEMPLATES_DIR, NGINX_TEMPLATE_FILE_NAME)
NAME_REGEX = re.compile('^[0-9a-zA-Z_]+$')


def switch_nginx(*args):
    """
    modifies nginx config so that it connects to the containers of the specified version name
    """
    if len(args) == 1:
        version_name = args[0]
        if not NAME_REGEX.match(version_name):
            print 'Invalid version name'
            return
    else:
        print 'Incorrect arguments'
        return

    try:
        template = DOCKER_TEMPLATES_ENV.get_template(NGINX_TEMPLATE_FILE_NAME)
    except TemplateNotFound:
        print 'Template %s not found' % TEMPLATE_FILE_PATH
        return
    try:
        with open('/tmp/anbardari_read', 'w') as conf_file:
            conf_file.write(
                template.render(
                    socket_path=os.path.join(SHARED_DIR_OUTSIDE_CONTAINER, version_name, GUNICORN_SOCKET_FILE_NAME),
                    nginx_error_log_path=os.path.join(NGINX_LOG_DIR, 'error.log'),
                    nginx_access_log_path=os.path.join(NGINX_LOG_DIR, 'access.log'),
                    nginx_port=NGINX_PORT,
                    nginx_server_name=NGINX_SERVER_NAME,
                    development=DEBUG,
                    version_name=version_name,
                    base_dir=BASE_DIR,
                    gunicorn_port=GUNICORN_PORT,
                )
            )
    except OSError as error:
        print str(error)
        return
    result = subprocess.call('sudo mv /tmp/anbardari_read /etc/nginx/sites-enabled/anbardari', shell=True)
    if result:
        return
    result = subprocess.check_output('sudo service nginx configtest', shell=True)
    if 'done' not in result:
        print 'Nginx configtest failed'
        return
    result = subprocess.call('sudo service nginx reload', shell=True)
    if result:
        print 'Reloading nginx failed.'
        return
    print 'Successfully configured nginx'


def _add_shared_volumes(container_settings):
    options = []
    if 'shared_volumes' in container_settings:
        for outside_dir, inside_dir in container_settings['shared_volumes'].items():
            if not outside_dir.startswith('/'):
                outside_dir = os.path.join(BASE_DIR, outside_dir)
            options += ['-v', '%s:%s' % (outside_dir, inside_dir)]
    return options


def _add_extra_hosts(container_settings):
    options = []
    if 'extra_hosts' in container_settings:
        for extra_host in container_settings['extra_hosts']:
            options += ['--add-host', extra_host]
    return options


def _add_env_file(container_settings):
    options = []
    if 'env_file' in container_settings:
        options += ['--env-file', os.path.join(BASE_DIR, container_settings['env_file'])]
    return options


def _add_published_ports(container_settings):
    options = []
    if 'published_ports' in container_settings:
        for port_map in container_settings['published_ports']:
            options += ['--publish', port_map]
    return options


def _add_envs(version_name, service_name, container_name):
    options = ['--env', 'VERSION_NAME=%s' % version_name]
    options += ['--env', 'SERVICE_NAME=%s' % service_name]
    options += ['--env', 'SELF_CONTAINER_NAME=%s' % container_name]
    return options


def _deploy_container(version_name, container_settings, shared_dir):

    service_name = container_settings['name']
    container_name = '%s_%s' % (version_name, service_name)
    image = container_name

    launch_type = container_settings['launch_type']
    if launch_type == 'none':
        return
    elif launch_type == 'build':
        dockerfile = os.path.join(BASE_DIR, container_settings['dockerfile'])
        build_options = ['-t', container_name]
        # build_options += ['--build-arg', 'gunicorn_port=%s' % GUNICORN_PORT]
        build_options += ['-f', dockerfile, BASE_DIR]
        subprocess.call(['sudo', 'docker', 'build'] + build_options)
    elif launch_type == 'pull':
        image = container_settings['image']
        subprocess.call(['sudo', 'docker', 'pull', image])

    # Creating shared directory
    if not os.path.exists(shared_dir):
        os.makedirs(shared_dir)

    options = []
    options += _add_shared_volumes(container_settings)
    options += _add_extra_hosts(container_settings)
    options += _add_env_file(container_settings)
    options += _add_published_ports(container_settings)
    options += _add_envs(version_name, service_name, container_name)
    options += ["--restart=always"]
    options += ['-v', '%s:/shared_dir' % shared_dir]
    options += ['--hostname', '%s-%s' % (version_name, service_name)]
    options += ['--name', container_name]

    subprocess.call(['sudo', 'docker', 'run'] + options + ['-idt', image])


def launch(*args):
    """
    builds and runs all necessary containers for the project
    """
    if len(args) == 1:
        version_name = args[0]
        if not NAME_REGEX.match(version_name):
            print 'Invalid version name'
            return
    else:
        print 'Incorrect arguments'
        return

    result = subprocess.call('cp /etc/localtime docker/build/anbardari', shell=True)
    if result:
        return

    for container_settings in DOCKER_SETTINGS_DICT['containers']:
        _deploy_container(version_name, container_settings, os.path.join(SHARED_DIR_OUTSIDE_CONTAINER, version_name))


def nuke(*args):
    """
    stops and removes all containers of the specified version name and removes all of its files
    NOTE: please be extra careful when using this on production
    """
    if len(args) == 1:
        version_name = args[0]
        if not NAME_REGEX.match(version_name):
            print 'Invalid version name'
            return
    else:
        print 'Incorrect arguments'
        return

    print 'Launching Nuke...'
    for container_settings in DOCKER_SETTINGS_DICT['containers']:
        container_name = '%s_%s' % (version_name, container_settings['name'])
        subprocess.call(['sudo', 'docker', 'stop', container_name])
        subprocess.call(['sudo', 'docker', 'rm', '-f', container_name])
    subprocess.call(['sudo', 'rm', '-rf', os.path.join(SHARED_DIR_OUTSIDE_CONTAINER, version_name)])
    print 'Target Destroyed'


def _call_command_on_container(version_name, service_name, command_list):
    final_command_list = [
        'sudo',
        'docker',
        'exec',
        '-it',
        '%s_%s' % (version_name, service_name),
    ]
    final_command_list += command_list
    subprocess.call(final_command_list)


def _transfer_file(version_name, service_name, file_outside, file_inside, direction="out-in"):
    file_inside = "%s_%s:%s" % (version_name, service_name, file_inside)
    command_list = ['sudo', 'docker', 'cp']
    if direction == "in-out":
        command_list += [file_inside, file_outside]
    else:
        command_list += [file_outside, file_inside]
    subprocess.call(command_list)


def _copy_files_to_container(version_name, service_name, file_list, source, destination):
    for file_path in file_list:
        _transfer_file(version_name, service_name, os.path.join(source, file_path), destination, "out-in")


def _copy_files_from_container(version_name, service_name, file_list, source, destination):
    for file_path in file_list:
        _transfer_file(version_name, service_name, destination, os.path.join(source, file_path), "in-out")


def get_shell(*args):
    if len(args) == 1:
        version_name = args[0]
        if not NAME_REGEX.match(version_name):
            print 'Invalid version name'
            return
        service_name = 'anbardari'  # default value
    elif len(args) == 2:
        version_name = args[0]
        if not NAME_REGEX.match(version_name):
            print 'Invalid version name'
            return
        service_name = args[1]
        if not NAME_REGEX.match(service_name):
            print 'Invalid service name'
            return
    else:
        print 'Incorrect arguments'
        return
    _call_command_on_container(version_name, service_name,  ['bash'])


def reload_container(*args):
    if len(args) == 1:
        version_name = args[0]
        if not NAME_REGEX.match(version_name):
            print 'Invalid version name'
            return
    else:
        print 'Incorrect format, use: deploy.py reload [version_name]'
        return

    _copy_files_to_container(version_name, 'anbardari', os.listdir(BASE_DIR), BASE_DIR, '/opt/dbproject')
    _call_command_on_container(version_name, 'anbardari', ['chmod', '+x', 'anbardari_service.py'])
    _call_command_on_container(version_name, 'anbardari', ['./anbardari_service.py', 'restart'])


methods = {
    'launch': launch,
    'reload': reload_container,  # Use this command for development purposes only
    'switch_nginx': switch_nginx,
    'nuke': nuke,
    'shell': get_shell,
}

if sys.argv[1] in methods:
    methods[sys.argv[1]](*sys.argv[2:])
else:
    print 'Invalid method'
