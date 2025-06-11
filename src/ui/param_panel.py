from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QFormLayout, QMessageBox, QHeaderView, QComboBox
)
from PyQt5.QtCore import QTimer, QDateTime
from utils.telnet_manager import TelnetManager
import json

class ParamPanel(QWidget):
    def __init__(self, telnet_manager: TelnetManager = None):
        super().__init__()
        self.telnet_manager = telnet_manager
        self.init_ui()
        self.init_default_params()
        self.setup_timer()

    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # 파라미터 목록 테이블
        main_layout.addWidget(QLabel("파라미터 목록"))
        self.table = QTableWidget(0, 4)  # 동적으로 행 추가
        self.table.setHorizontalHeaderLabels(["Cell", "항목", "결과", "판정"])
        
        # 테이블 열 너비 자동 조정
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        main_layout.addWidget(self.table)

        # 제어 버튼들
        btn_layout1 = QHBoxLayout()
        self.refresh_btn = QPushButton("새로고침")
        self.get_all_btn = QPushButton("전체 읽기")
        self.set_btn = QPushButton("값 설정")
        self.save_csv_btn = QPushButton("CSV 저장")
        btn_layout1.addWidget(self.refresh_btn)
        btn_layout1.addWidget(self.get_all_btn)
        btn_layout1.addWidget(self.set_btn)
        btn_layout1.addWidget(self.save_csv_btn)
        main_layout.addLayout(btn_layout1)

        btn_layout2 = QHBoxLayout()
        self.add_param_btn = QPushButton("파라미터 추가")
        self.remove_param_btn = QPushButton("파라미터 삭제")
        self.auto_update_btn = QPushButton("자동 업데이트 시작")
        btn_layout2.addWidget(self.add_param_btn)
        btn_layout2.addWidget(self.remove_param_btn)
        btn_layout2.addWidget(self.auto_update_btn)
        main_layout.addLayout(btn_layout2)

        # 파라미터 상세 입력
        main_layout.addWidget(QLabel("파라미터 상세 입력"))
        form = QFormLayout()
        self.cell_edit = QLineEdit()
        self.item_edit = QLineEdit()
        self.value_edit = QLineEdit()
        self.command_combo = QComboBox()
        self.command_combo.addItems(["GET", "SET", "사용자 정의"])
        
        form.addRow("Cell", self.cell_edit)
        form.addRow("항목", self.item_edit)
        form.addRow("값/명령", self.value_edit)
        form.addRow("명령 유형", self.command_combo)
        main_layout.addLayout(form)

        self.setLayout(main_layout)

        # 이벤트 연결
        self.refresh_btn.clicked.connect(self.refresh_table)
        self.get_all_btn.clicked.connect(self.get_all_parameters)
        self.set_btn.clicked.connect(self.set_parameter)
        self.save_csv_btn.clicked.connect(self.save_to_csv)
        self.add_param_btn.clicked.connect(self.add_parameter)
        self.remove_param_btn.clicked.connect(self.remove_parameter)
        self.auto_update_btn.clicked.connect(self.toggle_auto_update)
        self.table.cellClicked.connect(self.on_cell_clicked)

    def init_default_params(self):
        """기본 파라미터 항목들을 추가한다."""
        default_params = [
            {"cell": "Cell0", "item": "Vision Status", "command": "GET Vision.Status"},
            {"cell": "Cell1", "item": "Job Name", "command": "GET Job.Name"},
            {"cell": "Cell2", "item": "Part Present", "command": "GET Vision.PartPresent"},
            {"cell": "Cell3", "item": "Overall Result", "command": "GET Vision.Result"},
            {"cell": "Cell4", "item": "Execution Time", "command": "GET Vision.ExecutionTime"}
        ]
        
        for param in default_params:
            self.add_param_to_table(param["cell"], param["item"], "", "", param["command"])

    def setup_timer(self):
        """자동 업데이트를 위한 타이머 설정"""
        self.auto_timer = QTimer()
        self.auto_timer.timeout.connect(self.get_all_parameters)
        self.auto_updating = False

    def add_param_to_table(self, cell: str, item: str, result: str, judgement: str, command: str = ""):
        """테이블에 파라미터 행을 추가한다."""
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        self.table.setItem(row, 0, QTableWidgetItem(cell))
        self.table.setItem(row, 1, QTableWidgetItem(item))
        self.table.setItem(row, 2, QTableWidgetItem(result))
        self.table.setItem(row, 3, QTableWidgetItem(judgement))
        
        # 명령어를 item에 저장 (사용자에게는 보이지 않음)
        item_widget = self.table.item(row, 1)
        if item_widget:
            item_widget.setData(0x0100, command)  # UserRole에 명령어 저장

    def on_cell_clicked(self, row: int, col: int):
        """테이블 셀 클릭 시 상세 입력창에 정보를 로드한다."""
        if row < self.table.rowCount():
            cell_item = self.table.item(row, 0)
            item_item = self.table.item(row, 1)
            result_item = self.table.item(row, 2)
            
            if cell_item:
                self.cell_edit.setText(cell_item.text())
            if item_item:
                self.item_edit.setText(item_item.text())
                # 저장된 명령어 로드
                command = item_item.data(0x0100)
                if command:
                    self.value_edit.setText(command)
            if result_item:
                pass  # 결과는 읽기 전용

    def get_parameter(self, command: str) -> str:
        """단일 파라미터를 읽어온다."""
        if not self.telnet_manager or not self.telnet_manager.connected:
            return "[연결 안됨]"
        
        try:
            response = self.telnet_manager.send_command(command)
            if response and response.strip():
                # 응답에서 실제 값만 추출 (에러 처리)
                clean_response = response.replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ').strip()
                return clean_response
            return "[응답 없음]"
        except Exception as e:
            return f"[오류: {e}]"

    def set_parameter(self):
        """선택된 파라미터에 값을 설정한다."""
        if not self.telnet_manager or not self.telnet_manager.connected:
            QMessageBox.warning(self, "경고", "Telnet에 연결되어 있지 않습니다.")
            return
        
        command = self.value_edit.text().strip()
        if not command:
            QMessageBox.warning(self, "경고", "명령어를 입력해 주세요.")
            return
        
        try:
            response = self.get_parameter(command)
            QMessageBox.information(self, "결과", f"명령 실행 결과:\n{response}")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"명령 실행 중 오류 발생:\n{e}")

    def get_all_parameters(self):
        """모든 파라미터를 읽어서 테이블을 업데이트한다."""
        if not self.telnet_manager or not self.telnet_manager.connected:
            return
        
        for row in range(self.table.rowCount()):
            item_widget = self.table.item(row, 1)
            if item_widget:
                command = item_widget.data(0x0100)
                if command:
                    result = self.get_parameter(command)
                    
                    # 결과 업데이트
                    result_item = QTableWidgetItem(result)
                    self.table.setItem(row, 2, result_item)
                    
                    # 판정 로직 (예시)
                    judgement = "OK" if "[오류" not in result and "[연결" not in result else "NG"
                    judgement_item = QTableWidgetItem(judgement)
                    self.table.setItem(row, 3, judgement_item)

    def refresh_table(self):
        """테이블을 새로고침한다."""
        self.get_all_parameters()

    def add_parameter(self):
        """새 파라미터를 추가한다."""
        cell = self.cell_edit.text().strip()
        item = self.item_edit.text().strip()
        command = self.value_edit.text().strip()
        
        if not cell or not item:
            QMessageBox.warning(self, "경고", "Cell과 항목을 입력해 주세요.")
            return
        
        self.add_param_to_table(cell, item, "", "", command)
        
        # 입력창 초기화
        self.cell_edit.clear()
        self.item_edit.clear()
        self.value_edit.clear()

    def remove_parameter(self):
        """선택된 파라미터를 삭제한다."""
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)
        else:
            QMessageBox.warning(self, "경고", "삭제할 행을 선택해 주세요.")

    def toggle_auto_update(self):
        """자동 업데이트를 시작/중지한다."""
        if not self.auto_updating:
            self.auto_timer.start(2000)  # 2초마다 업데이트
            self.auto_updating = True
            self.auto_update_btn.setText("자동 업데이트 중지")
        else:
            self.auto_timer.stop()
            self.auto_updating = False
            self.auto_update_btn.setText("자동 업데이트 시작")

    def save_to_csv(self):
        """현재 파라미터 데이터를 CSV로 저장한다."""
        try:
            import csv
            from PyQt5.QtWidgets import QFileDialog
            
            filename, _ = QFileDialog.getSaveFileName(
                self, "CSV 저장", f"parameters_{QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')}.csv",
                "CSV files (*.csv)")
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    # 헤더 작성
                    writer.writerow(["Cell", "항목", "결과", "판정", "시간"])
                    
                    # 데이터 작성
                    current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
                    for row in range(self.table.rowCount()):
                        row_data = []
                        for col in range(4):
                            item = self.table.item(row, col)
                            row_data.append(item.text() if item else "")
                        row_data.append(current_time)
                        writer.writerow(row_data)
                
                QMessageBox.information(self, "저장 완료", f"CSV 파일이 저장되었습니다:\n{filename}")
        except Exception as e:
            QMessageBox.critical(self, "저장 오류", f"CSV 저장 중 오류 발생:\n{e}")

    def set_telnet_manager(self, telnet_manager: TelnetManager):
        """TelnetManager를 설정한다."""
        self.telnet_manager = telnet_manager 