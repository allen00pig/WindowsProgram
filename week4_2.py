import tkinter as tk
import PIL
from tkinter.ttk import *

root = tk.Tk()
root.title('py_week4') # 設定標題
root.iconbitmap('123.ico')
root.geometry('600x600') # 設定視窗大小
root.configure(background='#FFCCFF') # 設定背景色   
root.resizable(False, False) # 設定 x 方向和 y 方向都不能縮放

def show():
    n, = listbox.curselection()   # 取得目前選取的選項
    text.set(listbox.get(n))   # 顯示選取的選項
    
frame = tk.Frame(root, width=10)   # 建立 Frame
frame.pack()

scrollbar = tk.Scrollbar(frame)   # 建立滾動條
scrollbar.pack(side='right', fill='y')   # 設定位置在右側，垂直填滿

listbox = tk.Listbox(frame, font=("芫荽",10),yscrollcommand=scrollbar.set)   # 建立 Listbox
menu = ['Apple','Banana','Orange','Grap','Papaya','Coconut','Apple','Banana','Orange','Grap','Papaya','Coconut','Apple','Banana','Orange','Grap','Papaya','Coconut']   # 建立選單的串列
for i in menu:
    listbox.insert(tk.END, i)   # 使用 for 迴圈添加選項
listbox.pack()

scrollbar.config(command=listbox.yview)   # 設定 scrollbar 綁定 listbox 的 yview

text = tk.StringVar()   # 建立字串物件
# text = tk.Text(root, font=("芫荽",10))
label = tk.Label(root, textvariable=text, font=("芫荽",10)).pack()

btn = tk.Button(root, text='Show', command=show, font=("芫荽",10)).pack()


root.mainloop()