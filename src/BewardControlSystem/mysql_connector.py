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
    except Error as db_connection_error:
        print("Error", db_connection_error)
    return connection

try:
    conn = create_con_db(db_config["mysql"]["host"],
                         db_config["mysql"]["user"],
                         db_config["mysql"]["pass"])

    cursor = conn.cursor()
    create_db_sql = 'CREATE DATABASE {}'.format('1st_db')
    cursor.execute(create_db_sql)
    cursor.close()
    conn.close()
except:
    print('БД уже создано')



conn = create_con_db(db_config["mysql"]["host"],
                    db_config["mysql"]["user"],
                    db_config["mysql"]["pass"],
                    "1st_db")
try:
    cursor = conn.cursor()
    #delete_bwd = '''DROP TABLE address_list'''
    #cursor.execute(delete_bwd)
    create_address_list='''
    CREATE TABLE IF NOT EXISTS address_list(
    id INT AUTO_INCREMENT,
    address TEXT NOT NULL,
    entrance INT, 
    ip TEXT NOT NULL,
    login TEXT NOT NULL,
    password  TEXT NOT NULL,
    owner TEXT NOT NULL,
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
    #delete_company_list='''DROP TABLE company_list'''
    #cursor.execute(delete_company_list)
    create_company_list='''
    CREATE TABLE IF NOT EXISTS company_list(
    id INT AUTO_INCREMENT,
    company_name TEXT NOT NULL,
    PRIMARY KEY (id))'''
    cursor.execute(create_company_list)
    conn.commit()
except Error as error:
    print(error)
finally:
    cursor.close()
    conn.close()


def add_new_address(address,entrance, ip,login, password, owner):
    try:
        conn = create_con_db(db_config["mysql"]["host"],
                             db_config["mysql"]["user"],
                             db_config["mysql"]["pass"],
                             "1st_db")
        cursor = conn.cursor()
        add_new_entry=f'''
        INSERT INTO 
        address_list (address, entrance,ip,login, password, owner)
         VALUES
         ('{address}','{entrance}','{ip}','{login}','{password}','{owner}');
         '''
        cursor.execute(add_new_entry)
        conn.commit()
        add_result = 'Адреса добавлены успешно'
        print(add_result)
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

def edt_address(id,address,entrance,ip,login, password, owner):
    try:
        conn = create_con_db(db_config["mysql"]["host"],
                             db_config["mysql"]["user"],
                             db_config["mysql"]["pass"],
                             "1st_db")
        cursor = conn.cursor()
        edit = f'''
        UPDATE address_list SET address = '{address}',entrance ='{entrance}', ip='{ip}',login='{login}', password='{password}', owner='{owner}'
        WHERE id='{id}'
        '''
        cursor.execute(edit)
        conn.commit()

    except Error as error:
        print('Ошибка обновления',error)
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
# Select which vpn enable (vpn list for vpn label)
def select_vpn_name():
    try:
        conn = create_con_db(db_config["mysql"]["host"],
                             db_config["mysql"]["user"],
                             db_config["mysql"]["pass"],
                             "1st_db")
        cursor = conn.cursor()
        select_name=f'''
        SELECT name FROM vpn_list'''
        cursor.execute(select_name)
        result = cursor.fetchall()
        return result
    except Error as error:
        print('Ошибка выборки имени из списка VPN', error)
    finally:
        cursor.close()
        conn.close()

def selection_log_and_pass_by_name(vpn):
    try:
        conn = create_con_db(db_config["mysql"]["host"],
                             db_config["mysql"]["user"],
                             db_config["mysql"]["pass"],
                             "1st_db")
        cursor = conn.cursor()
        select_logpas = f'''
        SELECT login, password FROM vpn_list WHERE name='{vpn}' '''
        cursor.execute(select_logpas)
        result = cursor.fetchall()
        return result
    except Error as error:
        print('Ошибка выборки логина и пароля по названию vpn, ', error)
    finally:
        cursor.close()
        conn.close()

def remove_all_bwd():
    try:
        conn = create_con_db(db_config["mysql"]["host"],
                             db_config["mysql"]["user"],
                             db_config["mysql"]["pass"],
                             "1st_db")
        cursor = conn.cursor()
        delete_all_bwd = '''
        DELETE FROM address_list'''
        cursor.execute(delete_all_bwd)
        conn.commit()
    except Error as error:
        print('Ошибка удаления всех записей,', error)
    finally:
        cursor.close()
        conn.close()

def remove_all_vpn():
    try:
        conn = create_con_db(db_config["mysql"]["host"],
                             db_config["mysql"]["user"],
                             db_config["mysql"]["pass"],
                             "1st_db")
        cursor = conn.cursor()
        delete_all_vpn = '''
        DELETE FROM vpn_list'''
        cursor.execute(delete_all_vpn)
        conn.commit()
    except Error as error:
        print('Ошибка удаления всех VPN,', error)
    finally:
        cursor.close()
        conn.close()

def values_company_table():
    try:
        conn = create_con_db(db_config["mysql"]["host"],
                             db_config["mysql"]["user"],
                             db_config["mysql"]["pass"],
                             "1st_db")
        cursor = conn.cursor()
        show_companies = '''
        SELECT * FROM company_list'''
        cursor.execute(show_companies)
        table = cursor.fetchall()
        return table
    except Error as error:
        print('Ошибка выборки компаний из таблицы ',error)
    finally:
        cursor.close()
        conn.close()

def add_company_to_listbox(company_name):
    try:
        conn = create_con_db(db_config["mysql"]["host"],
                             db_config["mysql"]["user"],
                             db_config["mysql"]["pass"],
                             "1st_db")
        cursor = conn.cursor()
        add_new_company = f'''
        INSERT INTO 
        company_list (company_name)
        VALUES
        ('{company_name}');
         '''
        cursor.execute(add_new_company)
        conn.commit()
    except Error as error:
        print('Ошибка добавления организцаии', error)
    finally:
        cursor.close()
        conn.close()

def delete_company(company_name):
    try:
        conn = create_con_db(db_config["mysql"]["host"],
                             db_config["mysql"]["user"],
                             db_config["mysql"]["pass"],
                             "1st_db")
        cursor = conn.cursor()
        delete = f'''
        DELETE FROM 
        company_list WHERE company_name='{company_name}'
         '''
        cursor.execute(delete)
        conn.commit()
    except Error as error:
        print('Ошибка удаления организцаии', error)
    finally:
        cursor.close()
        conn.close()

def select_all_bwd_by_logpas(login, password):
    try:
        conn = create_con_db(db_config["mysql"]["host"],
                             db_config["mysql"]["user"],
                             db_config["mysql"]["pass"],
                             "1st_db")
        cursor = conn.cursor()
        select = f'''
        SELECT ip FROM 
        address_list WHERE login='{login}' and password = '{password}'
         '''
        cursor.execute(select)
        ip  = cursor.fetchall()
        return ip
    except Error as error:
        print('Ошибка выборки по логину и паролю', error)
    finally:
        cursor.close()
        conn.close()

def get_vpn_by_company(owner):
    try:
        conn = create_con_db(db_config["mysql"]["host"],
                             db_config["mysql"]["user"],
                             db_config["mysql"]["pass"],
                             "1st_db")
        cursor = conn.cursor()
        get_vpn = f'''
        SELECT name, login, password FROM vpn_list WHERE owner='{owner}' '''
        cursor.execute(get_vpn)
        result = cursor.fetchall()
        return result
    except Error as error:
        print('Ошибка выборки логина и пароля по организации, ', error)
    finally:
        cursor.close()
        conn.close()
