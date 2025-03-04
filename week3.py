import tkinter as tk
#from PIL import Image, ImageTk
from tkinter.ttk import *

root = tk.Tk()

root.title('pythontk')        # 設定標題
root.iconbitmap('123.ico')

width = 500
height = 500
left = 300
top = 300
root.geometry(f'{width}x{height}+{left}+{top}')  # 定義視窗的尺寸和位置  (注意格式)

root.minsize(300, 300)    # 設定視窗最小為 200x200
root.maxsize(1000, 1000)    # 設定視窗最大為 500x500

root.resizable(False, False)   # 設定 x 方向和 y 方向都不能縮放

root.configure(background='#FFCCFF')   # 設定背景色


var1 = tk.StringVar()
var2 = tk.StringVar()
var3 = tk.StringVar()
var4 = tk.StringVar()

# radio_btn1 = tk.Radiobutton(root,text = 'Apple',variable=vari,value="Apple",font=('Arial',20,'bold'),padx=3,pady=3)
# radio_btn1.pack()
# radio_btn1.select()

# radio_btn2 = tk.Radiobutton(root,text='Banana',variable=vari,value="Banana",font=('Arial',20,'bold'),padx=3,pady=3)
# radio_btn2.pack()

# radio_btn3 = tk.Radiobutton(root,text='Cherry',variable=vari,value="Cgerry",font=('Arial',20,'bold'),padx=3,pady=3)
# radio_btn3.pack()

# radio_btn4 = tk.Radiobutton(root,text='Pineapple',variable=vari,value="Pineapple",font=('Arial',20,'bold'),padx=3,pady=3)
# radio_btn4.pack()

# mylabel = tk.Label(
#     root,
#     font=('Arial',20,'bold'),
#     padx=30,
#     pady=30,
#     relief='sunken',
#     textvariable=vari,
# )
# mylabel.pack()
vallab = tk.StringVar()

vallab = "Choose"
label = tk.Label(
    root,
    font=("芫荽",20),
    text= vallab,
    relief='sunken'
)
label.pack()

def show():
    print(var1.get(), var2.get(), var3.get(), var4.get())


check_btn1 = tk.Checkbutton(root,text = 'Apple',variable=var1,onvalue="Apple",offvalue="--",font=('Arial',20,'bold'),padx=3,pady=3,command=show)
check_btn1.pack()
check_btn1.deselect()

check_btn2 = tk.Checkbutton(root,text='Banana',variable=var2,onvalue="Banana",offvalue="--",font=('Arial',20,'bold'),padx=3,pady=3,command=show)
check_btn2.pack()
check_btn2.deselect()

check_btn3 = tk.Checkbutton(root,text='Cherry',variable=var3,onvalue="Cherry",offvalue="--",font=('Arial',20,'bold'),padx=3,pady=3,command=show)
check_btn3.pack()
check_btn3.deselect()
check_btn4 = tk.Checkbutton(root,text='Pineapple',variable=var4,onvalue="Pineapple",offvalue="--",font=('Arial',20,'bold'),padx=3,pady=3,command=show)
check_btn4.pack()
check_btn4.deselect()




root.mainloop()  # 放在主迴圈中
