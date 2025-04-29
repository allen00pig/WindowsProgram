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
grview.setGeometry(0, 0, 300, 300)
scene = QtWidgets.QGraphicsScene()
scene.setSceneRect(0, 0, 200, 200)
img1 = QtGui.QPixmap("1.jpg")
img1 = img1.scaled(200, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
qitem1 = QtWidgets.QGraphicsPixmapItem(img1)
img2 = QtGui.QPixmap("2.jpg")
img2 = img2.scaled(200, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)  
qitem2 = QtWidgets.QGraphicsPixmapItem(img2)

scene.addItem(qitem1)
scene.addItem(qitem2)
grview.setScene(scene)





Form.show()
sys.exit(app.exec())