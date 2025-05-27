from PyQt6 import QtWidgets, QtGui, QtCore, QtWebEngineWidgets
import sys, os

app = QtWidgets.QApplication(sys.argv)
Form = QtWidgets.QWidget()
screen = QtWidgets.QApplication.screens()
screen_size = screen[0].size()
screen_w = screen_size.width()
screen_h = screen_size.height()
Form.setWindowTitle("W15")
Form.setStyleSheet("background-color: #FFBBBB;")
Form.resize(1024, 768)
Form.setObjectName("W15")

Web = QtWebEngineWidgets.QWebEngineView(Form)
Web.move(0, 30)
Web.resize(1024, 768)
Web.setUrl(QtCore.QUrl("https://google.com"))
btn1 = QtWidgets.QPushButton(Form)
btn1.setText("reload")
btn1.setGeometry(0, 0, 100, 30)
btn1.clicked.connect(lambda: Web.reload())
btn2 = QtWidgets.QPushButton(Form)
btn2.setText("back")
btn2.setGeometry(100, 0, 100, 30)
btn2.clicked.connect(lambda: Web.back())
btn3 = QtWidgets.QPushButton(Form)
btn3.setText("forward")
btn3.setGeometry(200, 0, 100, 30)
btn3.clicked.connect(lambda: Web.forward())
btn4 = QtWidgets.QPushButton(Form)
btn4.setText("stop")
btn4.setGeometry(300, 0, 100, 30)
btn4.clicked.connect(lambda: Web.stop())

input_url = QtWidgets.QLineEdit(Form)
input_url.setGeometry(400, 0, 600, 30)
input_url.setPlaceholderText("輸入網址並按 Enter 鍵")
def load_url():
    url = input_url.text()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    Web.setUrl(QtCore.QUrl(url))
input_url.returnPressed.connect(load_url)
input_url.setStyleSheet("font-size: 16px; padding: 5px;")


Form.show()
sys.exit(app.exec())
