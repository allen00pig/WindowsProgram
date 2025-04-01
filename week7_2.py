import os
os.chdir("/")

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox



root = tk.Tk()
root.title("Week 7")
root.geometry('600x600') # 設定視窗大小
root.configure(background='#FFCCFF')

text = tk.StringVar()
text.set("")

def show():
    file_path = filedialog.askopenfilename()
    f = open(file_path, 'r')
    a=f.read()
    text.set(a)
    f.close()
    
def save():
    content = text_box.get("0.0", tk.END)
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("文字檔", "*.txt")]
    )
    f = open(file_path, 'w')
    f.write(content)
    messagebox.showinfo("儲存成功", "檔案已儲存！")
    
    
btn = tk.Button(root, text="Me is button", command=show, bg="#FFCCFF").pack()

mylabel = tk.Label(root, textvariable=text, bg="#FFCCFF", font=("Arial", 20)).pack()



root.mainloop()
