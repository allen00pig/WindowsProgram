import tkinter as tk

root = tk.Tk()
root.title('py_week5') # 設定標題
root.iconbitmap('123.ico')
root.geometry('600x600') # 設定視窗大小
root.configure(background='#FFCCFF') # 設定背景色 

a = tk.StringVar()
a.set('')

def spin():
    val1 = float(spinbox.get())
    val2 = float(spinbox2.get())
    a.set(val1+val2)

label = tk.Label(root, textvariable=a, font=('芫荽', 20), bg='yellow', fg='blue')

label.pack()


spinbox = tk.Spinbox(root, from_=0, to=100, increment=1, font=('芫荽', 20)
                     ,activebackground='red', background='yellow', width=10, relief='sunken'
                     , bd=10, fg='blue', justify='center'
                     ,wrap=True,format='%8.4f', state='readonly'
                     ,command=spin)
spinbox.pack()

spinbox2 = tk.Spinbox(root,from_=0, to=100, increment=0.1, font=('芫荽', 20)
                      ,activebackground='red', background='yellow'
                      , width=10, relief='sunken',command=spin
                      ,format='%8.4f', bd=10, fg='blue', justify='center')
spinbox2.pack()

anime = ["One piece","Attack on Titan","Demon Slayer"]

spinbox3 = tk.Spinbox(root, values=anime, font=('芫荽', 20), bg='yellow', fg='blue', command=spin)
spinbox3.pack()

root.mainloop()