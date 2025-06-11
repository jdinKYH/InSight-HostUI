from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QUrl

class BrowserWidget(QWidget):
    """
    In-Sight 웹페이지를 표시하는 브라우저 위젯
    """
    def __init__(self, url: str = "http://127.0.0.1"):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.webview = QWebEngineView()
        layout.addWidget(self.webview)
        self.webview.setUrl(QUrl(url)) 