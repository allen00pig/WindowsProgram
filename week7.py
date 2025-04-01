import tkinter as tk
from tkinter import messagebox


root = tk.Tk()
root.title("Week 7")
root.iconbitmap('123.ico')
root.geometry('600x600') # 設定視窗大小
root.configure(background='#FFCCFF')

a = tk.Label(root, text='AAA', background='#f90',font=('芫荽', 20))
b = tk.Label(root, text='BBB', background='#09c',font=('芫荽', 20))
c = tk.Label(root, text='CCC', background='#fc0',font=('芫荽', 20))
d = tk.Label(root, text='DDD', background='#f9c',font=('芫荽', 20))
# e = tk.Label(root, text='EEE', background='#aaa',font=('芫荽', 20))

a.grid(column=1,row=0,ipadx=20)
b.grid(column=2,row=1,ipady=20)
c.grid(column=3,row=2,padx=20)
d.grid(column=4,row=3,pady=20)

root.mainloop()