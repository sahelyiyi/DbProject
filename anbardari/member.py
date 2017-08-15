from anbardari.database_communication import c, get_items, get_items_by_fk


def order(member_code):
    pass


def deliver(member_code):
    pass


def take_delivery(member_code):
    pass


def edit_name(member_code, new_name):
    c.execute('UPDATE member SET name = ? WHERE code = ?', (new_name, member_code))

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
