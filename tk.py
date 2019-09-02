#!/usr/bin/env python
#coding:utf8
import tkinter as tk
import time
import client


def print_hello():
    print "E"
    app.update_item_status(29, "wifi","69","5GB","download", "red")

class App():
   def __init__(self):
       self.main = tk.Tk()
       self.main.title("耳机模拟器")
       #self.main.geometry('1080x720') 
       self.vars = dict()
       self.labels = dict()

   def create_menu(self):
       menubar = tk.Menu(self.main)
       fmenu = tk.Menu(menubar)
       for each in ['新建','退出']:
           fmenu.add_command(label=each, command=print_hello)
 
       amenu = tk.Menu(menubar)
       for each in ['版权信息','联系我们']:
           amenu.add_command(label=each, command=print_hello)
 
       menubar.add_cascade(label='文件',menu=fmenu)
       menubar.add_cascade(label='关于',menu=amenu)
 
       self.main.config(menu=menubar)

   def create_label(self):
       frame = tk.Frame(self.main)
       label = tk.Label(frame, width=15, text='序号',anchor="center")	
       label.pack(side="left")
       label = tk.Label(frame, width=15, text='设备序列号', anchor="center")	
       label.pack(side="left")
       label = tk.Label(frame, width=15, text='网络', anchor="center")	
       label.pack(side="left")
       label = tk.Label(frame, width=15, text='电池', anchor="center")	
       label.pack(side="left")
       label = tk.Label(frame, width=15, text='可用存储', anchor="center")	
       label.pack(side="left")
       label = tk.Label(frame, width=15, text='总存储', anchor="center")	
       label.pack(side="left")
       label = tk.Label(frame, width=20, text='状态', anchor="center")	
       label.pack(side="left")
       frame.pack()
   
   def update_item_status(self, index, wifi, level, avaiable, status, color):
       #wifi, level, avaiable, status
       self.vars[index][0].set(wifi)
       self.vars[index][1].set(level)
       self.vars[index][2].set(avaiable)
       self.vars[index][3].set(status)
       for x in self.labels[index]:
           x['bg'] = color

   def create_item_bar(self, index, uuid, sd):
       frame = tk.Frame(self.main)
       self.vars[index] = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]

       #index
       alabel = tk.Label(frame, width=15, text=str(index), justify="center",anchor="center")
       alabel.pack(side="left")

       #uuid
       blabel = tk.Label(frame, width=15, text=uuid)
       blabel.pack(side="left")

       #wifi
       clabel = tk.Label(frame,width=15,  textvariable=self.vars[index][0])
       clabel.pack(side="left")

       #level
       dlabel = tk.Label(frame, width=15, textvariable=self.vars[index][1])
       dlabel.pack(side="left")

       #avaiable
       elabel = tk.Label(frame, width=15, textvariable=self.vars[index][2])
       elabel.pack(side="left")

       #sd
       flabel = tk.Label(frame,width=15,  text=sd)
       flabel.pack(side="left")

       #download
       glabel = tk.Label(frame,width=15,  textvariable=self.vars[index][3])
       glabel.pack(side="left")
       frame.pack()

       self.labels[index] = [alabel, blabel, clabel, dlabel, elabel, flabel, glabel]
       for x in self.labels[index]:
           x['bg'] = "gray"
       for x in self.vars[index]:
           x.set("Unknow")

   def run(self):
       self.main.mainloop()

app = App()

if __name__ =='__main__':
    app.create_menu()
    app.create_label()
    for x in range (30):
        s = client.Headset(x)
        s.uuid = "123445"
        s.sd = "8GB"
        s.level = "83"
        app.create_item_bar(x, s.uuid, s.sd) 
        s.viewer(app.update_item_status)
        s.start()
        #app.update_item_status(x, "wifi","69","7GB","download", "blue")
    app.run()
