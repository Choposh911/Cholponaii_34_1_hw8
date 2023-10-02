import sqlite3


def create_connection(db_name):
    conn = None
    try:
        conn = sqlite3.connect(db_name)
    except sqlite3.Error as e:
        print(e)
    return conn


def create_table(conn, sql):
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
    except sqlite3.Error as e:
        print(e)


def insert_countries(conn, countries):
    sql = '''INSERT INTO countries (title) VALUES (?)'''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (countries,))
        conn.commit()
    except sqlite3.Error as e:
        print(e)


def insert_cities(conn, city_name, country_id):
    sql = '''INSERT INTO cities (title, country_id) VALUES (?, ?)'''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (city_name, country_id))
        conn.commit()
    except sqlite3.Error as e:
        print(e)


def insert_employees(conn, first_name, last_name, city_id):
    sql = '''INSERT INTO employees (first_name, last_name, city_id) VALUES (?, ?, ?)'''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (first_name, last_name, city_id))
        conn.commit()
    except sqlite3.Error as e:
        print(e)


def select_all_countries(conn):
    sql = '''SELECT * FROM countries'''
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows_list = cursor.fetchall()
        for row in rows_list:
            print(row)
    except sqlite3.Error as e:
        print(e)


def select_all_cities(conn):
    sql = '''SELECT * FROM cities'''
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows_list = cursor.fetchall()
        for row in rows_list:
            print(row)
    except sqlite3.Error as e:
        print(e)


def select_all_employees(conn):
    sql = '''SELECT * FROM employees'''
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows_list = cursor.fetchall()
        for row in rows_list:
            print(row)
    except sqlite3.Error as e:
        print(e)


def display_cities(conn):
    sql = '''SELECT title FROM cities'''
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows_list = cursor.fetchall()
        for row in rows_list:
            print(row[0])  # Обратите внимание, что мы используем row[0] для получения только названия города
    except sqlite3.Error as e:
        print(e)


def display_employees_by_city(conn, city_id):
    sql = '''
    SELECT employees.first_name, employees.last_name, countries.title, cities.title, cities.area
    FROM employees
    JOIN cities ON employees.city_id = cities.id
    JOIN countries ON cities.country_id = countries.id
    WHERE cities.id = ?
    '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (city_id,))
        rows_list = cursor.fetchall()
        for row in rows_list:
            print(row)
    except sqlite3.Error as e:
        print(e)


sql_create_countries_table = '''
CREATE TABLE IF NOT EXISTS countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR NOT NULL
)
'''

sql_create_cities_table = '''
CREATE TABLE IF NOT EXISTS cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR NOT NULL,
    area FLOAT DEFAULT 0,
    country_id INTEGER REFERENCES countries(id)
)
'''

sql_create_employees_table = '''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    city_id INTEGER REFERENCES cities(id)
)
'''

connection = create_connection('hw8.db')

if connection is not None:
    create_table(connection, sql_create_countries_table)
    create_table(connection, sql_create_cities_table)
    create_table(connection, sql_create_employees_table)

    insert_countries(connection, 'China')
    insert_countries(connection, 'Germany')
    insert_countries(connection, 'Korea')

    insert_cities(connection, 'Shanghai', 1)  # Привяжем Shanghai к стране с id=1
    insert_cities(connection, 'Berlin', 2)  # Привяжем Berlin к стране с id=2
    insert_cities(connection, 'Seoul', 3)  # Привяжем Seoul к стране с id=3

    insert_employees(connection, 'Sui', 'Zhai', 1)  # Привяжем Sui к городу с id=1
    insert_employees(connection, 'Mark', 'Smith', 2)  # Привяжем Mark к городу с id=2
    insert_employees(connection, 'Li', 'Min Ho', 3)  # Привяжем Li к городу с id=3

    print(
        "Вы можете отобразить список сотрудников по выбранному id города из перечня городов ниже, для выхода из программы введите 0:")
    display_cities(connection)

    while True:
        try:
            city_id = input("Введите id выбранного города: ")
            if city_id == '0':
                break
            display_employees_by_city(connection, int(city_id))
        except ValueError:
            print("Введите целое число.")

    connection.close()
