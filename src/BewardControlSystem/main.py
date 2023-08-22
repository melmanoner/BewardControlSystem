import tkinter as tk

from mysql_connector import add_new_address, get_vpn_from_address_list, \
    values_table,values_vpn_table, delete_select_address, delete_select_vpn,\
    edt_address, add_new_vpn, edit_vpn,select_vpn_name,selection_log_and_pass_by_name,\
    remove_all_bwd,remove_all_vpn,values_company_table,add_company_to_listbox,delete_company,select_all_bwd_by_logpas, get_vpn_by_company

from tkinter import *
from tkinter import ttk
import csv
from ttkthemes import ThemedStyle
import os
from tkinter import messagebox as mbox
from tkinter.messagebox import askyesno
import requests
from functions import update_combobox_company_values, Vpn, disable_vpn
import re
from tkinter import filedialog as fd
import pandas as pd
from panel_controller import BwdController

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

        style = ThemedStyle(self)
        style.set_theme("arc")
        style.configure("Treeview",
                        background='#FFF',
                        foreground='black',
                        rowheight=25,
                        fieldbackground='#FFF')

        style.map("Treeview",
                  background=[('selected','#347083')])







        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill=BOTH)


        bwd_frame = ttk.Frame(notebook)
        vpn_frame = ttk.Frame(notebook)



        bwd_frame.pack(fill=BOTH, expand=True)
        vpn_frame.pack(fill=BOTH, expand=True)



        notebook.add(bwd_frame, text='Бевард')
        notebook.add(vpn_frame, text='VPN')

# Filter panel
        def filterTreeView(*args):
            ItemsOnTreeView = tree.get_children()
            search = search_ent_var.get().capitalize()
            for eachItem in ItemsOnTreeView:
                if search in tree.item(eachItem)['values'][1]:
                    search_var = tree.item(eachItem)['values']
                    tree.delete(eachItem)
                    tree.insert("", 0, values=search_var)

        search_ent_var = StringVar()
        search_entry = Entry(bwd_frame, width=150, textvariable=search_ent_var)
        search_entry.pack(pady=10)
        #self.search_entry.insert(0,'Поиск')
        search_ent_var.trace('w', filterTreeView)





        # Create a bwd frame

        tree_frame = Frame(bwd_frame)
        tree_frame.pack(pady=10)


        tree = ttk.Treeview(tree_frame,
                            selectmode="extended",
                            columns=('ID','address','entrance','ip','login','password','owner', 'vpn'),
                            height=10, show='headings')


        tree.column("ID", width=30 ,anchor=CENTER)
        tree.column('address', width=250, anchor=CENTER)
        tree.column('entrance', width=250, anchor=CENTER)
        tree.column('ip', width=250, anchor=CENTER)
        tree.column('login', width=250, anchor=CENTER)
        tree.column('password', width=0, stretch=NO)
        tree.column('owner', width=250, anchor=CENTER)
        tree.column('vpn', width=0, stretch=NO)

        tree.heading("ID", text='ID')
        tree.heading("address", text="Адрес")
        tree.heading("entrance", text="Подъезд")
        tree.heading("ip", text='ip')
        tree.heading("login", text='Логин')
        tree.heading("password", text='')
        tree.heading("owner", text='Обслуживающая организация')
        tree.heading("vpn", text='VPN')

        # Create view for table
        def view_table():
            [tree.delete(i) for i in tree.get_children()]
            for row in values_table():
                tree.insert('','end',values=row)
        # Call view_table func
        view_table()



        tree.yview()
        tree.pack(side=LEFT, fill=X)

        # Create a Treeview Scrollbar
        tree_scroll = ttk.Scrollbar(tree_frame, command=tree.yview)
        tree_scroll.pack(side=RIGHT, fill=Y)
        tree.configure(yscrollcommand=tree_scroll.set)

        # Create Striped Row Tags (doesnt work, idk why)
        tree.tag_configure('oddrow', background='yellow')
        tree.tag_configure('evenrow', background='blue')

        # Add Record Entry Boxes

        data_frame = LabelFrame(bwd_frame, text="Таблица")
        data_frame.pack(fill="x", padx=20)

        entris = []
        def clear_entris():
            for entry in entris:
                entry.delete(0, END)
        id_entry = Entry(data_frame)
        id_entry.grid_remove()
        entris.append(id_entry)



        address_label = Label(data_frame, text="Адрес")
        address_label.grid(row=0, column=0, padx=10, pady=10)
        address_entry = Entry(data_frame)
        address_entry.grid(row=0, column=1, padx=10, pady=10)
        entris.append(address_entry)



        entrance_label = Label(data_frame, text='Подъезд')
        entrance_label.grid(row=0, column=2, padx=10, pady=10)
        entrance_entry = Entry(data_frame)
        entrance_entry.grid(row=0, column=3, pady=10, padx=10)
        entris.append(entrance_entry)



        ip_label = Label(data_frame, text="IP")
        ip_label.grid(row=0, column=4, padx=10, pady=10)
        ip_entry = Entry(data_frame)
        ip_entry.grid(row=0, column=5, padx=10, pady=10)
        entris.append(ip_entry)


        self.vpn_variable = IntVar()
        vpn_checkbtn = Checkbutton(data_frame, text='VPN', variable=self.vpn_variable, onvalue=1, offvalue=0)
        vpn_checkbtn.grid(row=0, column=6, padx=10, pady=10)



        login_bwd_label = Label(data_frame, text='Логин')
        login_bwd_label.grid(row=1, column=0, padx=10, pady=10)
        login_bwd_entry = Entry(data_frame)
        login_bwd_entry.grid(row=1, column=1, padx=10, pady=10)
        entris.append(login_bwd_entry)



        password_bwd_label = Label(data_frame, text='Пароль')
        password_bwd_label.grid(row=1, column=2, padx=10, pady=10)
        password_bwd_entry = Entry(data_frame, show='*')
        password_bwd_entry.grid(row=1, column=3, padx=10, pady=10)
        entris.append(password_bwd_entry)




        # there was
        # Update company combobox
        #         def update_combobox_company_values():
        #             company_list = []
        #             for i in values_company_table():
        #                 company_list.append(i[1])
        #             return company_list

        lists_for_combobox = update_combobox_company_values()

        owner_label = Label(data_frame, text="Обслуживающая организация")
        owner_label.grid(row=1, column=4, padx=10, pady=10)
        owner_entry = ttk.Combobox(data_frame, values=lists_for_combobox)
        owner_entry.grid(row=1, column=5, padx=10, pady=10)
        entris.append(owner_entry)


        #####################

        plus_btn = Button(data_frame, relief='flat', bg='#FFFFF0', text='Добавить обслуживающую\nорганизацию', cursor='hand2', command=ChildAddCompany)
        plus_btn.grid(row=1, column=6, padx=10,pady=10)

        def open_bwd_controller():
            Vpn(ip_entry.get(), login_bwd_entry.get(), password_bwd_entry.get(), self.vpn_variable.get(),
                get_vpn_by_company(owner_entry.get()))
            BwdController(address_entry.get(), entrance_entry.get(), login_bwd_entry.get(),password_bwd_entry.get(),ip_entry.get(), owner_entry.get())

        bwd_open_btn = Button(data_frame, bg='#FFFFF0', text='Открыть', relief='flat', cursor='hand2', command=open_bwd_controller)
        bwd_open_btn.grid(row=0, column=7, padx=10, pady=10)


########################################################################

        # Add Buttons for control sql
        button_frame = LabelFrame(bwd_frame, text="Управление списком адресов")
        button_frame.pack(fill=X, padx=20)

        def add_bwd():
            add_new_address( address_entry.get(),entrance_entry.get(),ip_entry.get(),login_bwd_entry.get(),password_bwd_entry.get(), owner_entry.get(), self.vpn_variable.get())
            clear_entris()
            view_table()
        add_button = Button(button_frame, relief='flat', bg='#FFFFF0', text="Добавить",cursor = 'hand2', command=add_bwd)
        add_button.grid(row=0, column=0, padx=10, pady=10)

        # Edit button
        def edit_address():
            edt_address(id_entry.get(), address_entry.get(),entrance_entry.get(),ip_entry.get(),login_bwd_entry.get(),password_bwd_entry.get(), owner_entry.get(), self.vpn_variable.get())
            view_table()



        edit_button = Button(button_frame, text="Изменить",bg='#FFFFF0', relief='flat', command=edit_address,cursor = 'hand2')
        edit_button.grid(row=0, column=1, padx=10, pady=10)

        def remove_command():
            delete_select_address(id_entry.get())
            view_table()
        remove_button = Button(button_frame,bg='#FFFFF0', text="Удалить выбранный",relief='flat', command=remove_command,cursor = 'hand2')
        remove_button.grid(row=0, column=2, padx=10, pady=10)

        def remove_all_warning():
            result = askyesno(title='Подтверждение операции', message='Вы действительно хотите удалить ВСЕ записи?')
            if result:
                remove_all_bwd()
                view_table()


        remove_all_button = Button(button_frame, text="Удалить все",bg='#FFFFF0', relief='flat',cursor = 'hand2', command=remove_all_warning)
        remove_all_button.grid(row=0, column=3, padx=10, pady=10)

        def import_from_excel():
            xlsx = fd.askopenfilename()
            df_address_list = pd.read_excel(f'''{xlsx}''')
            base_list=[]
            id_xlsx = df_address_list['ID'].tolist()
            address_xlsx = df_address_list['Адрес'].tolist()
            entrance_xlsx = df_address_list['Подъезд'].tolist()
            ip_xlsx = df_address_list['ip'].tolist()
            login_xlsx = df_address_list['Логин'].tolist()
            password_xlsx = df_address_list['Пароль'].tolist()
            company_xlsx = df_address_list['Обслуживающая организация'].tolist()
            vpn_xlsx = df_address_list['VPN'].tolist()
            base_list.append(id_xlsx)
            base_list.append(address_xlsx)
            base_list.append(entrance_xlsx)
            base_list.append(ip_xlsx)
            base_list.append(login_xlsx)
            base_list.append(password_xlsx)
            base_list.append(company_xlsx)
            base_list.append(vpn_xlsx)
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
                vpn_xlsx = value_for_db[7]

                add_new_address(address_xlsx, entrance_xlsx, ip_xlsx, login_xlsx, password_xlsx, company_xlsx, vpn_xlsx)

            view_table()





        add_bwd_from_xlsx = Button(button_frame,bg='#FFFFF0',text='Импорт из Excel', relief='flat',cursor='hand2', command=import_from_excel)
        add_bwd_from_xlsx.grid(row=0, column=4, padx=10, pady=10)




        #Add Buttons for control panel
        button_control_bwd_frame = LabelFrame(bwd_frame, text="Управление панелью")
        button_control_bwd_frame.pack(fill=X, padx=20)


        #--------------------------------------------------------------------------------------------------#
        ####################################################################################################
        # Click selection---------------------------------------------------------------------------#
        def select_record(event):
            # Clear entry boxes
            clear_entris()
            # Grab record Number
            selected = tree.focus()
            # Grab record values
            values = tree.item(selected, 'values')
            self.vpn_variable.set(values[-1])
            # outpts to entry boxes
            i=0
            for entry in entris:
                entry.insert(0, values[i])
                i = i + 1
        tree.bind('<Double-Button-1>', select_record)




        #tree.bind('<Double-Button-1>',  select_bwd)
        #--------------------------------------------------------------------------------------------------#


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



        bottom_frame = LabelFrame(bwd_frame)
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




        # Create frame for vpn

        vpn_list_frame = Frame(vpn_frame)
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
        vpn_label_frame = LabelFrame(vpn_frame, text='VPN')
        vpn_label_frame.pack(fill="x", padx=20)
        entris_vpn = []
        id_vpn_entry = Entry(vpn_label_frame)
        id_vpn_entry.grid_remove()
        entris_vpn.append(id_vpn_entry)
        id_vpn = id_vpn_entry.get()

        owner_vpn_label = Label(vpn_label_frame, text="Владелец")
        owner_vpn_label.grid(row=0, column=0, padx=10, pady=10)
        owner_vpn_entry = ttk.Combobox(vpn_label_frame, values=lists_for_combobox,state="readonly")
        owner_vpn_entry.grid(row=0, column=1, padx=10, pady=10)
        entris_vpn.append(owner_vpn_entry)
        owner_vpn = owner_vpn_entry.get()

        name_vpn_label = Label(vpn_label_frame, text="Название сети")
        name_vpn_label.grid(row=0, column=2, padx=10, pady=10)
        name_vpn_entry = Entry(vpn_label_frame)
        name_vpn_entry.grid(row=0, column=3, padx=10, pady=10)
        entris_vpn.append(name_vpn_entry)
        name_vpn = name_vpn_entry.get()

        login_vpn_label = Label(vpn_label_frame, text="Логин")
        login_vpn_label.grid(row=0, column=4, padx=10, pady=10)
        login_vpn_entry = Entry(vpn_label_frame)
        login_vpn_entry.grid(row=0, column=5, padx=10, pady=10)
        entris_vpn.append(login_vpn_entry)
        login_vpn = login_vpn_entry.get()

        password_vpn_label = Label(vpn_label_frame, text="Пароль")
        password_vpn_label.grid(row=0, column=6, padx=10, pady=10)
        password_vpn_entry = Entry(vpn_label_frame, show='*')
        password_vpn_entry.grid(row=0, column=7, padx=10, pady=10)
        entris_vpn.append(password_vpn_entry)
        password_vpn = password_vpn_entry.get()

        control_vpn_frame = LabelFrame(vpn_frame, text='Управление списком VPN')
        control_vpn_frame.pack(fill=X, padx=20)
        # Create add vpn func
        def add_vpn():
            add_new_vpn(owner_vpn, name_vpn, login_vpn, password_vpn)
            for entry in entris_vpn:
                entry.delete(0, 'end')
            view_vpn_table()
            show_vpn()
        # Add button
        add_vpn_button = Button(control_vpn_frame, text="Добавить", cursor='hand2', command=add_vpn)
        add_vpn_button.grid(row=0, column=0, padx=10, pady=10)
        # Button for edit vpn
        def edit_select_vpn():
            edit_vpn(id_vpn, owner_entry, name_vpn, login_vpn, password_vpn)
            view_vpn_table()
            show_vpn()
        edit_vpn_button = Button(control_vpn_frame, text='Изменить', command=edit_select_vpn)
        edit_vpn_button.grid(row=0, column=1, padx=10, pady=10)
        # Button for delete vpn
        def delete_sel_vpn():
            delete_select_vpn(id_vpn)
            view_vpn_table()
            show_vpn()
        delete_vpn_button = Button(control_vpn_frame, text="Удалить", cursor='hand2', command=delete_sel_vpn)
        delete_vpn_button.grid(row=0, column=2, padx=10, pady=10)

        def delete_all_vpn():
            result = askyesno(title='Подтверждение операции', message='Вы действительно хотите удалить ВСЕ записи в списке VPN?')
            if result:
                remove_all_vpn()
                view_vpn_table()
                show_vpn()
        delete_all_vpn_btn = Button(control_vpn_frame, text='Удалить все VPN', cursor='hand2', command=delete_all_vpn)
        delete_all_vpn_btn.grid(row=0, column=3, padx=10, pady=10)
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