"""
JOB 관리 그룹 프로토타입
- 기본 UI 레이아웃 확인
- 이벤트 처리 테스트
- 시뮬레이션된 Telnet 기능
"""

import sys
import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGroupBox, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLineEdit, QTextEdit, QLabel, QMessageBox, QWidget
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont


class MockTelnetManager:
    """모의 Telnet 매니저 (프로토타입용)"""
    
    def __init__(self):
        self.connected = False
        self.command_count = 0
    
    def is_connected(self):
        return self.connected
    
    def connect(self):
        self.connected = True
        return True
    
    def disconnect(self):
        self.connected = False
    
    def send_command(self, command: str) -> str:
        """명령 전송 시뮬레이션"""
        self.command_count += 1
        
        # 일반적인 In-Sight 명령에 대한 시뮬레이션 응답
        responses = {
            "SW8": "1",
            "GetImage": "1",
            "GetResults": "Cell[0].result=1 Cell[1].result=OK",
            "Online": "1", 
            "GET": "Cell[0].result=1",
            "Set": "1"
        }
        
        # 명령어에 따른 응답 또는 기본 응답
        if command.upper() in [k.upper() for k in responses.keys()]:
            for key, value in responses.items():
                if command.upper() == key.upper():
                    return f"0 {value}"  # In-Sight 성공 응답 형태
        
        # 기본 시뮬레이션 응답
        return f"0 Command_{self.command_count}_Response"


class JobPanelPrototype(QGroupBox):
    """
    JOB 관리 패널 프로토타입
    """
    
    # 시그널 정의
    command_executed = pyqtSignal(str, str)  # (command, result)
    error_occurred = pyqtSignal(str)         # error_message
    log_message = pyqtSignal(str)            # log_message
    
    def __init__(self, parent=None):
        super().__init__("JOB 관리", parent)
        
        # 모의 Telnet 매니저
        self.telnet_manager = MockTelnetManager()
        
        # UI 컨트롤 초기화
        self.btn_execute_1 = None
        self.btn_execute_2 = None
        self.line_command_1 = None
        self.line_command_2 = None
        
        self.setup_ui()
        self.connect_signals()
        
        # 프로토타입용 초기 연결 상태 설정
        self.telnet_manager.connect()
        self.update_button_states(True)
        
    def setup_ui(self):
        """UI 레이아웃 구성"""
        # 메인 레이아웃
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 15, 10, 10)
        
        # 첫 번째 행 (명령어 1)
        row1_layout = QHBoxLayout()
        self.btn_execute_1 = QPushButton("실행 1")
        self.btn_execute_1.setFixedSize(100, 30)
        self.btn_execute_1.setEnabled(False)  # 초기 비활성화
        self.btn_execute_1.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        
        self.line_command_1 = QLineEdit()
        self.line_command_1.setPlaceholderText("In-Sight Native Command 입력 (예: SW8)")
        self.line_command_1.setMaxLength(255)
        self.line_command_1.setFixedHeight(30)
        self.line_command_1.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 3px;
                padding: 5px;
                font-family: "Consolas", "Monaco", monospace;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        
        row1_layout.addWidget(self.btn_execute_1)
        row1_layout.addWidget(self.line_command_1)
        
        # 두 번째 행 (명령어 2)
        row2_layout = QHBoxLayout()
        self.btn_execute_2 = QPushButton("실행 2")
        self.btn_execute_2.setFixedSize(100, 30)
        self.btn_execute_2.setEnabled(False)  # 초기 비활성화
        self.btn_execute_2.setStyleSheet(self.btn_execute_1.styleSheet())
        
        self.line_command_2 = QLineEdit()
        self.line_command_2.setPlaceholderText("In-Sight Native Command 입력 (예: GetImage)")
        self.line_command_2.setMaxLength(255)
        self.line_command_2.setFixedHeight(30)
        self.line_command_2.setStyleSheet(self.line_command_1.styleSheet())
        
        row2_layout.addWidget(self.btn_execute_2)
        row2_layout.addWidget(self.line_command_2)
        
        # 메인 레이아웃에 추가
        main_layout.addLayout(row1_layout)
        main_layout.addLayout(row2_layout)
        
        # 최소 높이 설정
        self.setMinimumHeight(120)
        
        # 그룹박스 스타일
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin: 5px;
                padding-top: 10px;
                font-size: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }
        """)

    def connect_signals(self):
        """시그널-슬롯 연결"""
        # 버튼 클릭 시그널
        self.btn_execute_1.clicked.connect(self.execute_command_1)
        self.btn_execute_2.clicked.connect(self.execute_command_2)
        
        # Enter 키 시그널
        self.line_command_1.returnPressed.connect(
            lambda: self.on_line_edit_return_pressed(self.line_command_1, 1)
        )
        self.line_command_2.returnPressed.connect(
            lambda: self.on_line_edit_return_pressed(self.line_command_2, 2)
        )

    def execute_command_1(self):
        """명령어 1 실행"""
        command = self.line_command_1.text().strip()
        self.execute_command(command, 1)

    def execute_command_2(self):
        """명령어 2 실행"""
        command = self.line_command_2.text().strip()
        self.execute_command(command, 2)

    def execute_command(self, command: str, slot_number: int):
        """
        공통 명령 실행 메서드
        Args:
            command: 실행할 명령어
            slot_number: 슬롯 번호 (1 또는 2)
        """
        try:
            # 입력 유효성 검사
            if not command:
                self.show_error_message(f"슬롯 {slot_number}: 명령어를 입력해주세요.")
                return
                
            # Telnet 연결 확인
            if not self.telnet_manager or not self.telnet_manager.is_connected():
                self.show_error_message("Telnet이 연결되지 않았습니다.")
                return
            
            # 명령 전송 (시뮬레이션)
            self.log_command_execution(command, "", slot_number, "TX")
            result = self.telnet_manager.send_command(command)
            
            # 결과 처리
            if result:
                self.log_command_execution(command, result, slot_number, "RX")
                self.command_executed.emit(command, result)
                
                # 성공 메시지
                msg = f"슬롯 {slot_number} 실행 완료: {command} → {result}"
                self.log_message.emit(msg)
            else:
                error_msg = f"슬롯 {slot_number}: 명령 실행 실패"
                self.show_error_message(error_msg)
                self.error_occurred.emit(error_msg)
                
        except Exception as e:
            error_msg = f"슬롯 {slot_number} 오류: {str(e)}"
            self.show_error_message(error_msg)
            self.error_occurred.emit(error_msg)

    def update_button_states(self, telnet_connected: bool):
        """
        Telnet 연결 상태에 따른 버튼 활성화/비활성화
        Args:
            telnet_connected: Telnet 연결 상태
        """
        self.btn_execute_1.setEnabled(telnet_connected)
        self.btn_execute_2.setEnabled(telnet_connected)

    def on_line_edit_return_pressed(self, line_edit: QLineEdit, slot_number: int):
        """
        Enter 키 입력 처리
        Args:
            line_edit: 입력된 QLineEdit
            slot_number: 슬롯 번호
        """
        command = line_edit.text().strip()
        if command:  # 빈 명령어가 아닐 때만 실행
            self.execute_command(command, slot_number)

    def show_error_message(self, message: str):
        """
        오류 메시지 표시
        Args:
            message: 오류 메시지
        """
        error_msg = f"JOB 관리 오류: {message}"
        self.log_message.emit(error_msg)
        
        # 추가적으로 메시지박스도 표시 (프로토타입용)
        QMessageBox.warning(self, "JOB 관리 오류", message)

    def log_command_execution(self, command: str, result: str, slot_number: int, direction: str):
        """
        명령 실행 로그 기록
        Args:
            command: 실행된 명령어
            result: 실행 결과
            slot_number: 슬롯 번호
            direction: TX(전송) 또는 RX(수신)
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if direction == "TX":
            log_message = f"[{timestamp}] JOB 슬롯 {slot_number} TX: {command}"
        else:  # RX
            log_message = f"[{timestamp}] JOB 슬롯 {slot_number} RX: {result}"
        
        self.log_message.emit(log_message)


class JobPanelPrototypeWindow(QMainWindow):
    """프로토타입 테스트용 메인 윈도우"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JOB 관리 그룹 - 프로토타입")
        self.setGeometry(100, 100, 800, 600)
        
        self.setup_ui()
        
    def setup_ui(self):
        """UI 구성"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 제목
        title_label = QLabel("JOB 관리 그룹 프로토타입")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #1976d2;
                margin: 10px;
            }
        """)
        main_layout.addWidget(title_label)
        
        # JobPanel 프로토타입
        self.job_panel = JobPanelPrototype()
        main_layout.addWidget(self.job_panel)
        
        # 연결 상태 컨트롤
        connection_layout = QHBoxLayout()
        self.connection_label = QLabel("Telnet 연결 상태:")
        self.connection_status = QLabel("연결됨 (시뮬레이션)")
        self.connection_status.setStyleSheet("color: green; font-weight: bold;")
        
        self.toggle_connection_btn = QPushButton("연결 토글")
        self.toggle_connection_btn.clicked.connect(self.toggle_connection)
        
        connection_layout.addWidget(self.connection_label)
        connection_layout.addWidget(self.connection_status)
        connection_layout.addStretch()
        connection_layout.addWidget(self.toggle_connection_btn)
        
        main_layout.addLayout(connection_layout)
        
        # 로그 출력 영역
        log_label = QLabel("실행 로그:")
        log_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        main_layout.addWidget(log_label)
        
        self.log_output = QTextEdit()
        self.log_output.setFixedHeight(200)
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                font-family: "Consolas", "Monaco", monospace;
                font-size: 12px;
            }
        """)
        main_layout.addWidget(self.log_output)
        
        # 프로토타입 설명
        info_label = QLabel("""
프로토타입 사용법:
1. 텍스트 박스에 명령어 입력 (예: SW8, GetImage, GetResults)
2. "실행" 버튼 클릭 또는 Enter 키 입력
3. 아래 로그에서 실행 결과 확인
4. "연결 토글" 버튼으로 연결 상태 변경 테스트
        """)
        info_label.setStyleSheet("""
            QLabel {
                background-color: #e3f2fd;
                border: 1px solid #2196f3;
                border-radius: 5px;
                padding: 10px;
                font-size: 12px;
                margin-top: 10px;
            }
        """)
        main_layout.addWidget(info_label)
        
        # 시그널 연결
        self.job_panel.log_message.connect(self.add_log)
        self.job_panel.command_executed.connect(self.on_command_executed)
        self.job_panel.error_occurred.connect(self.on_error_occurred)
        
        # 초기 로그
        self.add_log("JOB 관리 프로토타입이 시작되었습니다.")
        self.add_log("Telnet 연결 상태: 시뮬레이션 모드")
        
    def toggle_connection(self):
        """연결 상태 토글"""
        if self.job_panel.telnet_manager.is_connected():
            self.job_panel.telnet_manager.disconnect()
            self.connection_status.setText("연결 해제됨")
            self.connection_status.setStyleSheet("color: red; font-weight: bold;")
            self.job_panel.update_button_states(False)
            self.add_log("Telnet 연결이 해제되었습니다.")
        else:
            self.job_panel.telnet_manager.connect()
            self.connection_status.setText("연결됨 (시뮬레이션)")
            self.connection_status.setStyleSheet("color: green; font-weight: bold;")
            self.job_panel.update_button_states(True)
            self.add_log("Telnet 연결이 설정되었습니다.")
    
    def add_log(self, message: str):
        """로그 메시지 추가"""
        self.log_output.append(message)
    
    def on_command_executed(self, command: str, result: str):
        """명령 실행 완료 시그널 처리"""
        self.add_log(f"✓ 명령 실행 성공: {command} → {result}")
    
    def on_error_occurred(self, error_message: str):
        """오류 발생 시그널 처리"""
        self.add_log(f"✗ 오류: {error_message}")


def main():
    """프로토타입 실행 함수"""
    app = QApplication(sys.argv)
    
    # 폰트 설정
    font = QFont("맑은 고딕", 9)
    app.setFont(font)
    
    window = JobPanelPrototypeWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main() 