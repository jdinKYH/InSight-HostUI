from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextEdit, QComboBox

class LogPanel(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("로그 출력"))
        self.log_edit = QTextEdit()
        self.log_edit.setReadOnly(True)
        main_layout.addWidget(self.log_edit)
        main_layout.addWidget(QLabel("로그 레벨/필터"))
        self.level_combo = QComboBox()
        self.level_combo.addItems(["ALL", "INFO", "WARNING", "ERROR"])
        main_layout.addWidget(self.level_combo)
        self.setLayout(main_layout) 