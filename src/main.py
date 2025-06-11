import sys
import logging
import os
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from utils.config import ConfigManager

def setup_logging() -> None:
    """
    파일 및 콘솔 로그 설정
    """
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler('logs/app.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def main() -> None:
    """
    애플리케이션 진입점
    """
    setup_logging()
    config = ConfigManager()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 