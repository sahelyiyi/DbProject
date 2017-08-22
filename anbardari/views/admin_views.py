from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt


from anbardari.admin import *


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


@csrf_exempt
def admin_monitor_goods(request):
    try:
        all_goods = get_all_goods()
        template = loader.get_template('show_all_objects.html')
        context = {
            'objects': all_goods,
        }
        return HttpResponse(template.render(context, request))
    except Exception as e:
        return HttpResponse(e)


@csrf_exempt
def admin_monitor_staffs(request):
    try:
        all_goods = get_all_staffs()
        template = loader.get_template('show_all_objects.html')
        context = {
            'objects': all_goods,
        }
        return HttpResponse(template.render(context, request))
    except Exception as e:
        return HttpResponse(e)


@csrf_exempt
def admin_monitor_members(request):
    try:
        all_goods = get_all_members()
        template = loader.get_template('show_all_objects.html')
        context = {
            'objects': all_goods,
        }
        return HttpResponse(template.render(context, request))
    except Exception as e:
        return HttpResponse(e)


@csrf_exempt
def admin_add_staff(request):
    national_code = request.POST['national_code']
    name = request.POST['name']
    personnel_code = request.POST['personnel_code']
    phone_number = request.POST['phone_number']
    work_hours = request.POST['work_hours']
    staff_type = request.POST['staff_type']
    add_staff(national_code, name, personnel_code, phone_number, work_hours, staff_type)
    return HttpResponse('staff has been made')


@csrf_exempt
def admin_add_member(request):
    name = request.POST['name']
    password = request.POST['password']
    add_member(name, password)
    return HttpResponse('member has been made')


@csrf_exempt
def admin_monitor_keeping_goods(request):
    try:
        keeper_goods = get_keeper_goods(request.POST['personnel_code'])
        template = loader.get_template('show_all_objects.html')
        context = {
            'objects': keeper_goods,
        }
        return HttpResponse(template.render(context, request))
    except:
        return HttpResponse("personnel code should be numeric")


@csrf_exempt
def admin_cal_keep_price(request):
    try:
        keep_price, sum_price = get_keep_price()
        keep_price.append(['SUM', sum_price])
        template = loader.get_template('show_all_objects.html')
        context = {
            'objects': keep_price,
        }
        return HttpResponse(template.render(context, request))
    except Exception as e:
        return HttpResponse(e)


@csrf_exempt
def admin_cal_staff(request):
    try:
        staff_price, sum_price = get_staff_price()
        staff_price.append(['SUM', sum_price])
        template = loader.get_template('show_all_objects.html')
        context = {
            'objects': staff_price,
        }
        return HttpResponse(template.render(context, request))
    except Exception as e:
        return HttpResponse(e)


@csrf_exempt
def admin_cal_all(request):
    try:
        staff_price, sum_staff_price = get_staff_price()
        keep_price, sum_keep_price = get_keep_price()
        all_price = staff_price + keep_price
        sum_price = sum_staff_price + sum_keep_price
        all_price.append(['SUM', sum_price])
        template = loader.get_template('show_all_objects.html')
        context = {
            'objects': all_price,
        }
        return HttpResponse(template.render(context, request))
    except Exception as e:
        return HttpResponse(e)
