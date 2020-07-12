##### import
import csv
from tkinter import ttk
from tkinter import simpledialog
from tkinter import *
from datetime import *
import json
import os
import os.path


#####function
def check_name():
	try:
		f = open("name.txt", "r", encoding="utf-8")
		return f.read()
	except FileNotFoundError:
		f = open("name.txt", "w", encoding="utf-8")
		namegui = Tk() 
		namegui.withdraw()
		name = simpledialog.askstring('กรอกข้อมูล','ใส่ชื่อของคุณ',parent=namegui)
		f.write(name)
		namegui.destroy()
		return name

default_config = {
	'buttom_color':'red',
	'background_color':'white',
	'font_name':'Cordia New'
	}


def update_config():

	try:
		global config
		f = open('config.json','r+', encoding='utf-8', errors='ignore')
		config = json.load(f)

	except FileNotFoundError:
		f = open('config.json','x',encoding='utf-8')
		json.dump(default_config,f)
		config = default_config



	global bg_color_buttom,bg_color,font_name
	bg_color = config['background_color']
	bg_color_buttom = config['buttom_color']
	font_name = config['font_name']

def write_config(config):
	os.remove('config.json')
	f = open('config.json','w', encoding='utf-8', errors='ignore')
	json.dump(config,f)
	# Do something with the file


def Expense(event=None):
	try:
		n = v_productname.get()
		p = float(v_productprice.get())
		a = float(v_productamount.get())
		tp = a*p
		time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		v_result.set(f'คุณกำลังบันทึกรายการ: {n} จำนวน {a} ชิ้น ราคาชิ้นละ {p:,.2f} บาท ราคารวมเท่ากับ {tp} บาท') 

		#data
		data = [n,p,a,tp,time]

		#save data to csv
		#name,priceperpiece,amount,totalprice,datetime
		write_expense_to_csv(data)
		add_expense_list(data)

	except ValueError:
		v_result.set('กรุณาใส่ข้อมูลให้ถูกต้อง')

	#reset ตัวแปร
	v_productname.set('')
	v_productamount.set('')
	v_productprice.set('')

	#ทำให้ cursor กลับไปช่องแรก
	E1.focus()
	
def write_expense_to_csv(ep):
	with open('expensedata.csv','a',newline='',encoding='utf-8') as file:
		fw = csv.writer(file) #fw = file writer
		fw.writerow(ep)
	print(f'รายการ : {ep[0]}')
	print('wrote data to csv')

def add_expense_list(data):
	table_expense.insert('','end',value=data)

def update_expense_table():
	try: 
		with open('expensedata.csv',newline='',encoding='utf-8') as file:
			fr = csv.reader(file)
			for dt in fr:
				table_expense.insert('','end',value=dt)
	except FileNotFoundError:
		f = open('expensedata.csv','x',encoding='utf-8')
		update_expense_table()

def window():
	global window_width,window_height
	window_width = 900
	window_height = 700
	screen_height = GUI.winfo_screenheight()
	screen_width = GUI.winfo_screenwidth()
	x = screen_width/2 - window_width/2
	y = screen_height/2 - window_height/2
	GUI.title('บัญชีรายรับรายจ่าย')
	GUI.geometry(f'{window_width}x{window_height}+{x:.0f}+{y:.0f}')
	print(f'User\'s screen resolution is {screen_width}x{screen_height}')
	GUI.bind('<Return>',Expense)
	GUI.configure(bg=bg_color)
	GUI.bind('<F12>',lambda x: GUI.destroy())
	GUI.bind('<F5>',preferences)

def set_text_entry(text,e):
    e.delete(0,END)
    e.insert(0,text)
    return

def preferences_apply():
	config["background_color"]=p_entry_1.get()
	config["buttom_color"]=p_entry_2.get()
	config["font_name"]=p_entry_3.get()
	print(config)
	write_config(config)
	p_result.set('บันทึกการตั้งค่าแล้ว จะใช้งานในการเปิดครั้งหน้า')

def FONT(size):
	return (font_name,size+2)

def preferences(event=None):
	global p_label_r,p_result,p_entry_1,p_entry_2,p_entry_3

	p_result = StringVar()

	#configure gui
	p_gui = Tk()
	p_gui.geometry('600x500')
	p_frame = Frame(p_gui)
	p_frame2 = Frame(p_gui)
	p_frame.grid(row=0,column=0)
	p_frame2.place(x=0,y=450)
	p_label_1 = Label(p_frame,text='Main background_color',font=FONT(18))
	p_label_1.grid(row=0,column=0)
	p_entry_1 = Entry(p_frame,font=FONT(18))
	p_entry_1.grid(row=0,column=1)
	p_label_2 = Label(p_frame,text='Buttom background_color',font=FONT(18))
	p_label_2.grid(row=1,column=0)
	p_entry_2 = Entry(p_frame,font=FONT(18))
	p_entry_2.grid(row=1,column=1)
	p_label_3 = Label(p_frame,text='Font name',font=FONT(18))
	p_label_3.grid(row=2,column=0)
	p_entry_3 = Entry(p_frame,font=FONT(18))
	p_entry_3.grid(row=2,column=1)
	p_label_r = Label(p_frame2,textvariable=p_result,font=FONT(18))
	p_label_r.grid(row=0,column=0)

	#ttk button style for preferences gui
	style_button = ttk.Style()
	style_button.configure('my.TButton', font=FONT(18))

	p_button_save = ttk.Button(p_frame,text='Apply',style='my.TButton',command = lambda: preferences_apply()) 
	p_button_save.grid(row=10,column=1)

	set_text_entry(bg_color,p_entry_1)
	set_text_entry(bg_color_buttom,p_entry_2)
	set_text_entry(font_name,p_entry_3)

def menubar():
	menubar = Menu(GUI)
	GUI.config(menu=menubar)
	filemenu = Menu(menubar,tearoff=0)
	menubar.add_cascade(label='File',menu=filemenu)
	filemenu.add_command(label='Exit (F12)',command=GUI.quit)

	viewmenu = Menu(menubar,tearoff=0)
	menubar.add_cascade(label='View',menu=viewmenu)
	viewmenu.add_command(label='Preferences (F5)',command=lambda : preferences())





name = check_name()

update_config()

#####TKINTER
GUI = Tk()

window()

menubar()


#TKFRAME
F1 = Frame(GUI,background=bg_color)
F1.place(x=10,y=5)

F_entry_label = Frame(GUI,background=bg_color)
F_entry_label.place(x=270,y=10)

F2 = Frame(GUI,background=bg_color)
F2.place(x=400,y=10)

F3 = Frame(GUI,background=bg_color)
F3.place(x=680,y=10)

F4 = Frame(GUI,background=bg_color)
F4.place(x=0,y=150)

Fbuttom = Frame(GUI,width=window_width,height=50,bg=bg_color_buttom)
Fbuttom.place(x=0,y=window_height-40)

#####defineing var for getting data from entry
v_productname = StringVar()
v_productamount = StringVar()
v_productprice = StringVar()

L_name = ttk.Label(F1,text=f'บัญชีรายรับรายจ่ายของคุณ\n{name}',background=bg_color,font=FONT(20),foreground='green')
L_name.grid(row=0,column=0)

L1 = ttk.Label(F_entry_label,text='ชื่อสินค้า',background=bg_color,font=FONT(18))
L1.grid(row=1,column=0)
L2 = ttk.Label(F_entry_label,text='จำนวน',background=bg_color,font=FONT(18))
L2.grid(row=2,column=0)
L3 = ttk.Label(F_entry_label,text='ราคาต่อชิ้น',background=bg_color,font=FONT(18))
L3.grid(row=3,column=0)


E1 = ttk.Entry(F2, textvariable=v_productname, width=20, font=FONT(17))
E1.grid(row=1,column=1)
E2 = ttk.Entry(F2, textvariable=v_productamount, width=20, font=FONT(17))
E2.grid(row=2,column=1)
E3 = ttk.Entry(F2, textvariable=v_productprice, width=20, font=FONT(17))
E3.bind('<Return>',Expense)
E3.grid(row=3,column=1)

style_button = ttk.Style()
style_button.configure('my.TButton', font=FONT(18))

B1 = ttk.Button(F3,text='บันทึก',style='my.TButton', command=lambda : Expense())
B1.grid(row=1,column=2,ipadx=20,ipady=37)

####RESULT LABEL
v_result = StringVar()
R1 = ttk.Label(Fbuttom, textvariable= v_result,background=bg_color_buttom, font=FONT(14),foreground = 'white')
R1.place(x=5,y=7)

#####Treeview

header = ['รายการ','ราคาต่อหน่วย','จำนวน','ราคารวม','วัน-เวลา']

table_expense = ttk.Treeview(F4,column=header,show='headings',height=30)
table_expense.pack()

style_treeview = ttk.Style()
style_treeview.configure("Treeview.Heading", font=FONT(12))
style_treeview.configure("Treeview", font=FONT(12))


update_expense_table()

for i in range(len(header)):
	table_expense.heading(header[i],text=header[i])
	table_expense.column(header[i],minwidth=0,width=int(window_width/5))






#####lastly mainloop
GUI.mainloop()