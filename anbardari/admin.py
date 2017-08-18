from datetime import datetime
from anbardari.database_communication import *
from anbardari.staff import SALARY_PER_HOUR

TEMPERATURE_COST = 40000
LIGHT_COST = 30000
TIME_COST = 1000


def date_to_integer(begin_date, end_date):
    d1 = datetime.strptime(begin_date, "%Y-%m-%d")
    d2 = datetime.strptime(end_date, "%Y-%m-%d")
    return (d2 - d1).days


def get_all_goods():
    return get_items('SELECT * from goods')


def get_all_staffs():
    return get_items('SELECT * from staff')


def get_all_members():
    return get_items('SELECT * from member')


def get_keep_price():
    sum_price = 0.0
    now = get_items('SELECT CURRENT_DATE')[0]
    goods = get_items('SELECT maintenance, entry_date, exit_date FROM goods')
    for good in goods:
        if good[2] == 'NULL':
            duration = date_to_integer(now.encode('utf-8'), good[1].encode('utf-8'))
        else:
            duration = date_to_integer(good[2].encode('utf-8'), good[1].encode('utf-8'))
        sum_price += (good[0]%2) * TEMPERATURE_COST + (good[0]/2) * LIGHT_COST + duration * TIME_COST


def add_staff(national_code, name, personnel_code, phone_number, work_hours, staff_type):
    if not check_exists('staff', 'personnel_code', personnel_code):
        insert('staff', [national_code, name, personnel_code, phone_number, work_hours])
        if staff_type == 'transferee':
            insert('transferee', [personnel_code])
        if staff_type == 'dischargerer':
            insert('dischargerer', [personnel_code])
        if staff_type == 'transferer':
            insert('transferer', [personnel_code])
        if staff_type == 'keeper':
            insert('keeper', [personnel_code])
        return True
    else:
        return False


def add_member(name, password):
    code = len(get_items('SELECT code FROM member')) + 1
    insert('member', [name, code, password])
    return True


def get_keeper_goods(personnel_code):
    first_query = 'SELECT good_code FROM caring Where personnel_code = %s' % personnel_code
    second_query = 'SELECT * FROM goods Where code = ?'
    return get_items_by_fk(first_query, second_query)


def get_staff_price():
    sum_price = 0.0
    staffs_work_hours = get_items('SELECT work_hours FROM staff')
    for work_hours in staffs_work_hours:
        sum_price += work_hours * SALARY_PER_HOUR
    return sum_price

