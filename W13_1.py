from PyQt6 import QtWidgets, QtGui, QtCore,QtMultimedia
import sys,os

app = QtWidgets.QApplication(sys.argv)

Form = QtWidgets.QWidget()
Form.setWindowTitle("W13_1")
Form.setStyleSheet("background-color: #FFCCCC;")
Form.resize(600, 480)
Form.setObjectName("W13_1")

a = 0

label = QtWidgets.QLabel(Form)
label.setGeometry(10, 10, 100, 30)
label.setStyleSheet("background-color: #FFCCCC; font-size: 20px;")

def count():
    global a
    a += 1
    label.setText(str(a))
    
def start():
    timer.start(500)          # 啟用定時器

def pause():
    timer.stop()              # 停止定時器

def reset():
    global a
    a = 0                     # 數值歸零
    label.setText('0')
    timer.stop()              # 停止定時器

    
timer = QtCore.QTimer(Form)
timer.timeout.connect(count)


btnStart = QtWidgets.QPushButton(Form)
btnStart.setGeometry(10, 50, 100, 30)
btnStart.setStyleSheet("background-color: #FFCCCC;")
btnStart.setText("Start")
btnStart.clicked.connect(lambda: start())

btnStop = QtWidgets.QPushButton(Form)
btnStop.setGeometry(10, 90, 100, 30)
btnStop.setStyleSheet("background-color: #FFCCCC;")
btnStop.setText("Stop")
btnStop.clicked.connect(lambda: pause())

btnReset = QtWidgets.QPushButton(Form)
btnReset.setGeometry(10, 130, 100, 30)
btnReset.setStyleSheet("background-color: #FFCCCC;")
btnReset.setText("Reset")
btnReset.clicked.connect(lambda: reset())

Form.show()
sys.exit(app.exec())
