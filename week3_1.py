import tkinter as tk
import PIL
from tkinter.ttk import *

import PIL.Image
import PIL.ImageTk

root = tk.Tk()

root.title('pythontk')        # 設定標題
root.iconbitmap('123.ico')

width = 700
height = 700
left = 300
top = 300
root.geometry(f'{width}x{height}+{left}+{top}')  # 定義視窗的尺寸和位置  (注意格式)

root.minsize(300, 300)    # 設定視窗最小為 200x200
root.maxsize(1000, 1000)    # 設定視窗最大為 500x500

# root.resizable(False, False)   # 設定 x 方向和 y 方向都不能縮放

root.configure(background='#FFCCFF')   # 設定背景色



# Img1 = tk.PhotoImage(
#     file="1.gif"
# )
# Img2 = tk.PhotoImage(
#     file="2.gif"
# )
# mylabel = tk.Label(
#     image=Img1
# )
# mylabel.pack(padx=10,pady=10)

# btn = tk.Button(
#     image=Img2
# )
# btn.pack(padx=10,pady=10)


Img1 = PIL.Image.open("1.gif")
Img2 = PIL.Image.open("1.jpg")

tk_Img1 = PIL.ImageTk.PhotoImage(Img1)
tk_Img2 = PIL.ImageTk.PhotoImage(Img2)

mylabel = tk.Label(
    image=tk_Img1
)
mylabel.pack(padx=10,pady=10)

btn = tk.Button(
    image=tk_Img2
)
btn.pack(padx=10,pady=10)




root.mainloop()  # 放在主迴圈中
