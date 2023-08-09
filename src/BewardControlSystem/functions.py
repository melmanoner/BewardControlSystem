from mysql_connector import values_company_table
import os

# Update company combobox
def update_combobox_company_values():
    company_list = []
    for i in values_company_table():
        company_list.append(i[1])
    return company_list


def disable_vpn():
    os.system('start hidden_bat_dis.vbs')