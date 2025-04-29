import sys
from PyQt6 import QtWidgets, QtGui, QtCore
import os

app = QtWidgets.QApplication(sys.argv)

Form = QtWidgets.QWidget()
Form.setWindowTitle("W11")
Form.resize(600, 480)
Form.setStyleSheet("background-color: #FFCCCC;")
Form.setWindowIcon(QtGui.QIcon("123.ico"))

grview = QtWidgets.QGraphicsView(Form)
grview.setGeometry(QtCore.QRect(50, 50, 500, 400))
scene = QtWidgets.QGraphicsScene(Form)
scene.setSceneRect(0, 0, 500, 400)
img = QtGui.QPixmap("2.png")
img = img.scaled(500, 400, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
x = 20
y = 20
dx = int((500 - img.width()) / 2)
dy = int((400 - img.height()) / 2)
scene.setSceneRect(x, y, img.width(), img.height())
scene.addPixmap(img)
grview.setScene(scene)





Form.show()
sys.exit(app.exec())