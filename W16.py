from PyQt6 import QtWidgets, QtGui, QtCore,QtMultimedia
import sys,os


app = QtWidgets.QApplication(sys.argv)
Form = QtWidgets.QMainWindow()
Form.setWindowTitle("W16")
Form.resize(1024, 800)
Form.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF;")

label1 = QtWidgets.QLabel(Form)
label1.setText("Mouse X: 0, Y: 0")
label1.setGeometry(QtCore.QRect(10, 10, 200, 30))

def mouseMove(self) :
    mx = QtGui.QCursor.pos().x();
    my = QtGui.QCursor.pos().y()
    label1.setText(f"Mouse X: {mx}, Y: {my}")
    
Form.setMouseTracking(True)
Form.mouseMoveEvent = mouseMove




Form.show()
sys.exit(app.exec())
