import sqlite3
import csv

DB_NAME = 'db.sqlite'
DROP_TABLE_COMMAND = 'DROP TABLE %s'
CHECK_TABLE_COMMAND = 'SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'%s\';'
FETCH_ALL_RECORD_COMMAND = 'SELECT * FROM %s;'


def connect_db(db_file):
    return sqlite3.connect(db_file)


def execute_command(connection, sql_cmd):
    cursor = connection.cursor()
    cursor.execute(sql_cmd)
    connection.commit()


def table_exists(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(CHECK_TABLE_COMMAND % table_name)
    result = cursor.fetchone()
    if result is None:
        return False
    else:
        return True


def create_table(connection, table_name):
    create_table_cmd = 'CREATE TABLE %s (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT, price INTEGER, shop TEXT)' % table_name
    if not table_exists(connection, table_name):
        print('Table \'%s\' does not exists, creating...' % table_name)
        execute_command(connection, create_table_cmd)
        print('Table \'%s\' created.' % table_name)
    else:
        execute_command(connection, DROP_TABLE_COMMAND % table_name)
        print('Table \'%s\' already exists, initializing...' % table_name)
        execute_command(connection, create_table_cmd)
        print('Table \'%s\' created.' % table_name)


def insert_data(connection, table_name):
    insert_record_cmd = 'INSERT INTO %s (item, price, shop) VALUES ("嚕嚕抱枕", 999, "嚕嚕小朋友")' % table_name
    execute_command(connection, insert_record_cmd)


def update_data(connection, table_name):
    update_record_cmd = 'UPDATE %s SET shop = "udn買東西2" where shop="udn買東西"' % table_name
    execute_command(connection, update_record_cmd)


def insert_bulk_record(connection, table_name, input_file):
    with open(input_file, 'r', encoding='UTF-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            insert_record_cmd = 'INSERT INTO %s (item, price, shop) VALUES ("%s", "%s", "%s")' % (table_name, row['Item'], row['Price'], row['Store'])
            execute_command(connection, insert_record_cmd)


def fetch_all_record_from_db(connection, sql_cmd):
    cursor = connection.cursor()
    cursor.execute(sql_cmd)
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def main():
    connection = connect_db(DB_NAME)
    table_name = 'record'
    input_file = 'ezprice.csv'
    try:
        create_table(connection, table_name)
        insert_data(connection, table_name)
        insert_bulk_record(connection, table_name, input_file)
        update_data(connection, table_name)
        fetch_all_record_from_db(connection, FETCH_ALL_RECORD_COMMAND % table_name)
        connection.close()
    except Exception:
        print('Encounter some exceptions while executing DB tasks, close the connection...')
        connection.close()

if __name__ == '__main__':
    main()

