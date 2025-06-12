"""
JOB 관리 패널 모듈

Cognex In-Sight 비전 시스템의 JOB(내부 프로그램) 실행을 위한 
간단한 명령어 인터페이스를 제공합니다.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QGroupBox, QPushButton, QLineEdit, QLabel)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
import logging
from datetime import datetime
from typing import Optional


class JobPanel(QWidget):
    """
    JOB 관리 패널 클래스
    
    주요 기능:
    - 2개의 명령어 슬롯 제공
    - Telnet을 통한 명령어 전송
    - 실시간 로그 기록
    - 연결 상태 관리
    """
    
    # 로그 전송을 위한 시그널
    log_message = pyqtSignal(str)
    
    def __init__(self, telnet_manager=None, log_panel=None):
        super().__init__()
        self.telnet_manager = telnet_manager
        self.log_panel = log_panel
        
        # UI 설정
        self.setup_ui()
        
        # 로그 시그널 연결
        if self.log_panel:
            self.log_message.connect(self.log_panel.add_log)
    
    def setup_ui(self):
        """UI 컴포넌트를 초기화합니다."""
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        # JOB 관리 그룹박스
        job_group = QGroupBox("JOB Management")
        job_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 5px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f8f8, stop:1 #e8e8e8);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #2c3e50;
            }
        """)
        
        job_layout = QVBoxLayout()
        job_layout.setSpacing(8)
        
        # 첫 번째 명령어 슬롯
        slot1_layout = QHBoxLayout()
        slot1_layout.setSpacing(10)
        
        self.execute_button_1 = QPushButton("Execute")
        self.execute_button_1.setFixedSize(100, 30)
        self.execute_button_1.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a90e2, stop:1 #357abd);
                border: 1px solid #2c5aa0;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5ba0f2, stop:1 #4682cd);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #357abd, stop:1 #2c5aa0);
            }
            QPushButton:disabled {
                background: #cccccc;
                color: #888888;
                border: 1px solid #aaaaaa;
            }
        """)
        
        self.command_input_1 = QLineEdit()
        self.command_input_1.setFixedSize(340, 30)
        self.command_input_1.setPlaceholderText("Enter Native Mode Command (e.g., SW8)")
        self.command_input_1.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                padding: 0 8px;
                font-size: 11px;
                background: white;
            }
            QLineEdit:focus {
                border: 2px solid #4a90e2;
            }
        """)
        
        slot1_layout.addWidget(self.execute_button_1)
        slot1_layout.addWidget(self.command_input_1)
        slot1_layout.addStretch()
        
        # 두 번째 명령어 슬롯
        slot2_layout = QHBoxLayout()
        slot2_layout.setSpacing(10)
        
        self.execute_button_2 = QPushButton("Execute")
        self.execute_button_2.setFixedSize(100, 30)
        self.execute_button_2.setStyleSheet(self.execute_button_1.styleSheet())
        
        self.command_input_2 = QLineEdit()
        self.command_input_2.setFixedSize(340, 30)
        self.command_input_2.setPlaceholderText("Enter Native Mode Command (e.g., GetImage)")
        self.command_input_2.setStyleSheet(self.command_input_1.styleSheet())
        
        slot2_layout.addWidget(self.execute_button_2)
        slot2_layout.addWidget(self.command_input_2)
        slot2_layout.addStretch()
        
        # 상태 표시 레이블
        self.status_label = QLabel("연결 상태를 확인하세요")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 10px;
                font-style: italic;
                padding: 2px;
            }
        """)
        
        # 레이아웃에 추가
        job_layout.addLayout(slot1_layout)
        job_layout.addLayout(slot2_layout)
        job_layout.addWidget(self.status_label)
        
        job_group.setLayout(job_layout)
        layout.addWidget(job_group)
        
        self.setLayout(layout)
        
        # 이벤트 연결
        self.execute_button_1.clicked.connect(lambda: self.execute_command(1))
        self.execute_button_2.clicked.connect(lambda: self.execute_command(2))
        
        # Enter 키 이벤트 연결
        self.command_input_1.returnPressed.connect(lambda: self.execute_command(1))
        self.command_input_2.returnPressed.connect(lambda: self.execute_command(2))
        
        # 초기 상태 업데이트 (UI 컴포넌트 초기화 완료 후)
        # QTimer를 사용하여 다음 이벤트 루프에서 실행
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(0, self.update_ui_state)
    
    def set_telnet_manager(self, telnet_manager):
        """TelnetManager 인스턴스를 설정합니다."""
        self.telnet_manager = telnet_manager
        self.update_ui_state()
    
    def set_log_panel(self, log_panel):
        """LogPanel 인스턴스를 설정하고 시그널을 연결합니다."""
        self.log_panel = log_panel
        if self.log_panel:
            self.log_message.connect(self.log_panel.add_log)
    
    def update_ui_state(self):
        """Telnet 연결 상태에 따라 UI 상태를 업데이트합니다."""
        try:
            is_connected = self.telnet_manager and getattr(self.telnet_manager, 'connected', False)
            
            # 버튼 활성화/비활성화 (안전한 체크)
            if hasattr(self, 'execute_button_1') and self.execute_button_1 is not None:
                self.execute_button_1.setEnabled(bool(is_connected))
            if hasattr(self, 'execute_button_2') and self.execute_button_2 is not None:
                self.execute_button_2.setEnabled(bool(is_connected))
        
            # 상태 레이블 업데이트
            if hasattr(self, 'status_label') and self.status_label is not None:
                if is_connected:
                    host = getattr(self.telnet_manager, 'host', 'Unknown')
                    port = getattr(self.telnet_manager, 'port', 23)
                    self.status_label.setText(f"연결됨: {host}:{port}")
                    self.status_label.setStyleSheet("""
                        QLabel {
                            color: #27ae60;
                            font-size: 10px;
                            font-weight: bold;
                            padding: 2px;
                        }
                    """)
                else:
                    self.status_label.setText("Telnet 연결이 필요합니다")
                    self.status_label.setStyleSheet("""
                        QLabel {
                            color: #e74c3c;
                            font-size: 10px;
                            font-weight: bold;
                            padding: 2px;
                        }
                    """)
        except Exception as e:
            # UI 업데이트 중 오류 발생 시 로그만 기록하고 계속 진행
            logging.error(f"JobPanel update_ui_state error: {e}")
    
    def execute_command(self, slot_number: int):
        """
        지정된 슬롯의 명령어를 실행합니다.
        
        Args:
            slot_number (int): 실행할 슬롯 번호 (1 또는 2)
        """
        # 입력 검증
        if slot_number == 1:
            command = self.command_input_1.text().strip()
            input_widget = self.command_input_1
        elif slot_number == 2:
            command = self.command_input_2.text().strip()
            input_widget = self.command_input_2
        else:
            self.add_log("[오류] 유효하지 않은 슬롯 번호")
            return
        
        if not command:
            self.add_log(f"[슬롯 {slot_number}] 명령어를 입력하세요")
            input_widget.setFocus()
            return
        
        # 연결 상태 확인
        if not self.telnet_manager or not self.telnet_manager.connected:
            self.add_log("[오류] Telnet 연결이 필요합니다")
            self.update_ui_state()
            return
        
        try:
            # 명령어 전송 로그
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            self.add_log(f"[{timestamp}] TX(슬롯{slot_number}): {command}")
            
            # 명령어 실행
            response = self.telnet_manager.send_command(command, wait_time=0.5)
            
            # 응답 로그
            if response:
                clean_response = response.strip()
                if clean_response:
                    self.add_log(f"[{timestamp}] RX(슬롯{slot_number}): {clean_response}")
                else:
                    self.add_log(f"[{timestamp}] RX(슬롯{slot_number}): [응답 없음]")
            else:
                self.add_log(f"[{timestamp}] RX(슬롯{slot_number}): [응답 없음]")
            
            # 성공 시 입력 필드 포커스
            input_widget.selectAll()
            input_widget.setFocus()
            
        except Exception as e:
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            error_msg = f"[{timestamp}] [오류] 명령어 실행 실패: {str(e)}"
            self.add_log(error_msg)
            logging.error(f"JobPanel execute_command error: {e}")
    
    def add_log(self, message: str):
        """
        로그 메시지를 추가합니다.
        
        Args:
            message (str): 로그 메시지
        """
        try:
            # LogPanel이 연결된 경우 시그널로 전송
            if self.log_panel:
                self.log_message.emit(message)
            
            # 추가로 표준 로깅에도 기록
            logging.info(f"JobPanel: {message}")
            
        except Exception as e:
            logging.error(f"JobPanel add_log error: {e}")
    
    def clear_commands(self):
        """모든 명령어 입력 필드를 지웁니다."""
        self.command_input_1.clear()
        self.command_input_2.clear()
    
    def get_command_history(self) -> dict:
        """현재 입력된 명령어들을 반환합니다."""
        return {
            'slot1': self.command_input_1.text().strip(),
            'slot2': self.command_input_2.text().strip()
        }
    
    def set_commands(self, slot1_command: str = "", slot2_command: str = ""):
        """명령어 입력 필드에 값을 설정합니다."""
        if slot1_command:
            self.command_input_1.setText(slot1_command)
        if slot2_command:
            self.command_input_2.setText(slot2_command) 