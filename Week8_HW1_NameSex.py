import tkinter as tk
from tkinter import messagebox

def submit():
    name = entry.get() #獲取輸入的姓名
    gender = var.get()  #獲取選擇的性別
    if not name or not gender:
        messagebox.showerror("錯誤", "請填寫所有欄位") #檢查是否有空欄位
    else:
        messagebox.showinfo("儲存成功",f"性別：{gender}\n姓名：{name}") #顯示輸入的姓名和性別

root = tk.Tk()
root.title("姓名和性別輸入 by C110181149") #設定標題
root.geometry("300x200") #設定視窗大小
root.configure(background="lightblue") #設定背景顏色


entry = tk.Entry(root) #建立輸入框
entry.pack(padx=10, pady=10, fill=tk.X, expand=True) #設定輸入框大小和位置
entry.config(font=('微軟正黑體', 20)) #設定輸入框字型

var = tk.StringVar()
var.set("男") #預設性別為男
gender_menu = tk.OptionMenu(root, var, "男", "女")#建立選單
gender_menu.config(font=('微軟正黑體', 20)) #設定選單字型
gender_menu.pack( padx=10, pady=10, fill=tk.X, expand=True)

submit_button = tk.Button(root, text="提交", command=submit,font=('微軟正黑體', 20)) #建立提交按鈕
submit_button.pack( padx=10, pady=10)

root.mainloop()
