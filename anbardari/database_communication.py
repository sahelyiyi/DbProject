import json
import sqlite3

from anbardari import entities

conn = sqlite3.connect('example.db')

c = conn.cursor()

def create_table(table_name, table_info):
    create_str = 'CREATE TABLE %s\n' % table_name
    attributes = []
    for attribute, type in table_info:
        attributes.append(attribute + ' ' + type)
    create_str += json.dumps(attributes)
    create_str = create_str.replace('"', '')
    create_str = create_str.replace('[', '(')
    create_str = create_str.replace(']', ')')
    c.execute(create_str)



# c.execute('''CREATE TABLE stocks
#              (date text, trans text, symbol text, qty real, price real)''')
#
# purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
#              ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
#              ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
#             ]
# c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)
#
# for row in c.execute('SELECT * FROM stocks ORDER BY price'):
#         print row
