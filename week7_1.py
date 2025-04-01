import tkinter as tk
from tkinter import messagebox


root = tk.Tk()
root.title("Week 7")
root.geometry('600x600') # 設定視窗大小
root.configure(background='#FFCCFF')

# a = tk.Label(root, text='AAA', background='#f90',font=('芫荽', 20))
# b = tk.Label(root, text='BBB', background='#09c',font=('芫荽', 20))
# c = tk.Label(root, text='CCC', background='#fc0',font=('芫荽', 20))
# d = tk.Label(root, text='DDD', background='#f9c',font=('芫荽', 20))
# # e = tk.Label(root, text='EEE', background='#aaa',font=('芫荽', 20))

# a.grid(column=1,row=0,ipadx=20)
# b.grid(column=2,row=1,ipady=20)
# c.grid(column=3,row=2,padx=20)
# d.grid(column=4,row=3,pady=20)

# a = tk.Label(root, text='AAA', background='#f90')
# b = tk.Label(root, text='BBB', background='#09c')

# a.pack(fill='y', expand=1)
# b.pack(fill='both', expand=1)

# a = tk.Label(root, text='AAA', background='#f90')
# b = tk.Label(root, text='BBB', background='#09c')
# c = tk.Label(root, text='CCC', background='#fc0')
# d = tk.Label(root, text='DDD', background='#0c9')
# e = tk.Label(root, text='EEE', background='#ccc')

# a.grid(column=0, row=0, sticky=tk.W+tk.S)
# b.grid(column=1, row=0, ipady=20)
# c.grid(column=0, row=1, sticky=tk.E+tk.N)
# d.grid(column=1, row=1, ipady=20)
# e.grid(column=0, row=2, ipadx=20)

frame = tk.Frame(root)
frame.pack(fill='x')

a = tk.Label(frame, text='AAA', background='#f90')
b = tk.Label(frame, text='BBB', background='#09c')
c = tk.Label(frame, text='CCC', background='#fc0')
d = tk.Label(frame, text='DDD', background='#0c9')
a.grid(column=0, row=0, padx=20)
b.grid(column=1, row=0, padx=20)
c.grid(column=0, row=1, padx=20)
d.grid(column=1, row=1, padx=20)

e = tk.Label(root, text='EEE', background='#ccc')
e.pack(fill='x')


root.mainloop()