from PyQt6 import QtWidgets, QtGui, QtCore,QtMultimedia
import sys,os


app = QtWidgets.QApplication(sys.argv)
Form = QtWidgets.QWidget()
screen = QtWidgets.QApplication.screens()
screen_size = screen[0].size()
screen_w = screen_size.width()
screen_h = screen_size.height()
Form.setWindowTitle("W15")
Form.setStyleSheet("background-color: #FFCCCC;")
Form.resize(600, 400)
Form.setObjectName("W15")

label1 = QtWidgets.QLabel(Form)
label1.setText("Hello, PyQt6!")
label1.setGeometry(QtCore.QRect(20, 20, 200, 30))
label1.setStyleSheet("font-size: 20px; color: blue;")

btn1 = QtWidgets.QPushButton(Form)
btn1.setText("Click to open a New Window")
btn1.setGeometry(QtCore.QRect(20, 60, 250, 30))
btn1.setStyleSheet("font-size: 16px; color: green;")
btn1.clicked.connect(lambda: Form2.show())

Form2 = QtWidgets.QWidget()
Form2.setWindowTitle("New Window")
Form2.setStyleSheet("background-color: #CCFFCC;")
label2 = QtWidgets.QLabel(Form2)
label2.setText("This is a new window!")
label2.setGeometry(QtCore.QRect(20, 20, 200, 30))
btn2 = QtWidgets.QPushButton(Form2)
btn2.setText("Close this Window")
btn2.setGeometry(QtCore.QRect(20, 60, 200, 30))
btn2.setStyleSheet("font-size: 16px; color: red;")
btn2.clicked.connect(Form2.close)


Form.show()
sys.exit(app.exec())
