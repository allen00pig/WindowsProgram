import tkinter as tk
from tkinter import messagebox
import tkinter.filedialog as filedialog

def show():
    file_path = filedialog.askopenfilename()
    f = open(file_path, 'r', encoding='utf-8')   
    a = f.read()
    text.set(a)
    f.close()
    
def save():
    content = text.get("0.0", tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    f = open(file_path, 'w', encoding='utf-8')
    f.write(content)
    f.close()

text = tk.StringVar()
text.set("")

# 建立主視窗
root = tk.Tk()
root.title("Text 元件範例")
root.geometry("400x300")

# 建立 Text 元件
textBox = tk.Text(root, height=10, width=40)
textBox.pack(pady=10)

# 建立按鈕
btn_show = tk.Button(root, text="SHOW", command=show)
btn_show.pack(pady=5)

btn_clear = tk.Button(root, text="SAVE", command=save)
btn_clear.pack(pady=5)

# 執行主迴圈
root.mainloop()
