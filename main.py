import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

import sympy
import math

import datetime
import matplotlib.pyplot as plt

#from scipy.misc import imread

D, Q,A, F, t, p, Ic, h, k, s, d, L, v,I, B,f,W, theta, Y = symbols('D Q A  F  t p Ic h k s d L v I B f W theta Y')
pharmacy = []

class Main(tk.Frame):

    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        db = DB()
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='add.gif')
        btn_open_add_dialog = tk.Button(toolbar, text='Добавить позицию', command=self.open_add_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_add_dialog.pack(side=tk.LEFT)


        self.update_img = tk.PhotoImage(file='update.gif')
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='#d7d8e0', bd=0, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.manage_img = tk.PhotoImage(file='manage2.gif')
        btn_manage_dialog = tk.Button(toolbar, text='Управление запасами', bg='#d7d8e0', bd=0, image=self.manage_img,
                                    compound=tk.TOP, command=lambda: [f() for f in [self.view_combobox,
                                                                                    self.open_manage_dialog]])
        btn_manage_dialog.pack(side=tk.LEFT)

        self.settings_img = tk.PhotoImage(file='settings.gif')
        btn_settings_dialog = tk.Button(toolbar, text='Настройки', bg='#d7d8e0', bd=0, image=self.settings_img,
                                      compound=tk.TOP, command = self.open_settings_dialog)
        btn_settings_dialog.pack(side=tk.LEFT)

        self.patient_img = tk.PhotoImage(file='person.gif')
        btn_patient_dialog = tk.Button(toolbar, text='Пациенты', bg='#d7d8e0', bd=0, image=self.patient_img,
                                        compound=tk.TOP,  command=lambda: [f() for f in [self.view_combobox,self.open_patient_dialog]])
        btn_patient_dialog.pack(side=tk.RIGHT)

        self.tree = ttk.Treeview(self, columns=('ID', 'description', 'costs', 'quantity', 'expiration','demand', 'needLevel'),
                                 height=15, show='headings')

        self.tree.column('ID', width=25, anchor=tk.CENTER)
        self.tree.column('description', width=150, anchor=tk.CENTER)
        self.tree.column('costs', width=70, anchor=tk.CENTER)
        self.tree.column('quantity', width=70, anchor=tk.CENTER)
        self.tree.column('expiration', width=100, anchor=tk.CENTER)
        self.tree.column('demand', width=70, anchor=tk.CENTER)
        self.tree.column('needLevel', width=70, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('description', text='Наименование')
        self.tree.heading('costs', text='Стоимость')
        self.tree.heading('quantity', text='Количество')
        self.tree.heading('expiration', text='Срок годности')
        self.tree.heading('demand', text='Спрос на препарат')
        self.tree.heading('needLevel', text='Необходимость')
        self.tree.pack()

    def records(self, description, costs, quantity, expiration, demand, needLevel):

        self.db.insert_data(description, costs, quantity, expiration, demand, needLevel)
        self.view_records()

    def update_record(self, description, costs, quantity, expiration, demand, needLevel):
        self.db.c.execute('''UPDATE pharma SET description=?, costs=?, quantity=?, expiration=?, demand=?, needLevel=? WHERE ID=?''',
                          (description, costs, quantity, expiration, demand, needLevel, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()



    def view_records(self):
        self.db.c.execute('''SELECT * FROM pharma''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]


    def getValue(self, name):

        self.db.c.execute('''SELECT costs, expiration,  demand, quantity, needLevel FROM pharma WHERE description=?''', (name,))
        for row in self.db.c.fetchall():
            return row

    def view_combobox(self):
        pharmacy.clear()
        self.db.c.execute('''SELECT description FROM pharma''')
        for row in self.db.c.fetchall():
            pharmacy.append(row[0])

    def open_add_dialog(self):
      Child()

    def open_update_dialog(self):
       Update()

    def open_manage_dialog(self):
        Manage()

    def open_settings_dialog(self):
        Settings()
    def open_patient_dialog(self):
        Patients()
    def open_settings_edit_dialog(self):
        Settings_edit()


class Child(tk.Toplevel):
    from tkinter import messagebox
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):

        self.geometry('400x300+400+300')
        self.resizable(False, False)

        label_description = tk.Label(self, text='Наименование:')
        label_description.place(x=50, y=20)
        label_quantity = tk.Label(self, text='Количество:')
        label_quantity.place(x=50, y=50)
        label_price = tk.Label(self, text='Цена:')
        label_price.place(x=50, y=80)
        label_expiration = tk.Label(self, text='Срок годности:')
        label_expiration.place(x=50, y=110)
        label_demand = tk.Label(self, text="Кол-во нуждающихся: ")
        label_demand.place(x=50, y=140)
        label_needLevel = tk.Label(self, text="Уровень необходимости: ")
        label_needLevel.place(x=50, y=170)



        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=200, y=20)

        self.entry_quantity = ttk.Entry(self)
        self.entry_quantity.place(x=200, y=50)

        self.entry_price = ttk.Entry(self)
        self.entry_price.place(x=200, y=80)

        self.entry_expiration = ttk.Entry(self)
        self.entry_expiration.place(x=200, y=110)

        self.entry_demand = ttk.Entry(self)
        self.entry_demand.place(x=200, y=140)

        self.needLevel = tk.IntVar()
        self.first = ttk.Radiobutton(self, text='1', value='1', variable=self.needLevel)
        self.first.place(x=200, y=170)
        self.second = ttk.Radiobutton(self, text='2', value='2', variable=self.needLevel)
        self.second.place(x=200, y=190)
        self.third = ttk.Radiobutton(self, text='3', value='3', variable=self.needLevel)
        self.third.place(x=200, y=210)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=290, y=250)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=210, y=250)
        self.btn_ok.bind('<Button-1>', lambda event: self.check_empty())
        self.grab_set()
        self.focus_set()

    def check_empty(self):
        if (len(self.entry_description.get()) != 0) & (len(self.entry_price.get()) != 0) & (
                len(self.entry_quantity.get()) != 0):
            self.view.records(self.entry_description.get(),
                              self.entry_price.get(),
                              self.entry_quantity.get(), self.entry_expiration.get(), self.entry_demand.get(), self.needLevel.get())
        else:
            self.messagebox.showwarning("   Предупреждение   ", "Вы не ввели значение!")
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('pharma.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS pharma (id integer primary key, description text, costs real, quantity integer,
            expiration date, demand integer, needLevel integer)''')
        self.conn.commit()

    def insert_data(self, description, costs, quantity, expiration, demand, needLevel):
        self.c.execute('''INSERT INTO pharma (description, costs, quantity,expiration, demand,needLevel) VALUES (?, ?, ?, ?, ?,?)''',
                       (description, costs, quantity,expiration, demand,needLevel))

        self.conn.commit()

    def insert_data_person(self, person, reciept, quantity):
        self.c.execute(
            '''INSERT INTO patients (person, reciept, quantity) VALUES (?, ?, ?)''',
            (person, reciept, quantity))

        self.conn.commit()
    def delete_record(self):
        self.c.execute(
            '''DELETE FROM pharma WHERE ID=?''',
            (self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

class AddPatients(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_addpatients()
        self.view = app
        db = DB()
        self.db = db
        p = Patients()


    def init_addpatients(self):

        self.geometry('400x300+400+300')
        self.resizable(False, False)

        label_person = tk.Label(self, text='ФИО:')
        label_person.place(x=50, y=20)
        label_quantity = tk.Label(self, text='Количество:')
        label_quantity.place(x=50, y=80)
        label_reciept = tk.Label(self, text='Назначенный препарат:')
        label_reciept.place(x=50, y=50)

        self._variable = tk.StringVar()
        self.combobox1 = ttk.Combobox(self, state="readonly", values=pharmacy, textvariable=self._variable, )
        self.combobox1.place(x=125, y=50)

        self.entry_person = ttk.Entry(self)
        self.entry_person.place(x=200, y=20)

        self.entry_quantity = ttk.Entry(self)
        self.entry_quantity.place(x=200, y=80)


        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=290, y=250)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=210, y=250)
        self.btn_ok.bind('<Button-1>', lambda event: self.records_person(self.entry_person.get(), self._variable.get(),
                                                                           self.entry_quantity.get()))
        self.grab_set()
        self.focus_set()

    def records_person(self, person, reciept, quantity):
        self.db.insert_data_person(person, reciept, quantity)
        self.view_records_person()

class Patients(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_patients()
        self.view = app
        db = DB()
        self.db = db

    def init_patients(self):

        self.toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        btn_add_patient = tk.Button(self.toolbar, text='Добавить', command=self.open_add_patient_dialog, bg='#d7d8e0',
                                        bd=0, compound=tk.TOP)
        btn_add_patient.pack(side=tk.LEFT)

        self.geometry('400x300+400+300')
        self.resizable(False, False)

        self.tree = ttk.Treeview(self, columns=(
        'ID', 'person', 'reciept', 'quantity'),
                                 height=15, show='headings')

        self.tree.column('ID', width=25, anchor=tk.CENTER)
        self.tree.column('person', width=150, anchor=tk.CENTER)
        self.tree.column('reciept', width=70, anchor=tk.CENTER)
        self.tree.column('quantity', width=70, anchor=tk.CENTER)


        self.tree.heading('ID', text='ID')
        self.tree.heading('person', text='ФИО')
        self.tree.heading('reciept', text='Препарат')
        self.tree.heading('quantity', text='Назначенное кол-во')

        self.tree.pack()

    def records_person(self, person, costs, quantity):
        self.db.insert_data_person(person, reciept, quantity)
        self.view_records_person()

    def update_record_person(self,person, reciept, quantity):
        self.db.c.execute(
            '''UPDATE patients SET person=?, reciept=?, quantity=? WHERE ID=?''',
            (
            person, reciept, quantity, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records_person()

    def view_records_person(self):
        self.db.c.execute('''SELECT * FROM patients''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_add_patient_dialog(self):
        AddPatients()


class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app

    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Сохранить')
        btn_edit.place(x=210, y=250)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_description.get(),
                                                                          self.entry_price.get(),
                                                                          self.entry_quantity.get(),
                                                                          self.entry_expiration.get(),
                                                                          self.entry_demand.get(), self.needLevel.get()))

        self.btn_ok.destroy()

class Manage(tk.Toplevel):
    from tkinter import messagebox
    def __init__(self):
        super().__init__(root)
        self.init_manage()
        self.view = app
        db = DB()
        self.db = db

    def init_manage(self):
        self.title('Управление')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        self._variable = tk.StringVar()
        label_pharmacy = tk.Label(self, text='Выберите препарат')
        label_pharmacy.place(x=125, y=25)
        self.combobox1 = ttk.Combobox(self, state="readonly",  values = pharmacy, textvariable=self._variable, )
        self.combobox1.place(x=125, y=50)

        self.mod = tk.StringVar()
        self.space = ttk.Radiobutton(self,  text= 'Учесть площадь', value = 'space', variable = self.mod)
        self.space.place(x = 125, y=110)
        self.CSL = ttk.Radiobutton(self, text='Учесть уровень обслуживания', value='CSL', variable= self.mod)
        self.CSL.place(x=125, y = 130)
        self.all = ttk.Radiobutton(self, text='Простой случай', value='all', variable=self.mod)
        self.all.place(x=125, y=150)

        self.btn_next = ttk.Button(self, text='Далее')
        self.btn_next.bind('<Button-1>', lambda event:{self.getMethod()})
        self.btn_next.place(x=145, y = 190 )

    def getMethod(self):
        savedData = []
        file_ = open('settings.txt', 'r')
        for line in file_.readlines():
            savedData.append(line)
        self.L = float(savedData[0]     )
        self.A = float(savedData[1])
        self.h = float(savedData[2] )
        self.t = float(savedData[3])
        self.I = float(savedData[4])
        self.Ic = float(savedData[5])
        self.F = float(savedData[6])
        self.W = float(savedData[6])
        selected = self._variable.get()
        print(selected)
        self.p, self.date,self.D, quantity, koef =self.view.getValue(selected)

        method  = self.mod.get()
        self.v = 1
        self.theta = 1

        koef = int(koef)
        if koef == 1:
            self.k = 1
        elif koef==2:
            self.k = 0.75
        elif koef==3:
            self.k = 0.5

        now = datetime.datetime.now()
        start_date = datetime.datetime.strptime(self.date, '%d.%m.%Y')
        self.f = 0.5
        Y=B=0
        self.d = round(365/(start_date - now).days,2) + round( self.D/quantity,2)
        print(self.d)
        self.s=5
        print(self.D, self.d , self.A, self.F, self.t, self.p, self.Ic, self.h, self.k, self.s,  self.L, self.v,self.I)

        if method == 'all':
            Q, sum =self.method_all(self.D, self.d, self.A, self.F, self.t, self.p, self.Ic, self.h, self.k, self.s,  self.L, self.v,self.I)

        elif method == 'CSL':
            Q, sum, B = self.method_space(self.D, self.d, self.A, self.F, self.t, self.p, self.Ic, self.h, self.k, self.s,  self.L, self.v,self.I, self.W, self.f)

        elif method == 'space':
            Q, sum, Y = self.method_CLS(self.D, self.d, self.A, self.F, self.t, self.p, self.Ic, self.h, self.k, self.s,  self.L, self.v,self.I, self.theta)

        print(Q, sum)
        reorderPoint =  int(self.k*self.s*sqrt(self.L) + self.D)
        #img = plt.imread("graph.png")
        #plt.scatter(x, y, zorder=1)
        #plt.imshow(img, zorder=0, extent=[0, 16.0, 0, 14.0])

        fig,ax = plt.subplots(1)
        fig = plt.gcf()
        fig.canvas.set_window_title(selected)
        ax.set_xticklabels([])
        plt.plot([0,20], [reorderPoint,reorderPoint], label='Точка перезаказа '+str(reorderPoint)+' ед.', linewidth=2)
        plt.plot([0, 20], [self.D, self.D], '--r' , label='Критическая точка '+str(self.D)+' ед.', linewidth=2)
        plt.plot([0, 20], [quantity, quantity], '-g', label='Наличие ' +str(quantity)+' ед.', linewidth=2)
        plt.plot([0, 20], [quantity+int(Q), quantity+int(Q)], '-w', label='\n'+'\n'+'Сделать заказ на ' + str(int((Q)*6/10)) +
                                                                          ' ед. '+'\n'+'при достижении точки перезаказа', linewidth=2)
        plt.legend()
        plt.show()


    def method_all(self, D, d, A, F, t, p, Ic, h, k, s,  L, v,I):
        ETC = '(D/Q)*(A+F)+(p*Ic/2)*(Q-2*D*t+((D*t)**2)/Q)+h*Q/2+(h+p*Ic)*k*s*sqrt(L)' \
              '+D*(d*(L**2)+v)-((D*t)**2)*p*I/(2*Q)'

        dIETC_dQ = diff(ETC, Q)
        Q_ = solve(dIETC_dQ, Q)[1]
        Qi = int(eval(str(Q_)))
        ietc= self.IETC(Qi, float(D), float(d), float(A), float(F), float(t), float(p), float(Ic), float(h),
                        float(k), float(s),  float(L), float(v),float(I))
        return (Qi, ietc)

    def method_space(self, D, d, A, F, t, p, Ic, h, k, s,  L, v,I, W,f):
        ETC = '(D/Q)*(A+F)+(p*Ic/2)*(Q-2*D*t+((D*t)**2)/Q)+h*Q/2+(h+p*Ic)*k*s*sqrt(L)' \
              '+D*(d*(L**2)+v)-((D*t)**2)*p*I/(2*Q)+B*(f*Q-W)'

        B = symbols('B')
        dIETC_dQ = diff(ETC, Q)
        Q_ = solve(dIETC_dQ, Q)[1]
        B_ =   str(Q_) + '-W/f'
        _B = solve(B_,B)[0]
        _B = eval(str(_B))
        B = _B
        Qi = eval(str(Q_))
        ietc_B = self.IETC_B(Qi, float(D), float(d), float(A), float(F), float(t), float(p), float(Ic), float(h),
                        float(k), float(s),  float(L), float(v),float(I), float(W), float(f), float(B))
        return (Qi, ietc_B, B)

    def method_CLS(self, D, d, A, F, t, p, Ic, h, k, s,  L, v,I, theta):
        ETC =  '(D/Q)*(A+F)+(p*Ic/2)*(Q-2*D*t+((D*t)**2)/Q)+h*Q/2+(h+p*Ic)*k*s*sqrt(L)' \
               '+D*(d*(L**2)+v)-((D*t)**2)*p*I/(2*Q)+Y*theta*Q'
        Y = symbols('Y')
        dIETC_dQ = diff(ETC, Q)
        Q_ = solve(dIETC_dQ, Q)[1]
        Y_ = str(Q_) + '+s*sqrt(L)'
        _Y = solve(Y_, Y)[0]
        _Y = eval(str(_Y))
        Y = _Y
        Qi = eval(str(Q_))
        ietc_Y= self.IETC_Y(Qi, float(D), float(d), float(A), float(F), float(t), float(p), float(Ic), float(h),
                        float(k), float(s),  float(L), float(v),float(I), float(theta), float(Y))
        return (Qi, ietc_Y, Y)

    def IETC(self, Qi, D, d, A, F, t, p, Ic, h, k, s,  L, v,I ):
        return ((D/Qi)*(A+F)+(p*Ic/2)*(Qi-2*D*t+((D*t)**2)/Qi)+h*Qi/2+(h+p*Ic)*k*s*sqrt(L)+D*(d*(L**2)+v)-((D*t)**2)*p*I/(2*Qi))
    def IETC_B (self, Qi, D, d, A, F, t, p, Ic, h, k, s,  L, v,I, W,f, B):
        return ((D/Qi)*(A+F)+(p*Ic/2)*(Qi-2*D*t+((D*t)**2)/Qi)+h*Qi/2+(h+p*Ic)*k*s*sqrt(L)+D*(d*(L**2)+v)-((D*t)**2)*p*I/(2*Qi)+B*(f*Qi-W))
    def IETC_Y(self, Qi, D, d, A, F, t, p, Ic, h, k, s,  L, v,I, theta, Y):
        return ((D/Qi)*(A+F)+(p*Ic/2)*(Qi-2*D*t+((D*t)**2)/Qi)+h*Qi/2+(h+p*Ic)*k*s*sqrt(L)+D*(d*(L**2)+v)-((D*t)**2)*p*I/(2*Qi)+Y*theta*Qi)



class Settings(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_settings()
        self.view = app

    def init_settings(self):
        self.title('Настройки')
        self.geometry('400x300+400+300')
        self.resizable(False, False)
        savedData = []
        file_ = open('settings.txt', 'r')
        for line in file_.readlines():
            savedData.append(line)

        label_leadtime = tk.Label(self, text='Время выполнения заказа')
        label_leadtime.place(x=40, y=25)
        self.leadtime = tk.Label(self, text = savedData[0])
        self.leadtime.place(x=230, y=25)

        label_orderingCost = tk.Label(self,  text='Расходы на организацию заказа')
        label_orderingCost.place(x=40, y=50)
        self.orderingCost = tk.Label(self, text=savedData[1])
        self.orderingCost.place(x=230, y=50)

        label_holdingCost = tk.Label(self, text='Стоимость хранения в год')
        label_holdingCost.place(x=40, y=75)
        self.holdingCost = tk.Label(self, text=savedData[2])
        self.holdingCost.place(x=230, y=75)


        label_creditPeriod = tk.Label(self,  text='Кредитный период')
        label_creditPeriod.place(x=40, y=100)
        self.creditPeriod = tk.Label(self,text=savedData[3])
        self.creditPeriod.place(x=230, y=100)

        label_deposit = tk.Label(self,text='Общая процентная ставка')
        label_deposit.place(x=40, y=125)
        self.deposit = tk.Label(self,text=savedData[4])
        self.deposit.place(x=230, y=125)

        label_act = tk.Label(self, text='Процент за акции')
        label_act.place(x=40, y=150)
        self.act = tk.Label(self, text=savedData[5])
        self.act.place(x=230, y=150)

        label_transport = tk.Label(self, text='Транспортные расходы')
        label_transport.place(x=40, y=175)
        self.transport = tk.Label(self, text=savedData[6])
        self.transport.place(x=230, y=175)

        label_floor = tk.Label(self, text='Площадь места хранения')
        label_floor.place(x=40, y=200)
        self.floor = tk.Label(self, text=savedData[7])
        self.floor.place(x=230, y=200)


        self.btn_save = ttk.Button(self, text='Редактировать')
        self.btn_save.bind('<Button-1>', lambda event: {self.view.open_settings_edit_dialog()})
        self.btn_save.place(x=70, y=260)
        btn_cancel_save = ttk.Button(self, text='Закрыть',  command=self.destroy)
        btn_cancel_save.place(x=200, y=260)



class Settings_edit (tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_settings_edit()
        self.view = app

    def init_settings_edit(self):
        self.title('Настройки')
        self.geometry('400x300+400+300')
        self.resizable(False, False)


        self.inp_L = tk.StringVar()
        label_leadtime = tk.Label(self, text='Время выполнения заказа')
        label_leadtime.place(x=40, y=25)
        self.entry_leadtime = ttk.Entry(self, textvariable = self.inp_L)
        self.entry_leadtime.place(x=230, y=25)

        self.inp_A = tk.StringVar()
        label_orderingCost = tk.Label(self,  text='Расходы на организацию заказа')
        label_orderingCost.place(x=40, y=50)
        self.entry_orderingCost = ttk.Entry(self, textvariable = self.inp_A)
        self.entry_orderingCost.place(x=230, y=50)

        self.inp_h = tk.StringVar()
        label_holdingCost = tk.Label(self, text='Стоимость хранения в год')
        label_holdingCost.place(x=40, y=75)
        self.entry_holdingCost = ttk.Entry(self, textvariable = self.inp_h)
        self.entry_holdingCost.place(x=230, y=75)

        self.inp_t = tk.StringVar()
        label_creditPeriod = tk.Label(self,  text='Кредитный период')
        label_creditPeriod.place(x=40, y=100)
        self.entry_creditPeriod = ttk.Entry(self,textvariable=self.inp_t)
        self.entry_creditPeriod.place(x=230, y=100)

        self.inp_I = tk.StringVar()
        label_deposit = tk.Label(self,text='Общая процентная ставка')
        label_deposit.place(x=40, y=125)
        self.entry_deposit = ttk.Entry(self,textvariable = self.inp_I)
        self.entry_deposit.place(x=230, y=125)

        self.inp_Ic = tk.StringVar()
        label_act = tk.Label(self, text='Процент за акции')
        label_act.place(x=40, y=150)
        self.entry_act = ttk.Entry(self, textvariable=self.inp_Ic)
        self.entry_act.place(x=230, y=150)

        self.inp_F = tk.StringVar()
        label_transport = tk.Label(self, text='Транспортные расходы')
        label_transport.place(x=40, y=175)
        self.entry_transport = ttk.Entry(self, textvariable=self.inp_F)
        self.entry_transport.place(x=230, y=175)

        self.inp_W = tk.StringVar()
        label_floor = tk.Label(self, text='Площадь места хранения')
        label_floor.place(x=40, y=200)
        self.entry_floor = ttk.Entry(self, textvariable=self.inp_W)
        self.entry_floor.place(x=230, y=200)

        self.btn_save = ttk.Button(self, text='Сохранить')
        self.btn_save.bind('<Button-1>', lambda event: {self.saveInput()})
        self.btn_save.place(x=70, y=240)
        btn_cancel_save = ttk.Button(self, text='Закрыть',  command=self.destroy)
        btn_cancel_save.place(x=200, y=240)

    def saveInput(self):
        I = self.inp_I.get()
        Ic = self.inp_Ic.get()
        L= self.inp_L.get()
        t = self.inp_t.get()
        A = self.inp_A.get()
        h = self.inp_h.get()
        F = self.inp_F.get()
        W = self.inp_W.get()
        file_=open('settings.txt', 'w', encoding='utf-8')
        file_.write(L + '\n'+A+ '\n'+h+'\n'+t+ '\n'+I+'\n'+Ic+'\n'+F+'\n'+W)

        root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Управление запасами лекарств")
    root.geometry("650x450+300+200")
    root.resizable(False, False)
    root.mainloop()

