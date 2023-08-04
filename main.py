from mysql_connector import create_con_db,add_new_address, \
    values_table,values_vpn_table, delete_select_address, delete_select_vpn,\
    edt_address, add_new_vpn, edit_vpn,select_vpn_name,selection_log_and_pass_by_name
from tkinter import *
from tkinter import ttk
import csv
from ttkthemes import ThemedStyle
import os

main_window = Tk()
main_window.geometry("800x600")
main_window.title("Система управления бевардом")
style = ThemedStyle(main_window)
style.set_theme("arc")
style.configure("Treeview",
                background='#FFF',
                foreground='black',
                rowheight=25,
                fieldbackground='#FFF')

style.map("Treeview",
          background=[('selected','#347083')])







notebook = ttk.Notebook(main_window)
notebook.pack(expand=True, fill=BOTH)


bwd_frame = ttk.Frame(notebook)
vpn_frame = ttk.Frame(notebook)


bwd_frame.pack(fill=BOTH, expand=True)
vpn_frame.pack(fill=BOTH, expand=True)


notebook.add(bwd_frame, text='Бевард')
notebook.add(vpn_frame, text='VPN')


# Create a Treeview Frame

tree_frame = Frame(bwd_frame)
tree_frame.pack(pady=10)

# Create a Treeview Scrollbar

tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT,fill=Y)



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
tree_vpn.column('password',width=250, anchor=CENTER)
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
owner_vpn_label = Label(vpn_label_frame, text="Владелец")
owner_vpn_label.grid(row=0, column=0, padx=10, pady=10)
owner_vpn_entry = Entry(vpn_label_frame)
owner_vpn_entry.grid(row=0, column=1, padx=10, pady=10)
entris_vpn.append(owner_vpn_entry)
name_vpn_label = Label(vpn_label_frame, text="Название сети")
name_vpn_label.grid(row=0, column=2, padx=10, pady=10)
name_vpn_entry = Entry(vpn_label_frame)
name_vpn_entry.grid(row=0, column=3, padx=10, pady=10)
entris_vpn.append(name_vpn_entry)
login_vpn_label = Label(vpn_label_frame, text="Логин")
login_vpn_label.grid(row=0, column=4, padx=10, pady=10)
login_vpn_entry = Entry(vpn_label_frame)
login_vpn_entry.grid(row=0, column=5, padx=10, pady=10)
entris_vpn.append(login_vpn_entry)
password_vpn_label = Label(vpn_label_frame, text="Пароль")
password_vpn_label.grid(row=0, column=6, padx=10, pady=10)
password_vpn_entry = Entry(vpn_label_frame)
password_vpn_entry.grid(row=0, column=7, padx=10, pady=10)
entris_vpn.append(password_vpn_entry)
control_vpn_frame = LabelFrame(vpn_frame, text='Управление списком VPN')
control_vpn_frame.pack(fill=X, padx=20)
# Create add vpn func
def add_vpn():
    owner = owner_vpn_entry.get()
    name = name_vpn_entry.get()
    login = login_vpn_entry.get()
    password = password_vpn_entry.get()
    add_new_vpn(owner, name, login, password)
    for entry in entris_vpn:
        entry.delete(0, 'end')
    view_vpn_table()
# Add button
add_vpn_button = Button(control_vpn_frame, text="Добавить", cursor='hand2', command=add_vpn)
add_vpn_button.grid(row=0, column=0, padx=10, pady=10)
# Button for edit vpn
def edit_select_vpn():
    id = id_vpn_entry.get()
    owner = owner_vpn_entry.get()
    name = name_vpn_entry.get()
    login = login_vpn_entry.get()
    password = password_vpn_entry.get()
    edit_vpn(id, owner, name, login, password)
    view_vpn_table()
edit_vpn_button = Button(control_vpn_frame, text='Изменить', command=edit_select_vpn)
edit_vpn_button.grid(row=0, column=1, padx=10, pady=10)
# Button for delete vpn
def delete_sel_vpn():
    delete_select_vpn(id_vpn_entry.get())
    view_vpn_table()
delete_vpn_button = Button(control_vpn_frame, text="Удалить", cursor='hand2', command=delete_sel_vpn)
delete_vpn_button.grid(row=0, column=2, padx=10, pady=10)
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

tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set,
                    selectmode="extended",
                    columns=('ID','address','ip','owner'),
                    height=10, show='headings')

tree.column("ID", width=30 ,anchor=CENTER)
tree.column('address', width=250, anchor=CENTER)
tree.column('ip', width=250, anchor=CENTER)
tree.column('owner', width=250, anchor=CENTER)

tree.heading("ID", text='ID')
tree.heading("address", text="Адрес")
tree.heading("ip", text='ip')
tree.heading("owner", text='owner')

# Create view for table
def view_table():
    [tree.delete(i) for i in tree.get_children()]
    for row in values_table():
        tree.insert('','end',values=row)
# Call view_table func
view_table()

tree.yview()
tree.pack(side=TOP, fill=X)

# Create Striped Row Tags (doesnt work, idk why)
tree.tag_configure('oddrow', background='yellow')
tree.tag_configure('evenrow', background='blue')

# Add Record Entry Boxes

data_frame = LabelFrame(bwd_frame, text="Запись")
data_frame.pack(fill="x", padx=20)

entris = []
id_entry = Entry(data_frame)
id_entry.grid_remove()
entris.append(id_entry)

address_label = Label(data_frame, text="Адрес")
address_label.grid(row=0, column=0, padx=10, pady=10)
address_entry = Entry(data_frame)
address_entry.grid(row=0, column=1, padx=10, pady=10)
entris.append(address_entry)

ip_label = Label(data_frame, text="IP")
ip_label.grid(row=0, column=2, padx=10, pady=10)
ip_entry = Entry(data_frame)
ip_entry.grid(row=0, column=3, padx=10, pady=10)
entris.append(ip_entry)

owner_label = Label(data_frame, text="Владелец")
owner_label.grid(row=0, column=4, padx=10, pady=10)
owner_entry = Entry(data_frame)
owner_entry.grid(row=0, column=5, padx=10, pady=10)
entris.append(owner_entry)

# Add Buttons for control sql
button_frame = LabelFrame(bwd_frame, text="Управление списком адресов")
button_frame.pack(fill=X, padx=20)

add_button = Button(button_frame, text="Добавить",cursor = 'hand2')
add_button.grid(row=0, column=0, padx=10, pady=10)

# Edit button
def edit_address():
    address = address_entry.get()
    ip = ip_entry.get()
    owner = owner_entry.get()
    id = id_entry.get()
    edt_address(id, address,ip,owner)
    view_table()


edit_button = Button(button_frame, text="Изменить", command=edit_address,cursor = 'hand2')
edit_button.grid(row=0, column=1, padx=10, pady=10)

def remove_command():
    delete_select_address(id_entry.get())
    view_table()
remove_button = Button(button_frame, text="Удалить выбранный", command=remove_command,cursor = 'hand2')
remove_button.grid(row=0, column=2, padx=10, pady=10)

remove_all_button = Button(button_frame, text="Удалить все",cursor = 'hand2')
remove_all_button.grid(row=0, column=3, padx=10, pady=10)

vpn_button = Button(button_frame, text="VPN",cursor = 'hand2')
vpn_button.grid(row=0, column=4, padx=10, pady=10)

#Add Buttons for control panel
button_control_bwd_frame = LabelFrame(bwd_frame, text="Управление панелью")
button_control_bwd_frame.pack(fill=X, padx=20)

# Create radiobutton for vpn connection-------------------------------------------------------------#
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
            create_vbs_en = open('hidden_bat_en.vbs', 'w')
            create_vbs_en.write('Set WshShell = CreateObject("WScript.Shell")\nWshShell.Run chr(34) & "enable_vpn.bat" & Chr(34), 0\nSet WshShell = Nothing')
            create_vbs_dis = open('hidden_bat_dis.vbs', 'w')
            create_vbs_dis.write('Set WshShell = CreateObject("WScript.Shell")\nWshShell.Run chr(34) & "disable_vpn.bat" & Chr(34), 0\nSet WshShell = Nothing')
            create_bat_dis = open('disable_vpn.bat','w')
            create_bat_dis.write(f'@echo OFF\nrasdial {vpn} /DISCONNECT')
            create_bat_en = open('enable_vpn.bat', 'w')
            for obj in selection_log_and_pass_by_name(vpn):
                create_bat_en.write(f'@echo OFF\nrasdial {vpn} {obj[0]} {obj[1]}')
            os.system('start hidden_bat.vbs')

def disable_vpn():
    os.system('start hidden_bat_dis.vbs')

disable_vpn_radiobutton = ttk.Radiobutton(bwd_frame, text='Отключить',variable=state_vpn, value='off', command=disable_vpn)
disable_vpn_radiobutton.pack(padx=0, pady=0, anchor=NW)

for vpn in vpn_list:
    vpn = ttk.Radiobutton(bwd_frame, text=vpn,variable=state_vpn, value=vpn,command=select_vpn)
    vpn.pack(padx=0,pady=0, anchor=NW)
    i=i+1

#--------------------------------------------------------------------------------------------------#
####################################################################################################
# Double click selection---------------------------------------------------------------------------#
def select_record(event):
    # Clear entry boxes
    for entry in entris:
        entry.delete(0, END)
    # Grab record Number
    selected = tree.focus()
    # Grab record values
    values = tree.item(selected, 'values')
    # outpts to entry boxes
    i=0
    for entry in entris:
        entry.insert(0, values[i])
        i=i+1

tree.bind('<Double-Button-1>', select_record)
#--------------------------------------------------------------------------------------------------#



main_window = mainloop()