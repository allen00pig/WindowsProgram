from PyQt6 import QtWidgets ,QtGui ,QtCore
import sys

app = QtWidgets.QApplication(sys.argv)

Form = QtWidgets.QWidget()
Form.setWindowTitle("W10")
Form.resize(360, 240)
Form.setStyleSheet("background-color: #FFCCCC;")

label1 = QtWidgets.QLabel(Form)
label1.setText("Hello, World!")
label1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

font = QtGui.QFont()
font.setFamily("Arial")
font.setPointSize(20)
font.setBold(True)
font.setItalic(True)
font.setStrikeOut(True)
label1.setFont(font)

imglabel = QtWidgets.QLabel(Form)
imglabel.setGeometry(60,60, 100, 100)
img = QtGui.QImage('1.jpg')                 # 讀取圖片
imglabel.setPixmap(QtGui.QPixmap.fromImage(img))  # 加入圖片

label3 = QtWidgets.QLabel(Form)
label3.setText('hello world, how are you?')
label3.move(300, 10)    # 設定位置
label3.setWordWrap(True)    # 設定可以換行

label3.setStyleSheet('''
    background:#fff;
    color:#f00;
    font-size:20px;
    font-weight:bold;
    border:2px dashed #000;
    padding:20px;
    text-align:center;
''')

btn1 = QtWidgets.QPushButton(Form)
btn1.setText("Press Me to plus 1")
btn1.move(270, 270)

btn2 = QtWidgets.QPushButton(Form)
btn2.setText("Press Me to minus 1")
btn2.setGeometry(270, 300, 100, 50)
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
a = 0
def show():
    global a
    a = a + 1
    label1.setText(str(a))
label = QtWidgets.QLabel(Form)
label.setText('0')
label.setStyleSheet('font-size:20px;')
label.setGeometry(50,30,100,30)

btn = QtWidgets.QPushButton(Form)
btn.setText('增加數字')
btn.setGeometry(50,60,100,30)
btn.clicked.connect(show)  

Form.show()
sys.exit(app.exec())