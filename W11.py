from PyQt6 import QtWidgets ,QtGui ,QtCore
import sys

app = QtWidgets.QApplication(sys.argv)

Form = QtWidgets.QWidget()
Form.setWindowTitle("W11")
Form.resize(600, 480)
Form.setStyleSheet("background-color: #FFCCCC;")
Form.setWindowIcon(QtGui.QIcon("123.ico"))

def Rb_show():
    BtnLabel.setText("You selected: " + str(group.checkedId()))
    
arr = ['','','']
    
def Ck_show(cb,i):
    if cb.isChecked():
        arr[i] = str(cb.text())
    else:
        arr[i] = ''
    output = ''.join(arr)
    BtnLabel2.setText(output)


rb_a = QtWidgets.QRadioButton("Option A", Form)
rb_a.setGeometry(QtCore.QRect(50, 50, 100, 30))
rb_a.setStyleSheet('''
                   QRadioButton{
                       color: #0000FF; font-size: 16px;
                   }
                   QRadioButton:hover{
                       background-color: #FFCCFF;
                   }
                   ''')

rb_a.setChecked(True)
rb_b = QtWidgets.QRadioButton("Option B", Form)
rb_b.setGeometry(QtCore.QRect(50, 100, 100, 30))
rb_b.setStyleSheet("color: #00FF00; font-size: 16px;")

rb_c = QtWidgets.QRadioButton("Option C", Form)
rb_c.setGeometry(QtCore.QRect(50, 150, 100, 30))
rb_c.setStyleSheet("color: #FF0000; font-size: 16px;")

rb_d = QtWidgets.QRadioButton("Option D", Form)
rb_d.setGeometry(QtCore.QRect(50, 200, 100, 30))
rb_d.setStyleSheet("color: #FFFF00; font-size: 16px;")

group = QtWidgets.QButtonGroup(Form)
group.addButton(rb_a, 1)
group.addButton(rb_b, 2)
group.addButton(rb_c, 3)
group.addButton(rb_d, 4)
group.buttonClicked.connect(Rb_show)

BtnLabel = QtWidgets.QLabel(Form)
BtnLabel.setGeometry(QtCore.QRect(200, 50, 300, 30))
BtnLabel.setStyleSheet("color: #000000; font-size: 16px;")

cb_style = '''
        QCheckBox{
            color: #0000FF; font-size: 16px;
        }
        QCheckBox:hover{
            background-color: #FFCCFF;
        }
        QCheckBox:checked{
            background-color: #FFCCFF;
        }
            
'''

cb_a = QtWidgets.QCheckBox("Check A", Form)
cb_a.setGeometry(QtCore.QRect(200, 100, 100, 30))
cb_a.setStyleSheet(cb_style)
cb_a.setText("Check A")
cb_a.clicked.connect(lambda:Ck_show(cb_a, 0))

cb_b = QtWidgets.QCheckBox("Check B", Form)
cb_b.setGeometry(QtCore.QRect(200, 150, 100, 30))
cb_b.setStyleSheet("color: #00FF00; font-size: 16px;")
cb_b.setText("Check B")
cb_b.clicked.connect(lambda:Ck_show(cb_b, 1))

cb_c = QtWidgets.QCheckBox("Check C", Form)
cb_c.setGeometry(QtCore.QRect(200, 200, 100, 30))
cb_c.setStyleSheet("color: #FF0000; font-size: 16px;")
cb_c.setText("Check C")
cb_c.clicked.connect(lambda:Ck_show(cb_c, 2))

BtnLabel2 = QtWidgets.QLabel(Form)
BtnLabel2.setGeometry(QtCore.QRect(350, 100, 300, 30))
BtnLabel2.setStyleSheet("color: #000000; font-size: 16px;")





Form.show()
sys.exit(app.exec())
