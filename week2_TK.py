import tkinter as tk

root= tk.Tk()

root.title('pythontk')        # 設定標題
root.iconbitmap('123.ico')

width = 500
height = 500
left = 300
top = 300
root.geometry(f'{width}x{height}+{left}+{top}')  # 定義視窗的尺寸和位置  (注意格式)

root.minsize(300, 300)    # 設定視窗最小為 200x200
root.maxsize(1000, 1000)    # 設定視窗最大為 500x500

n = 0
a = tk.StringVar()
a.set(n)

def add():
    global n
    n = n + 1
    a.set(n)
    

def reduce():
    global n
    n = n - 1
    a.set(n)

def zero():
    global n
    n = 0
    a.set(n)


mylabel = tk.Label(root,
                   textvariable=a,
                   font=('Arial', 20))
mylabel.pack()

btn = tk.Button(
    root,
    text="Press Me to plus 1",
    font=('微軟中黑體',20),
    command=add
)
btn.pack()

btn2 = tk.Button(
    root,
    text="Press Me to minus 1",
    font=('微軟中黑體',20),
    command=reduce
)
btn2.pack()

btn3 = tk.Button(
    root,
    text="Press Me to 0",
    font=('微軟中黑體',20),
    command=zero
)
btn3.pack()

root.mainloop()