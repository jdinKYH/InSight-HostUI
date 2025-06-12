from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from .telnet_panel import TelnetPanel
from .param_panel import ParamPanel
from .log_panel import LogPanel
from .job_panel import JobPanel

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        
        # 3분할 본문
        content_layout = QHBoxLayout()
        
        # TelnetPanel 생성
        self.telnet_panel = TelnetPanel()
        
        # 중앙 패널 컨테이너 생성
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(5)
        
        # JobPanel 생성 및 추가
        self.job_panel = JobPanel()
        central_layout.addWidget(self.job_panel)
        
        # ParamPanel 생성 및 추가
        self.param_panel = ParamPanel()
        central_layout.addWidget(self.param_panel, 1)  # stretch=1로 남은 공간 차지
        
        central_widget.setLayout(central_layout)
        
        # LogPanel 생성
        self.log_panel = LogPanel()
        
        # 레이아웃에 패널들 추가
        content_layout.addWidget(self.telnet_panel, 1)
        content_layout.addWidget(central_widget, 2)
        content_layout.addWidget(self.log_panel, 1)
        
        main_layout.addLayout(content_layout, stretch=1)
        self.setLayout(main_layout)
        
        # 컴포넌트 간 연결 설정
        self.setup_connections()
    
    def setup_connections(self):
        """컴포넌트 간 연결을 설정합니다."""
        # TelnetManager를 ParamPanel에 전달
        self.param_panel.set_telnet_manager(self.telnet_panel.telnet)
        
        # TelnetManager를 JobPanel에 전달
        self.job_panel.set_telnet_manager(self.telnet_panel.telnet)
        
        # LogPanel을 JobPanel에 전달
        self.job_panel.set_log_panel(self.log_panel)
        
        # TelnetPanel의 연결 상태 변경 시 JobPanel UI 업데이트
        # TelnetPanel에서 상태 변경 시그널이 있다면 연결
        if hasattr(self.telnet_panel, 'connection_changed'):
            self.telnet_panel.connection_changed.connect(self.job_panel.update_ui_state)

 