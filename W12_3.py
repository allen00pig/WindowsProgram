import sys
from PyQt6 import QtWidgets, QtGui, QtCore
import os

app = QtWidgets.QApplication(sys.argv)

Form = QtWidgets.QWidget()
Form.setWindowTitle("W12_3")
Form.resize(600, 480)
Form.setStyleSheet("background-color: #FFCCCC;")
Form.setWindowIcon(QtGui.QIcon("123.ico"))


label = QtWidgets.QLabel(Form)
label.setGeometry(20,20,120,30)

def show():
    label.setText(t1.time().toString())  # 顯示時間

def show2():
    label.setText(d1.date().toString())  # 顯示日期


now = QtCore.QTime.currentTime()   # 取得目前電腦時間

t1 = QtWidgets.QTimeEdit(Form)
t1.setGeometry(140,20,120,30)
t1.setDisplayFormat('hh:mm:ss')
t1.setTime(now)                    # 設定時間
t1.setTimeRange(QtCore.QTime(3, 00, 00), QtCore.QTime(23, 30, 00))
t1.editingFinished.connect(show)

d1 = QtWidgets.QDateEdit(Form)
d1.setGeometry(270,20,120,30)
d1.setDisplayFormat('yyyy/MM/dd')
d1.setDate(QtCore.QDate.currentDate())  # 設定日期
d1.dateChanged.connect(show2)

d2 = QtWidgets.QDateEdit(Form)
d2.setGeometry(400,20,120,30)
d2.setDisplayFormat('dd/MM/yyyy')
d2.setDate(QtCore.QDate.currentDate())  # 設定日期
n = 0

def more():
    global bar, bar1, bar2 ,n
    n += 10
    bar.setValue(n)  # 設定進度條的值
    
def less():
    global bar, bar1, bar2 ,n
    n -= 10
    bar.setValue(n)  # 設定進度條的值

bar = QtWidgets.QProgressBar(Form)
bar.setGeometry(20, 70, 500, 30)
bar.setValue(50)  # 設定進度條的值
bar.setTextVisible(True)  # 顯示進度條的值
bar.setFormat('%v')

bar1 = QtWidgets.QProgressBar(Form)
bar1.setGeometry(20, 110, 500, 30)
bar1.setRange(0, 100)  # 設定進度條的範圍
bar1.setValue(50)  # 設定進度條的值
bar1.setTextVisible(True)  # 顯示進度條的值
bar1.setStyleSheet('''
    QProgressBar {
        background-color: #fff;
        border: 2px solid #000;
        border-radius: 5px;
    }
    QProgressBar::chunk {
        background-color: #f00;
        width: 20px;
    }
''')
bar1.setFormat('%v/%m')

bar2 = QtWidgets.QProgressBar(Form)
bar2.setGeometry(20, 150, 500, 30)
bar2.setRange(0, 100)  # 設定進度條的範圍
bar2.setValue(50)  # 設定進度條的值
bar2.setStyleSheet('''
    QProgressBar {
        background-color: #fff;
        border: 2px solid #000;
        border-radius: 5px;
    }
    QProgressBar::chunk {
        background-color: #0f0;
        width: 20px;
    }
''')
bar2.setFormat('%p%')

btn3 = QtWidgets.QPushButton(Form)
btn3.setGeometry(20, 200, 100, 30)
btn3.setText("More")
btn3.setStyleSheet('''
    QPushButton {
        background-color: #0f0;
        border: 2px solid #000;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #0c0;
    }
''')
btn3.clicked.connect(more)

btn4 = QtWidgets.QPushButton(Form)
btn4.setGeometry(130, 200, 100, 30)
btn4.setText("Less")
btn4.setStyleSheet('''
    QPushButton {
        background-color: #f00;
        border: 2px solid #000;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #c00;
    }
''')
btn4.clicked.connect(less)

Form.show()
sys.exit(app.exec())