import json
import sqlite3

conn = sqlite3.connect('example.db')

c = conn.cursor()


def convert_list_to_tuple_in_str(string):
    return string.replace('[', '(').replace(']', ')')


def _add_attrs(attrs_list):
    str = ''
    attributes = []
    for attribute, attr_type in attrs_list:
        attributes.append(attribute + ' ' + attr_type)
    str += json.dumps(attributes)
    str = str.replace('"', '')
    return str[1:-1]


def _add_fk(foreign_keys):
    str = ''
    for key1, key2 in foreign_keys:
        str += 'FOREIGN KEY(%s) REFERENCES %s' % (key1, key2)
    return str

def create_table(table_name, table_info):
    create_str = 'CREATE TABLE if not exists %s (\n' % table_name
    create_str += _add_attrs(table_info['attrs_list'])
    if 'foreign_keys' in table_info:
        create_str += (',\n' + _add_fk(table_info['foreign_keys']))
    create_str += '\n)'
    c.execute(create_str)


def get_items(query):
    items = []
    for item in c.execute(query):
        items.append(item[0])
    return items


def get_items_by_fk(first_query, second_query):
    first_items = []
    second_items = []
    for first_item in c.execute(first_query):
        first_items.append(first_item[0])
    for first_item in first_items:
        for item in c.execute(second_query % first_item):
            second_items.append(item[0])
    return second_items


def insert(table_name, data):
    insert_str = 'INSERT INTO %s VALUES %s' % (table_name, json.dumps(data))
    insert_str = convert_list_to_tuple_in_str(insert_str)
    c.execute(insert_str)


def check_exists(table_name, code_name, code):
    try:
        query = 'SELECT %s FROM %s Where %s = %s' % (code_name, table_name, code_name, code)
        if len(get_items(query)):
            return True
        else:
            return False
    except:
        return False