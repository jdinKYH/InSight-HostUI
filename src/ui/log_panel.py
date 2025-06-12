from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextEdit, QComboBox
from PyQt5.QtCore import QDateTime

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
    
    def add_log(self, message: str):
        """
        로그 메시지를 추가합니다.
        
        Args:
            message (str): 추가할 로그 메시지
        """
        # 타임스탬프가 이미 포함되어 있지 않은 경우에만 추가
        if not message.startswith('['):
            timestamp = QDateTime.currentDateTime().toString("HH:mm:ss.zzz")
            formatted_message = f"[{timestamp}] {message}"
        else:
            formatted_message = message
        
        # 로그 텍스트에 추가
        self.log_edit.append(formatted_message)
        
        # 자동 스크롤 (최신 로그가 보이도록)
        scrollbar = self.log_edit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def clear_log(self):
        """로그를 모두 지웁니다."""
        self.log_edit.clear()
    
    def get_log_text(self) -> str:
        """현재 로그 텍스트를 반환합니다."""
        return self.log_edit.toPlainText() 