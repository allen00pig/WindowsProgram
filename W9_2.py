import tkinter as tk
from tkinter import messagebox

def add(): # 計算加法
    global operator
    operator = "+"
    
def subtract(): # 計算減法
    global operator
    operator = "-"
    

def multiply(): # 計算乘法
    global operator
    operator = "*"
    

def divide(): # 計算除法
    global operator
    operator = "/"

def show_result(): # 顯示計算結果
    try:
        num1 = float(entry1.get())  # 取得第一個數字
        num2 = float(entry2.get()) # 取得第二個數字
        if operator == "+": 
            result.set(num1 + num2)
        elif operator == "-":
            result.set(num1 - num2)
        elif operator == "*":
            result.set(num1 * num2)
        elif operator == "/":
            if num2 == 0: # 除數不能為零
                raise ZeroDivisionError
            result.set(num1 / num2)
    except ZeroDivisionError: # 處理除數為零的情況
        result.set("除數不能為零")
        messagebox.showerror("錯誤", "幹嘛，除數不能為零")
    except ValueError: # 處理非數字輸入的情況
        result.set("輸入錯誤")
        messagebox.showerror("錯誤", "給我數字阿~!!!!")
    except Exception as e: # 處理其他錯誤
        result.set("輸入錯誤")
        messagebox.showerror("錯誤", f"你是不是沒給我運算符號？")

def clear(): # 清除輸入框和結果
    entry1.delete(0, tk.END)  # 清除第一個輸入框
    entry2.delete(0, tk.END)  # 清除第二個輸入框
    result.set("0")

def focus1(event):
    global f
    f = 1

def focus2(event):
    global f
    f = 2

root = tk.Tk()
root.geometry("300x400")
root.title("簡易計算器")
root.configure(background="white")

entry1 = tk.Entry(root, font=("Arial", 14), background="#E6E6FA")
entry1.bind("<FocusIn>", focus1)
entry1.pack(pady=10)

entry2 = tk.Entry(root, font=("Arial", 14), background="#E6E6FA")
entry2.bind("<FocusIn>", focus2)
entry2.pack(pady=10)

result = tk.StringVar()
result.set("0")

result_label = tk.Label(root, textvariable=result, font=("Arial", 14))
result_label.pack(pady=20)

def but(n):
    n = str(n)
    if f == 1:
        t = len(entry1.get())
        entry1.insert(t, n)
    elif f == 2:
        t = len(entry2.get())
        entry2.insert(t, n)
    else:
        t = len(entry1.get())
        entry1.insert(t, n)
numFrame = tk.Frame(root, bg="white")
numFrame.pack(pady=5)

# 數字按鈕
buttons = [
    ("0", 1, 3), ("1", 0, 0), ("2", 0, 1), ("3", 0, 2),
    ("4", 1, 0), ("5", 1, 1), ("6", 1, 2), ("7", 2, 0),
    ("8", 2, 1), ("9", 2, 2)
]
for text, row, col in buttons:
    tk.Button(numFrame, text=text, command=lambda n=text: but(n), font=("Arial", 14)).grid(row=row, column=col, padx=10)

frame = tk.Frame(root, bg="white")
frame.pack(pady=10)

# 運算符按鈕
add_button = tk.Button(frame, text="+", command=add, font=("Arial", 14))
add_button.pack(side="left", padx=10)

subtract_button = tk.Button(frame, text="-", command=subtract, font=("Arial", 14))
subtract_button.pack(side="left", padx=10)

multiply_button = tk.Button(frame, text="*", command=multiply, font=("Arial", 14))
multiply_button.pack(side="left", padx=10)

divide_button = tk.Button(frame, text="/", command=divide, font=("Arial", 14))
divide_button.pack(side="left", padx=10)

# 等於按鈕
result_button = tk.Button(frame, text="=", command=show_result, font=("Arial", 14))
result_button.pack(pady=10)

# 清除按鈕
clear_button = tk.Button(root, text="清除", command=clear, font=("Arial", 14))
clear_button.pack()

root.mainloop()