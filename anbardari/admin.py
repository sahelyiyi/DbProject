from datetime import datetime
from anbardari.database_communication import *
from anbardari.staff import SALARY_PER_HOUR

TEMPERATURE_COST = 40000
LIGHT_COST = 30000
TIME_COST = 1000


def get_all_goods():
    return get_items('SELECT * from goods')


def get_all_staffs():
    return get_items('SELECT * from staff')


def get_all_members():
    return get_items('SELECT * from member')


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
    first_query = 'SELECT good_code FROM caring Where keeper_personnel_code = %s' % personnel_code
    second_query = 'SELECT * FROM goods Where code = ?'
    return get_items_by_fk(first_query, second_query)


def get_keep_price():
    sum_price = 0.0
    goods = get_items('SELECT code, name, (maintenance%2) * ? + (maintenance/2) * ? + (julianday(exit_date) - julianday(entry_date)) * ? FROM goods', (TEMPERATURE_COST, LIGHT_COST, TIME_COST,))
    for good in goods:
        sum_price += good[2]
    return goods, sum_price


def get_staff_price():
    sum_price = 0.0
    staffs_work_hours = get_items('SELECT personnel_code, name, work_hours * ?  FROM staff', (SALARY_PER_HOUR,))
    for staff in staffs_work_hours:
        sum_price += staff[2]
    return staffs_work_hours, sum_price

