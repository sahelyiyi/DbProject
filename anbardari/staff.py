from anbardari.database_communication import *

SALARY_PER_HOUR = 10000

def add_goods(barcode, code, name, group_title, base_price, price, maintenance, production_date, entry_date, exit_date, producer):
    if check_exists('team', 'title', group_title):
        insert('goods', [barcode, code, name, group_title, base_price, price, maintenance, production_date, entry_date, exit_date, producer])
        return True
    else:
        return False


def add_exit_date(goods_barcode, exit_date):
    try:
        c.execute('UPDATE goods SET exit_date = ? WHERE barcode = ?', (exit_date, goods_barcode))
        conn.commit()
        return True
    except:
        return False


def get_salary(personnel_code):
    salary = get_items('SELECT work_hours FROM staff WHERE personnel_code = ?', (personnel_code,))
    if len(salary):
        return salary[0] * SALARY_PER_HOUR
    else:
        return -1


def add_group(title, maintenance, base_price):
    insert('team', [title, maintenance, base_price])


def add_caring(personnel_code, goods_barcode):
    if check_exists('keeper', 'personnel_code', personnel_code) and check_exists('goods', 'barcode', goods_barcode):
        good_code = get_items('SELECT code FROM goods WHERE barcode = ?', (goods_barcode,))[0]
        insert('caring', [good_code, personnel_code])
        return True
    else:
        return False
