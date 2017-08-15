import json

from anbardari.database_communication import c

mock_data = {
    'goods': [
        ('1', '1', 'shampoo', 'wash', '1.0', '2.0', 'null', 'null', 'null', 'null', 'golrang'),
        ('2', '2', 'saboon', 'wash', '3.0', '4.0', 'null', 'null', 'null', 'null', 'null')
    ],
    'member' : [
        ('sahel', '1'),
        ('yas', '2')
    ],
    'member_basket': [
        ('1', '1'),
        ('1', '2'),
        ('2', '1'),
    ]
}

for entity_name , values in mock_data.iteritems():
    tempplate = json.dumps(["?"] * len(values[0])).replace('"', '').replace('[', '(').replace(']', ')')
    c.executemany('INSERT INTO %s VALUES %s' % (entity_name, tempplate), values)

# for row in c.execute('SELECT member_goods_code FROM member_basket Where member_code = 1'):
#         for item in c.execute('SELECT name FROM goods Where code = %s' % row[0]):
#             print item[0]
