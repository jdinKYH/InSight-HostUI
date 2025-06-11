from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStatusBar, QLabel, QLineEdit, QTableWidget, QPushButton, QTextEdit, QTabWidget, QApplication
from PyQt5.QtCore import Qt, QTimer, QDateTime, QUrl
from PyQt5.QtGui import QFont
from .browser_widget import BrowserWidget
from .settings_page import SettingsPage

class MainWindow(QMainWindow):
    """
    애플리케이션의 메인 윈도우 클래스 (Header, TabWidget, StatusBar 배치)
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("In-Sight HostUI")
        self.setMinimumSize(1280, 720)
        # 시작 시 최대화 상태로 설정
        self.setWindowState(Qt.WindowMaximized)
        self._init_ui()

    def _init_ui(self) -> None:
        # 중앙 위젯 및 전체 레이아웃
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Header
        self.header = QWidget()
        self.header.setFixedHeight(80)
        self.header.setStyleSheet("background-color: #1976d2;")
        header_layout = QHBoxLayout()
        self.header.setLayout(header_layout)
        
        # 좌측 회사명
        self.company_label = QLabel("KNST R&D")
        self.company_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        self.company_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        # 중앙 타이틀
        self.program_label = QLabel("In-Sight Host UI")
        self.program_label.setStyleSheet("color: white; font-size: 40px; font-weight: bold; font-family: 'Segoe UI', 'Bahnschrift', 'Arial Black', Arial, sans-serif;")
        self.program_label.setAlignment(Qt.AlignCenter)
        
        # 우측 영역 (날짜/시간 + 종료 버튼)
        right_widget = QWidget()
        right_layout = QHBoxLayout()
        right_widget.setLayout(right_layout)
        right_layout.setContentsMargins(0, 5, 10, 5)  # 우측 여백 조정
        
        # 날짜/시간/버전 영역
        datetime_widget = QWidget()
        datetime_layout = QVBoxLayout()
        datetime_widget.setLayout(datetime_layout)
        datetime_layout.setContentsMargins(0, 0, 20, 0)  # 버튼과의 간격
        datetime_layout.setSpacing(5)
        
        self.date_label = QLabel()
        self.date_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.date_label.setAlignment(Qt.AlignCenter)
        
        self.time_label = QLabel()
        self.time_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.time_label.setAlignment(Qt.AlignCenter)
        
        self.version_label = QLabel("ver 25.1.0.0")
        self.version_label.setStyleSheet("color: white; font-size: 14px;")
        self.version_label.setAlignment(Qt.AlignCenter)
        
        datetime_layout.addWidget(self.date_label)
        datetime_layout.addWidget(self.time_label)
        datetime_layout.addWidget(self.version_label)
        
        # 종료 버튼
        self.exit_button = QPushButton("종료")
        self.exit_button.setFixedSize(70, 50)  # 크기 조정
        self.exit_button.setStyleSheet("""
            QPushButton {
                background-color: #e53935;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:pressed {
                background-color: #c62828;
            }
        """)
        self.exit_button.clicked.connect(self._on_exit_clicked)
        
        right_layout.addStretch()  # 좌측에 공간 추가
        right_layout.addWidget(datetime_widget)
        right_layout.addWidget(self.exit_button)
        
        # 헤더 레이아웃 배치
        header_layout.addWidget(self.company_label, stretch=1)
        header_layout.addWidget(self.program_label, stretch=2)
        header_layout.addWidget(right_widget, stretch=1)
        main_layout.addWidget(self.header)
        self._init_header_timer()

        # 탭 위젯
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #333333;
                color: white;
                padding: 15px 40px;
                margin-right: 2px;
                font-size: 16px;
                font-weight: bold;
                border: none;
                min-width: 120px;
            }
            QTabBar::tab:selected {
                background-color: #4caf50;
                font-weight: bold;
            }
            QTabBar::tab:hover:!selected {
                background-color: #555555;
            }
        """)
        
        # 메인 탭
        self.main_tab = QWidget()
        self._init_main_tab()
        self.tab_widget.addTab(self.main_tab, "메인")
        
        # 설정 탭
        self.settings_tab = SettingsPage()
        self.tab_widget.addTab(self.settings_tab, "설정")
        
        # 데이터 검색 탭 (빈 위젯)
        self.data_search_tab = QWidget()
        data_search_layout = QVBoxLayout()
        data_search_label = QLabel("데이터 검색 기능")
        data_search_label.setAlignment(Qt.AlignCenter)
        data_search_label.setStyleSheet("font-size: 24px; color: #666666;")
        data_search_layout.addWidget(data_search_label)
        self.data_search_tab.setLayout(data_search_layout)
        self.tab_widget.addTab(self.data_search_tab, "데이터 검색")
        
        # 로그 탭 (빈 위젯)
        self.log_tab = QWidget()
        log_layout = QVBoxLayout()
        log_label = QLabel("로그 기능")
        log_label.setAlignment(Qt.AlignCenter)
        log_label.setStyleSheet("font-size: 24px; color: #666666;")
        log_layout.addWidget(log_label)
        self.log_tab.setLayout(log_layout)
        self.tab_widget.addTab(self.log_tab, "로그")
        
        # 기본 탭을 메인으로 설정
        self.tab_widget.setCurrentIndex(0)
        
        main_layout.addWidget(self.tab_widget, stretch=1)

        # StatusBar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("시스템이 준비되었습니다.")

    def _init_main_tab(self) -> None:
        """메인 탭의 기존 UI 구성"""
        main_layout = QHBoxLayout()
        self.main_tab.setLayout(main_layout)

        # BrowserArea (좌측 2/3)
        self.browser_area = BrowserWidget(url="http://127.0.0.1")
        main_layout.addWidget(self.browser_area, stretch=2)

        # ControlPanel (우측 1/3)
        self.control_panel = QWidget()
        control_layout = QVBoxLayout()
        self.control_panel.setLayout(control_layout)
        
        # 주소창
        address_label = QLabel("주소:")
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("In-Sight 장비 주소 입력")
        control_layout.addWidget(address_label)
        control_layout.addWidget(self.address_input)
        
        # 그리드
        grid_label = QLabel("검사 결과")
        self.device_table = QTableWidget(3, 4)  # 예시: 3행 4열
        self.device_table.setHorizontalHeaderLabels(["Cell", "항목", "결과", "판정"])
        control_layout.addWidget(grid_label)
        control_layout.addWidget(self.device_table)
        
        # 버튼
        button_layout = QHBoxLayout()
        self.connect_button = QPushButton("접속")
        self.refresh_button = QPushButton("새로고침")
        button_layout.addWidget(self.connect_button)
        button_layout.addWidget(self.refresh_button)
        control_layout.addLayout(button_layout)

        # 로그 창
        self.log_textedit = QTextEdit()
        self.log_textedit.setReadOnly(True)
        self.log_textedit.setFixedHeight(100)
        control_layout.addWidget(QLabel("로그"))
        control_layout.addWidget(self.log_textedit)

        control_layout.addStretch(1)
        main_layout.addWidget(self.control_panel, stretch=1)

        # 버튼 이벤트 연결
        self.connect_button.clicked.connect(self._on_connect_clicked)
        self.refresh_button.clicked.connect(self._on_refresh_clicked)

    def _init_header_timer(self) -> None:
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_datetime)
        self.timer.start(1000)
        self._update_datetime()

    def _update_datetime(self) -> None:
        now = QDateTime.currentDateTime()
        self.date_label.setText(now.toString("yyyy-MM-dd"))
        self.time_label.setText(now.toString("HH:mm:ss"))

    def _on_exit_clicked(self) -> None:
        """출구 버튼 클릭 시 애플리케이션 종료"""
        QApplication.quit()

    def append_log_message(self, message: str) -> None:
        """
        로그 창에 메시지 추가
        """
        self.log_textedit.append(message)

    def _on_connect_clicked(self) -> None:
        """
        주소창의 URL로 브라우저를 이동시키고 상태바에 결과 메시지 출력
        """
        url = self.address_input.text().strip()
        if not url:
            self.status_bar.showMessage("주소를 입력하세요.")
            self.append_log_message("[경고] 주소가 입력되지 않았습니다.")
            return
        # URL 자동 보정
        if not (url.startswith("http://") or url.startswith("https://")):
            url = "http://" + url
        try:
            self.browser_area.webview.setUrl(QUrl(url))
            self.status_bar.showMessage(f"{url} 로 접속 시도 중...")
            self.append_log_message(f"[접속] {url} 로 접속 시도 중...")
        except Exception as e:
            self.status_bar.showMessage(f"접속 실패: {e}")
            self.append_log_message(f"[에러] 접속 실패: {e}")

    def _on_refresh_clicked(self) -> None:
        """
        브라우저 페이지 새로고침 및 상태바/로그 메시지 출력
        """
        try:
            self.browser_area.webview.reload()
            self.status_bar.showMessage("페이지를 새로고침했습니다.")
            self.append_log_message("[새로고침] 페이지를 새로고침했습니다.")
        except Exception as e:
            self.status_bar.showMessage(f"새로고침 실패: {e}")
            self.append_log_message(f"[에러] 새로고침 실패: {e}") 