"""
JOB 관리 패널 모듈

Cognex In-Sight 비전 시스템의 JOB(내부 프로그램) 실행을 위한 
간단한 명령어 인터페이스를 제공합니다.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QGroupBox, QPushButton, QLineEdit, QLabel,
                           QDialog, QListWidget, QListWidgetItem, 
                           QDialogButtonBox, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont
import logging
from datetime import datetime
from typing import Optional, List


class FileSelectionDialog(QDialog):
    """파일 선택 다이얼로그"""
    
    def __init__(self, file_list: List[str], parent=None):
        super().__init__(parent)
        self.selected_file = None
        self.setup_ui(file_list)
    
    def setup_ui(self, file_list: List[str]):
        """UI 설정"""
        self.setWindowTitle("JOB 파일 선택")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        # 안내 레이블
        info_label = QLabel("JOB 파일을 선택하세요:")
        info_label.setStyleSheet("font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(info_label)
        
        # 파일 리스트
        self.file_list_widget = QListWidget()
        self.file_list_widget.setStyleSheet("""
            QListWidget {
                border: 1px solid #cccccc;
                border-radius: 4px;
                background: white;
                selection-background-color: #4a90e2;
                selection-color: white;
                font-size: 12px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eeeeee;
                color: #2c3e50;
                font-weight: normal;
            }
            QListWidget::item:hover {
                background-color: #f0f8ff;
                font-weight: bold;
            }
            QListWidget::item:selected {
                background-color: #4a90e2;
                color: white;
                font-weight: bold;
                border: 2px solid #357abd;
            }
            QListWidget::item:selected:hover {
                background-color: #357abd;
                color: white;
                font-weight: bold;
            }
        """)
        
        for file_name in file_list:
            item = QListWidgetItem(file_name)
            item.setFont(QFont("Arial", 10, QFont.Normal))
            self.file_list_widget.addItem(item)
        
        layout.addWidget(self.file_list_widget)
        
        # 버튼
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept_selection)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
        
        # 더블클릭으로 선택
        self.file_list_widget.itemDoubleClicked.connect(self.accept_selection)
        
        # 선택 변경 시 폰트 업데이트
        self.file_list_widget.itemSelectionChanged.connect(self.update_selection_font)
    
    def accept_selection(self):
        """선택 확인"""
        current_item = self.file_list_widget.currentItem()
        if current_item:
            self.selected_file = current_item.text()
            self.accept()
        else:
            QMessageBox.warning(self, "선택 오류", "파일을 선택해주세요.")
    
    def update_selection_font(self):
        """선택된 항목의 폰트를 굵게 업데이트"""
        for i in range(self.file_list_widget.count()):
            item = self.file_list_widget.item(i)
            if item.isSelected():
                # 선택된 항목은 굵은 글씨
                font = QFont("Arial", 10, QFont.Bold)
                item.setFont(font)
            else:
                # 선택되지 않은 항목은 일반 글씨
                font = QFont("Arial", 10, QFont.Normal)
                item.setFont(font)


class JobPanel(QWidget):
    """
    JOB 관리 패널 클래스
    
    주요 기능:
    - JOB 파일 지정 (첫 번째 슬롯)
    - 명령어 실행 (두 번째 슬롯)
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
        self.selected_job_file = None  # 선택된 JOB 파일명
        self.current_job_file = None   # 현재 적용 중인 JOB 파일명
        
        # 타이머 설정 (5초 버튼 비활성화용)
        self.job_file_timer = QTimer()
        self.job_file_timer.timeout.connect(self.enable_job_file_button)
        self.job_file_timer.setSingleShot(True)
        
        self.current_job_timer = QTimer()
        self.current_job_timer.timeout.connect(self.enable_current_job_button)
        self.current_job_timer.setSingleShot(True)
        
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
        
        # 첫 번째 슬롯 - JOB 파일 지정
        slot1_layout = QHBoxLayout()
        slot1_layout.setSpacing(10)
        
        self.job_file_button = QPushButton("JOB 파일 지정")
        self.job_file_button.setFixedSize(120, 30)
        self.job_file_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #27ae60, stop:1 #219a52);
                border: 1px solid #1e8449;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2ecc71, stop:1 #27ae60);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #219a52, stop:1 #1e8449);
            }
            QPushButton:disabled {
                background: #cccccc;
                color: #888888;
                border: 1px solid #aaaaaa;
            }
        """)
        
        self.job_file_display = QLineEdit()
        self.job_file_display.setFixedSize(320, 30)
        self.job_file_display.setPlaceholderText("선택된 JOB 파일이 여기에 표시됩니다")
        self.job_file_display.setReadOnly(True)
        self.job_file_display.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                padding: 0 8px;
                font-size: 11px;
                background: #f8f9fa;
                color: #2c3e50;
            }
        """)
        
        slot1_layout.addWidget(self.job_file_button)
        slot1_layout.addWidget(self.job_file_display)
        slot1_layout.addStretch()
        
        # 두 번째 슬롯 - 명령어 실행
        slot2_layout = QHBoxLayout()
        slot2_layout.setSpacing(10)
        
        self.execute_button_2 = QPushButton("적용 JOB 파일")
        self.execute_button_2.setFixedSize(120, 30)
        self.execute_button_2.setStyleSheet("""
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
        
        self.current_job_display = QLineEdit()
        self.current_job_display.setFixedSize(320, 30)
        self.current_job_display.setPlaceholderText("현재 적용 중인 JOB 파일이 여기에 표시됩니다")
        self.current_job_display.setReadOnly(True)
        self.current_job_display.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                padding: 0 8px;
                font-size: 11px;
                background: #f8f9fa;
                color: #2c3e50;
            }
        """)
        
        slot2_layout.addWidget(self.execute_button_2)
        slot2_layout.addWidget(self.current_job_display)
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
        self.job_file_button.clicked.connect(self.select_job_file)
        self.execute_button_2.clicked.connect(self.get_current_job_file)
        
        # 초기 상태 업데이트
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(0, self.update_ui_state)
        
        # 초기 현재 JOB 파일 조회
        QTimer.singleShot(100, self.get_current_job_file)
    
    def select_job_file(self):
        """JOB 파일 선택 기능"""
        # 연결 상태 확인
        if not self.telnet_manager or not self.telnet_manager.connected:
            self.add_log("[오류] Telnet 연결이 필요합니다")
            QMessageBox.warning(self, "연결 오류", "Telnet 연결이 필요합니다.")
            return
        
        # 버튼 비활성화 (JOB 파일 지정 버튼과 적용 JOB 파일 버튼 모두)
        self.disable_buttons_for_5_seconds()
        
        try:
            # 파일 목록 요청
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            self.add_log(f"[{timestamp}] TX: Get FileList")
            
            response = self.telnet_manager.send_command("Get FileList", wait_time=1.0)
            
            if not response:
                self.add_log(f"[{timestamp}] RX: [응답 없음]")
                QMessageBox.warning(self, "통신 오류", "파일 목록을 가져올 수 없습니다.")
                return
            
            # 응답 파싱
            response_clean = response.replace('\r', '').strip()
            lines = [line.strip() for line in response_clean.split('\n') if line.strip()]
            self.add_log(f"[{timestamp}] RX: {response.strip()}")
            self.add_log(f"[디버그] 파싱된 라인 수: {len(lines)}")
            
            if not lines:
                QMessageBox.warning(self, "응답 오류", "잘못된 응답 형식입니다.")
                return
            
            # 첫 번째 줄: 성공/실패 여부
            try:
                result_code = int(lines[0].strip())
                if result_code != 1:
                    self.add_log(f"[오류] 파일 목록 가져오기 실패: 코드 {result_code}")
                    QMessageBox.warning(self, "실행 오류", f"파일 목록 가져오기에 실패했습니다. (코드: {result_code})")
                    return
            except (ValueError, IndexError):
                QMessageBox.warning(self, "응답 오류", "응답 형식이 올바르지 않습니다.")
                return
            
            # 두 번째 줄: 파일 개수
            try:
                if len(lines) < 2:
                    QMessageBox.warning(self, "응답 오류", "파일 개수 정보가 없습니다.")
                    return
                file_count = int(lines[1].strip())
            except ValueError:
                QMessageBox.warning(self, "응답 오류", "파일 개수를 읽을 수 없습니다.")
                return
            
            # 파일 목록 추출 (.job, .jobx 파일만)
            job_files = []
            self.add_log(f"[디버그] 파일 개수: {file_count}, 전체 라인 수: {len(lines)}")
            
            for i in range(2, min(len(lines), 2 + file_count)):
                filename = lines[i].strip()
                self.add_log(f"[디버그] 파일 {i-1}: '{filename}' (길이: {len(filename)})")
                
                if filename.lower().endswith('.job') or filename.lower().endswith('.jobx'):
                    job_files.append(filename)
                    self.add_log(f"[디버그] JOB 파일 추가: '{filename}'")
                else:
                    self.add_log(f"[디버그] JOB 파일 아님: '{filename}' (확장자: '{filename.lower()[-4:] if len(filename) >= 4 else 'N/A'}')")
            
            self.add_log(f"[디버그] 최종 JOB 파일 목록: {job_files}")
            
            if not job_files:
                QMessageBox.information(self, "파일 없음", "JOB 파일(.job, .jobx)이 없습니다.")
                return
            
            # 파일 선택 다이얼로그 표시
            dialog = FileSelectionDialog(job_files, self)
            if dialog.exec_() == QDialog.Accepted and dialog.selected_file:
                self.load_job_file(dialog.selected_file)
                
        except Exception as e:
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            error_msg = f"[{timestamp}] [오류] 파일 목록 가져오기 실패: {str(e)}"
            self.add_log(error_msg)
            QMessageBox.critical(self, "오류", f"파일 목록 가져오기 중 오류가 발생했습니다:\n{str(e)}")
            logging.error(f"JobPanel select_job_file error: {e}")
    
    def load_job_file(self, filename: str):
        """선택된 JOB 파일 로드"""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            command = f"LF{filename}"
            self.add_log(f"[{timestamp}] TX: {command}")
            
            response = self.telnet_manager.send_command(command, wait_time=1.0)
            
            if not response:
                self.add_log(f"[{timestamp}] RX: [응답 없음]")
                QMessageBox.warning(self, "통신 오류", "파일 로드 응답을 받을 수 없습니다.")
                return
            
            # 응답 파싱
            self.add_log(f"[{timestamp}] RX: {response.strip()}")
            
            try:
                result_code = int(response.strip().split('\n')[0])
                if result_code == 1:
                    # 성공
                    self.selected_job_file = filename
                    self.job_file_display.setText(filename)
                    
                    # 파일 지정 성공 시 자동으로 적용 JOB 파일 텍스트박스 업데이트
                    self.current_job_file = filename
                    self.current_job_display.setText(filename)
                    
                    self.add_log(f"[성공] JOB 파일 로드 완료: {filename}")
                    QMessageBox.information(self, "성공", f"JOB 파일이 성공적으로 로드되었습니다:\n{filename}")
                else:
                    # 실패
                    self.add_log(f"[오류] JOB 파일 로드 실패: 코드 {result_code}")
                    QMessageBox.warning(self, "로드 실패", f"JOB 파일 로드에 실패했습니다. (코드: {result_code})")
            except (ValueError, IndexError):
                QMessageBox.warning(self, "응답 오류", "파일 로드 응답 형식이 올바르지 않습니다.")
                
        except Exception as e:
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            error_msg = f"[{timestamp}] [오류] JOB 파일 로드 실패: {str(e)}"
            self.add_log(error_msg)
            QMessageBox.critical(self, "오류", f"JOB 파일 로드 중 오류가 발생했습니다:\n{str(e)}")
            logging.error(f"JobPanel load_job_file error: {e}")

    def disable_buttons_for_5_seconds(self):
        """JOB 파일 지정 버튼과 적용 JOB 파일 버튼을 5초간 비활성화"""
        # 버튼 비활성화
        self.job_file_button.setEnabled(False)
        self.execute_button_2.setEnabled(False)
        
        # 5초 후 활성화 타이머 시작
        self.job_file_timer.start(5000)  # 5초
        self.current_job_timer.start(5000)  # 5초
        
        self.add_log("[정보] 버튼이 5초간 비활성화됩니다")
    
    def enable_job_file_button(self):
        """JOB 파일 지정 버튼 활성화"""
        if self.telnet_manager and self.telnet_manager.connected:
            self.job_file_button.setEnabled(True)
            self.add_log("[정보] JOB 파일 지정 버튼이 활성화되었습니다")
    
    def enable_current_job_button(self):
        """적용 JOB 파일 버튼 활성화"""
        if self.telnet_manager and self.telnet_manager.connected:
            self.execute_button_2.setEnabled(True)
            self.add_log("[정보] 적용 JOB 파일 버튼이 활성화되었습니다")

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
            
            # 버튼 활성화/비활성화 (타이머가 실행 중이 아닐 때만)
            if hasattr(self, 'job_file_button') and self.job_file_button is not None:
                if not self.job_file_timer.isActive():
                    self.job_file_button.setEnabled(bool(is_connected))
            if hasattr(self, 'execute_button_2') and self.execute_button_2 is not None:
                if not self.current_job_timer.isActive():
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
            logging.error(f"JobPanel update_ui_state error: {e}")
    
    def get_current_job_file(self):
        """현재 적용 중인 JOB 파일을 조회합니다."""
        # 연결 상태 확인
        if not self.telnet_manager or not self.telnet_manager.connected:
            self.add_log("[오류] Telnet 연결이 필요합니다")
            return
        
        try:
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            self.add_log(f"[{timestamp}] TX: GF")
            
            response = self.telnet_manager.send_command("GF", wait_time=1.0)
            
            if not response:
                self.add_log(f"[{timestamp}] RX: [응답 없음]")
                return
            
            # 응답 파싱
            lines = response.strip().split('\n')
            self.add_log(f"[{timestamp}] RX: {response.strip()}")
            
            if not lines:
                self.add_log("[오류] 잘못된 응답 형식입니다")
                return
            
            # 첫 번째 줄: 성공/실패 여부
            try:
                result_code = int(lines[0].strip())
                if result_code != 1:
                    self.add_log(f"[오류] 현재 JOB 파일 조회 실패: 코드 {result_code}")
                    self.current_job_display.setText("조회 실패")
                    return
            except (ValueError, IndexError):
                self.add_log("[오류] 응답 형식이 올바르지 않습니다")
                return
            
            # 두 번째 줄: 파일명
            if len(lines) >= 2:
                current_filename = lines[1].strip()
                self.current_job_file = current_filename
                self.current_job_display.setText(current_filename)
                self.add_log(f"[정보] 현재 적용 중인 JOB 파일: {current_filename}")
            else:
                self.add_log("[오류] 파일명 정보가 없습니다")
                self.current_job_display.setText("파일명 없음")
                
        except Exception as e:
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            error_msg = f"[{timestamp}] [오류] 현재 JOB 파일 조회 실패: {str(e)}"
            self.add_log(error_msg)
            logging.error(f"JobPanel get_current_job_file error: {e}")
            self.current_job_display.setText("조회 오류")

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
    
    def get_command_history(self) -> dict:
        """현재 상태 정보를 반환합니다."""
        return {
            'selected_job_file': self.selected_job_file,
            'current_job_file': self.current_job_file
        }
    
    def set_commands(self, job_file: str = "", current_file: str = ""):
        """파일 정보를 설정합니다."""
        if job_file:
            self.selected_job_file = job_file
            self.job_file_display.setText(job_file)
        if current_file:
            self.current_job_file = current_file
            self.current_job_display.setText(current_file)
    
    def get_selected_job_file(self) -> Optional[str]:
        """선택된 JOB 파일명을 반환합니다."""
        return self.selected_job_file
    
    def get_current_job_file_name(self) -> Optional[str]:
        """현재 적용 중인 JOB 파일명을 반환합니다."""
        return self.current_job_file 