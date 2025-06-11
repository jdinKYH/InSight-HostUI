from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from .telnet_panel import TelnetPanel
from .param_panel import ParamPanel
from .log_panel import LogPanel

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        

        
        # 3분할 본문
        content_layout = QHBoxLayout()
        
        # TelnetPanel 생성
        self.telnet_panel = TelnetPanel()
        
        # ParamPanel에 TelnetManager 전달
        self.param_panel = ParamPanel()
        self.param_panel.set_telnet_manager(self.telnet_panel.telnet)
        
        self.log_panel = LogPanel()
        
        content_layout.addWidget(self.telnet_panel, 1)
        content_layout.addWidget(self.param_panel, 2)
        content_layout.addWidget(self.log_panel, 1)
        
        main_layout.addLayout(content_layout, stretch=1)
        self.setLayout(main_layout)

 