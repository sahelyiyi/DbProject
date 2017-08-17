import datetime
import logging

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from anbardari.database_communication import *
from anbardari.member import *
from settings import DEFAULT_DELIVER_COST

logger = logging.getLogger(__name__)


@csrf_exempt
def helloworld(request):
    return HttpResponse('hello world.')


@csrf_exempt
def load_back(request, response, member_code, url='member_get_goods'):
    template = loader.get_template('back.html')
    context = {
        'response': response,
        'code': member_code,
        'url': url,
    }
    return HttpResponse(template.render(context, request))


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
    member_goods = get_goods(request.POST['code'])
    template = loader.get_template('get_goods.html')
    context = {
        'objects': member_goods,
        'code': request.POST['code'],
    }
    return HttpResponse(template.render(context, request))


@csrf_exempt
def member_edit_name(request):
    if edit_name(request.POST['code'], request.POST['new_name']):
        return HttpResponse('your name changed to %s' % request.POST['new_name'])
    else:
        return HttpResponse('your name did not eddited')


@csrf_exempt
def member_cal_price(request):
    return HttpResponse(calculate_keep_price(request.POST['code']))


@csrf_exempt
def member_take_delivery(request):  # sefaresh gereftan
    try:
        member_code = request.POST['code']
        good_name = request.POST['good_name']
        transferer_personal_code = request.POST['transferer_code']
        date = get_date()
        code = len(get_items('SELECT * FROM instruction')) + 1
        good_code = get_items('SELECT code FROM goods Where name=?', (good_name,))[0]
        take_delivery(code, good_code, member_code, transferer_personal_code, date, DEFAULT_DELIVER_COST)
        delete('member_basket', ['member_code', 'member_goods_code'], [member_code, member_code])
        return load_back(request, 'take delivery request sent.', member_code)
    except Exception as e:
        return HttpResponse(e)


@csrf_exempt
def member_take_delivery_list(request):
    try:
        member_code = request.POST['code']
        first_query = 'SELECT good_code from recieve Where member_code=?'
        second_query = 'SELECT name from goods Where code=?'
        all_take_deliveries = get_items_by_fk(first_query, second_query, (member_code,))
        template = loader.get_template('show_all_objects.html')
        context = {
            'objects': all_take_deliveries,
        }
        return HttpResponse(template.render(context, request))
    except Exception as e:
        return HttpResponse(e)


@csrf_exempt
def member_deliver(request):
    try:
        member_code = request.POST['code']
        good_name = request.POST['good_name']
        transferee_personal_code = request.POST['transferee_code']
        date = get_date()
        code = len(get_items('SELECT * FROM instruction')) + 1
        good_code = get_items('SELECT code FROM goods Where name=?', (good_name,))[0]
        deliver(code, good_code, member_code, transferee_personal_code, date)
        return load_back(request, 'delivery request sent.', member_code, 'show_all_goods')
    except Exception as e:
        return HttpResponse(e)


@csrf_exempt
def member_deliver_list(request):
    try:
        member_code = request.POST['code']
        first_query = 'SELECT good_code from transfer Where member_code=?'
        second_query = 'SELECT name from goods Where code=?'
        all_deliveries = get_items_by_fk(first_query, second_query, (member_code,))
        template = loader.get_template('show_all_objects.html')
        context = {
            'objects': all_deliveries,
        }
        return HttpResponse(template.render(context, request))
    except Exception as e:
        return HttpResponse(e)


@csrf_exempt
def show_all_goods(request):
    all_goods = get_items('SELECT name from goods')
    template = loader.get_template('show_all_objects.html')
    context = {
        'objects': all_goods,
        'data': {'code': request.POST['code']},
        'item': 'good_name',
        'bottom_value': 'deliver',
        'url': 'show_transferees',
    }
    return HttpResponse(template.render(context, request))


@csrf_exempt
def member_order(request):
    try:
        member_code = request.POST['code']
        good_name = request.POST['good_name']
        transferee_personal_code = request.POST['dischargerer_code']
        date = get_date()
        code = len(get_items('SELECT * FROM instruction')) + 1
        good_code = get_items('SELECT code FROM goods Where name=?', (good_name,))[0]
        order(code, good_code, member_code, transferee_personal_code, date)
        delete('member_basket', ['member_code', 'member_goods_code'], [member_code, good_code])
        return load_back(request, 'order request sent.', member_code)
    except Exception as e:
        return HttpResponse(e)


@csrf_exempt
def member_order_list(request):
    try:
        member_code = request.POST['code']
        first_query = 'SELECT good_code from instruction Where member_code=?'
        second_query = 'SELECT name from goods Where code=?'
        all_orders = get_items_by_fk(first_query, second_query, (member_code,))
        template = loader.get_template('show_all_objects.html')
        context = {
            'objects': all_orders,
        }
        return HttpResponse(template.render(context, request))
    except Exception as e:
        return HttpResponse(e)


@csrf_exempt
def add_to_basket(request):
    member_code = request.POST['code']
    good_name = request.POST['good_name']
    if add_good(member_code, good_name):
        return show_all_goods(request)
    else:
        return HttpResponse('error')


@csrf_exempt
def remove_from_basket(request):
    member_code = request.POST['code']
    good_name = request.POST['good_name']
    if remove_good(member_code, good_name):
        return member_get_goods(request)
    else:
        return HttpResponse('error')


@csrf_exempt
def show_transferers(request):
    all_transferers = get_items('SELECT personnel_code from transferer')
    member_code = request.POST['code']
    if all_transferers:
        template = loader.get_template('show_all_objects.html')
        context = {
            'objects': all_transferers,
            'data': {'code': request.POST['code'], 'good_name': request.POST['good_name']},
            'item': 'transferer_code',
            'bottom_value': 'take delivery',
            'url': 'member_take_delivery',
        }
        return HttpResponse(template.render(context, request))
    else:
        return load_back(request, 'there is no transferers.', member_code)


@csrf_exempt
def show_dischargerers(request):
    all_dischargerers = get_items('SELECT personnel_code from dischargerer')
    member_code = request.POST['code']
    if all_dischargerers:
        template = loader.get_template('show_all_objects.html')
        context = {
            'objects': all_dischargerers,
            'data': {'code': request.POST['code'], 'good_name': request.POST['good_name']},
            'item': 'dischargerer_code',
            'bottom_value': 'order',
            'url': 'member_order',
        }
        return HttpResponse(template.render(context, request))
    else:
        return load_back(request, 'there is no dischargerers.', member_code)


@csrf_exempt
def show_transferees(request):
    all_transferees = get_items('SELECT personnel_code from transferee')
    member_code = request.POST['code']
    if all_transferees:
        template = loader.get_template('show_all_objects.html')
        context = {
            'objects': all_transferees,
            'data': {'code': member_code, 'good_name': request.POST['good_name']},
            'item': 'transferee_code',
            'bottom_value': 'deliver',
            'url': 'member_deliver',
        }
        return HttpResponse(template.render(context, request))
    else:
        return load_back(request, 'there is no transferees.', member_code)