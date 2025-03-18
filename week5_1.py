import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.title('py_week5') # 設定標題
root.iconbitmap('123.ico')
root.geometry('600x600') # 設定視窗大小
root.configure(background='#FFCCFF') # 設定背景色 

group = tk.LabelFrame(root, text='Group', font=("芫荽",10, 'bold'),
                      fg='blue', padx=10, pady=10)
group.pack(padx=20, pady=20)

a = tk.Label(group, text='First', font=("芫荽",10,'bold'),fg='red').pack()
b = tk.Label(group, text='Second', font=("芫荽",10,'bold'),fg="green").pack()
c = tk.Label(group, text='Third', font=("芫荽",10,'bold')).pack()

canvas = tk.Canvas(root, width=500, height=500)

canvas.create_text(100, 100, text='Hello, Python')
canvas.create_text(0, 0, text='Hello, World', anchor='nw', fill='red')
canvas.create_text(0, 200, text = "Allen0", anchor='sw',fill="blue")
canvas.create_text(200, 0, text = "Allen1", anchor='ne',fill="green") 
canvas.create_text(200, 200, text = "Allen2", anchor='se',fill="yellow")
font = ("芫荽",10,'bold')

canvas.create_line(0, 0, 500, 500, fill='red', width=5,dash=(4, 4))
canvas.create_line(0, 500, 500, 0, fill='blue', width=5)
canvas.create_rectangle(100, 100, 400, 400, dash=(4, 4))

canvas.create_oval(100, 100, 400, 400, fill='yellow')

canvas.create_arc(100, 100, 400, 400, start=0, extent=90, fill='red')
canvas.create_arc(100, 100, 400, 400, start=60, extent=180, fill='blue', outline='black')

img = Image.open('1.jpg')
TK_img = ImageTk.PhotoImage(img)
canvas.create_image(250, 250, image=TK_img)

canvas.pack()

root.mainloop()