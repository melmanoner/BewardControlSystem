import mysql.connector
from mysql.connector import Error
from config import db_config

def create_con_db(db_host,user_name, user_password, db_name=None):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = db_host,
            user = user_name,
            passwd = user_password,
            database = db_name
        )
        print("Suc")
    except Error as db_connection_error:
        print("Error", db_connection_error)
    return connection

#conn = create_con_db(db_config["mysql"]["host"],
#                     db_config["mysql"]["user"],
#                     db_config["mysql"]["pass"])
#
#cursor = conn.cursor()
#create_db_sql = 'CREATE DATABASE {}'.format('1st_db')
#cursor.execute(create_db_sql)
#cursor.close()
#conn.close()



conn = create_con_db(db_config["mysql"]["host"],
                    db_config["mysql"]["user"],
                    db_config["mysql"]["pass"],
                    "1st_db")
try:
    cursor = conn.cursor()
    create_address_list='''
    CREATE TABLE IF NOT EXISTS address_list(
    id INT AUTO_INCREMENT,
    address TEXT NOT NULL,
    ip TEXT NOT NULL,
    owner INT NOT NULL,
    PRIMARY KEY (id))'''
    cursor.execute(create_address_list)
    create_vpn_list='''
    CREATE TABLE IF NOT EXISTS vpn_list(
    id INT AUTO_INCREMENT,
    owner TEXT NOT NULL,
    name TEXT NOT NULL,
    login TEXT NOT NULL,
    password TEXT NOT NULL,
    PRIMARY KEY (id))'''
    cursor.execute(create_vpn_list)
    conn.commit()
    print('Таблицы созданы')
except Error as error:
    print(error)
finally:
    cursor.close()
    conn.close()


def add_new_address(address, ip, owner):
    try:
        conn = create_con_db(db_config["mysql"]["host"],
                             db_config["mysql"]["user"],
                             db_config["mysql"]["pass"],
                             "1st_db")
        cursor = conn.cursor()
        add_new_entry=f'''
        INSERT INTO 
        address_list (address,ip, owner)
         VALUES
         ('{address}','{ip}','{owner}');
         '''
        cursor.execute(add_new_entry)
        conn.commit()
        add_result = 'Адреса добавлены успешно'
        return add_result
    except Error as error:
        print('Ошибка добавления',error)
        err_result = 'Ошибка добавления!'
        return err_result
    finally:
        cursor.close()
        conn.close()
def values_table():
    try:
        conn = create_con_db(db_config["mysql"]["host"],
                             db_config["mysql"]["user"],
                             db_config["mysql"]["pass"],
                             "1st_db")
        cursor = conn.cursor()
        show_tab = '''
        SELECT * FROM address_list'''
        cursor.execute(show_tab)
        table = cursor.fetchall()
        return table
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()

def values_vpn_table():
    try:
        conn = create_con_db(db_config["mysql"]["host"],
                             db_config["mysql"]["user"],
                             db_config["mysql"]["pass"],
                             "1st_db")
        cursor = conn.cursor()
        show_tab = '''
        SELECT * FROM vpn_list'''
        cursor.execute(show_tab)
        table = cursor.fetchall()
        return table
    except Error as error:
        print('Ошибка выборки из таблицы VPN',error)
    finally:
        cursor.close()
        conn.close()


def delete_select_address(id):
    try:
        conn = create_con_db(db_config["mysql"]["host"],
                             db_config["mysql"]["user"],
                             db_config["mysql"]["pass"],
                             "1st_db")
        cursor = conn.cursor()
        delete_select = f'''
        DELETE FROM address_list WHERE id={id}'''
        cursor.execute(delete_select)
        conn.commit()
    except Error as error:
        print('Ошибка удаления',error)
    finally:
        cursor.close()
        conn.close()

def delete_select_vpn(id):
    try:
        conn = create_con_db(db_config["mysql"]["host"],
                             db_config["mysql"]["user"],
                             db_config["mysql"]["pass"],
                             "1st_db")
        cursor = conn.cursor()
        delete_select_vpn = f'''
                DELETE FROM vpn_list WHERE id={id}'''
        cursor.execute(delete_select_vpn)
        conn.commit()
    except Error as error:
        print('Ошибка удаления VPN', error)
    finally:
        cursor.close()
        conn.close()

def edt_address(id,address,ip,owner):
    try:
        conn = create_con_db(db_config["mysql"]["host"],
                             db_config["mysql"]["user"],
                             db_config["mysql"]["pass"],
                             "1st_db")
        cursor = conn.cursor()
        edit = f'''
        UPDATE address_list SET address = '{address}', ip='{ip}', owner='{owner}'
        WHERE id={id}
        '''
        cursor.execute(edit)
        conn.commit()
    except Error as error:
        print('Ошибка обовления',error)
    finally:
        cursor.close()
        conn.close()

def edit_vpn(id, owner, name, login, password):
    try:
        conn = create_con_db(db_config["mysql"]["host"],
                             db_config["mysql"]["user"],
                             db_config["mysql"]["pass"],
                             "1st_db")
        cursor = conn.cursor()
        edit = f'''
        UPDATE vpn_list SET owner = '{owner}', name='{name}', login='{login}', password='{password}'
        WHERE id={id}
        '''
        cursor.execute(edit)
        conn.commit()
    except Error as error:
        print('Ошибка обовления',error)
    finally:
        cursor.close()
        conn.close()


def add_new_vpn(owner, name, login, password):
    try:
        conn = create_con_db(db_config["mysql"]["host"],
                             db_config["mysql"]["user"],
                             db_config["mysql"]["pass"],
                             "1st_db")
        cursor = conn.cursor()
        add_new_vpn=f'''
        INSERT INTO 
        vpn_list (owner, name, login, password)
         VALUES
         ('{owner}','{name}','{login}','{password}');
         '''
        cursor.execute(add_new_vpn)
        conn.commit()
    except Error as error:
        print('Ошибка добавления VPN',error)
    finally:
        cursor.close()
        conn.close()
