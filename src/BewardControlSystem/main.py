import tkinter as tk

from mysql_connector import add_new_address, \
    values_table,values_vpn_table, delete_select_address, delete_select_vpn,\
    edt_address, add_new_vpn, edit_vpn,select_vpn_name,selection_log_and_pass_by_name,\
    remove_all_bwd,remove_all_vpn,values_company_table,add_company_to_listbox,delete_company,select_all_bwd_by_logpas

from tkinter import *
from tkinter import ttk
import csv
from ttkthemes import ThemedStyle
import os
from tkinter import messagebox as mbox
from tkinter.messagebox import askyesno
import requests
from functions import update_combobox_company_values, disable_vpn
import re
from tkinter import filedialog as fd
import pandas as pd

class MainWindow(tk.Tk):
    def __init__(self,*args, **kwargs):
        self.main_window = tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Система управления бевардом")
        self.app()
    def app(self):
        # Sorry for my english, I usually write from my head, but sometimes I look into the translator. I try to get used.
        # Create main window
        #self.main_window = Tk()
        #main_window.geometry("900x600")

        self.style = ThemedStyle(self)
        self.style.set_theme("arc")
        self.style.configure("Treeview",
                        background='#FFF',
                        foreground='black',
                        rowheight=25,
                        fieldbackground='#FFF')

        self.style.map("Treeview",
                  background=[('selected','#347083')])







        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill=BOTH)


        self.bwd_frame = ttk.Frame(self.notebook)
        self.vpn_frame = ttk.Frame(self.notebook)



        self.bwd_frame.pack(fill=BOTH, expand=True)
        self.vpn_frame.pack(fill=BOTH, expand=True)



        self.notebook.add(self.bwd_frame, text='Бевард')
        self.notebook.add(self.vpn_frame, text='VPN')

# Filter panel
        def filterTreeView(*args):
            ItemsOnTreeView = self.tree.get_children()
            search = self.search_ent_var.get().capitalize()
            for eachItem in ItemsOnTreeView:
                if search in self.tree.item(eachItem)['values'][1]:
                    self.search_ent_var = self.tree.item(eachItem)['values']
                    self.tree.delete(eachItem)

                    self.tree.insert("", 0, values=self.search_ent_var)

        self.search_ent_var = StringVar()
        self.search_entry = Entry(self.bwd_frame, width=150, textvariable=self.search_ent_var)
        self.search_entry.pack(pady=10)
        #self.search_entry.insert(0,'Поиск')
        self.search_ent_var.trace('w', filterTreeView)





        # Create a bwd frame

        self.tree_frame = Frame(self.bwd_frame)
        self.tree_frame.pack(pady=10)


        # Create a Treeview Scrollbar

        self.tree_scroll = ttk.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=RIGHT,fill=Y)



        self.tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set,
                            selectmode="extended",
                            columns=('ID','address','entrance','ip','login','password','owner'),
                            height=10, show='headings')

        self.tree.column("ID", width=30 ,anchor=CENTER)
        self.tree.column('address', width=250, anchor=CENTER)
        self.tree.column('entrance', width=250, anchor=CENTER)
        self.tree.column('ip', width=250, anchor=CENTER)
        self.tree.column('login', width=250, anchor=CENTER)
        self.tree.column('password', width=0, stretch=NO)
        self.tree.column('owner', width=250, anchor=CENTER)

        self.tree.heading("ID", text='ID')
        self.tree.heading("address", text="Адрес")
        self.tree.heading("entrance", text="Подъезд")
        self.tree.heading("ip", text='ip')
        self.tree.heading("login", text='Логин')
        self.tree.heading("password", text='')
        self.tree.heading("owner", text='Обслуживающая организация')

        # Create view for table
        def view_table():
            [self.tree.delete(i) for i in self.tree.get_children()]
            for row in values_table():
                self.tree.insert('','end',values=row)
        # Call view_table func
        view_table()

        self.tree.yview()
        self.tree.pack(side=TOP, fill=X)
        #self.tree['yscrollcommand'] = self.tree_scroll.set

        # Create Striped Row Tags (doesnt work, idk why)
        self.tree.tag_configure('oddrow', background='yellow')
        self.tree.tag_configure('evenrow', background='blue')

        # Add Record Entry Boxes

        self.data_frame = LabelFrame(self.bwd_frame, text="Таблица")
        self.data_frame.pack(fill="x", padx=20)

        entris = []
        def clear_entris():
            for entry in entris:
                entry.delete(0, END)
        self.id_entry = Entry(self.data_frame)
        self.id_entry.grid_remove()
        entris.append(self.id_entry)
        self.id = self.id_entry.get()

        self.address_label = Label(self.data_frame, text="Адрес")
        self.address_label.grid(row=0, column=0, padx=10, pady=10)
        self.address_entry = Entry(self.data_frame)
        self.address_entry.grid(row=0, column=1, padx=10, pady=10)
        entris.append(self.address_entry)
        self.address = self.address_entry.get()

        self.ip_label = Label(self.data_frame, text="IP")
        self.ip_label.grid(row=0, column=2, padx=10, pady=10)
        self.ip_entry = Entry(self.data_frame)
        self.ip_entry.grid(row=0, column=3, padx=10, pady=10)
        entris.append(self.ip_entry)
        self.ip = self.ip_entry.get()


        self.login_bwd_label = Label(self.data_frame, text='Логин')
        self.login_bwd_label.grid(row=1, column=0, padx=10, pady=10)
        self.login_bwd_entry = Entry(self.data_frame)
        self.login_bwd_entry.grid(row=1, column=1, padx=10, pady=10)
        entris.append(self.login_bwd_entry)
        self.login = self.login_bwd_entry.get()


        self.password_bwd_label = Label(self.data_frame, text='Пароль')
        self.password_bwd_label.grid(row=1, column=2, padx=10, pady=10)
        self.password_bwd_entry = Entry(self.data_frame, show='*')
        self.password_bwd_entry.grid(row=1, column=3, padx=10, pady=10)
        entris.append(self.password_bwd_entry)
        self.password = self.password_bwd_entry.get()

        self.entrance_label = Label(self.data_frame, text='Подъезд')
        self.entrance_label.grid(row=0, column=4, padx=10,pady=10)
        self.entrance_entry = Entry(self.data_frame)
        self.entrance_entry.grid(row=0, column=5, pady=10, padx=10)
        entris.append(self.entrance_entry)
        self.entrance = self.entrance_entry.get()

        # there was
        # Update company combobox
        #         def update_combobox_company_values():
        #             company_list = []
        #             for i in values_company_table():
        #                 company_list.append(i[1])
        #             return company_list

        lists_for_combobox = update_combobox_company_values()

        self.owner_label = Label(self.data_frame, text="Обслуживающая организация")
        self.owner_label.grid(row=1, column=4, padx=10, pady=10)
        self.owner_entry = ttk.Combobox(self.data_frame, values=lists_for_combobox, state="readonly")
        self.owner_entry.grid(row=1, column=5, padx=10, pady=10)
        entris.append(self.owner_entry)
        self.owner = self.owner_entry.get()

        #####################

        plus_btn = Button(self.data_frame, text='Добавить обслуживающую\nорганизацию', cursor='hand2', command=ChildAddCompany)
        plus_btn.grid(row=1, column=6, padx=10,pady=10)
########################################################################

        # Add Buttons for control sql
        button_frame = LabelFrame(self.bwd_frame, text="Управление списком адресов")
        button_frame.pack(fill=X, padx=20)

        def add_bwd():
            add_new_address(self.address,self.entrance, self.ip, self.login, self.password, self.owner)
            clear_entris()
            view_table()
        add_button = Button(button_frame, text="Добавить",cursor = 'hand2', command=add_bwd)
        add_button.grid(row=0, column=0, padx=10, pady=10)

        # Edit button
        def edit_address():
            edt_address(self.id, self.address,self.entrance,self.ip,self.login,self.password,self.owner)
            view_table()


        edit_button = Button(button_frame, text="Изменить", command=edit_address,cursor = 'hand2')
        edit_button.grid(row=0, column=1, padx=10, pady=10)

        def remove_command():
            delete_select_address(self.id)
            view_table()
        remove_button = Button(button_frame, text="Удалить выбранный", command=remove_command,cursor = 'hand2')
        remove_button.grid(row=0, column=2, padx=10, pady=10)

        def remove_all_warning():
            result = askyesno(title='Подтверждение операции', message='Вы действительно хотите удалить ВСЕ записи?')
            if result:
                remove_all_bwd()
                view_table()


        remove_all_button = Button(button_frame, text="Удалить все",cursor = 'hand2', command=remove_all_warning)
        remove_all_button.grid(row=0, column=3, padx=10, pady=10)

        def callback():
            xlsx = fd.askopenfilename()
            df_address_list = pd.read_excel(f'''{xlsx}''')
            base_list=[]
            id_xlsx = df_address_list['ID'].tolist()
            address_xlsx = df_address_list['Адрес'].tolist()
            entrance_xlsx = df_address_list['Подъезд'].tolist()
            ip_xlsx = df_address_list['ip'].tolist()
            login_xlsx = df_address_list['Логин'].tolist()
            password_xlsx = df_address_list['Пароль'].tolist()
            company_xlsx = df_address_list['Компания'].tolist()
            base_list.append(id_xlsx)
            base_list.append(address_xlsx)
            base_list.append(entrance_xlsx)
            base_list.append(ip_xlsx)
            base_list.append(login_xlsx)
            base_list.append(password_xlsx)
            base_list.append(company_xlsx)
            x = 0
            for i in id_xlsx:
                x += 1
                value_for_db = []
                if x == id_xlsx[-1]:
                    break
                for elem in base_list:
                    value_for_db.append(elem[x])
                address_xlsx = value_for_db[1]
                entrance_xlsx = value_for_db[2]
                ip_xlsx = value_for_db[3]
                login_xlsx = value_for_db[4]
                password_xlsx = value_for_db[5]
                company_xlsx = value_for_db[6]
                add_new_address(address_xlsx, entrance_xlsx, ip_xlsx, login_xlsx, password_xlsx, company_xlsx)

            view_table()





        add_bwd_from_xlsx = Button(button_frame,text='Импорт из Excel',command=callback)
        add_bwd_from_xlsx.grid(row=0, column=4, padx=10, pady=10)



        #Add Buttons for control panel
        button_control_bwd_frame = LabelFrame(self.bwd_frame, text="Управление панелью")
        button_control_bwd_frame.pack(fill=X, padx=20)

        # Create radiobutton for vpn connection------------------------------------------------------------#

        vpn_list = []
        vpn_name = select_vpn_name()
        for obj in vpn_name:
            vpn_list.append(obj[0])
        state_vpn = StringVar()
        i=0
        def select_vpn():
            for vpn in vpn_list:
                if state_vpn.get() == f'{vpn}':
                    # Create vbs files for hidde execution bat

                    # VBS doesnt work anymore, idk why, fix it late :)
                    #create_vbs_en = open('hidden_bat_en.vbs', 'w')
                    #create_vbs_en.write('Set WshShell = CreateObject("WScript.Shell")\nWshShell.Run chr(34) & "enable_vpn.bat" & Chr(34), 0\nSet WshShell = Nothing')

                    create_bat_en = open('enable_vpn.bat', 'w')
                    for obj in selection_log_and_pass_by_name(vpn):
                        create_bat_en.write(f'@echo OFF\nrasdial {vpn} {obj[0]} {obj[1]}\nexit 1')
                    create_vbs_dis = open('hidden_bat_dis.vbs', 'w')
                    create_vbs_dis.write('Set WshShell = CreateObject("WScript.Shell")\nWshShell.Run chr(34) & "disable_vpn.bat" & Chr(34), 0\nSet WshShell = Nothing')
                    create_bat_dis = open('disable_vpn.bat', 'w')
                    create_bat_dis.write(f'@echo OFF\nrasdial {vpn} /DISCONNECT')
                    os.system('start enable_vpn.bat')



        bottom_frame = LabelFrame(self.bwd_frame)
        bottom_frame.pack()

        # Label for vpn controller
        vpn_controller_frame = LabelFrame(bottom_frame, text="VPN")
        vpn_controller_frame.pack(fill="y", padx=20, side=LEFT)
        disable_vpn_radiobutton = ttk.Radiobutton(vpn_controller_frame, text='Отключить',variable=state_vpn, value='off', command=disable_vpn)
        disable_vpn_radiobutton.grid(row=0, column=0)

        def show_vpn():
            i=1
            vpn_list = []
            vpn_name = select_vpn_name()
            for obj in vpn_name:
                vpn_list.append(obj[0])
            for vpn in vpn_list:
                vpn = ttk.Radiobutton(vpn_controller_frame, text=vpn, variable=state_vpn, value=vpn, command=select_vpn)
                vpn.grid(row=i, column=0, padx=10, pady=10)
                i+=1
        show_vpn()

        # Label for bwd controller
        bwd_controller_frame = LabelFrame(bottom_frame, text='Контроллер')
        bwd_controller_frame.pack(fill='x', padx=20, side=RIGHT)

        def open_door():
            try:
                r = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/intercom_cgi?action=maindoor''')
                if r.status_code == 200:
                    mbox.showinfo('Успешно', 'Дверь открыта')
                else:
                    mbox.showinfo('Что-то пошло не так', 'Ошибка открытия двери')
            except Exception:
                mbox.showwarning('Ошибка', 'Проверьте выбран ли адрес и включён ли VPN')

        open_door = Button(bwd_controller_frame, text='Открыть дверь',cursor = 'hand2', command=open_door)
        open_door.grid(row=0, column=0, padx=10, pady=10)

        enabled = IntVar()

        def autocollectkeys():
            try:
                if enabled.get() == 1:
                    r = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/mifare_cgi?action=set&AutoCollectKeys=on''')
                    print('Автозапись включена')
                    if r.status_code == 200:
                        mbox.showinfo('Успешно','Автозапись включена')
                    else:
                        mbox.showwarning('Ошибка','Ошбика включения автозаписи')
                elif enabled.get() == 0:
                    r = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/mifare_cgi?action=set&AutoCollectKeys=off''')
                    if r.status_code == 200:
                        mbox.showinfo('Успешно','Автозапись отключена')
                    else:
                        mbox.showwarning('Ошибка','Ошбика отключения автозаписи')
            except Exception:
                mbox.showwarning('Ошибка', 'Проверьте выбран ли адрес и включён ли VPN')

        autorecord = Checkbutton(bwd_controller_frame, text='Включить автозапись', cursor='hand2',variable=enabled, command=autocollectkeys)
        autorecord.grid(row=0, column=1,padx=10, pady=10)

        key_label = Label(bwd_controller_frame, text='Ключ/Индекс/Код')
        key_label.grid(row=0, column=2,padx=10, pady=10)

        add_key_entry = Entry(bwd_controller_frame)
        add_key_entry.grid(row=0, column=3, padx=10, pady=10)
        key_value = add_key_entry.get()

        #mifare_cgi?action=add&Key=806F858A0F6605

        def add_key():
            try:
                mifare = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/mifare_cgi?action=add&Key={key_value}''')
                rfid = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/rfid_cgi?action=add&Key={key_value}''')
                if mifare.status_code or rfid.status_code == 200:
                    add_key_entry.delete(0, END)
                    mbox.showinfo('Успешно', 'Ключ добавлен')
                else:
                    mbox.showwarning('Ошибка', 'Ключ не добавлен')
            except Exception:
                mbox.showwarning('Ошибка', 'Проверьте выбран ли адрес и подключен ли VPN')

        add_key_btn = Button(bwd_controller_frame, text='Добавить ключ', cursor='hand2', command=add_key)
        add_key_btn.grid(row=0, column=4, padx=10, pady=10)

        def add_key_to_all_bwd():
            try:
                ip_list = select_all_bwd_by_logpas(self.login, self.password)
                i=0
                for ip in ip_list:
                    add_key_rfid = requests.get(f'''http://{self.login}:{self.password}@{ip[0]}/cgi-bin/rfid_cgi?action=add&Key={key_value}''')
                    add_key_mifare = requests.get(f'''http://{self.login}:{self.password}@{ip[0]}/cgi-bin/mifare_cgi?action=add&Key={key_value}''')
                    if add_key_rfid.status_code or add_key_mifare.status_code == 200:
                        i+=1
                mbox.showinfo('Успешно',f'''Ключ добавлен в {i} панель(и/ей)''')
            except Exception:
                mbox.showwarning('Ошибка', 'Проверьте выбран ли адрес и подключен ли VPN')


        add_key_to_all_bwd_btn = Button(bwd_controller_frame, text='Добавить во все панели', cursor='hand2', command=add_key_to_all_bwd)
        add_key_to_all_bwd_btn.grid(row=1, column=4, pady=10,padx=10)

        def add_code_for_scan():
            try:
                code_value = add_key_entry.get()
                add_code_mf = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/mifare_cgi?action=set&ScanCode={code_value}&ScanCodeActive=on''')
                add_code_rf = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/rfid_cgi?action=set&RegCode={code_value}&ScanCodeActive=on''')
                if add_code_mf.status_code or add_code_rf.status_code == 200:
                    mbox.showinfo('Успешно', 'Код для записи ключей успешно установлен')
                else:
                    mbox.showwarning('Ошибка', 'Что-то пошло не так. Код не установлен')
            except Exception:
                mbox.showwarning('Ошибка', 'Проверьте выбран ли адрес и подключен ли VPN')

        add_scan_code = Button(bwd_controller_frame, text='Установить код сканирования RFID', cursor='hand2', command=add_code_for_scan)
        add_scan_code.grid(row=1, column=2, pady=10,padx=10)

        def disable_scan_code():
            try:
                disable_code = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/mifare_cgi?action=set&ScanCodeActive=off''')
                if disable_code.status_code == 200:
                    mbox.showinfo('Успешно', 'Код отключен')
                else:
                    mbox.showwarning('Ошибка', 'Ошибка отключения кода')
            except Exception:
                mbox.showwarning('Ошибка', 'Проверьте выбран ли адрес и подключен ли VPN', cursor='hand2', command=disable_scan_code)
        scan_code_off_btn = Button(bwd_controller_frame, text='Отключить код сканирования')
        scan_code_off_btn.grid(row=1, column=3, pady=10, padx=10)


        def delete_key():
            try:
                mifare = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/mifare_cgi?action=delete&Key={key_value}''')
                rfid = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/rfid_cgi?action=delete&Key={key_value}''')
                if mifare.status_code or rfid.status_code == 200:
                    add_key_entry.delete(0, END)
                    mbox.showinfo('Успешно', 'Ключ удален')
                else:
                    mbox.showwarning('Ошибка', 'Ошибка удаления')
            except Exception:
                mbox.showwarning('Ошибка', 'Проверьте выбран ли адрес и подключен ли VPN')

        delete_key_button = Button(bwd_controller_frame, text='Удалить', cursor='hand2', command=delete_key)
        delete_key_button.grid(row=0, column=5, padx=10,pady=10)

        def delete_key_in_all_bwd():
            try:
                ip_list = select_all_bwd_by_logpas(self.login, self.password)
                i=0
                for ip in ip_list:
                    delete_key_rfid = requests.get(f'''http://{self.login}:{self.password}@{ip[0]}/cgi-bin/rfid_cgi?action=delete&Key={key_value}''')
                    delete_key_mifare = requests.get(f'''http://{self.login}:{self.password}@{ip[0]}/cgi-bin/mifare_cgi?action=delete&Key={key_value}''')
                    if delete_key_mifare.status_code or delete_key_rfid.status_code == 200:
                        i+=1
                mbox.showinfo('Успешно',f'''Ключ удален в {i} панель''')
            except Exception:
                mbox.showwarning('Ошибка', 'Проверьте выбран ли адрес и подключен ли VPN')


        add_key_to_all_bwd_btn = Button(bwd_controller_frame, text='Удалить со всех панелей', cursor='hand2', command=delete_key_in_all_bwd)
        add_key_to_all_bwd_btn.grid(row=1, column=5, pady=10,padx=10)


        # Create func for show all keys in bwd

        def show_all_mifare_keys():
            try:
                r = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/mifare_cgi?action=list''')


                show_keys_window = Tk()

                all_information = r.text

                mf_tree_frame = ttk.Frame(show_keys_window)
                mf_tree_frame.pack(fill=BOTH, expand=True)
                tree_scroll = Scrollbar(mf_tree_frame)
                tree_scroll.pack(side=RIGHT, fill=Y)
                tree_mf = ttk.Treeview(mf_tree_frame, yscrollcommand=tree_scroll.set,
                                       selectmode="extended",
                                       columns=('ID', 'key_value'),
                                       height=10, show='headings')

                tree_mf.heading('ID', text='ID')
                tree_mf.heading('key_value', text='Код ключа')

                tree_mf.column('ID', width=50, anchor=CENTER)
                tree_mf.column('key_value', width=250, anchor=CENTER)

                tree_mf.yview()
                tree_mf.pack(side=TOP, fill=X)
                i=1
                while True:
                    find_key_word = all_information.find('Key')
                    if find_key_word == -1:
                        break
                    all_information = all_information[find_key_word:]
                    first_key = all_information.find('=')
                    if first_key == -1:
                        break
                    start = first_key + 1
                    end = first_key + 15
                    key = all_information[start:end]
                    all_information = all_information[end+1:]
                    i += 1
                    values_mf = [i, key]
                    tree_mf.insert('', 'end', values=values_mf)
            except Exception:
                mbox.showwarning('Ошибка', 'Проверьте выбран ли адрес и включён ли VPN')




        show_all_mifare_keys_btn = Button(bwd_controller_frame, text='Показать список\nMIFARE ключей', cursor='hand2', command=show_all_mifare_keys)
        show_all_mifare_keys_btn.grid(row=1, column=0, padx=10, pady=10)

        def show_all_rfid_keys():
            try:
                r = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/rfid_cgi?action=list''')
                show_rfid_window = Tk()

                all_information = r.text


                mf_tree_frame = ttk.Frame(show_rfid_window)
                mf_tree_frame.pack(fill=BOTH, expand=True)
                tree_scroll = Scrollbar(mf_tree_frame)
                tree_scroll.pack(side=RIGHT, fill=Y)
                tree_mf = ttk.Treeview(mf_tree_frame, yscrollcommand=tree_scroll.set,
                                       selectmode="extended",
                                       columns=('ID', 'key_value'),
                                       height=10, show='headings')

                tree_mf.heading('ID', text='ID')
                tree_mf.heading('key_value', text='Код ключа')

                tree_mf.column('ID', width=50, anchor=CENTER)
                tree_mf.column('key_value', width=250, anchor=CENTER)

                tree_mf.yview()
                tree_mf.pack(side=TOP, fill=X)
                i = 1

                while True:
                    find_key_word = all_information.find('KeyValue')
                    if find_key_word == -1:
                        break
                    all_information = all_information[find_key_word:]
                    first_key = all_information.find('=')
                    if first_key == -1:
                        break
                    start = first_key + 1
                    end = first_key + 15
                    key = all_information[start:end]
                    all_information = all_information[end + 1:]
                    i += 1
                    values_mf = [i, key]
                    tree_mf.insert('', 'end', values=values_mf)
            except Exception:
                mbox.showwarning('Ошибка', 'Проверьте выбран ли адрес и включён ли VPN')

        show_all_rfid_keys_btn = Button(bwd_controller_frame, text='Показать список\nRFID ключей', cursor='hand2', command=show_all_rfid_keys)
        show_all_rfid_keys_btn.grid(row=1, column=1, padx=10, pady=10)

        #--------------------------------------------------------------------------------------------------#
        ####################################################################################################
        # Double click selection---------------------------------------------------------------------------#
        def select_record(event):
            # Clear entry boxes
            clear_entris()
            # Grab record Number
            selected = self.tree.focus()
            # Grab record values
            values = self.tree.item(selected, 'values')
            # outpts to entry boxes
            i=0
            for entry in entris:
                entry.insert(0, values[i])
                i=i+1

        self.tree.bind('<Double-Button-1>', select_record)
        #--------------------------------------------------------------------------------------------------#


        # Create frame for vpn

        vpn_list_frame = Frame(self.vpn_frame)
        vpn_list_frame.pack(pady=10)
        tree_vpn_scroll = Scrollbar(vpn_list_frame)
        tree_vpn_scroll.pack(side=RIGHT, fill=Y)
        tree_vpn = ttk.Treeview(vpn_list_frame, yscrollcommand = tree_vpn_scroll,
                                selectmode='extended',
                                columns=('ID','owner','name','login','password'),
                                height=10, show='headings')
        tree_vpn.column('ID', width=30, anchor=CENTER)
        tree_vpn.column('owner', width=250, anchor=CENTER)
        tree_vpn.column('name',width=250, anchor=CENTER)
        tree_vpn.column('login', width=250,anchor=CENTER)
        tree_vpn.column('password',width=0, stretch=NO)
        tree_vpn.heading('ID', text='ID')
        tree_vpn.heading('owner', text='Владелец')
        tree_vpn.heading('name', text='Название сети')
        tree_vpn.heading('login', text='Логин')
        tree_vpn.heading('password', text='Пароль')
        def view_vpn_table():
            [tree_vpn.delete(i) for i in tree_vpn.get_children()]
            for row in values_vpn_table():
                tree_vpn.insert('','end', values=row)
        view_vpn_table()
        self.vpn_label_frame = LabelFrame(self.vpn_frame, text='VPN')
        self.vpn_label_frame.pack(fill="x", padx=20)
        entris_vpn = []
        self.id_vpn_entry = Entry(self.vpn_label_frame)
        self.id_vpn_entry.grid_remove()
        entris_vpn.append(self.id_vpn_entry)
        self.id_vpn = self.id_vpn_entry.get()

        self.owner_vpn_label = Label(self.vpn_label_frame, text="Владелец")
        self.owner_vpn_label.grid(row=0, column=0, padx=10, pady=10)
        self.owner_vpn_entry = ttk.Combobox(self.vpn_label_frame, values=lists_for_combobox,state="readonly")
        self.owner_vpn_entry.grid(row=0, column=1, padx=10, pady=10)
        entris_vpn.append(self.owner_vpn_entry)
        self.owner_vpn = self.owner_vpn_entry.get()

        self.name_vpn_label = Label(self.vpn_label_frame, text="Название сети")
        self.name_vpn_label.grid(row=0, column=2, padx=10, pady=10)
        self.name_vpn_entry = Entry(self.vpn_label_frame)
        self.name_vpn_entry.grid(row=0, column=3, padx=10, pady=10)
        entris_vpn.append(self.name_vpn_entry)
        self.name_vpn = self.name_vpn_entry.get()

        self.login_vpn_label = Label(self.vpn_label_frame, text="Логин")
        self.login_vpn_label.grid(row=0, column=4, padx=10, pady=10)
        self.login_vpn_entry = Entry(self.vpn_label_frame)
        self.login_vpn_entry.grid(row=0, column=5, padx=10, pady=10)
        entris_vpn.append(self.login_vpn_entry)
        self.login_vpn = self.login_vpn_entry.get()

        self.password_vpn_label = Label(self.vpn_label_frame, text="Пароль")
        self.password_vpn_label.grid(row=0, column=6, padx=10, pady=10)
        self.password_vpn_entry = Entry(self.vpn_label_frame, show='*')
        self.password_vpn_entry.grid(row=0, column=7, padx=10, pady=10)
        entris_vpn.append(self.password_vpn_entry)
        self.password_vpn = self.password_vpn_entry.get()

        self.control_vpn_frame = LabelFrame(self.vpn_frame, text='Управление списком VPN')
        self.control_vpn_frame.pack(fill=X, padx=20)
        # Create add vpn func
        def add_vpn():
            add_new_vpn(self.owner_vpn, self.name_vpn, self.login_vpn, self.password_vpn)
            for entry in entris_vpn:
                entry.delete(0, 'end')
            view_vpn_table()
            show_vpn()
        # Add button
        add_vpn_button = Button(self.control_vpn_frame, text="Добавить", cursor='hand2', command=add_vpn)
        add_vpn_button.grid(row=0, column=0, padx=10, pady=10)
        # Button for edit vpn
        def edit_select_vpn():
            edit_vpn(self.id_vpn, self.owner_entry, self.name_vpn, self.login_vpn, self.password_vpn)
            view_vpn_table()
            show_vpn()
        edit_vpn_button = Button(self.control_vpn_frame, text='Изменить', command=edit_select_vpn)
        edit_vpn_button.grid(row=0, column=1, padx=10, pady=10)
        # Button for delete vpn
        def delete_sel_vpn():
            delete_select_vpn(self.id_vpn)
            view_vpn_table()
            show_vpn()
        self.delete_vpn_button = Button(self.control_vpn_frame, text="Удалить", cursor='hand2', command=delete_sel_vpn)
        self.delete_vpn_button.grid(row=0, column=2, padx=10, pady=10)

        def delete_all_vpn():
            result = askyesno(title='Подтверждение операции', message='Вы действительно хотите удалить ВСЕ записи в списке VPN?')
            if result:
                remove_all_vpn()
                view_vpn_table()
                show_vpn()
        self.delete_all_vpn_btn = Button(self.control_vpn_frame, text='Удалить все VPN', cursor='hand2', command=delete_all_vpn)
        self.delete_all_vpn_btn.grid(row=0, column=3, padx=10, pady=10)
        # Select Record
        def select_record(event):
            # Clear entry boxes
            for entry in entris_vpn:
                entry.delete(0, END)
            # Grab record Number
            selected = tree_vpn.focus()
            # Grab record values
            values = tree_vpn.item(selected, 'values')
            # outpts to entry boxes
            i = 0
            for entry in entris_vpn:
                entry.insert(0, values[i])
                i = i + 1
        tree_vpn.bind('<Double-Button-1>', select_record)


        tree_vpn.yview()
        tree_vpn.pack(side=TOP, fill=X)

class ChildAddCompany(tk.Tk):
    def __init__(self, *args, **kwargs):
        self.child_window = tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Система управления бевардом")
        self.child_for_add_company_to_list()

    def child_for_add_company_to_list(self):
        self.style = ThemedStyle(self)
        self.style.set_theme("arc")
        self.company_entry = ttk.Entry(self)
        self.company_entry.grid(column=0, row=0, padx=6, pady=6, sticky=EW)

        def add_company():
            company_name = self.company_entry.get()
            add_company_to_listbox(company_name)
            view_list_company()
            new_combobox_company = update_combobox_company_values()
            main_app.owner_entry['values'] = main_app.owner_vpn_entry['values'] = new_combobox_company

        self.add_btn = ttk.Button(self, text="Добавить", command=add_company)
        self.add_btn.grid(row=0, column=1, padx=6, pady=6)
        self.company_tree = ttk.Treeview(self,
                                    selectmode="extended", columns=('id', 'company'), height=10, show='headings')
        self.company_tree.grid(row=1, column=0)
        self.company_tree.column('id', width=30, anchor=CENTER)
        self.company_tree.column('company', width=250, anchor=CENTER)
        self.company_tree.heading('id', text='ID')
        self.company_tree.heading('company', text='Организации')

        def view_list_company():
            [self.company_tree.delete(i) for i in self.company_tree.get_children()]
            for row in values_company_table():
                self.company_tree.insert('', 'end', values=row)

        view_list_company()

        def delete_select_company():
            selected = self.company_tree.focus()
            company_name = self.company_tree.item(selected, 'values')
            delete_company(company_name[1])
            view_list_company()
            new_combobox_company = update_combobox_company_values()
            main_app.owner_entry['values'] = main_app.owner_vpn_entry['values'] = new_combobox_company

        self.delete_btn = ttk.Button(self, text="Удалить", command=delete_select_company)
        self.delete_btn.grid(row=1, column=1, padx=6, pady=6)

if __name__ == "__main__":
    #--------------------------------------------------------------------#
    # Create func for disable vpn when destroy main window

    main_app = MainWindow()
    def on_close():
        disable_vpn()
        main_app.destroy()
    main_app.protocol('WM_DELETE_WINDOW', on_close)
    main_app = mainloop()