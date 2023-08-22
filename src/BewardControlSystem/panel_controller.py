from tkinter import ttk
import tkinter as tk
from tkinter import *
import requests
from ttkthemes import ThemedStyle
from functions import disable_vpn
import cv2
from tkinter import messagebox as mbox
from tkinter.messagebox import askyesno

class BwdController(tk.Tk):
    def __init__(self, address,entrance, login, password, ip, company):
        self.bwd_controller_window = tk.Tk.__init__(self)
        self.wm_geometry('800x600')
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

        frame_video_audio.pack(expand=True, fill=BOTH)
        frame_keys.pack(expand=True, fill=BOTH)
        frame_intercom.pack(expand=True, fill=BOTH)
        frame_network.pack(expand=True, fill=BOTH)
        frame_sip.pack(expand=True, fill=BOTH)
        frame_sys.pack(expand=True, fill=BOTH)


        bwd_notebook.add(frame_intercom, text='Домофон')
        bwd_notebook.add(frame_keys, text='Ключи')
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














        audio_param_label = Label(frame_video_audio,text='Параметры видео')
        audio_param_label.grid(row=0, column=0)

        get_param_audio = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/videocoding_cgi?action=get''')
        get_param_audio_label = Label(frame_video_audio, text=get_param_audio.text)
        get_param_audio_label.grid(row=1, column=0)





