##### import
import csv
from tkinter import ttk
from tkinter import simpledialog
from tkinter import *
from datetime import *
import json
import os
from urllib.request import urlopen
from PIL import Image, ImageTk
import base64
import webbrowser


default_config = {
	'buttom_color':'red',
	'background_color':'white',
	'side_color':'lightgrey',
	'font_name':'Cordia New',
	'currency':'บาท'
	}

#####function
def callback(url):
    webbrowser.open_new(url)

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

def update_config():

	##try loading config from file
	try:
		global config
		f = open('config.json','r+', encoding='utf-8', errors='ignore')
		config = json.load(f)
	#if file doesnt exist , create one and use default config as config for now
	except FileNotFoundError:
		f = open('config.json','x',encoding='utf-8')
		json.dump(default_config,f)
		config = default_config

	#configssss

	global bg_color_buttom,bg_color,font_name,bg_color_side,currency


	bg_color = config['background_color']
	bg_color_buttom = config['buttom_color']
	font_name = config['font_name']
	bg_color_side = config['side_color']
	currency = config['currency']

	print(config)

def write_config(config):
	#if user wanna change config , delete the whole config and recreate it with data that user provided 
	os.remove('config.json')
	f = open('config.json','w', encoding='utf-8', errors='ignore')
	json.dump(config,f)
	#need restart for config to work

def Expense(zz,event=None):
	if zz == 'e':
		#try to put all data into the csv
		try:
			n = str(v_productname.get())
			p = float(v_productprice.get())
			a = float(v_productamount.get())
			tp = a*p
			time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			v_result.set(f'คุณกำลังบันทึกรายการ: {n} จำนวน {a} ชิ้น ราคาชิ้นละ {p:,.2f} บาท ราคารวมเท่ากับ {tp} บาท') 
			data = [n,p,a,tp,time]
			#name,priceperpiece,amount,totalprice,datetime
			write_expense_to_csv(data,zz)
		#but if valueerror (user provided wrong data or None) then tell them to input correctly
		except ValueError:
			v_result.set('กรุณาใส่ข้อมูลให้ถูกต้อง')

		#reset ตัวแปร because we saved the data
		v_productname.set('')
		v_productamount.set('')
		v_productprice.set('')

		#ทำให้ cursor กลับไปช่องแรก
		E1expense.focus()

	elif zz == 'i':
		#try to put all data into the csv
		try:
			n = str(vi_productname.get())
			p = float(vi_productprice.get())
			a = float(vi_productamount.get())
			tp = a*p
			time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			v_result.set(f'คุณกำลังบันทึกรายการ: {n} จำนวน {a} ชิ้น ราคาชิ้นละ {p:,.2f} บาท ราคารวมเท่ากับ {tp} บาท') 
			data = [n,p,a,tp,time]
			#name,priceperpiece,amount,totalprice,datetime
			write_expense_to_csv(data,zz)
			#but if valueerror (user provided wrong data or None) then tell them to input correctly
		except ValueError:
			vi_result.set('กรุณาใส่ข้อมูลให้ถูกต้อง')

		#reset ตัวแปร because we saved the data
		vi_productname.set('')
		vi_productamount.set('')
		vi_productprice.set('')

		#ทำให้ cursor กลับไปช่องแรก
		E1income.focus()
		summarize()

def write_expense_to_csv(data,zz):

	if zz == 'e':
		filename = 'expensedata.csv'
		table_expense.insert('','end',value=data)

	elif zz == 'i':
		filename = 'incomedata.csv'
		table_income.insert('','end',value=data)

	file = open(filename,'a',newline='',encoding='utf-8')
	fw = csv.writer(file) #fw = file writer
	fw.writerow(data)
	print(f'รายการ : {data[0]}')
	print('wrote data to csv')
	summarize()

def update_expense_table(zz):
	if zz == 'e':
		filename = 'expensedata.csv'
		table = table_expense
	elif zz == 'i':
		filename = 'incomedata.csv'
		table = table_income

	#try getting data from csv
	try: 
		with open(filename,newline='',encoding='utf-8') as file:
			fr = csv.reader(file)
			for data in fr:
				table.insert('','end',value=data)

	#if expensedata.csv doesnt exist, create one
	except FileNotFoundError:
		f = open(filename,'x',encoding='utf-8')
		update_expense_table(zz)

def FONT(size):
	return (font_name,size+2)

def set_text_entry(text,e):
	#setting text into entry for the preference
	e.delete(0,END)
	e.insert(0,text)
	return

def window():
	global GUI,window_width,window_height
	GUI = Tk()
	GUI.resizable(False, False)
	window_width = 1400
	window_height = 700
	screen_height = GUI.winfo_screenheight()
	screen_width = GUI.winfo_screenwidth()
	x = screen_width/2 - window_width/2
	y = screen_height/2 - window_height/2
	GUI.title('บัญชีรายรับรายจ่าย')
	GUI.geometry(f'{window_width}x{window_height}+{x:.0f}+{y:.0f}')
	print(f'User\'s screen resolution is {screen_width}x{screen_height}')
	GUI.configure(bg=bg_color)
	GUI.bind('<F12>',lambda x: GUI.destroy())
	GUI.bind('<F5>',preferences)

def preferences_apply():
	#getting the data from preferences entry and putting that into config
	config["background_color"]=p_entry_1.get()
	config["buttom_color"]=p_entry_2.get()
	config["side_color"]=p_entry_3.get()
	print(config)
	write_config(config)
	p_result.set('บันทึกการตั้งค่าแล้ว จะใช้งานในการเปิดครั้งหน้า')

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
	p_label_3 = Label(p_frame,text='Side background color',font=FONT(18))
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
	#set_text_entry(font_name,p_entry_4)
	set_text_entry(bg_color_side,p_entry_3)

def menubar():
	menubar = Menu(GUI)
	GUI.config(menu=menubar)
	filemenu = Menu(menubar,tearoff=0)
	menubar.add_cascade(label='File',menu=filemenu)
	filemenu.add_command(label='Exit (F12)',command=GUI.quit)

	viewmenu = Menu(menubar,tearoff=0)
	menubar.add_cascade(label='View',menu=viewmenu)
	viewmenu.add_command(label='Preferences (F5)',command=lambda : preferences())

def tab():
	global tab1,tab2

	tab_parent = ttk.Notebook(GUI)
	tab_parent.pack(fill=BOTH, expand=1)

	tab1 = ttk.Frame(tab_parent, style = 'TFrame')
	tab2 = ttk.Frame(tab_parent, style = 'TFrame')

	tab_parent.add(tab1, text="รายจ่าย")
	tab_parent.add(tab2, text="รายรับ")

def widgets_expense():

	global v_productname,v_productamount,v_productprice,v_result,table_expense,E1expense
	F1 = Frame(tab1,background=bg_color)
	F1.place(x=0,y=10)

	F_entry_label = Frame(tab1,background=bg_color)
	F_entry_label.place(x=270,y=10)

	F2 = Frame(tab1,background=bg_color)
	F2.place(x=400,y=10)

	F3 = Frame(tab1,background=bg_color)
	F3.place(x=680,y=10)

	F4 = Frame(tab1,background=bg_color)
	F4.place(x=0,y=150)

	Fbuttom = Frame(tab1,width=window_width,height=50,bg=bg_color_buttom)
	Fbuttom.place(x=0,y=window_height-80)

	#####defineing var for getting data from entry
	v_productname = StringVar()
	v_productamount = StringVar()
	v_productprice = StringVar()

	L_name = ttk.Label(F1,text=f'บัญชีรายรับรายจ่ายของคุณ\n{name}',background=bg_color,font=FONT(20),foreground='green')
	L_name.grid(row=0,column=0)

	L1 = ttk.Label(F_entry_label,text='รายการ',background=bg_color,font=FONT(18))
	L1.grid(row=1,column=0)
	L2 = ttk.Label(F_entry_label,text='จำนวน',background=bg_color,font=FONT(18))
	L2.grid(row=2,column=0)
	L3 = ttk.Label(F_entry_label,text='ราคาต่อหน่วย',background=bg_color,font=FONT(18))
	L3.grid(row=3,column=0)


	E1expense = ttk.Entry(F2, textvariable=v_productname, width=20, font=FONT(17))
	E1expense.grid(row=1,column=1)
	E2 = ttk.Entry(F2, textvariable=v_productamount, width=20, font=FONT(17))
	E2.grid(row=2,column=1)
	E3 = ttk.Entry(F2, textvariable=v_productprice, width=20, font=FONT(17))
	E3.bind('<Return>',lambda event, x='e':Expense(x))
	E3.grid(row=3,column=1)

	B1 = ttk.Button(F3,text='บันทึก',style='my.TButton', command=lambda x = 'e': Expense(x))
	B1.grid(row=1,column=2,ipadx=20,ipady=7)

	B2 = ttk.Button(F3,text='ลบรายการที่เลือก',style='my.TButton', command=lambda x = 'e': delete_selected(x))
	B2.grid(row=2,column=2,ipadx=11,ipady=7)

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

	update_expense_table('e')

	for i in range(len(header)):
		table_expense.heading(header[i],text=header[i])
		table_expense.column(header[i],minwidth=0,width=180)

def widgets_income():

	global vi_productname,vi_productamount,vi_productprice,vi_result,table_income,E1income
	F1 = Frame(tab2,background=bg_color)
	F1.place(x=0,y=10)

	F_entry_label = Frame(tab2,background=bg_color)
	F_entry_label.place(x=270,y=10)

	F2 = Frame(tab2,background=bg_color)
	F2.place(x=400,y=10)

	F3 = Frame(tab2,background=bg_color)
	F3.place(x=680,y=10)

	F4 = Frame(tab2,background=bg_color)
	F4.place(x=0,y=150)

	Fbuttom = Frame(tab2,width=window_width,height=50,bg=bg_color_buttom)
	Fbuttom.place(x=0,y=window_height-80)

	#####defineing var for getting data from entry
	vi_productname = StringVar()
	vi_productamount = StringVar()
	vi_productprice = StringVar()

	L_name = ttk.Label(F1,text=f'บัญชีรายรับรายจ่ายของคุณ\n{name}',background=bg_color,font=FONT(20),foreground='green')
	L_name.grid(row=0,column=0)

	L1 = ttk.Label(F_entry_label,text='รายการ',background=bg_color,font=FONT(18))
	L1.grid(row=1,column=0)
	L2 = ttk.Label(F_entry_label,text='จำนวน',background=bg_color,font=FONT(18))
	L2.grid(row=2,column=0)
	L3 = ttk.Label(F_entry_label,text='ราคาต่อหน่วย',background=bg_color,font=FONT(18))
	L3.grid(row=3,column=0)


	E1income = ttk.Entry(F2, textvariable=vi_productname, width=20, font=FONT(17))
	E1income.grid(row=1,column=1)
	E2 = ttk.Entry(F2, textvariable=vi_productamount, width=20, font=FONT(17))
	E2.grid(row=2,column=1)
	E3 = ttk.Entry(F2, textvariable=vi_productprice, width=20, font=FONT(17))
	E3.bind('<Return>',lambda event, x='e':Expense(x))
	E3.grid(row=3,column=1)

	B1 = ttk.Button(F3,text='บันทึก',style='my.TButton', command=lambda x = 'i': Expense(x))
	B1.grid(row=1,column=2,ipadx=20,ipady=7)

	B2 = ttk.Button(F3,text='ลบรายการที่เลือก',style='my.TButton', command=lambda x = 'i': delete_selected(x))
	B2.grid(row=2,column=2,ipadx=11,ipady=7)

	####RESULT LABEL
	vi_result = StringVar()
	R1 = ttk.Label(Fbuttom, textvariable= vi_result,background=bg_color_buttom, font=FONT(14),foreground = 'white')
	R1.place(x=5,y=7)

	#####Treeview

	header = ['รายการ','ราคาต่อหน่วย','จำนวน','ราคารวม','วัน-เวลา']

	table_income = ttk.Treeview(F4,column=header,show='headings',height=30)
	table_income.pack()

	style_treeview = ttk.Style()
	style_treeview.configure("Treeview.Heading", font=FONT(12))
	style_treeview.configure("Treeview", font=FONT(12))

	update_expense_table('i')

	for i in range(len(header)):
		table_income.heading(header[i],text=header[i])
		table_income.column(header[i],minwidth=0,width=180)

def delete_selected(expense_income):
	if expense_income == 'e':
		table = table_expense
	else:
		table = table_income
		
	selected_item = table.selection()[0]
	table.delete(selected_item)

def summarize():
	global frame_side

	frame_side = Frame(GUI,background=bg_color_side,width=500,height=window_height)
	frame_side.place(x=904,y=33)

	total_expense = 0
	total_income = 0

	try:
		with open('expensedata.csv',newline='',encoding='utf-8',errors='ignore') as file:
			fr = csv.reader(file) #fw = file writer
			for data in fr:
				total_expense += float(data[3])	
		with open('incomedata.csv',newline='',encoding='utf-8',errors='ignore') as file:
			fr = csv.reader(file) #fw = file writer
			for data in fr:
				total_income += float(data[3])
		skip = False
	except FileNotFoundError:
		file = open('expensedata.csv','x')
		file = open('incomedata.csv','x')

		skip = True

	if not skip:
		summary_label = Label(frame_side,font=FONT(22),bg=bg_color_side,text=f'คุณมีรายรับ = {total_income} {currency}\nคุณมีรายจ่าย = {total_expense} {currency}\nเงินเหลือ = {total_income-total_expense} {currency}')
		summary_label.place(x=155,y=20)

	link1 = Label(frame_side, text="My github", font=FONT(28), fg="red", bg=bg_color_side, cursor="hand2")
	link1.place(x=185,y=500)
	link1.bind("<Button-1>", lambda e: callback("https://github.com/whydude"))

def icon():
	'''global image
			
				url = 'https://raw.githubusercontent.com/whydude/money/master/1.gif'
				raw_image = urlopen(url).read()
				b64_data = base64.encodebytes(raw_image)
				photo = PhotoImage(data=b64_data)
			
				canvas = Canvas(frame_side)
				canvas.place(x=55,y=300)
			
				canvas.create_image(20, 20, anchor=NW, image = photo)'''

	pass

#actually doing thing

def hide_files():
	file_list = ['expensedata.csv','incomedata.csv','config.json','name.txt']
	for i in file_list:
		os.system(f"attrib +h {i}" )

def show_files():
	file_list = ['expensedata.csv','incomedata.csv','config.json','name.txt']
	for i in file_list:
		os.system(f"attrib -h {i}" )

update_config()

name = check_name()

window()
##styles
style_button = ttk.Style()
style_button.configure('my.TButton', font=FONT(18))
style_tab = ttk.Style()
style_tab.configure('TNotebook.Tab', font=FONT(12), bg=bg_color)
style_tframe = ttk.Style()
style_tframe.configure('TFrame',background=bg_color)

menubar()

tab()

summarize()

icon()

widgets_expense()

widgets_income()

hide_files()

GUI.mainloop()