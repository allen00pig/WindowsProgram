import tkinter as tk
import PIL
from tkinter.ttk import *

import PIL.Image
import PIL.ImageTk

root = tk.Tk()

root.iconbitmap('123.ico')

root.title('Week3')

root.geometry('400x400')


root.configure(background='#FFCCFF')   # 設定背景色


scrollbar = tk.Scrollbar(root)
scrollbar.pack(side="right",fill='y')

a = tk.StringVar()
b = tk.StringVar()

a.set("")

def show():
    a.set(b.get())
    
def clear():
    b.set("")
    a.set("")
    entry.delete(0,'end')

label = tk.Label(root,relief="flat",textvariable=a ,font=("芫荽",20))
label.pack()
entry = tk.Entry(root,relief="flat",textvariable=b,font=("芫荽",20))  # 放入單行輸入框
entry.pack()

# 
btn1 = tk.Button(
    root,
    text="Press Me to display",
    font=('芫荽',20),
    command=show
)

btn2 = tk.Button(
        root,
    text="Press Me to clear",
    font=('芫荽',20),
    command=clear
)
btn1.pack()
btn2.pack()


root.mainloop()