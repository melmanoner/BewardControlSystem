from mysql_connector import values_company_table,get_vpn_by_company
import os

# Update company combobox
def update_combobox_company_values():
    company_list = []
    for i in values_company_table():
        company_list.append(i[1])
    return company_list


def disable_vpn():
    os.system('start hidden_bat_dis.vbs')

class Vpn():
    def __init__(self, name, login, password,vpn_variable, get_vpn):
        self.name = name
        self.login = login
        self.password = password
        self.get_vpn = get_vpn
        self.vpn_variable = vpn_variable
        if vpn_variable == 1:
            create_bat_en = open('enable_vpn.bat', 'w')
            vpn_name = ''
            for obj in get_vpn:
                create_bat_en.write(f'@echo OFF\nrasdial {obj[0]} {obj[1]} {obj[2]}\nexit 1')
                vpn_name = obj[0]
            create_vbs_dis = open('hidden_bat_dis.vbs', 'w')
            create_vbs_dis.write(
                'Set WshShell = CreateObject("WScript.Shell")\nWshShell.Run chr(34) & "disable_vpn.bat" & Chr(34), 0\nSet WshShell = Nothing')
            create_bat_dis = open('disable_vpn.bat', 'w')
            create_bat_dis.write(f'@echo OFF\nrasdial {vpn_name} /DISCONNECT')
            os.system('start enable_vpn.bat')
        else:
            pass

