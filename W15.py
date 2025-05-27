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

Form_h = Form.height()
Form_w = Form.width()


btn1 = QtWidgets.QPushButton(Form)
btn1.setText("Biggest")
btn1.setGeometry(QtCore.QRect(20, 20, 100, 30))
btn1.clicked.connect(lambda: Form.showMaximized())

btn2 = QtWidgets.QPushButton(Form)
btn2.setText("Normal")
btn2.setGeometry(QtCore.QRect(140, 20, 100, 30))
btn2.clicked.connect(lambda: Form.showNormal())

btn3 = QtWidgets.QPushButton(Form)
btn3.setText("Move Screen")
btn3.clicked.connect(lambda: Form.move(100, 100))
btn3.setGeometry(QtCore.QRect(260, 20, 100, 30))

btn4 = QtWidgets.QPushButton(Form)
btn4.setText("Smallest")
btn4.setGeometry(QtCore.QRect(380, 20, 100, 30))
btn4.clicked.connect(lambda: Form.showMinimized())

btn5 = QtWidgets.QPushButton(Form)
btn5.setText("Center")
btn5.setGeometry(QtCore.QRect(500, 20, 100, 30))
btn5.clicked.connect(lambda: CenterForm())


def CenterForm():
    global Form_w, Form_h, screen_w, screen_h
    newX = int((screen_w - Form_w) / 2)
    newY = int((screen_h - Form_h) / 2)
    Form.move(newX, newY)

def closeEvent(self):
    print("Form is closing")

def moveEvent(self):
    print(f"Form moved to ({Form.x()}, {Form.y()})")

def resizeEvent(self):
    print(f"Form resized to {Form.width()}x{Form.height()}")

def showEvent(self):
    print("Form is shown")

def focusInEvent(self):
    print("Form is focused")
    
def focusOutEvent(self):
    print("Form lost focus")    

Form.setFocus()
Form.closeEvent = closeEvent
Form.moveEvent = moveEvent
Form.resizeEvent = resizeEvent
Form.showEvent = showEvent
Form.focusInEvent = focusInEvent
Form.focusOutEvent = focusOutEvent

Form.show()
sys.exit(app.exec())
