import json
import unittest

from anbardari.database_communication import c
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


