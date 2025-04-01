import tkinter as tk
from tkinter import messagebox, filedialog

def show_text():
    content = text_box.get("1.0", tk.END)
    messagebox.showinfo("你輸入的內容", content)

def clear_text():
    text_box.delete("1.0", tk.END)

def save_to_file():
    content = text_box.get("1.0", tk.END)
    if content.strip() == "":
        messagebox.showwarning("警告", "沒有內容可以儲存！")
        return

    # 開啟儲存檔案對話框
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("文字檔", "*.txt")],
        title="儲存為..."
    )
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            messagebox.showinfo("成功", f"檔案已儲存：\n{file_path}")
        except Exception as e:
            messagebox.showerror("錯誤", f"儲存失敗：\n{e}")

# 建立主視窗
root = tk.Tk()
root.title("Text 元件儲存範例")
root.geometry("400x350")

# 建立 Text 元件
text_box = tk.Text(root, height=12, width=40)
text_box.pack(pady=10)

# 建立按鈕
btn_show = tk.Button(root, text="顯示內容", command=show_text)
btn_show.pack(pady=5)
btn_clear = tk.Button(root, text="清除內容", command=clear_text)
btn_clear.pack(pady=5)

btn_save = tk.Button(root, text="儲存成檔案", command=save_to_file)
btn_save.pack(pady=5)

# 執行主迴圈
root.mainloop()
