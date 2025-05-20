import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTimeEdit, QLabel, QMessageBox
from PyQt6.QtCore import QTime

def handle_user_time_changed(time):
    """當使用者完成時間編輯後觸發的函數。"""
    formatted_time = time.toString("HH:mm:ss")
    QMessageBox.information(None, "時間已編輯", f"使用者已選擇時間：{formatted_time}")
    print(f"使用者已選擇時間：{formatted_time}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("QTimeEdit userTimeChanged 範例 (無 Class - PyQt6)")
    window.setGeometry(100, 100, 300, 150)

    layout = QVBoxLayout()

    time_edit = QTimeEdit()
    time_edit.setTime(QTime.currentTime())  # 設定初始時間

    time_label = QLabel("請編輯時間：")
    result_label = QLabel("上次編輯時間：")

    # 連接 userTimeChanged 信號到 handle_user_time_changed 函數
    time_edit.userTimeChanged.connect(handle_user_time_changed)

    layout.addWidget(time_label)
    layout.addWidget(time_edit)
    layout.addWidget(result_label)
    window.setLayout(layout)

    window.show()
    sys.exit(app.exec())