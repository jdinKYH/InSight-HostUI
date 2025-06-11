from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QPushButton, QTextEdit
)
from PyQt5.QtCore import Qt, QDateTime, QThread, pyqtSignal
from utils.telnet_manager import TelnetManager
import threading
import time

class TelnetPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.telnet = TelnetManager()
        self._rx_thread = None
        self._rx_stop = threading.Event()
        main_layout = QVBoxLayout()
        
        # 연결 설정
        form = QFormLayout()
        self.address_edit = QLineEdit("192.168.0.111")
        self.port_edit = QLineEdit("23")
        self.mode_label = QLabel("Client")
        self.status_label = QLabel("연결 안됨")
        form.addRow("서버 주소", self.address_edit)
        form.addRow("포트", self.port_edit)
        form.addRow("모드", self.mode_label)
        form.addRow("상태", self.status_label)
        main_layout.addLayout(form)

        # 연결 버튼
        btn_layout = QHBoxLayout()
        self.connect_btn = QPushButton("연결")
        self.disconnect_btn = QPushButton("해제")
        self.test_btn = QPushButton("테스트")
        btn_layout.addWidget(self.connect_btn)
        btn_layout.addWidget(self.disconnect_btn)
        btn_layout.addWidget(self.test_btn)
        main_layout.addLayout(btn_layout)

        # 자동 로그인 섹션
        login_form = QFormLayout()
        self.username_edit = QLineEdit("admin")
        self.password_edit = QLineEdit("")
        self.password_edit.setEchoMode(QLineEdit.Password)
        login_form.addRow("사용자명", self.username_edit)
        login_form.addRow("패스워드", self.password_edit)
        main_layout.addLayout(login_form)
        
        self.login_btn = QPushButton("자동 로그인")
        main_layout.addWidget(self.login_btn)

        # 통신 데이터 입력
        main_layout.addWidget(QLabel("통신 데이터 입력"))
        self.data_edit = QTextEdit()
        main_layout.addWidget(self.data_edit)

        self.send_btn = QPushButton("전송")
        main_layout.addWidget(self.send_btn)

        # 통신 로그
        main_layout.addWidget(QLabel("통신 로그"))
        self.log_edit = QTextEdit()
        self.log_edit.setReadOnly(True)
        main_layout.addWidget(self.log_edit)

        self.setLayout(main_layout)

        # 이벤트 연결
        self.connect_btn.clicked.connect(self._on_connect)
        self.disconnect_btn.clicked.connect(self._on_disconnect)
        self.test_btn.clicked.connect(self._on_test)
        self.login_btn.clicked.connect(self._on_login)
        self.send_btn.clicked.connect(self._on_send)

    def _log(self, msg: str):
        self.log_edit.append(msg)

    def _now(self):
        return QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")

    def _on_connect(self):
        host = self.address_edit.text().strip()
        try:
            port = int(self.port_edit.text().strip())
        except Exception:
            self._log(f"[{self._now()}] [에러] 포트 번호가 올바르지 않습니다.")
            return
        self._log(f"[{self._now()}] 연결 시도: {host}:{port}")
        
        # 동기식 telnetlib으로 연결 및 초기 수신 (연결 상태 유지)
        msg = self.telnet.connect_and_receive_initial(host, port)
        if msg and 'Welcome to In-Sight' in msg:
            self.status_label.setText("연결됨")
            self._log(f"[{self._now()}] 연결 성공")
            # Welcome 메시지를 깔끔하게 표시
            clean_msg = msg.replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ').strip()
            self._log(f"[{self._now()}] {clean_msg}")
        else:
            self.status_label.setText("연결 안됨")
            self._log(f"[{self._now()}] [에러] 연결 실패 또는 수신 없음: {repr(msg)}")

    def _on_login(self):
        if not self.telnet.connected:
            self._log(f"[{self._now()}] [에러] 먼저 연결해 주세요.")
            return
        
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        
        self._log(f"[{self._now()}] 자동 로그인 시작: {username}")
        success = self.telnet.login(username, password)
        
        if success:
            self._log(f"[{self._now()}] 로그인 성공")
        else:
            self._log(f"[{self._now()}] [에러] 로그인 실패")

    def _on_disconnect(self):
        self.telnet.disconnect()
        self.status_label.setText("연결 안됨")
        self._log(f"[{self._now()}] 연결 해제")
        self._stop_rx_thread()

    def _on_test(self):
        if not self.telnet.connected:
            self._log(f"[{self._now()}] [에러] 연결되어 있지 않습니다.")
            return
        self._log(f"[{self._now()}] 테스트: GET 명령 전송")
        response = self.telnet.send_command("GET")
        if response and response.strip():
            clean_response = response.replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ').strip()
            self._log(f"[{self._now()}] 응답: {clean_response}")
        else:
            self._log(f"[{self._now()}] (응답 없음)")

    def _on_send(self):
        if not self.telnet.connected:
            self._log(f"[{self._now()}] [에러] 연결되어 있지 않습니다.")
            return
        data = self.data_edit.toPlainText().strip()
        
        if not data:
            self._log(f"[{self._now()}] [에러] 전송할 데이터를 입력해 주세요.")
            return
        
        self._log(f"[{self._now()}] 명령 전송: {data}")
        response = self.telnet.send_command(data)
        
        if response and response.strip():
            clean_response = response.replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ').strip()
            self._log(f"[{self._now()}] 응답: {clean_response}")
        else:
            self._log(f"[{self._now()}] (응답 없음)")

    def _start_rx_thread(self):
        # 현재는 사용하지 않음 (동기식 처리)
        pass

    def _stop_rx_thread(self):
        # 현재는 사용하지 않음 (동기식 처리)
        pass

    def _rx_loop(self):
        # 현재는 사용하지 않음 (동기식 처리)
        pass 