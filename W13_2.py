from PyQt6 import QtWidgets, QtGui, QtCore,QtMultimedia
import sys,os


app = QtWidgets.QApplication(sys.argv)
Form = QtWidgets.QWidget()
Form.setWindowTitle("W13_2")
Form.setStyleSheet("background-color: #FFCCCC;")
Form.resize(600, 480)
Form.setObjectName("W13_2")


def key(self):
    keycode = self.key()
    label.setText(str(keycode))

Form.keyPressEvent = key
label = QtWidgets.QLabel(Form)
label.setGeometry(10, 10, 100, 30)

label2 = QtWidgets.QLabel(Form)
label2.setGeometry(10, 50, 100, 30)

label2.setText(f'''
    x: {Form.x()}
    y: {Form.y()}
    width: {Form.width()}
    height: {Form.height()}
    windowTitle: {Form.windowTitle()}
    '''
)



Form.show()
sys.exit(app.exec())
