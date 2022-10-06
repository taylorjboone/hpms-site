import sqlite3

class Database():
    def __init__(self):
        # Connects to the sqlite database and instantiates a cursor
        self.conn = sqlite3.connect('pm/static/data/kortni_db.sqlite')
        self.cur = self.conn.cursor()

    # Creates a new table {table_name} in database
    # {table_dict} is a dictionary with new column names as keys and sqlite3 datatypes as values (all in strings)
    def create_table(self, table_name, table_dict):
        cols = ''
        for column, dtype in table_dict.items():
            cols += f'{column} {dtype},'
        cols = cols[0:-1]
        statement = f'CREATE TABLE IF NOT EXISTS {table_name} ({cols})'
        print(statement)
        self.cur.execute(statement)

    # Drops {table_name} from database
    def drop_table(self, table_name):
        statement = f'DROP TABLE {table_name}'
        self.cur.execute(statement)
        print(f'Dropped {table_name}')


    # Inserts new record into {table} from {values_dict}. values_dict is a dictionary with keys being column names and values being data
    def add_record(self, table, values_dict):
        columns,values = '',''
        for column in values_dict.keys():
            columns += f'{column},'
        for value in values_dict.values():
            values += f'\'{value}\','
        values = values[:-1]
        columns = columns[:-1]
        statement = f'INSERT INTO {table}({columns}) VALUES({values})'
        print(statement)
        self.cur.execute(statement)
        self.conn.commit()

    # View names of all tables in database
    def view_tables(self):
        res = self.cur.execute('SELECT name FROM sqlite_master')
        print(res.fetchall())

    # View names of all columns in {table_name}
    def view_columns(self, table_name):
        self.cur.execute(f'select * from {table_name}')
        colnames = self.cur.description
        print(colnames)

    #
    def query_table(self, table_name, columns):
        statement = f'SELECT {columns} FROM {table_name}'
        self.cur.execute(statement)
        rows = self.cur.fetchall()

        for row in rows:
            print(row)


table_dict = {
    'activityCode': 'TEXT',
    'activityDescription': 'TEXT',
    'unitsOfMeasurement': 'TEXT',
    'plannedDate': 'TEXT'
}

values_dict = {
    'activityCode': '381',
    'activityDescription': 'Bridge Structure Replacement',
    'unitsOfMeasurement': 'Employee Hours (EH)',
    'plannedDate': '2022-09-12'
}

stoop = Database()
# stoop.drop_table('kortni_table')
stoop.create_table('kortni_table', table_dict)
stoop.view_columns('kortni_table')
stoop.add_record('kortni_table', values_dict)
stoop.query_table('kortni_table', '*')