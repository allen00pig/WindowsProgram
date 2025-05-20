import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                             QDateEdit, QPushButton, QCalendarWidget,
                             QMessageBox)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QFont

def handle_date_changed(date, current_date_label):
    print(f"日期已改變 (dateChanged 信號)：{date.toString('yyyy-MM-dd')}")
    current_date_label.setText(f"目前選擇的日期：{date.toString('yyyy-MM-dd')}")

def handle_user_date_changed(date):
    QMessageBox.information(None, "日期選擇", f"使用者已選擇日期：{date.toString('yyyy-MM-dd')}")
    print(f"使用者已選擇日期 (userDateChanged 信號)：{date.toString('yyyy-MM-dd')}")

def get_current_date(date_edit):
    current_date = date_edit.date()
    QMessageBox.information(None, "目前日期", f"目前 QDateEdit 中的日期是：{current_date.toString('yyyy-MM-dd')}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("QDateEdit 功能範例")
    window.setGeometry(100, 100, 400, 300)

    layout = QVBoxLayout()

    # 建立 QDateEdit 部件
    date_edit = QDateEdit()
    date_edit.setFont(QFont("Arial", 12))
    layout.addWidget(date_edit)

    # 設定初始日期
    initial_date = QDate(2025, 5, 20)
    date_edit.setDate(initial_date)
    print(f"初始日期已設定為：{initial_date.toString('yyyy/MM/dd')}")

    # 設定日期顯示格式
    date_edit.setDisplayFormat("yyyy-MM-dd")
    print(f"日期顯示格式已設定為：{date_edit.displayFormat()}")

    # 設定日期範圍
    min_date = QDate(2024, 1, 1)
    max_date = QDate(2026, 12, 31)
    date_edit.setDateRange(min_date, max_date)
    print(f"日期範圍已設定為：{min_date.toString('yyyy/MM/dd')} 到 {max_date.toString('yyyy/MM/dd')}")

    # 啟用日曆彈出
    date_edit.setCalendarPopup(True)
    print("日曆彈出已啟用")

    # 取得並自訂日曆小部件
    calendar = date_edit.calendarWidget()
    if calendar:
        calendar.setFirstDayOfWeek(Qt.DayOfWeek.Monday)
        calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.ISOWeekNumbers)
        print("日曆小部件的第一天已設定為星期一，垂直表頭顯示週數")

    # 建立用於顯示目前日期的標籤
    current_date_label = QLabel(f"目前選擇的日期：{date_edit.date().toString('yyyy-MM-dd')}")
    layout.addWidget(current_date_label)

    # 連接日期改變信號
    date_edit.dateChanged.connect(lambda date: handle_date_changed(date, current_date_label))
    date_edit.userDateChanged.connect(handle_user_date_changed)

    # 按鈕用於取得目前日期
    get_date_button = QPushButton("取得目前選擇的日期")
    get_date_button.clicked.connect(lambda: get_current_date(date_edit))
    layout.addWidget(get_date_button)

    window.setLayout(layout)
    window.show()
    sys.exit(app.exec())