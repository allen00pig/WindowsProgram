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

btn = tk.Button(root,
                text= "按鈕",
                font= ("微軟中黑體",30,'bold'),
                fg='#225522',bg='#552255',
                padx=10,
                pady=10,
                relief='solid',
                activebackground='#ff0011'
)

btn.pack()

mylabel = tk.Label(
    root,
    text='hello world\nHELLO',
    font=('Arial',20,'bold'),
    padx=30,
    pady=30,
    relief='sunken',
)
mylabel.pack()

a = tk.StringVar()
a.set("HI")
mylabel2 = tk.Label(root,textvariable=a,font=('Arial',20))
mylabel2.pack()

vari = tk.StringVar()

radio_btn1 = tk.Radiobutton(root,text = 'APPLE',variable=vari,value="apple",padx=3,pady=3)
radio_btn1.pack()
radio_btn1.select()

radio_btn2 = tk.Radiobutton(root,text='Banana',variable=vari,value="banana",padx=3,pady=3)
radio_btn2.pack()

root.mainloop()  # 放在主迴圈中
