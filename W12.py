import sys
from PyQt6 import QtWidgets, QtGui, QtCore
import os

app = QtWidgets.QApplication(sys.argv)

Form = QtWidgets.QWidget()
Form.setWindowTitle("W12")
Form.resize(600, 480)
Form.setStyleSheet("background-color: #FFCCCC;")
Form.setWindowIcon(QtGui.QIcon("123.ico"))

def show():
    text,ok = QtWidgets.QInputDialog.getText(Form, "", "Enter text:")
    label1.setText(text)

def showInt():
    num,ok = QtWidgets.QInputDialog.getInt(Form, "", "Enter number:")
    label1.setText(str(num))
    
def showDouble():
    num,ok = QtWidgets.QInputDialog.getDouble(Form, "", "Enter number:")
    label1.setText(str(num))

label1 = QtWidgets.QLabel(Form)
label1.setGeometry(10, 10, 580, 50)
label1.setStyleSheet('''
    background:#fff;
    color:#f00;
    font-size:20px;
    padding:1px;
    text-align:center;
''')

btn1 = QtWidgets.QPushButton(Form)
btn1.setGeometry(10, 70, 580, 50)
btn1.setText("Press Me to show Input Dialog")
btn1.clicked.connect(show)
btn1.setStyleSheet('''
    QPushButton {
        font-size:20px;
        color: #f00;
        background: #ff0;
        border: 2px solid #000;
    }
    QPushButton:hover {
        color: #ff0;
        background: #f00;
    }
''')

btn2 = QtWidgets.QPushButton(Form)
btn2.setGeometry(10, 130, 580, 50)
btn2.setText("Press Me to show Int Input Dialog")
btn2.clicked.connect(showInt)
btn2.setStyleSheet('''
    QPushButton {
        font-size:20px;
        color: #f00;
        background: #ff0;
        border: 2px solid #000;
    }
    QPushButton:hover {
        color: #ff0;
        background: #f00;
    }
''')

btn3 = QtWidgets.QPushButton(Form)
btn3.setGeometry(10, 190, 580, 50)
btn3.setText("Press Me to show Double Input Dialog")
btn3.clicked.connect(showDouble)
btn3.setStyleSheet('''
    QPushButton {
        font-size:20px;
        color: #f00;
        background: #ff0;
        border: 2px solid #000;
    }
    QPushButton:hover {
        color: #ff0;
        background: #f00;
    }
''')

now = QtCore.QTime.currentTime()

t1 = QtWidgets.QTimeEdit(Form)
t1.setGeometry(10, 250, 580, 50)
t1.setDisplayFormat("hh:mm:ss")
t1.setTime(now)

t2 = QtWidgets.QTimeEdit(Form)
t2.setGeometry(10, 310, 580, 50)
t2.setDisplayFormat("hh:mm ap")
t2.setTime(now)

t3 = QtWidgets.QTimeEdit(Form)
t3.setGeometry(10, 370, 580, 50)
t3.setDisplayFormat("ap hh:mm:ss")
t3.setTime(now)



Form.show()
sys.exit(app.exec())