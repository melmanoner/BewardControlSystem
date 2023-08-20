from tkinter import ttk
import tkinter as tk
from tkinter import *
import requests
from ttkthemes import ThemedStyle
from functions import disable_vpn

class BwdController(tk.Tk):
    def __init__(self, login, password, ip, company):
        self.bwd_controller_window = tk.Tk.__init__(self)
        self.wm_title('Сюда вписать адрес')
        self.wm_geometry('800x600')
        style = ThemedStyle(self)
        style.set_theme("arc")
        self.login = login
        self.password = password
        self.ip = ip
        self.bwd_controller_child()
        self.company = company
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

        bwd_notebook.add(frame_video_audio, text='Аудио и видео')
        bwd_notebook.add(frame_network, text='Сеть')
        bwd_notebook.add(frame_sip, text='SIP')
        bwd_notebook.add(frame_keys, text='Ключи')
        bwd_notebook.add(frame_intercom, text='Домофон')
        bwd_notebook.add(frame_sys,text='Системные')

        audio_param_label = Label(self,text='Параметры аудио')
        audio_param_label.pack()

        get_param_audio = requests.get(f'''http://{self.login}:{self.password}@{self.ip}/cgi-bin/audio_cgi?action=get''')
        get_param_audio_label = Label(frame_video_audio, text=get_param_audio.text)
        get_param_audio_label.pack()



