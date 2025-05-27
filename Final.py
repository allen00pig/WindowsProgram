import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout,
    QPushButton, QMessageBox, QVBoxLayout, QLabel, QComboBox  # 新增 QComboBox
)
from PyQt6.QtCore import Qt

class Cell(QPushButton):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.setFixedSize(30, 30)

    def reset(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.setText('')
        self.setEnabled(True)

class Minesweeper(QMainWindow):
    def __init__(self, rows=10, cols=10, mines=10):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.total_mines = mines

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('PyQt6 踩地雷')

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        # 新增難度選擇
        self.difficulty_box = QComboBox()
        self.difficulty_box.addItems(['簡單', '普通', '困難'])
        self.difficulty_box.currentIndexChanged.connect(self.change_difficulty)
        self.layout.addWidget(self.difficulty_box)

        self.status_label = QLabel('遊戲進行中...')
        self.layout.addWidget(self.status_label)

        self.grid = QGridLayout()
        self.layout.addLayout(self.grid)

        self.cells = [[Cell(x, y) for y in range(self.cols)] for x in range(self.rows)]
        for x in range(self.rows):
            for y in range(self.cols):
                cell = self.cells[x][y]
                cell.clicked.connect(lambda _, cx=x, cy=y: self.handle_click(cx, cy))
                cell.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
                cell.customContextMenuRequested.connect(lambda _, cx=x, cy=y: self.toggle_flag(cx, cy))
                self.grid.addWidget(cell, x, y)

        self.place_mines()

    def change_difficulty(self, index):
        # 根據難度設定 rows, cols, mines
        if index == 0:  # 簡單
            self.rows, self.cols, self.total_mines = 8, 8, 10
        elif index == 1:  # 普通
            self.rows, self.cols, self.total_mines = 12, 12, 25
        else:  # 困難
            self.rows, self.cols, self.total_mines = 16, 16, 50

        # 移除舊格子
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # 重新建立格子
        self.cells = [[Cell(x, y) for y in range(self.cols)] for x in range(self.rows)]
        for x in range(self.rows):
            for y in range(self.cols):
                cell = self.cells[x][y]
                cell.clicked.connect(lambda _, cx=x, cy=y: self.handle_click(cx, cy))
                cell.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
                cell.customContextMenuRequested.connect(lambda _, cx=x, cy=y: self.toggle_flag(cx, cy))
                self.grid.addWidget(cell, x, y)

        self.status_label.setText('遊戲進行中...')
        self.place_mines()

        # 根據難度調整視窗大小
        if index == 0:
            self.resize(350, 400)
        elif index == 1:
            self.resize(500, 550)
        else:
            self.resize(650, 700)

    def place_mines(self):
        positions = [(x, y) for x in range(self.rows) for y in range(self.cols)]
        mine_positions = random.sample(positions, self.total_mines)
        for x, y in mine_positions:
            self.cells[x][y].is_mine = True

    def toggle_flag(self, x, y):
        cell = self.cells[x][y]
        if cell.is_revealed:
            return
        cell.is_flagged = not cell.is_flagged
        cell.setText('🚩' if cell.is_flagged else '')

    def handle_click(self, x, y):
        cell = self.cells[x][y]
        if cell.is_flagged or cell.is_revealed:
            return

        self.reveal_cell(x, y)

        if self.check_win():
            self.game_over(True)

    def reveal_cell(self, x, y):
        cell = self.cells[x][y]
        if cell.is_revealed or cell.is_flagged:
            return

        cell.is_revealed = True
        cell.setEnabled(False)

        if cell.is_mine:
            cell.setText('💣')
            self.game_over(False)
            return

        count = self.count_adjacent_mines(x, y)
        if count > 0:
            cell.setText(str(count))
        else:
            cell.setText('')
            for nx, ny in self.get_neighbors(x, y):
                self.reveal_cell(nx, ny)

    def count_adjacent_mines(self, x, y):
        return sum(1 for nx, ny in self.get_neighbors(x, y) if self.cells[nx][ny].is_mine)

    def get_neighbors(self, x, y):
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.rows and 0 <= ny < self.cols and (dx != 0 or dy != 0):
                    neighbors.append((nx, ny))
        return neighbors

    def check_win(self):
        for row in self.cells:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True

    def game_over(self, win):
        for row in self.cells:
            for cell in row:
                if cell.is_mine:
                    cell.setText('💣')
                cell.setEnabled(False)
        msg = '你贏了！🎉' if win else '你踩到地雷了！💥'
        self.status_label.setText(msg)
        QMessageBox.information(self, '遊戲結束', msg)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Minesweeper(rows=10, cols=10, mines=15)
    game.show()
    sys.exit(app.exec())
