import tkinter as tk
import PIL
from tkinter.ttk import *

root = tk.Tk()
root.title('py_week4') # 設定標題
root.iconbitmap('123.ico')
root.geometry('600x600') # 設定視窗大小
root.configure(background='#FFCCFF') # 設定背景色   
# root.resizable(False, False) # 設定 x 方向和 y 方向都不能縮放

MainScrollbar = tk.Scrollbar(root)          # 建立滾動條
MainScrollbar.pack(side='right', fill='y')  # 將滾動條加在右側，垂直填滿



a = tk.StringVar()
# b = tk.StringVar()

a.set("")

def show():
    a.set(text.get(0.0,'end-1c'))
    showText.insert(tk.INSERT, text.get(0.0,'end-1c'))
    
    
def clear():
    a.set("")
    text.delete(0.0,'end')
    showText.delete(0.0,'end')
    
showLabel = tk.Label(root, text=("顯示:"), font=("芫荽",10)).pack()
showFrame = tk.Frame(root,height=10, width=10)
showTextScrollbar = tk.Scrollbar(showFrame)               # 將 Frame 裡放入 Scrollbar
showTextScrollbar.pack(side='right', fill='y')


showText = tk.Text(showFrame ,font=("芫荽",10),height=10, width=10, yscrollcommand=showTextScrollbar.set)
# showText.insert(tk.INSERT, a.get)
showText.pack()

showTextScrollbar.config(command=showText.yview)
showFrame.pack()

entryLabel = tk.Label(root, text="輸入:", font=("芫荽",10)).pack()
# text = tk.Text(root,relief="flat",height='8',font=("芫荽",20))  # 放入單行輸入框
# text.pack()
frame = tk.Frame(root, height=10, width=10)   # 建立 Frame
TextScrollbar = tk.Scrollbar(frame)               # 將 Frame 裡放入 Scrollbar
TextScrollbar.pack(side='right', fill='y')        # 設定位置在右側，垂直填滿

# 在 Frame 裡放入 text，設定 yscrollcommand=scrollbar.set
text = tk.Text(frame, height=10, width=10,font=("芫荽",10), yscrollcommand=TextScrollbar.set)
text.pack()

TextScrollbar.config(command=text.yview)    # 設定 scrollbar 綁定 text 的 yview
frame.pack()


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