#!/usr/bin/env python
#coding:utf8
import tkinter as tk
import time
import client
import tkSimpleDialog as dl  
import tkinter.messagebox

TOTAL = 100
Current = 0
headsets = []

def auto():
    for x in range (TOTAL):
        s = client.Headset(x)
        s.uuid = str(100000000000 + x) 
        s.sd = 8
        s.level = 83
        app.create_item_bar(x, s.uuid, s.sd) 
        s.viewer(app.update_item_status)
        headsets.append(s)

def create():
    global Current
    guess = myDialog(app.main)  
    s = client.Headset(Current)
    s.uuid, s.level, s.sd  = guess.result
    app.create_item_bar(Current, s.uuid, s.sd) 
    s.viewer(app.update_item_status)
    headsets.append(s)
    Current += 1

def start_headset():
    for  s in headsets:
        s.start()

def exit_loop():
    for  s in headsets:
        s.join()

class myDialog(dl.Dialog):
    def body(self, master):
        self.title("添加耳机设备")
        tk.Label(master, text="设备序列号:").grid(row=0)
        tk.Label(master, text="电池电量:").grid(row=1)
        tk.Label(master, text="内存大小:").grid(row=2)

        self.e1 = tk.Entry(master)
        self.e2 = tk.Entry(master)
        self.e3 = tk.Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        return self.e1 # initial focus

    def apply(self):
        uuid = self.e1.get()
        level = int(self.e2.get())
        sd = int(self.e3.get())

        self.result = uuid,level, sd # or something

def Contact():
    tkinter.messagebox.showinfo('联系我们','广州市黄浦区天丰路3号启明大厦1楼广州启辰电子公司')

def About():
    tkinter.messagebox.showinfo('关于我们','广州启辰电子公司')

class App():
   def __init__(self):
       self.main = tk.Tk()
       self.main.title("耳机模拟器")
       self.main.geometry('1080x720') 
       self.vars = dict()
       self.labels = dict()

   def create_menu(self):
       menubar = tk.Menu(self.main, font=("Bold", 12))
       fmenu = tk.Menu(menubar)
       fmenu.add_command(label='自动', command=auto)
       fmenu.add_command(label='新建', command=create)
       fmenu.add_command(label='启动', command=start_headset)
       fmenu.add_command(label='退出', command=exit_loop)
 
       amenu = tk.Menu(menubar)
       amenu.add_command(label='关于我们', command=About)
       amenu.add_command(label='联系我们', command=Contact)
 
       menubar.add_cascade(label='文件',menu=fmenu)
       menubar.add_cascade(label='关于',menu=amenu)
 
       self.main.config(menu=menubar)

   def create_label(self):
       frame = tk.Frame(self.main)
       label = tk.Label(frame, font=("Arial", 11), width=15, text='序号',anchor="center")	
       label.pack(side="left")
       label = tk.Label(frame, font=("Arial", 11), width=15, text='设备序列号', anchor="center")	
       label.pack(side="left")
       label = tk.Label(frame, font=("Arial", 11), width=15, text='网络', anchor="center")	
       label.pack(side="left")
       label = tk.Label(frame, font=("Arial", 11), width=15, text='电池', anchor="center")	
       label.pack(side="left")
       label = tk.Label(frame, font=("Arial", 11), width=15, text='可用存储', anchor="center")	
       label.pack(side="left")
       label = tk.Label(frame, font=("Arial", 11), width=15, text='总存储', anchor="center")	
       label.pack(side="left")
       label = tk.Label(frame, font=("Arial", 11), width=20, text='状态', anchor="center")	
       label.pack(side="left")
       frame.pack()
       self.vscrollbar = tk.Scrollbar(self.main)
       self.c = tk.Canvas(self.main, background = "#D2D2D2",yscrollcommand=self.vscrollbar.set)

       self.vscrollbar.config(command=self.c.yview)
       self.vscrollbar.pack(side=tk.RIGHT, fill=tk.Y) 

       self.frame =tk.Frame(self.c) #Create the frame which will hold the widgets

       self.c.pack(side="top", fill="both", expand=True)
       self.c.create_window(0,0, window=self.frame, anchor="center")


   
   def update_item_status(self, index, wifi, level, avaiable, status, color):
       #wifi, level, avaiable, status
       self.vars[index][0].set(wifi)
       self.vars[index][1].set(str(level))
       self.vars[index][2].set(str(avaiable) + "GB")
       self.vars[index][3].set(status)
       for x in self.labels[index]:
           x['bg'] = color

   def create_item_bar(self, index, uuid, sd):
       self.vars[index] = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
       frame = tk.Frame(self.frame)
       #index
       alabel = tk.Label(frame, width=17, font=("Arial", 12), text=str(index))
       alabel.pack(side="left")

       #uuid
       blabel = tk.Label(frame, width=17, font=("Arial", 12), text=uuid)
       blabel.pack(side="left")

       #wifi
       clabel = tk.Label(frame, width=17, font=("Arial", 12),  textvariable=self.vars[index][0])
       clabel.pack(side="left")

       #level
       dlabel = tk.Label(frame, width=17, font=("Arial", 12), textvariable=self.vars[index][1])
       dlabel.pack(side="left")

       #avaiable
       elabel = tk.Label(frame, width=17, font=("Arial", 12), textvariable=self.vars[index][2])
       elabel.pack(side="left")

       #sd
       flabel = tk.Label(frame, width=17, font=("Arial", 12),  text=str(sd) + "GB")
       flabel.pack(side="left")

       #download
       glabel = tk.Label(frame, width=17,  font=("Arial", 12), textvariable=self.vars[index][3])
       glabel.pack(side="left")
       frame.pack() 
 
       self.labels[index] = [alabel, blabel, clabel, dlabel, elabel, flabel, glabel]
       for x in self.labels[index]:
           x['bg'] = "gray"
       for x in self.vars[index]:
           x.set("Unknow")

       self.main.update()
       self.c.config(scrollregion=self.c.bbox("all"))

   def run(self):
       self.main.mainloop()

app = App()

if __name__ =='__main__':
    app.create_menu()
    app.create_label()
    app.run()
