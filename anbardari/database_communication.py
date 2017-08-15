import json
import sqlite3

conn = sqlite3.connect('example.db')

c = conn.cursor()


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


def update_task(conn, task):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE tasks
              SET priority = ? ,
                  begin_date = ? ,
                  end_date = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)