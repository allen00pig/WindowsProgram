import sys
from PyQt6 import QtWidgets, QtCore, QtGui

app = QtWidgets.QApplication(sys.argv)

Form = QtWidgets.QWidget()
Form.setObjectName("W11_HW1")
Form.resize(500, 400)
Form.setWindowTitle("PyQt6 Advanced Styling")
TitleLabel = QtWidgets.QLabel(Form)
TitleLabel.setText("Welcome to PyQt6 Styling!")
TitleLabel.setGeometry(100,100,300,100)
TitleLabel.setStyleSheet('''
    font-size: 30px;
    color: green;
    background-color: yellow;
    border: 3px solid red;
    padding: 50px;
    qproperty-alignment: 'AlignCenter';
''')




Form.show()
sys.exit(app.exec())