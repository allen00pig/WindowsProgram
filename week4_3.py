import tkinter as tk
import PIL
from tkinter.ttk import *

root = tk.Tk()
root.title('py_week4') # 設定標題
root.iconbitmap('123.ico')
root.geometry('600x600') # 設定視窗大小
root.configure(background='#FFCCFF') # 設定背景色 

def show(*e):
    a.set(value.get())  

a = tk.StringVar()
a.set('OptionMenu')

label = tk.Label(root, textvariable=a, font=("芫荽",10))
label.pack()

optionList = ['Dragon Ball','One pices','Naruto','Bleach','Attack on Titan','One Punch','My Hero Academia','Black Clover','Demon Slayer','Tokyo Ghoul','Death Note','Sword Art Online','Fairy Tail','Hunter x Hunter','Fullmetal Alchemist','JoJo\'s Bizarre Adventure','Re:Zero','Dr. Stone','The Promised Neverland','Fire Force','Haikyuu!!','Kuroko\'s Basketball','Slam Dunk','Prince of Tennis','Eyeshield 21','Hajime no Ippo','Initial D','Yowamushi Pedal','Megalo Box','Ashita no Joe','Ping Pong','Free!','K-On!','Love Live!','BanG Dream!','Zombieland Saga','Revue Starlight','Symphogear','Idolmaster']
value = tk.StringVar()
value.set('')

menu = tk.OptionMenu(root, value, *optionList)
menu.config(font=("芫荽",10))
menu.pack()

value.trace_add('write', show)
#btn = tk.Button(root, text='Show', command=show, font=("芫荽",10)).pack()


root.mainloop()