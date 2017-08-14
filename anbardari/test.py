
from anbardari.database_communication import c

purchases = [
    ('yas', '1234'),
    ('sahel', '4321'),
]

c.executemany('INSERT INTO member VALUES (?,?)', purchases)

for row in c.execute('SELECT * FROM member ORDER BY name'):
        print row
