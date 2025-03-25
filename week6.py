import tkinter as tk

root = tk.Tk()

root.title('py_week5') # 設定標題
root.iconbitmap('123.ico')
root.geometry('600x600') # 設定視窗大小
root.configure(background='#FFCCFF') # 設定背景色  

a = tk.Label(root, text='AAA', background='#f90',font=('芫荽', 20))
b = tk.Label(root, text='BBB', background='#09c',font=('芫荽', 20))
c = tk.Label(root, text='CCC', background='#fc0',font=('芫荽', 20))
d = tk.Label(root, text='DDD', background='#f9c',font=('芫荽', 20))
e = tk.Label(root, text='EEE', background='#aaa',font=('芫荽', 20))

a.grid(column=0,row=0,ipadx=20)
b.grid(column=1,row=0,ipady=20)
c.grid(column=2,row=0)
d.grid(column=0,row=1,padx=20)
e.grid(column=1,row=1,pady=20)




root.mainloop()