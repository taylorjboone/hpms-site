import sqlite3

class Database():
    def __init__(self):
        conn = sqlite3.connect('pm/static/data/kortni_db.sqlite')
        self.cur = conn.cursor()

    def create_table(self, table_name, table_dict):
        cols = ''
        for column, dtype in table_dict.items():
            cols += f'{column} {dtype},'
        cols = cols[0:-1]
        statement = f'CREATE TABLE {table_name} ({cols})'
        self.cur.execute(statement)

    def add_record(self, table, values_list):
        values = ''
        for value in values_list:
            values += f'{value}'
        statement = f'''
            INSERT INTO {table} VALUES
                ({values})'''

        self.cur.execute(statement)

    def view_tables(self):
        res = self.cur.execute('SELECT name FROM sqlite_master')
        print(res.fetchall())

    def view_columns(self, table_name):
        self.cur.execute(f'select * from {table_name}')
        colnames = self.cur.description
        print(colnames)


table_dict = {
            'username': 'TEXT',
            'password': 'TEXT',
        }

stoop = Database()
# stoop.create_table('kortni_table')
stoop.view_columns('kortni_table')