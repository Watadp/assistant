import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QVBoxLayout, QToolBar, QWidget, QSplitter, QPushButton
from PyQt5.QtGui import QColor, QPalette

class LeftToolbar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dark_mode = False  # Biến để theo dõi trạng thái Dark Mode
        self.init_ui()

    def init_ui(self):
        # Tạo thanh toolbar
        toolbar = QToolBar("Left Toolbar")
        self.addToolBar(toolbar)

        # Tạo các action cho toolbar
        action1 = QAction("Action 1", self)
        action2 = QAction("Action 2", self)
        action3 = QAction("Action 3", self)

        # Thêm các action vào thanh toolbar
        toolbar.addAction(action1)
        toolbar.addAction(action2)
        toolbar.addAction(action3)

        # Tạo layout cho cửa sổ chính
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Tạo Splitter
        splitter = QSplitter()

        # Tạo layout cho phần taskbar
        toolbar_widget = QWidget()
        toolbar_layout = QVBoxLayout(toolbar_widget)
        toolbar_layout.addWidget(toolbar)

        # Thêm Splitter vào layout chính
        main_layout.addWidget(splitter)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Thiết lập kích thước cho thanh toolbar
        splitter.addWidget(toolbar_widget)
        splitter.setSizes([int(self.width() / 3), int(self.width() * 2 / 3)])


        # Nút chuyển đổi Dark Mode
        toggle_mode_btn = QPushButton("Toggle Mode", self)
        toggle_mode_btn.clicked.connect(self.toggle_mode)
        main_layout.addWidget(toggle_mode_btn)

        self.setCentralWidget(main_widget)
        self.setWindowTitle("Left Toolbar")
        self.setGeometry(100, 100, 600, 400)

        # Thiết lập màu nền Dark Mode
        self.set_app_palette()
        self.resize(980, 625)
        self.show()

    def set_app_palette(self):
        # Thiết lập màu nền
        dark_mode_color = QColor("#27263c") if self.dark_mode else QColor("white")
        palette = self.palette()
        palette.setColor(QPalette.Window, dark_mode_color)
        self.setPalette(palette)

    def toggle_mode(self):
        self.dark_mode = not self.dark_mode
        self.set_app_palette()

def run_app():
    app = QApplication(sys.argv)
    left_toolbar_app = LeftToolbar()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_app()
