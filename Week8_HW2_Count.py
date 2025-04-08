import tkinter as tk
from tkinter import messagebox

def increase(): # 增加計數器的值
    count.set(count.get() + 1)  # 更新計數器的值
    if count.get() > 10:
        result = messagebox.askyesno("提示", "數字已經超過10\n是否要重置？") # 提示用戶是否要重置
        if result: # 如果用戶選擇是
            count.set(0) # 重置計數器的值
        else: # 如果用戶選擇否
            count.set(count.get())
    
def decrease(): # 減少計數器的值
    count.set(count.get() - 1) # 更新計數器的值
    if count.get() > 10:
        result = messagebox.askyesno("提示", "數字已經超過10\n是否要重置？") # 提示用戶是否要重置
        if result: # 如果用戶選擇是
            count.set(0) # 重置計數器的值
        else: # 如果用戶選擇否
            count.set(count.get())

def reset(): # 重置計數器的值
    count.set(0) # 更新計數器的值
  
    
root = tk.Tk() # 建立主視窗 
root.title("計數 by C110181149") # 設定標題
root.configure(background='#FFCCFF') # 設定背景色


count = tk.IntVar() 
count.set(0)
count_label = tk.Label(root, textvariable=count, font=('微軟正黑體', 20)) # 顯示計數的Label
count_label.pack( padx=10, pady=10, fill=tk.X, expand=True) # 設定Label的大小和位置

frame = tk.Frame(root) # 建立一個Frame來放置按鈕
frame.pack(fill='x') # 設定Frame的大小和位置

increase_button = tk.Button(frame, text="增加", command=increase,font=('微軟正黑體', 20)) # 建立增加按鈕 
increase_button.grid(column=0, row=0, padx=20) # 設定按鈕的大小和位置

decrease_button = tk.Button(frame, text="減少", command=decrease,font=('微軟正黑體', 20))  # 建立減少按鈕
decrease_button.grid(column=1, row=0, padx=20) # 設定按鈕的大小和位置

reset_button = tk.Button(frame, text="重置", command=reset,font=('微軟正黑體', 20)) # 建立重置按鈕
reset_button.grid(column=2, row=0, padx=20) # 設定按鈕的大小和位置


    

root.mainloop()
