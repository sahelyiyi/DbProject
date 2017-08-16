from anbardari.database_communication import *

SALARY_PER_HOUR = 10000

def add_goods_info(barcode, code, name, group_title, base_price, price, maintenance, production_date, entry_date, exit_date, producer):
    if check_exists('team', 'title', group_title):
        insert('goods', [barcode, code, name, group_title, base_price, price, maintenance, production_date, entry_date, exit_date, producer])
        return True
    else:
        return False


def add_exit_date(goods_barcode, exit_date):
    c.execute('UPDATE goods SET exit_date = ? WHERE barcode = ?', (exit_date, goods_barcode))


def get_salary(personal_code):
    query = 'SELECT work_hours FROM staff WHERE personal_code = %s' % personal_code
    items = get_items(query)
    if len(items):
        return items[0] * SALARY_PER_HOUR
    else:
        return -1
