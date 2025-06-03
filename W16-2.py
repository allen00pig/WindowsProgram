from PyQt6 import QtWidgets, QtGui, QtCore,QtMultimedia
import sys,os


app = QtWidgets.QApplication(sys.argv)
Form = QtWidgets.QMainWindow()
Form.setWindowTitle("W16")
Form.resize(1024, 818)
Form.setStyleSheet("background-color: #777;")

canvas = QtGui.QPixmap(1024, 768)
canvas.fill(QtGui.QColor("#ffffff"))

label = QtWidgets.QLabel(Form)
label.setGeometry(0, 40, 1024, 768)
label.setPixmap(canvas)

last_x, last_y = None, None
penSize = 10
penColor = QtGui.QColor("#000000")

def release(self):
    global last_x, last_y
    last_x, last_y = None, None
    
def press(self):
    global penColor, penSize,canvas
    mx = int(QtGui.QEnterEvent.position(self).x())
    my = int(QtGui.QEnterEvent.position(self).y())
    qPainter = QtGui.QPainter(canvas)
    qPainter.begin(canvas)
    qPainter.setPen(QtGui.QPen(QtGui.QColor(penColor), penSize, QtCore.Qt.PenStyle.SolidLine,QtCore.Qt.PenCapStyle.RoundCap))
    qPainter.drawPoint(mx, my)
    qPainter.end()
    label.setPixmap(canvas)
    Form.update()

def draw(self):
    global last_x, last_y, penColor, penSize, canvas
    mx = int(QtGui.QEnterEvent.position(self).x())
    my = int(QtGui.QEnterEvent.position(self).y())
    if last_x is None:
        last_x, last_y = mx, my
        return
    qPainter = QtGui.QPainter()
    qPainter.begin(canvas)
    pen = QtGui.QPen(QtGui.QColor(penColor), penSize, QtCore.Qt.PenStyle.SolidLine,QtCore.Qt.PenCapStyle.RoundCap)
    pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)

    qPainter.setPen(pen)
    qPainter.drawLine(last_x, last_y, mx, my)
    qPainter.end()
    label.setPixmap(canvas)
    Form.update()
    last_x, last_y = mx, my
    
label.mousePressEvent = press
label.mouseMoveEvent = draw
label.mouseReleaseEvent = release

def change_pen_color(self, color):
    global penColor,btnColor
    penColor = QtGui.QColor(color)
    for i in btnColor:
        btnColor[i].setDisabled(False)
    self.setDisabled(True)
    
colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#00ffff', '#ff00ff', '#ffffff', '#000000']
btnColor = {}
for i in colors:
    index = colors.index(i)
    btnColor[i] = QtWidgets.QPushButton(Form)
    btnColor[i].setStyleSheet('''
        QPushButton {
            background: '''+i+''';
            margin-right: 5px;
        }
        QPushButton:disabled {
            border: 3px solid #000;
        }
    ''')
    btnColor[i].setGeometry(10 + index * 40, 780, 30, 30)
    btnColor[i].clicked.connect(lambda checked,b = btnColor[i],c = i: change_pen_color(b,c))

def new_canvas():
    ret = mbox.question(Form, 'question', '確定要清除畫布嗎？')
    if ret == mbox.StandardButton.Yes:
        canvas.fill(QtGui.QColor("#ffffff"))
        label.setPixmap(canvas)
    else:
        return
    
def save_canvas():
    filePath,filterType = QtWidgets.QFileDialog.getSaveFileName(Form, "Save Image", "", "PNG Files (*.png);;JPEG Files (*.jpg);;BMP Files (*.bmp)")
    if filePath:
        label.pixmap().save(filePath)
        
def close_app():
    ret = QtWidgets.QMessageBox.question(Form, 'question', '確定要關閉應用程式嗎？')
    if ret == QtWidgets.QMessageBox.StandardButton.Yes:
        app.quit()
    else:
        return
mbox = QtWidgets.QMessageBox(Form)
menuBar = QtWidgets.QMenuBar(Form)
menuFile = QtWidgets.QMenu("File")
actionNew = QtGui.QAction("New")
actionNew.triggered.connect(new_canvas)
menuFile.addAction(actionNew)
actionSave = QtGui.QAction("Save")
menuFile.addAction(actionSave)
actionSave.triggered.connect(save_canvas)
actionExit = QtGui.QAction("Exit")
actionExit.triggered.connect(close_app)
menuFile.addAction(actionExit)
menuBar.addMenu(menuFile)


Form.show()
sys.exit(app.exec())
