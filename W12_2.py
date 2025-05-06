import sys
import os
from PyQt6 import QtWidgets, QtCore, QtGui

app = QtWidgets.QApplication(sys.argv)
app.setApplicationName("W12_2")

Form = QtWidgets.QWidget()
Form.setObjectName("W12_2")
Form.setWindowTitle("W12_2")
Form.resize(600, 480)
Form.setStyleSheet("background-color: #FFCCCC;")
Form.setWindowIcon(QtGui.QIcon("123.ico"))

def show():
    items = ["a", "b", "c", "d","e"]
    item,ok = QtWidgets.QInputDialog.getItem(Form, "Select Item", "Items:", items, 0, False)
    label1.setText(item)
    
label1 = QtWidgets.QLabel(Form)
label1.setGeometry(10, 10, 580, 50)
label1.setObjectName("label1")
label1.setStyleSheet("font-size:30px ;")

btn1 = QtWidgets.QPushButton(Form)
btn1.setGeometry(10, 70, 580, 50)
btn1.setObjectName("btn1")
btn1.setText("Select Item")
btn1.setStyleSheet("font-size:20px ;")
btn1.clicked.connect(show)

Form.show()
sys.exit(app.exec())