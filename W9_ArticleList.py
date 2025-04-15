import tkinter as tk
from tkinter import messagebox

def add_task():
    task = entry.get()
    if task != "":
        listbox.insert(tk.END, task)
        add_button_for_task(listbox.size() - 1)  # 傳入新增項目的索引
        entry.delete(0, tk.END)
        messagebox.showinfo("Success", "事項已添加")
    else:
        messagebox.showwarning("Warning", "給我加東西啊~!!!!")

def add_button_for_task(index):
    # 為每個任務新增一個按鈕，並綁定到對應的索引
    button = tk.Button(button_frame, text="完成", command=lambda: delete_task(index))
    button.pack(fill="x", pady=2)

def delete_task(index):
    # 刪除 listbox 中的項目
    if 0 <= index < listbox.size():
        listbox.delete(index)
        # 刪除對應的按鈕
        button_frame.winfo_children()[index].destroy()
        # 更新按鈕的索引
        update_button_commands()
        messagebox.showinfo("Success", "事項已刪除")

def update_button_commands():
    # 更新按鈕的命令，使其索引與 listbox 的項目保持一致
    for i, button in enumerate(button_frame.winfo_children()):
        button.config(command=lambda idx=i: delete_task(idx))

root = tk.Tk()
root.title("W9_1") # 設定標題
root.geometry("400x300")  # 設定視窗大小
root.configure(background="#98FB98") # 設定背景色

entry = tk.Entry(root, width=40) # 設定輸入框的寬度
entry.pack(pady=10)

add_button = tk.Button(root, text="添加", command=add_task)
add_button.pack(pady=10)

# 使用框架來排列 listbox 和按鈕列
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, pady=10)

listbox = tk.Listbox(main_frame, width=30, height=10)
listbox.pack(side="left", padx=5)

button_frame = tk.Frame(main_frame)
button_frame.pack(side="left", fill="y")

root.mainloop()