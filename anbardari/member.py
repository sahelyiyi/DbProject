from anbardari.database_communication import *


def order(code, good_code, member_code, dischargerer_personal_code, date):
    if check_exists('dischargerer', 'personnel_code', dischargerer_personal_code):
        insert('instruction', [code, good_code, member_code, dischargerer_personal_code, date])
        return True
    else:
        return False


def deliver(code, good_code, member_code, transferee_personal_code, date):#tahvil dadan
    if check_exists('transferee', 'personnel_code', transferee_personal_code):
        insert('transfer', [code, good_code, member_code, transferee_personal_code, date])
        return True
    else:
        return False


def take_delivery(code, good_code, member_code, transferer_personal_code, date, cost):#tahvil gereftan
    if check_exists('transferer', 'personnel_code', transferer_personal_code):
        insert('recieve', [code, good_code, member_code, transferer_personal_code, date, cost])
        return True
    else:
        return False


def edit_name(member_code, new_name):
    try:
        c.execute('UPDATE member SET name = ? WHERE code = ?', (new_name, member_code))
        conn.commit()
        return True
    except:
        return False


def get_goods(member_code):
    first_query = 'SELECT member_goods_code FROM member_basket Where member_code = %s' % member_code
    second_query = 'SELECT name FROM goods Where code = %s'
    return get_items_by_fk(first_query, second_query)


def calculate_keep_price(member_code):
    sum_price = 0.0
    first_query = 'SELECT member_goods_code FROM member_basket Where member_code = %s' % member_code
    second_query = 'SELECT base_price FROM goods Where code = %s'
    for price in get_items_by_fk(first_query, second_query):
        sum_price += price
    return sum_price
