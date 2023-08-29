from tkinter import ttk
import tkinter as tk
from tkinter import *
import requests
from ttkthemes import ThemedStyle
from functions import disable_vpn
import cv2
from tkinter import messagebox as mbox
from tkinter.messagebox import askyesno
from mysql_connector import select_all_bwd_by_logpas
from tkinter import filedialog as fd
import pandas as pd
import csv

class BwdController(tk.Tk):
    def __init__(self, address,entrance, login, password, ip, company):
        self.bwd_controller_window = tk.Tk.__init__(self)
        self.wm_geometry('1000x600')
        style = ThemedStyle(self)
        style.set_theme("arc")
        self.address = address
        self.entrance = entrance
        self.login = login
        self.password = password
        self.ip = ip
        self.bwd_controller_child()
        self.company = company
        self.wm_title(self.address+' подъезд '+ self.entrance)
        self.wm_protocol('WM_DELETE_WINDOW', self.on_close)



    def on_close(self):
        disable_vpn()
        self.destroy()

    def bwd_controller_child(self):
        #back_btn = Button(self, text='<- назад', relief='flat', bg='#FFFFF0')
        #back_btn.pack(side=LEFT)
        bwd_notebook = ttk.Notebook(self)
        bwd_notebook.pack(expand=True, fill=BOTH)



        frame_video_audio = ttk.Frame(bwd_notebook)
        frame_keys = ttk.Frame(bwd_notebook)
        frame_intercom = ttk.Frame(bwd_notebook)
        frame_network = ttk.Frame(bwd_notebook)
        frame_sip = ttk.Frame(bwd_notebook)
        frame_sys = ttk.Frame(bwd_notebook)
        frame_display = ttk.Frame(bwd_notebook)

        frame_video_audio.pack(expand=True, fill=BOTH)
        frame_keys.pack(expand=True, fill=BOTH)
        frame_intercom.pack(expand=True, fill=BOTH)
        frame_network.pack(expand=True, fill=BOTH)
        frame_sip.pack(expand=True, fill=BOTH)
        frame_sys.pack(expand=True, fill=BOTH)
        frame_display.pack(expand=True, fill=BOTH)


        bwd_notebook.add(frame_intercom, text='Домофон')
        bwd_notebook.add(frame_keys, text='Ключи')
        bwd_notebook.add(frame_display, text='Дисплей')
        bwd_notebook.add(frame_network, text='Сеть')
        bwd_notebook.add(frame_sip, text='SIP')
        bwd_notebook.add(frame_sys, text='Системные')
        bwd_notebook.add(frame_video_audio, text='Видео')


        def open_door():
            try:
                r = requests.get(
                    f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/intercom_cgi?action=maindoor''')
                if r.status_code == 200:
                    ok_label = Label(frame_intercom, text='Ок')
                    ok_label.grid(row=0, column=0, padx=5,pady=5)
                else:
                    not_ok_label = Label(frame_intercom, text='Ошибка')
                    not_ok_label.grid(row=0, column=0, padx=5, pady=5)
            except Exception:
                mbox.showwarning('Ошибка', 'Проверьте выбран ли адрес и включён ли VPN')
        open_door_btn = Button(frame_intercom, text='Открыть дверь', command=open_door)
        open_door_btn.grid(row=1, column=0, padx=10, pady=10)

        def open_alterdoor():
            try:
                r = requests.get(
                    f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/intercom_cgi?action=altdoor''')
                if r.status_code == 200:
                    ok_label = Label(frame_intercom, text='Ок')
                    ok_label.grid(row=0, column=0, padx=5,pady=5)
                else:
                    not_ok_label = Label(frame_intercom, text='Ошибка')
                    not_ok_label.grid(row=0, column=0, padx=5, pady=5)
            except Exception:
                mbox.showwarning('Ошибка', 'Проверьте выбран ли адрес и включён ли VPN')

        open_door_btn = Button(frame_intercom, text='Открыть вторую дверь', command=open_alterdoor)
        open_door_btn.grid(row=2, column=0, padx=10, pady=10)

        def state_serv_code():
            try:
                get_param = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/intercom_cgi?action=get''')
                text_param = get_param.text
                first_half = text_param.find('DoorCodeActive=')
                second_half = first_half+17
                if text_param[first_half:second_half] == 'DoorCodeActive=on':
                    set_state_code = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/intercom_cgi?action=set&DoorCodeActive=off''')
                    if set_state_code.status_code == 200:
                        response_label = Label(frame_intercom, text='Ok')
                        response_label.grid(row=0, column=0, padx=5, pady=5)
                    else:
                        response_label = Label(frame_intercom, text=set_code)
                        response_label.grid(row=0, column=0, padx=5, pady=5)
                else:
                    set_state_code = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/intercom_cgi?action=set&DoorCodeActive=on''')
                    if set_state_code.status_code == 200:
                        response_label = Label(frame_intercom, text='Ok')
                        response_label.grid(row=0, column=0, padx=5, pady=5)
                    else:
                        response_label = Label(frame_intercom, text=set_code)
                        response_label.grid(row=0, column=0, padx=5, pady=5)
            except Exception:
                mbox.showwarning('Ошибка', 'Проверьте выбран ли адрес и включён ли VPN')

        set_state_serv_code_btn = Button(frame_intercom, text='Вкл/Выкл сервисный код', command=state_serv_code)
        set_state_serv_code_btn.grid(row=3, column=0, padx=5, pady=5)


        settings_param_label = Label(frame_intercom, text='Параметры')
        settings_param_label.grid(row=0, column=1, padx=5, pady=5)

        get_param = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/intercom_cgi?action=get''')
        get_param_label = Label(frame_intercom, text=get_param.text)
        get_param_label.grid(row=1, column=1, padx=5, pady=5, rowspan=6)

        #linelevel_label = Label(frame_intercom, text='Уровень линии в квартире')
        #linelevel_label.grid(row=0, column=2, padx=5, pady=5)

        appart_label = Label(frame_intercom, text='Квартира')
        appart_label.grid(row=0, column=2, padx=5, pady=5)

        appart_entry = Entry(frame_intercom, text='Квартира')
        appart_entry.grid(row=1, column=2, padx=5, pady=5)

        code_label = Label(frame_intercom, text='Код')
        code_label.grid(row=2, column=2, padx=5, pady=5)

        code_entry = Entry(frame_intercom)
        code_entry.grid(row=3, column=2, padx=5, pady=5)



        def get_linelevel():
            apparment = appart_entry.get()
            get_linelvl = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/intercom_cgi?action=linelevel&Apartment={apparment}''')
            linelevel_response_label = Label(frame_intercom, text=get_linelvl.text)
            linelevel_response_label.grid(row=4, column=2, padx=5, pady=5)

        linelevel_btn = Button(frame_intercom, text='Проверить уровень линии в квартире', command=get_linelevel)
        linelevel_btn.grid(row=5, column=2, padx=5, pady=5)



        def get_appart_param():
            try:
                appart = appart_entry.get()
                get_param = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/apartment_cgi?action=get&Number={appart}''')
                if get_param.status_code == 200:
                    response = Label(frame_intercom, text=get_param.text)
                    response.grid(row=0, column=3, padx=5, pady=5, rowspan=4)
                else:
                    response = Label(frame_intercom, text='Ошибка')
                    response.grid(row=0, column=3, padx=5, pady=5)

            except Exception:
                mbox.showwarning('Ошибка', 'Проверьте выбран ли адрес и включён ли VPN')

        get_apart_param_btn = Button(frame_intercom, text='Получить параметры квартиры', command=get_appart_param)
        get_apart_param_btn.grid(row=6, column=2, padx=5, pady=5)

        def set_code():
            try:
                appart = appart_entry.get()
                code = code_entry.get()
                set_code = requests.get(
                    f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/apartment_cgi?action=set&Number={appart}&DoorCode={code}''')
                if set_code.status_code == 200:
                    response_label = Label(frame_intercom, text='Ok')
                    response_label.grid(row=4, column=2, padx=5, pady=5)
                else:
                    response_label = Label(frame_intercom, text=set_code)
                    response_label.grid(row=4, column=2, padx=5, pady=5)
            except Exception:
                mbox.showwarning('Ошибка', 'Проверьте выбран ли адрес и включён ли VPN')

        set_code_btn = Button(frame_intercom, text='Изменить код открытия по квартире', command=set_code)
        set_code_btn.grid(row=7, column=2, padx=5, pady=5)

        def code_state():
            try:
                appart = appart_entry.get()
                get_param = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/apartment_cgi?action=get&Number={appart}''')
                parametrs = get_param.text
                first_half = parametrs.find('DoorCodeActive=')
                second_half = first_half+17
                check_state_code  = parametrs[first_half:second_half]
                if check_state_code == 'DoorCodeActive=on':
                    code_state = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/apartment_cgi?action=set&Number={appart}&DoorCodeActive=off''')
                    if code_state.status_code == 200:
                        response_label = Label(frame_intercom, text='Ok')
                        response_label.grid(row=4, column=2, padx=5, pady=5)
                    else:
                        response_label = Label(frame_intercom, text=set_code)
                        response_label.grid(row=4, column=2, padx=5, pady=5)
                else:
                    code_state = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/apartment_cgi?action=set&Number={appart}&DoorCodeActive=on''')
                    if code_state.status_code == 200:
                        response_label = Label(frame_intercom, text='Ok')
                        response_label.grid(row=4, column=2, padx=5, pady=5)
                    else:
                        response_label = Label(frame_intercom, text=set_code)
                        response_label.grid(row=4, column=2, padx=5, pady=5)
            except Exception:
                mbox.showwarning('Ошибка', 'Проверьте выбран ли адрес и включён ли VPN')


        state_code_btn = Button(frame_intercom, text='Вкл/Выкл код открытия', command=code_state)
        state_code_btn.grid(row=8, column=2, padx=5, pady=5)

        def set_serv_code():
            try:
                code = code_entry.get()
                set_code = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/intercom_cgi?action=set&DoorCode={code}''')
                if set_code.status_code == 200:
                    response_label = Label(frame_intercom, text='Ok')
                    response_label.grid(row=4, column=2, padx=5, pady=5)
                else:
                    response_label = Label(frame_intercom, text=set_code)
                    response_label.grid(row=4, column=2, padx=5, pady=5)
            except Exception:
                mbox.showwarning('Ошибка', 'Проверьте выбран ли адрес и включён ли VPN')

        set_serv_code_btn = Button(frame_intercom, text='Изменить сервисный код', command=set_serv_code)
        set_serv_code_btn.grid(row=9, column=2, padx=5, pady=5)


# Key Frame

        self.keys_autocollect_var = BooleanVar()

        params_for_enable = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/mifare_cgi?action=get''').text
        first_half_params_keys = params_for_enable.find('AutoCollectKeys=')
        second_half_params_keys = first_half_params_keys+18
        keys_autocollect_params = params_for_enable[first_half_params_keys:second_half_params_keys]
        if keys_autocollect_params == 'AutoCollectKeys=on':
            self.keys_autocollect_var=1
        else:
            self.keys_autocollect_var=0


        def autocollectkeys():
            try:
                if self.keys_autocollect_var== 0:
                    self.keys_autocollect_var = 1
                    collect_key = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/mifare_cgi?action=set&AutoCollectKeys=on''')
                    if collect_key.status_code == 200:
                        response_label = Label(frame_keys, text='Автозапись включена')
                        response_label.grid(row=0, column=0, padx=5, pady=5)
                    else:
                        response_label = Label(frame_keys, text='Ошибка')
                        response_label.grid(row=0, column=0, padx=5, pady=5)
                elif self.keys_autocollect_var == 1:
                    self.keys_autocollect_var = 0
                    collect_key = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/mifare_cgi?action=set&AutoCollectKeys=off''')
                    if collect_key.status_code == 200:
                        response_label = Label(frame_keys, text='Автозапись отключена')
                        response_label.grid(row=0, column=0, padx=5, pady=5)
                    else:
                        response_label = Label(frame_keys, text='Ошибка')
                        response_label.grid(row=0, column=0, padx=5, pady=5)
            except Exception:
                mbox.showwarning('Ошибка', 'Проверьте выбран ли адрес и включён ли VPN')

        autorecord = Checkbutton(frame_keys, text='Включить автозапись', cursor='hand2',onvalue=1, offvalue=0, variable=self.keys_autocollect_var,command=autocollectkeys)
        autorecord.grid(row=1, column=0, padx=5, pady=5)

        key_label = Label(frame_keys, text='Ключ/Индекс/Код')
        key_label.grid(row=0, column=1, padx=5, pady=5)

        key_entry = Entry(frame_keys)
        key_entry.grid(row=1, column=1, padx=5, pady=5)

        def add_key():
            try:
                mifare = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/mifare_cgi?action=add&Key={key_entry.get()}''')
                rfid = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/rfid_cgi?action=add&Key={key_entry.get()}''')
                if mifare.status_code or rfid.status_code == 200:
                    key_entry.delete(0, END)
                    response_label = Label(frame_keys, text='Ключ добавлен')
                    response_label.grid(row=2, column=1, pady=5, padx=5)
                else:
                    response_label = Label(frame_keys, text='Ошибка')
                    response_label.grid(row=2, column=1, pady=5, padx=5)
            except Exception:
                mbox.showwarning('Ошибка', 'Проверьте выбран ли адрес и подключен ли VPN')

        key_add_btn = Button(frame_keys, text='Добавить', command=add_key)
        key_add_btn.grid(row=3, column=1, padx=5, pady=5)

        def add_key_to_all_bwd():
            try:
                ip_list = select_all_bwd_by_logpas(self.login, self.password)
                i=0
                for ip in ip_list:
                    add_key_rfid = requests.get(f'''http://{self.login}:{self.password}@{ip[0]}/cgi-bin/rfid_cgi?action=add&Key={key_entry.get()}''')
                    add_key_mifare = requests.get(f'''http://{self.login}:{self.password}@{ip[0]}/cgi-bin/mifare_cgi?action=add&Key={key_entry.get()}''')
                    if add_key_rfid.status_code or add_key_mifare.status_code == 200:
                        i+=1
                response_label = Label(frame_keys, text=f'''Ключ добавлен в {i} панелей''')
                response_label.grid(row=2, column=1, pady=5, padx=5)
            except Exception:
                mbox.showwarning('Ошибка', 'Проверьте выбран ли адрес и подключен ли VPN')


        add_key_to_all_bwd_btn = Button(frame_keys, text='Добавить во все панели', cursor='hand2', command=add_key_to_all_bwd)
        add_key_to_all_bwd_btn.grid(row=4, column=1, pady=5,padx=5)

        def delete_key():
            try:
                mifare = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/mifare_cgi?action=delete&Key={key_entry.get()}''')
                rfid = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/rfid_cgi?action=delete&Key={key_entry.get()}''')
                if mifare.status_code or rfid.status_code == 200:
                    key_entry.delete(0, END)
                    response_label = Label(frame_keys, text='Ключ удален')
                    response_label.grid(row=2, column=1, pady=5, padx=5)
                else:
                    response_label = Label(frame_keys, text='Ошибка')
                    response_label.grid(row=2, column=1, pady=5, padx=5)
            except Exception:
                mbox.showwarning('Ошибка', 'Проверьте выбран ли адрес и подключен ли VPN')

        delete_key_button = Button(frame_keys, text='Удалить', cursor='hand2', command=delete_key)
        delete_key_button.grid(row=5, column=1, padx=5,pady=5)

        def delete_key_in_all_bwd():
            try:
                ip_list = select_all_bwd_by_logpas(self.login, self.password)
                i=0
                for ip in ip_list:
                    delete_key_rfid = requests.get(f'''http://{self.login}:{self.password}@{ip[0]}/cgi-bin/rfid_cgi?action=delete&Key={key_entry.get()}''')
                    delete_key_mifare = requests.get(f'''http://{self.login}:{self.password}@{ip[0]}/cgi-bin/mifare_cgi?action=delete&Key={key_entry.get()}''')
                    if delete_key_mifare.status_code or delete_key_rfid.status_code == 200:
                        i+=1
                response_label = Label(frame_keys, text=f'''Ключ удален в {i} панелей''')
                response_label.grid(row=2, column=1, pady=5, padx=5)
            except Exception:
                mbox.showwarning('Ошибка', 'Проверьте выбран ли адрес и подключен ли VPN')


        add_key_to_all_bwd_btn = Button(frame_keys, text='Удалить со всех панелей', cursor='hand2', command=delete_key_in_all_bwd)
        add_key_to_all_bwd_btn.grid(row=6, column=1, pady=5,padx=5)

        def add_code_for_scan():
            try:
                code_value = key_entry.get()
                add_code_mf = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/mifare_cgi?action=set&ScanCode={code_value}&ScanCodeActive=on''')
                add_code_rf = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/rfid_cgi?action=set&RegCode={code_value}&ScanCodeActive=on''')
                if add_code_mf.status_code or add_code_rf.status_code == 200:
                    response_label = Label(frame_keys, text='Код сканирования установлен')
                    response_label.grid(row=2, column=1, pady=5, padx=5)
                else:
                    response_label = Label(frame_keys, text='Ошибка')
                    response_label.grid(row=2, column=1, pady=5, padx=5)
            except Exception:
                mbox.showwarning('Ошибка', 'Проверьте выбран ли адрес и подключен ли VPN')

        add_scan_code = Button(frame_keys, text='Установить код сканирования RFID', cursor='hand2', command=add_code_for_scan)
        add_scan_code.grid(row=1, column=2, pady=10,padx=10)

        def disable_scan_code():
            try:
                disable_code = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/mifare_cgi?action=set&ScanCodeActive=off''')
                if disable_code.status_code == 200:
                    response_label = Label(frame_keys, text='Код сканирования отключен')
                    response_label.grid(row=2, column=1, pady=5, padx=5)
                else:
                    response_label = Label(frame_keys, text='Ошибка')
                    response_label.grid(row=2, column=1, pady=5, padx=5)
            except Exception:
                mbox.showwarning('Ошибка', 'Проверьте выбран ли адрес и подключен ли VPN', cursor='hand2', command=disable_scan_code)
        scan_code_off_btn = Button(frame_keys, text='Отключить код сканирования', command=disable_scan_code)
        scan_code_off_btn.grid(row=2, column=2, pady=10, padx=10)

        def show_all_mifare_keys():
            try:
                r = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/mifare_cgi?action=list''')
                show_keys_window = Tk()
                all_information = r.text
                mf_tree_frame = ttk.Frame(show_keys_window)
                mf_tree_frame.pack(fill=BOTH, expand=True)
                tree_mf = ttk.Treeview(mf_tree_frame,
                                       selectmode="extended",
                                       columns=('ID', 'key_value'),
                                       height=10, show='headings')
                tree_scroll = Scrollbar(mf_tree_frame, command=tree_mf.yview)
                tree_scroll.pack(side=RIGHT, fill=Y)
                tree_mf.configure(yscrollcommand=tree_scroll.set)
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
                response_label = Label(frame_keys, text='Ошибка! Проверьте ключи RFID')
                response_label.grid(row=0, column=0, pady=5, padx=5)




        show_all_mifare_keys_btn = Button(frame_keys, text='Показать список\nMIFARE ключей', cursor='hand2', command=show_all_mifare_keys)
        show_all_mifare_keys_btn.grid(row=2, column=0, padx=10, pady=10)

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
                tree_mf.heading('akey_value', text='Код ключа')

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
                response_label = Label(frame_keys, text='Ошибка! Проверьте ключи MIFARE')
                response_label.grid(row=0, column=0, pady=5, padx=5)

        show_all_rfid_keys_btn = Button(frame_keys, text='Показать список\nRFID ключей', cursor='hand2', command=show_all_rfid_keys)
        show_all_rfid_keys_btn.grid(row=3, column=0, padx=5, pady=5)

        def export_mf():
            url = f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/mifare_cgi?action=export'''
            get = requests.get(url)
            get_content = get.text



            mf_list = []
            while get_content != '':
                mf_list.append(get_content[:35])
                get_content = get_content[36:]
            #for key in mf_list:
            #    print(key)
            filepath = fd.asksaveasfile(defaultextension='.csv',initialfile="key.csv")
            #list_of_list = []
            #list_of_list.append(mf_list)
            #for key in mf_list:
            #    # writer.writerows([key])
            #    print(key)

            with open(filepath.name, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(mf_list)





            #with csv_file:
            #    writer = csv.writer(csv_file)
            #    for elem in mf_list:
            #        writer.writerow(elem)

            #with csv_file:
            #    writer = csv.writer(csv_file)
            #    for row in get.content:
            #        writer.writerow(row)


            #df = pd.read_excel(f'''{filepath}''')
            #content = pd.DataFrame(mf_list)
            #content.to_csv(filepath)

            #with open(filepath, "w") as file:
            #    file.write(get.content)


        export_mf_btn = Button(frame_keys, text='Экспорт Mifare', command=export_mf)
        export_mf_btn.grid(row=4, column=0, padx=5, pady=5)

        def import_mf():
            mf_file = fd.askopenfilename()
            url = f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/mifare_cgi?action=import'''
            post = requests.post(url, file=mf_file)
            if post.status_code == 200:
                response_label = Label(frame_keys, text='Успешно')
                response_label.grid(row=0, column=0, pady=5, padx=5)
            else:
                response_label = Label(frame_keys, text='Ошибка')
                response_label.grid(row=0, column=0, pady=5, padx=5)
        import_mf_btn = Button(frame_keys, text='Импорт Mifare', command=import_mf)
        import_mf_btn.grid(row=5, column=0, padx=5, pady=5)

# Display Frame
        ticker_label = Label(frame_display, text='Бегущая строка')
        ticker_label.grid(row=0, column=1, padx=10, pady=10)

        ticker_entry = Entry(frame_display)
        ticker_entry.grid(row=1, column=1, padx=10, pady=10)

        def edit_ticker():
            try:
                r = requests.get(
                    f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/display_cgi?action=set&TickerText={ticker_entry.get()}''')
                if r.status_code == 200:
                    response_label = Label(frame_display, text='Бегущая строка изменена!')
                    response_label.grid(row=2, column=1, pady=5, padx=5)
                else:
                    response_label = Label(frame_display, text='Ошибка!')
                    response_label.grid(row=2, column=1, pady=5, padx=5)
            except Exception:
                response_label = Label(frame_display, text='Ошибка')
                response_label.grid(row=2, column=1, pady=5, padx=5)

        ticker_btn = Button(frame_display, text='Изменить', cursor='hand2', command=edit_ticker)
        ticker_btn.grid(row=3, column=1, padx=10, pady=10)

        def enable_ticker():
            try:
                r = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/display_cgi?action=set&TickerEnable=on''')
                if r.status_code == 200:
                    response_label = Label(frame_display, text='Бегущая строка включена!')
                    response_label.grid(row=2, column=1, pady=5, padx=5)
                else:
                    response_label = Label(frame_display, text='Ошибка!')
                    response_label.grid(row=2, column=1, pady=5, padx=5)
            except Exception:
                response_label = Label(frame_display, text='Ошибка')
                response_label.grid(row=2, column=1, pady=5, padx=5)

        ticker_checkbutton = Button(frame_display, text='Вкл бегущую строку', command=enable_ticker)
        ticker_checkbutton.grid(row=1, column=2, padx=5, pady=5)

# Lan frame

        ping_entry = Entry(frame_network)
        ping_entry.grid(row=1, column=2, padx=5, pady=5)

        def ping():
            r = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/ping_cgi?action=start&host={ping_entry.get()}''')
            if r.status_code == 200:
                response = Label(frame_network, text=r.text)
                response.grid(row=0, column=1, padx=5, pady=5)
            else:
                response = Label(frame_network, text='Ошибка')
                response.grid(row=0, column=1, padx=5, pady=5)

        ping_btn = Button(frame_network, text='Пинг', command=ping)
        ping_btn.grid(row=2, column=1, padx=5, pady=5)

        audio_param_label = Label(frame_video_audio,text='Параметры видео')
        audio_param_label.grid(row=0, column=0)

        get_param_audio = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/videocoding_cgi?action=get''')
        get_param_audio_label = Label(frame_video_audio, text=get_param_audio.text)
        get_param_audio_label.grid(row=1, column=0)

#SIP Frame
        sip_reg_status = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/sip_cgi?action=regstatus''')
        sip_label = Label(frame_sip, text=sip_reg_status.text)
        sip_label.grid(row=15, column=0, pady=5, padx=5)

        def enable_account_sip1():
            if sip_reg_status.text[:13] == 'AccountEnable0':
                enable = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/sip_cgi?action=set&AccountEnable1''')
                if enable.status_code == 200:
                    mbox.showinfo('SIP1 Включен')
                else:
                    mbox.showwarning('Ошибка','Ошибка включения SIP1')
            else:
                disable = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/sip_cgi?action=set&AccountEnable0''')
                if disable.status_code == 200:
                    mbox.showinfo('SIP1 Отключен')
                else:
                    mbox.showwarning('Ошибка','Ошибка включения SIP1')

        #account_enable_label = Label(frame_sip, text='Вкл/Откл SIP 1')
        #account_enable_label.grid(row=0, column=0, pady=5, padx=5)

        account_enable_checkbox = Checkbutton(frame_sip, text='Вкл/Откл SIP 1')
        account_enable_checkbox.grid(row=0, column=1, pady=5, padx=5)

        acc_name1_label = Label(frame_sip, text='Имя:')
        acc_name1_label.grid(row=1, column=0,pady=5, padx=5)

        acc_name1_entry = Entry(frame_sip)
        acc_name1_entry.grid(row=1, column=1, pady=5, padx=5)

        acc_number1_label = Label(frame_sip, text='Номер:')
        acc_number1_label.grid(row=2, column=0, pady=5, padx=5)

        acc_number1_entry = Entry(frame_sip)
        acc_number1_entry.grid(row=2, column=1, pady=5, padx=5)

        acc_user1_label = Label(frame_sip, text='Имя пользователя:')
        acc_user1_label.grid(row=3, column=0, pady=5, padx=5)

        acc_user1_entry = Entry(frame_sip)
        acc_user1_entry.grid(row=3, column=1, pady=5, padx=5)

        acc_pass1_label = Label(frame_sip, text='Пароль:')
        acc_pass1_label.grid(row=4, column=0, pady=5, padx=5)

        acc_pass1_entry = Entry(frame_sip)
        acc_pass1_entry.grid(row=4, column=1, pady=5, padx=5)

        acc_port1_label = Label(frame_sip, text='Порт:')
        acc_port1_label.grid(row=5, column=0, pady=5, padx=5)

        acc_port1_entry = Entry(frame_sip)
        acc_port1_entry.grid(row=5, column=1, pady=5, padx=5)

        server_enable_label = Label(frame_sip, text='Разрешить регистрацию')
        server_enable_label.grid(row=6, column=0, pady=5, padx=5)
        reg_serv_dhcp_label = Label(frame_sip, text='Получать значения сервера регистрации по dhcp')
        reg_serv_dhcp_label.grid(row=7, column=0, pady=5, padx=5)

        server_enable_checkbox = Checkbutton(frame_sip)
        server_enable_checkbox.grid(row=6, column=1, pady=5, padx=5)
        reg_serv_dhcp_checkbox = Checkbutton(frame_sip)
        reg_serv_dhcp_checkbox.grid(row=7, column=1, pady=5, padx=5)

        serv_url1_label = Label(frame_sip, text='Сервер регестрации:')
        serv_url1_label.grid(row=8, column=0, pady=5, padx=5)

        serv_url1_entry = Entry(frame_sip)
        serv_url1_entry.grid(row=8, column=1, pady=5, padx=5)

        serv_port1_label = Label(frame_sip, text='Порт:')
        serv_port1_label.grid(row=9, column=0, pady=5, padx=5)

        serv_port1_entry = Entry(frame_sip)
        serv_port1_entry.grid(row=9, column=1, pady=5, padx=5)

        sip_url1_label = Label(frame_sip, text='SIP сервер:')
        sip_url1_label.grid(row=10, column=0, pady=5, padx=5)

        sip_url1_entry = Entry(frame_sip)
        sip_url1_entry.grid(row=10, column=1, pady=5, padx=5)

        sip_port1_label = Label(frame_sip, text='Sip Порт:')
        sip_port1_label.grid(row=11, column=0, pady=5, padx=5)

        sip_port1_entry = Entry(frame_sip)
        sip_port1_entry.grid(row=11, column=1, pady=5, padx=5)

        proxy_url1_label = Label(frame_sip, text='Proxy сервер:')
        proxy_url1_label.grid(row=12, column=0, pady=5, padx=5)

        proxy_url1_entry = Entry(frame_sip)
        proxy_url1_entry.grid(row=12, column=1, pady=5, padx=5)

        proxy_port1_label = Label(frame_sip, text='Proxy Порт:')
        proxy_port1_label.grid(row=13, column=0, pady=5, padx=5)

        proxy_port1_entry = Entry(frame_sip)
        proxy_port1_entry.grid(row=13, column=1, pady=5, padx=5)

        enable_sip1_btn = Button(frame_sip, text='Зарегестрировать SIP 1')
        enable_sip1_btn.grid(row=14, column=1, pady=5, padx=5)

#SIP 2


        account2_enable_checkbox = Checkbutton(frame_sip, text='Вкл/Откл SIP 2')
        account2_enable_checkbox.grid(row=0, column=3, pady=5, padx=5)

        acc_name2_label = Label(frame_sip, text='Имя:')
        acc_name2_label.grid(row=1, column=2, pady=5, padx=5)

        acc_name2_entry = Entry(frame_sip)
        acc_name2_entry.grid(row=1, column=3, pady=5, padx=5)

        acc_number2_label = Label(frame_sip, text='Номер:')
        acc_number2_label.grid(row=2, column=2, pady=5, padx=5)

        acc_number2_entry = Entry(frame_sip)
        acc_number2_entry.grid(row=2, column=3, pady=5, padx=5)

        acc_user2_label = Label(frame_sip, text='Имя пользователя:')
        acc_user2_label.grid(row=3, column=2, pady=5, padx=5)

        acc_user2_entry = Entry(frame_sip)
        acc_user2_entry.grid(row=3, column=3, pady=5, padx=5)

        acc_pass2_label = Label(frame_sip, text='Пароль:')
        acc_pass2_label.grid(row=4, column=2, pady=5, padx=5)

        acc_pass2_entry = Entry(frame_sip)
        acc_pass2_entry.grid(row=4, column=3, pady=5, padx=5)

        acc_port2_label = Label(frame_sip, text='Порт:')
        acc_port2_label.grid(row=5, column=2, pady=5, padx=5)

        acc_port2_entry = Entry(frame_sip)
        acc_port2_entry.grid(row=5, column=3, pady=5, padx=5)

        server2_enable_label = Label(frame_sip, text='Разрешить регистрацию')
        server2_enable_label.grid(row=6, column=2, pady=5, padx=5)
        reg_serv2_dhcp_label = Label(frame_sip, text='Получать значения сервера регистрации по dhcp')
        reg_serv2_dhcp_label.grid(row=7, column=2, pady=5, padx=5)

        server2_enable_checkbox = Checkbutton(frame_sip)
        server2_enable_checkbox.grid(row=6, column=3, pady=5, padx=5)
        reg_serv2_dhcp_checkbox = Checkbutton(frame_sip)
        reg_serv2_dhcp_checkbox.grid(row=7, column=3, pady=5, padx=5)

        serv_url2_label = Label(frame_sip, text='Сервер регестрации:')
        serv_url2_label.grid(row=8, column=2, pady=5, padx=5)

        serv_url2_entry = Entry(frame_sip)
        serv_url2_entry.grid(row=8, column=3, pady=5, padx=5)

        serv_port2_label = Label(frame_sip, text='Порт:')
        serv_port2_label.grid(row=9, column=2, pady=5, padx=5)

        serv_port2_entry = Entry(frame_sip)
        serv_port2_entry.grid(row=9, column=3, pady=5, padx=5)

        sip_url2_label = Label(frame_sip, text='SIP сервер:')
        sip_url2_label.grid(row=10, column=2, pady=5, padx=5)

        sip_url2_entry = Entry(frame_sip)
        sip_url2_entry.grid(row=10, column=3, pady=5, padx=5)

        sip_port2_label = Label(frame_sip, text='Sip Порт:')
        sip_port2_label.grid(row=11, column=2, pady=5, padx=5)

        sip_port2_entry = Entry(frame_sip)
        sip_port2_entry.grid(row=11, column=3, pady=5, padx=5)

        proxy_url2_label = Label(frame_sip, text='Proxy сервер:')
        proxy_url2_label.grid(row=12, column=2, pady=5, padx=5)

        proxy_url2_entry = Entry(frame_sip)
        proxy_url2_entry.grid(row=12, column=3, pady=5, padx=5)

        proxy_port2_label = Label(frame_sip, text='Proxy Порт:')
        proxy_port2_label.grid(row=13, column=2, pady=5, padx=5)

        proxy_port2_entry = Entry(frame_sip)
        proxy_port2_entry.grid(row=13, column=3, pady=5, padx=5)

        enable_sip2_btn = Button(frame_sip, text='Зарегестрировать SIP 2')
        enable_sip2_btn.grid(row=14, column=3, pady=5, padx=5)


#/cgi-bin/sip_cgi?action=set&AccountEnable1={}&AccName1={}&AccNumber1={}&AccUser1={}&={}&AccPort1={}&ServerEnable1={}&RegServerDhcp1={}&RegServerUrl1={}&RegServerPort1={}&SipServerUrl1={}&SipServerPort1={}&SipServerPort1={}&ProxyServerUrl1={}&ProxyServerPort1={}


        def enable_sip1():
            reg_serv = requests.get(f'''http://{self.login}:{self.password}@{self.ip}
                /cgi-bin/sip_cgi?action=set&AccountEnable1={account_enable_checkbox}
                &AccName1={acc_name1_entry.get()}&
                AccNumber1={acc_number1_entry.get()}&
                AccUser1={acc_user1_entry.get()}&
                AccPassword1={acc_pass1_entry.get()}&
                AccPort1={acc_port1_entry.get()}&
                ServerEnable1={server_enable_checkbox}&
                RegServerDhcp1={reg_serv_dhcp_checkbox}&
                RegServerUrl1={serv_url1_entry.get()}&
                RegServerPort1={serv_port1_entry.get()}&
                SipServerUrl1={sip_url1_entry.get()}&
                SipServerPort1={sip_port1_entry.get()}&
                ProxyServerUrl1={proxy_url1_entry.get()}&
                ProxyServerPort1={proxy_port1_entry.get()}
                    ''')





