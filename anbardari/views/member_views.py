import logging


from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt


from anbardari.database_communication import *


logger = logging.getLogger(__name__)


@csrf_exempt
def helloworld(request):
    return HttpResponse('hello world.')


@csrf_exempt
def base_page(request):
    template = loader.get_template('base_page.html')
    return HttpResponse(template.render({}, request))


@csrf_exempt
def register_member_page(request):
    template = loader.get_template('register_member_page.html')
    return HttpResponse(template.render({}, request))


def _sign_in_member(name, password, request):
    if check_exists('member', 'name', name):
        query = 'SELECT password FROM member Where name = ?'
        if get_items(query, (name,))[0] == password:
            code = get_items('SELECT code FROM member Where name = ?', (name,))[0]
            template = loader.get_template('home_member_page.html')
            return HttpResponse(template.render({'code': code}, request))
        else:
            return HttpResponse('password is incorrect.')
    else:
        return HttpResponse('user not exists.')


@csrf_exempt
def sign_in_member(request):
    name = request.POST['user_name']
    password = request.POST['password']
    return _sign_in_member(name, password, request)


@csrf_exempt
def sign_up_member(request):
    name = request.POST['new_user_name']
    password = request.POST['new_password']
    conf_pass = request.POST['conf_password']
    if password != conf_pass:
        return HttpResponse('passwords does not match')
    if check_exists('member', 'name', name):
        return HttpResponse('user already exists')
    code = len(get_items('SELECT code FROM member')) + 1
    insert('member', [name, code, password])
    return _sign_in_member(name, password, request)


@csrf_exempt
def member_get_goods(request):
    return HttpResponse(request.POST)


@csrf_exempt
def member_edit_name(request):
    pass


@csrf_exempt
def member_cal_price(request):
    pass


@csrf_exempt
def member_take_delivery(request):
    pass


@csrf_exempt
def member_deliver(request):
    pass


@csrf_exempt
def member_order(request):
    pass
