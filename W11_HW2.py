import sys
from PyQt6 import QtWidgets, QtCore, QtGui

app = QtWidgets.QApplication(sys.argv)

Form = QtWidgets.QWidget()
Form.setObjectName("W11_HW2")
Form.setWindowTitle("動態顯示單選與複選")
Form.resize(500, 400)
Form.setStyleSheet("background-color: #222222;")

RB_btn1 = QtWidgets.QRadioButton("選項 1", Form)
RB_btn1.setGeometry(QtCore.QRect(50, 50, 100, 30))
RB_btn2 = QtWidgets.QRadioButton("選項 2", Form)
RB_btn2.setGeometry(QtCore.QRect(50, 100, 100, 30))

CB_btnA = QtWidgets.QCheckBox("選項 A", Form)
CB_btnA.setGeometry(QtCore.QRect(50, 150, 100, 30))
CB_btnB = QtWidgets.QCheckBox("選項 B", Form)
CB_btnB.setGeometry(QtCore.QRect(50, 200, 100, 30))
CB_btnC = QtWidgets.QCheckBox("選項 C", Form)
CB_btnC.setGeometry(QtCore.QRect(50, 250, 100, 30))
CB_btnD = QtWidgets.QCheckBox("選項 D", Form)
CB_btnD.setGeometry(QtCore.QRect(50, 300, 100, 30))




def update_ui():
    if RB_btn1.isChecked():
        CB_btnA.show()
        CB_btnB.show()
        CB_btnC.show()
        CB_btnD.hide()
    elif RB_btn2.isChecked():
        CB_btnA.hide()
        CB_btnB.hide()
        CB_btnC.hide()
        CB_btnD.show()


# 更改複選框的樣式
# 根據是否選中來改變顏色
# 這裡使用綠色表示選中，紅色表示未選中
def update_checkbox_styles():
    for cb in [CB_btnA, CB_btnB, CB_btnC, CB_btnD]:
        if cb.isChecked():
            cb.setStyleSheet("background-color: green;")
        else:
            cb.setStyleSheet("background-color: red;")

# 連接使其更新 UI
RB_btn1.clicked.connect(update_ui)
RB_btn2.clicked.connect(update_ui)
CB_btnA.clicked.connect(lambda: (update_ui(), update_checkbox_styles()))
CB_btnB.clicked.connect(lambda: (update_ui(), update_checkbox_styles()))
CB_btnC.clicked.connect(lambda: (update_ui(), update_checkbox_styles()))
CB_btnD.clicked.connect(lambda: (update_ui(), update_checkbox_styles()))

# 啟動 UI 更新
update_ui()
update_checkbox_styles()


Form.show()
sys.exit(app.exec())