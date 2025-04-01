import tkinter as tk
from tkinter import messagebox

def show_text():
    content = text_box.get("1.0", tk.END)  # 從第1行第0個字開始抓到結尾
    messagebox.showinfo("你輸入的內容", content)

def clear_text():
    text_box.delete("1.0", tk.END)

# 建立主視窗
root = tk.Tk()
root.title("Text 元件範例")
root.geometry("400x300")

# 建立 Text 元件
text_box = tk.Text(root, height=10, width=40)
text_box.pack(pady=10)

# 建立按鈕
btn_show = tk.Button(root, text="顯示內容", command=show_text)
btn_show.pack(pady=5)

btn_clear = tk.Button(root, text="清除內容", command=clear_text)
btn_clear.pack(pady=5)

# 執行主迴圈
root.mainloop()
