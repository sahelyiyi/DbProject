from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt


from anbardari.database_communication import *


@csrf_exempt
def base_page(request):
    template = loader.get_template('base_page.html')
    return HttpResponse(template.render({}, request))


@csrf_exempt
def register_admin_page(request):
    template = loader.get_template('register_admin_page.html')
    return HttpResponse(template.render({}, request))


def _sign_in_admin(name, password, request):
    if check_exists('admin', 'name', name):
        query = 'SELECT password FROM admin Where name = ?'
        if get_items(query, (name,))[0] == password:
            template = loader.get_template('home_admin_page.html')
            return HttpResponse(template.render({}, request))
        else:
            return HttpResponse('password is incorrect.')
    else:
        return HttpResponse('admin not exists.')


@csrf_exempt
def sign_in_admin(request):
    name = request.POST['user_name']
    password = request.POST['password']
    return _sign_in_admin(name, password, request)


@csrf_exempt
def sign_up_admin(request):
    name = request.POST['new_user_name']
    password = request.POST['new_password']
    conf_pass = request.POST['conf_password']
    if password != conf_pass:
        return HttpResponse('passwords does not match')
    if check_exists('admin', 'name', name):
        return HttpResponse('user already exists')
    insert('admin', [name, password])
    return _sign_in_admin(name, password, request)
