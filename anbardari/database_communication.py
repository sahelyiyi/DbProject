import json
import sqlite3

conn = sqlite3.connect('example.db')

c = conn.cursor()


def create_table(table_name, table_info):
    create_str = 'CREATE TABLE if not exists %s\n' % table_name
    attributes = []
    for attribute, attr_type in table_info:
        attributes.append(attribute + ' ' + attr_type)
    create_str += json.dumps(attributes)
    create_str = create_str.replace('"', '')
    create_str = create_str.replace('[', '(')
    create_str = create_str.replace(']', ')')
    c.execute(create_str)

