import datetime
import json
import unittest

from anbardari.member import *
from anbardari.mock import *

if __name__ == '__main__':
    unittest.main()


class MemberTest(unittest.TestCase):

    def test_get_goods(self):
        print 'get goods ' + json.dumps(get_goods(1))
        # correct_results = []
        # for row in c.execute('SELECT member_goods_code FROM member_basket Where member_code = %s' % member_code):
        #         for item in c.execute('SELECT name FROM goods Where code = %s' % row[0]):
        #             correct_results.append(item[0])
        # results = get_goods(member_code)
        # self.assertEqual(correct_results, results)

    def test_calculate_keep_price(self):
        print 'get price ' + str(calculate_keep_price(1))

    def test_edit_name(self):
        member_code = 1
        prev_name = get_items('SELECT name FROM member Where code = %s' % member_code)[0]
        edit_name(member_code, 'sahelyiy')
        new_name = get_items('SELECT name FROM member Where code = %s' % member_code)[0]
        print 'edit name from ' + prev_name + ' to ' + new_name

    def test_deliver(self):
        code = 1
        good_code = 1
        member_code = 1
        transferee_personnel_code = 1
        date = datetime.datetime.now().strftime('YYYY-MM-dd')
        if deliver(code, good_code, member_code, transferee_personnel_code , date):
            first_query = 'SELECT good_code FROM transfer Where code = %s' % member_code
            second_query = 'SELECT name FROM goods Where code = ?'
            goods = json.dumps(get_items_by_fk(first_query, second_query))
            member_name = get_items('SELECT name FROM member Where code = %s' % member_code)[0]
            print member_name + ' deliveries ' + goods
        else:
            print 'deliveries err: user does not exists.'

    def test_take_delivery(self):
        code = 1
        good_code = 2
        member_code = 1
        transferer_personnel_code = 1
        date = datetime.datetime.now().strftime('YYYY-MM-dd')
        cost = 10.5
        if take_delivery(code, good_code, member_code, transferer_personnel_code , date, cost):
            first_query = 'SELECT good_code FROM recieve Where code = %s' % member_code
            second_query = 'SELECT name FROM goods Where code = ?'
            goods = json.dumps(get_items_by_fk(first_query, second_query))
            member_name = get_items('SELECT name FROM member Where code = %s' % member_code)[0]
            print member_name + ' take deliveries ' + goods
        else:
            print 'take deliveries err: user does not exists.'

    def test_order(self):
        code = 1
        good_code = 2
        member_code = 1
        transferer_personnel_code = 1
        date = datetime.datetime.now().strftime('YYYY-MM-dd')
        cost = 10.5
        if take_delivery(code, good_code, member_code, transferer_personnel_code , date, cost):
            first_query = 'SELECT good_code FROM recieve Where code = %s' % member_code
            second_query = 'SELECT name FROM goods Where code = ?'
            goods = json.dumps(get_items_by_fk(first_query, second_query))
            member_name = get_items('SELECT name FROM member Where code = %s' % member_code)[0]
            print member_name + ' order ' + goods
        else:
            print 'order err: user does not exists.'
