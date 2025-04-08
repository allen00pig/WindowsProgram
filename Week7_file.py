import os
os.chdir('/')       # 移動路徑到根目錄

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

root = tk.Tk()   # 建立 tkinter 視窗物件
root.title('Tkinter')

width=500
height=800
left=300
top=300

root.geometry(f'{width}x{height}+{left}+{top}')  # 定義視窗的尺寸和位置

root.minsize(200, 200)    # 設定視窗最小為 200x200
root.maxsize(800, 800)    # 設定視窗最大為 800x800

root.configure(background='gray')   # 設定背景色red

#檔案的內容放到文字變數中
text = tk.StringVar()   # 設定 text 為文字變數
text.set('')            # 設定 text 的內容

#把檔案內容讀取存成字串到text中
def show():
    file_path = filedialog.askopenfilename()
    f = open(file_path,'r')      # 根據檔案路徑開啟檔案
    a = f.read()                 # 讀取檔案內容  
    text.set(a)                  # 設定變數為檔案內容
    f.close()                    # 關閉檔案

#把文字輸入盒變成檔案
def save():
    content = text_box.get("0.0", tk.END) #tk.END (最後一行最後一字)
    file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("文字檔", "*.txt")])
    f = open(file_path,'w')      # 根據檔案路徑開啟檔案
    f.write(content)
    messagebox.showinfo("儲存檔案","成功")


# Button 設定 command 參數
btn = tk.Button(root,
                text='開啟舊檔',
                font=('Arial',20,'bold'),
                command=show
              )
btn.place(x=20, y=250)

#輸入文字使用
text_box = tk.Text(root, height=12, width=40, font=('Arial',10,'bold'))
text_box.place(x=20, y=20)

# 建立按鈕
btn_show = tk.Button(root,
                text='另存新檔',
                font=('Arial',20,'bold'),command=save)
btn_show.place(x=180, y=250)


mylabel = tk.Label(root, textvariable=text, font=('Arial',20))
mylabel.place(x=20, y=380)




















root.mainloop()  # 放在主迴圈中
