from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QFormLayout, QMessageBox, QHeaderView, QComboBox
)
from PyQt5.QtCore import QTimer, QDateTime, Qt
from utils.telnet_manager import TelnetManager
import json

class ParamPanel(QWidget):
    def __init__(self, telnet_manager: TelnetManager = None):
        super().__init__()
        self.telnet_manager = telnet_manager
        self.init_ui()
        self.init_default_params()

    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # 파라미터 목록 테이블
        main_layout.addWidget(QLabel("파라미터 목록"))
        self.table = QTableWidget(0, 4)  # 4열로 변경 (No 열 다시 추가)
        self.table.setHorizontalHeaderLabels(["No", "Cell", "항목", "값"])
        
        # 테이블 열 너비 설정 - 지정된 열은 두 배로 넓히기
        header = self.table.horizontalHeader()
        
        # 기본 크기 설정
        self.table.setColumnWidth(0, 80)   # No 열 - 두 배 넓히기 (기본 40 -> 80)
        self.table.setColumnWidth(1, 160)  # Cell 열 - 두 배 넓히기 (기본 80 -> 160)
        self.table.setColumnWidth(3, 200)  # 값 열 - 두 배 넓히기 (기본 100 -> 200)
        
        # 항목 열은 나머지 공간 사용
        header.setSectionResizeMode(0, QHeaderView.Fixed)        # No 열 - 고정 크기
        header.setSectionResizeMode(1, QHeaderView.Fixed)        # Cell 열 - 고정 크기  
        header.setSectionResizeMode(2, QHeaderView.Stretch)      # 항목 열 - 확장
        header.setSectionResizeMode(3, QHeaderView.Fixed)        # 값 열 - 고정 크기
        
        main_layout.addWidget(self.table)

        # 제어 버튼들 (첫 번째 행 삭제)
        btn_layout = QHBoxLayout()
        self.add_param_btn = QPushButton("파라메터 추가")
        self.remove_param_btn = QPushButton("파라메터 삭제")
        self.save_csv_btn = QPushButton("CSV 저장")
        self.load_csv_btn = QPushButton("CSV 불러오기")
        self.send_params_btn = QPushButton("파라메터 전송")
        btn_layout.addWidget(self.add_param_btn)
        btn_layout.addWidget(self.remove_param_btn)
        btn_layout.addWidget(self.save_csv_btn)
        btn_layout.addWidget(self.load_csv_btn)
        btn_layout.addWidget(self.send_params_btn)
        main_layout.addLayout(btn_layout)

        # 파라미터 상세 입력
        main_layout.addWidget(QLabel("파라미터 상세 입력"))
        form = QFormLayout()
        self.cell_edit = QLineEdit()
        self.item_edit = QLineEdit()
        self.value_edit = QLineEdit()
        self.command_combo = QComboBox()
        self.command_combo.addItems(["SI (Set Integer)", "SF (Set Float)", "SS (Set String)"])
        
        form.addRow("Cell", self.cell_edit)
        form.addRow("항목", self.item_edit)
        form.addRow("값/명령", self.value_edit)
        form.addRow("명령 유형", self.command_combo)
        main_layout.addLayout(form)

        self.setLayout(main_layout)

        # 이벤트 연결 (삭제된 버튼들의 이벤트 제거)
        self.save_csv_btn.clicked.connect(self.save_to_csv)
        self.load_csv_btn.clicked.connect(self.load_from_csv)
        self.send_params_btn.clicked.connect(self.send_parameters)
        self.add_param_btn.clicked.connect(self.add_parameter)
        self.remove_param_btn.clicked.connect(self.remove_parameter)
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
        
        for i, param in enumerate(default_params, 1):
            self.add_param_to_table(i, param["cell"], param["item"], "", param["command"])

    def add_param_to_table(self, no: int, cell: str, item: str, value: str, command: str = ""):
        """테이블에 파라미터 행을 추가한다."""
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        # 4열 구조로 복원: No(0), Cell(1), 항목(2), 값(3)
        no_item = QTableWidgetItem(str(no))
        no_item.setTextAlignment(Qt.AlignCenter)  # No 열 중간 맞춤
        self.table.setItem(row, 0, no_item)
        
        cell_item = QTableWidgetItem(cell)
        cell_item.setTextAlignment(Qt.AlignCenter)  # Cell 열 중간 맞춤
        self.table.setItem(row, 1, cell_item)
        
        item_item = QTableWidgetItem(item)
        item_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 항목 열 왼쪽 맞춤
        self.table.setItem(row, 2, item_item)
        
        value_item = QTableWidgetItem(value)
        value_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)  # 값 열 오른쪽 맞춤
        self.table.setItem(row, 3, value_item)
        
        # 명령어를 항목 열에 저장 (사용자에게는 보이지 않음)
        if item_item:
            item_item.setData(0x0100, command)  # UserRole에 명령어 저장

    def on_cell_clicked(self, row: int, col: int):
        """테이블 셀 클릭 시 상세 입력창에 정보를 로드한다."""
        if row < self.table.rowCount():
            cell_item = self.table.item(row, 1)  # Cell 열
            item_item = self.table.item(row, 2)  # 항목 열
            value_item = self.table.item(row, 3) # 값 열
            
            if cell_item:
                self.cell_edit.setText(cell_item.text())
            if item_item:
                self.item_edit.setText(item_item.text())
                # 저장된 명령어 로드
                command = item_item.data(0x0100)
                if command:
                    self.value_edit.setText(command)
            if value_item:
                pass  # 값은 읽기 전용

    def add_parameter(self):
        """새 파라미터를 추가한다."""
        cell = self.cell_edit.text().strip()
        item = self.item_edit.text().strip()
        value = self.value_edit.text().strip()  # 값/명령 필드의 값을 가져옴
        
        if not cell or not item:
            QMessageBox.warning(self, "경고", "Cell과 항목을 입력해 주세요.")
            return
        
        # No는 현재 행 개수 + 1로 자동 설정
        no = self.table.rowCount() + 1
        self.add_param_to_table(no, cell, item, value, value)
        
        # 입력창 초기화
        self.cell_edit.clear()
        self.item_edit.clear()
        self.value_edit.clear()

    def remove_parameter(self):
        """선택된 파라미터를 삭제한다."""
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)
            # No 열 재정렬
            self.renumber_rows()
        else:
            QMessageBox.warning(self, "경고", "삭제할 행을 선택해 주세요.")

    def renumber_rows(self):
        """행 삭제 후 No 열을 다시 번호매김한다."""
        for row in range(self.table.rowCount()):
            no_item = QTableWidgetItem(str(row + 1))
            no_item.setTextAlignment(Qt.AlignCenter)  # No 열 중간 맞춤
            self.table.setItem(row, 0, no_item)

    def save_to_csv(self):
        """현재 파라미터 데이터를 CSV로 저장한다."""
        try:
            import csv
            from PyQt5.QtWidgets import QFileDialog
            
            filename, _ = QFileDialog.getSaveFileName(
                self, "CSV 저장", f"parameters_{QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')}.csv",
                "CSV files (*.csv)")
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                    writer = csv.writer(csvfile)
                    # 헤더 작성 (No, Cell, 항목, 값만)
                    writer.writerow(["No", "Cell", "항목", "값"])
                    
                    # 데이터 작성 (4개 열만)
                    for row in range(self.table.rowCount()):
                        row_data = []
                        for col in range(4):  # No, Cell, 항목, 값 (4열만)
                            item = self.table.item(row, col)
                            row_data.append(item.text() if item else "")
                        writer.writerow(row_data)
                
                QMessageBox.information(self, "저장 완료", f"CSV 파일이 저장되었습니다:\n{filename}")
        except Exception as e:
            QMessageBox.critical(self, "저장 오류", f"CSV 저장 중 오류 발생:\n{e}")

    def load_from_csv(self):
        """CSV 파일에서 파라미터 데이터를 불러온다."""
        try:
            import csv
            from PyQt5.QtWidgets import QFileDialog
            
            filename, _ = QFileDialog.getOpenFileName(
                self, "CSV 불러오기", "", "CSV files (*.csv)")
            
            if filename:
                # 기존 테이블 내용 삭제
                self.table.setRowCount(0)
                
                with open(filename, 'r', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    header = next(reader, None)  # 헤더 행 건너뛰기
                    
                    for row_idx, row_data in enumerate(reader, 1):
                        if len(row_data) >= 4:  # 최소 4개 열이 있어야 함
                            no = row_idx
                            cell = row_data[1] if len(row_data) > 1 else f"Cell{row_idx-1}"
                            item = row_data[2] if len(row_data) > 2 else f"Item{row_idx-1}"
                            value = row_data[3] if len(row_data) > 3 else ""
                            
                            # 명령어는 기본값으로 설정 (CSV에서 복원하기 어려우므로)
                            command = f"GET {item}"
                            
                            self.add_param_to_table(no, cell, item, value, command)
                
                QMessageBox.information(self, "불러오기 완료", f"CSV 파일이 불러와졌습니다:\n{filename}")
        except Exception as e:
            QMessageBox.critical(self, "불러오기 오류", f"CSV 불러오기 중 오류 발생:\n{e}")

    def send_parameters(self):
        """파라미터 목록을 Telnet으로 전송한다."""
        if not self.telnet_manager or not self.telnet_manager.connected:
            QMessageBox.warning(self, "경고", "Telnet에 연결되어 있지 않습니다.")
            return
        
        try:
            sent_count = 0
            error_count = 0
            
            for row in range(self.table.rowCount()):
                cell_item = self.table.item(row, 1)  # Cell 열
                value_item = self.table.item(row, 3)  # 값 열
                
                if cell_item and value_item:
                    cell = cell_item.text().strip()
                    value = value_item.text().strip()
                    
                    if cell and value:
                        # 명령 유형 결정 (값의 타입에 따라 자동 판단)
                        command_type = self.determine_command_type(value)
                        
                        # 명령어 생성: 명령유형 + Cell + 값
                        command = f"{command_type}{cell}{value}"
                        
                        try:
                            response = self.telnet_manager.send_command(command)
                            sent_count += 1
                            print(f"전송 성공: {command} -> {response}")
                        except Exception as e:
                            error_count += 1
                            print(f"전송 실패: {command} -> {e}")
            
            # 결과 메시지
            if error_count == 0:
                QMessageBox.information(self, "전송 완료", 
                    f"모든 파라미터가 성공적으로 전송되었습니다.\n전송된 항목: {sent_count}개")
            else:
                QMessageBox.warning(self, "전송 완료", 
                    f"파라미터 전송이 완료되었습니다.\n성공: {sent_count}개, 실패: {error_count}개")
                    
        except Exception as e:
            QMessageBox.critical(self, "전송 오류", f"파라미터 전송 중 오류 발생:\n{e}")

    def determine_command_type(self, value: str) -> str:
        """값의 타입에 따라 명령 유형을 자동 판단한다."""
        try:
            # 정수인지 확인
            int(value)
            return "SI"  # Set Integer
        except ValueError:
            try:
                # 실수인지 확인
                float(value)
                return "SF"  # Set Float
            except ValueError:
                # 문자열
                return "SS"  # Set String

    def set_telnet_manager(self, telnet_manager: TelnetManager):
        """TelnetManager를 설정한다."""
        self.telnet_manager = telnet_manager 