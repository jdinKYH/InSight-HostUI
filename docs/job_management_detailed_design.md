# JOB 관리 그룹 상세 설계 문서

**버전:** 1.0  
**작성일:** 2024-12-19  
**기반:** job_management_specification.md 요구사항 명세서  
**목적:** JobPanel 클래스의 상세 구현 설계

---

## 📐 UI 레이아웃 상세 설계

### 전체 구조
```
┌─────────────────────────────────────────────────────────┐
│                  JOB 관리 (QGroupBox)                   │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────┐  ┌─────────────────────────────────────┐ │
│ │   실행 1    │  │         명령어 1 입력               │ │
│ │ (QPushButton)│  │        (QLineEdit)                 │ │
│ └─────────────┘  └─────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────┐  ┌─────────────────────────────────────┐ │
│ │   실행 2    │  │         명령어 2 입력               │ │
│ │ (QPushButton)│  │        (QLineEdit)                 │ │
│ └─────────────┘  └─────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 레이아웃 매니저
- **메인 레이아웃**: `QVBoxLayout`
- **각 행 레이아웃**: `QHBoxLayout` 
- **구조**: 2개의 QHBoxLayout을 QVBoxLayout에 배치

### 컨트롤 상세 스펙

#### 1. QGroupBox ("JOB 관리")
```python
- 제목: "JOB 관리"
- 최소 높이: 120px
- 여백: 10px
- 프레임 스타일: QFrame.StyledPanel
```

#### 2. QPushButton (실행 버튼들)
```python
- 크기: 고정 너비 100px, 높이 30px
- 텍스트: "실행 1", "실행 2" 
- 스타일: 기본 QPushButton 스타일
- 활성화 조건: Telnet 연결 상태에 따라
```

#### 3. QLineEdit (명령어 입력)
```python
- 높이: 30px
- placeholder: "In-Sight Native Command 입력"
- 최대 길이: 255자
- Enter 키 지원: 입력 후 Enter 시 해당 명령 실행
```

---

## 🏗️ 클래스 구조 상세 설계

### JobPanel 클래스 정의
```python
from PyQt5.QtWidgets import (QGroupBox, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLineEdit, QMessageBox)
from PyQt5.QtCore import pyqtSignal, QObject
import logging

class JobPanel(QGroupBox):
    """
    JOB 관리 패널 클래스
    - 2개의 명령어 입력 슬롯과 실행 버튼 제공
    - Telnet을 통한 In-Sight Native Command 전송
    """
    
    # 시그널 정의
    command_executed = pyqtSignal(str, str)  # (command, result)
    error_occurred = pyqtSignal(str)         # error_message
    
    def __init__(self, parent=None, telnet_manager=None):
        """
        초기화
        Args:
            parent: 부모 위젯
            telnet_manager: TelnetManager 인스턴스 (기존 Telnet Panel과 공유)
        """
        super().__init__("JOB 관리", parent)
        self.telnet_manager = telnet_manager
        self.logger = logging.getLogger(__name__)
        
        # UI 컨트롤 초기화
        self.btn_execute_1 = None
        self.btn_execute_2 = None
        self.line_command_1 = None
        self.line_command_2 = None
        
        self.setup_ui()
        self.connect_signals()
        
    def setup_ui(self):
        """UI 레이아웃 구성"""
        
    def connect_signals(self):
        """시그널-슬롯 연결"""
        
    def execute_command_1(self):
        """명령어 1 실행"""
        
    def execute_command_2(self):
        """명령어 2 실행"""
        
    def execute_command(self, command: str, slot_number: int):
        """공통 명령 실행 메서드"""
        
    def update_button_states(self, telnet_connected: bool):
        """Telnet 연결 상태에 따른 버튼 활성화/비활성화"""
        
    def on_line_edit_return_pressed(self, line_edit: QLineEdit, slot_number: int):
        """Enter 키 입력 처리"""
        
    def show_error_message(self, message: str):
        """오류 메시지 표시"""
        
    def log_command_execution(self, command: str, result: str, slot_number: int):
        """명령 실행 로그 기록"""
```

---

## 🔧 메서드 상세 구현

### 1. setup_ui() 메서드
```python
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
    
    self.line_command_1 = QLineEdit()
    self.line_command_1.setPlaceholderText("In-Sight Native Command 입력")
    self.line_command_1.setMaxLength(255)
    self.line_command_1.setFixedHeight(30)
    
    row1_layout.addWidget(self.btn_execute_1)
    row1_layout.addWidget(self.line_command_1)
    
    # 두 번째 행 (명령어 2)
    row2_layout = QHBoxLayout()
    self.btn_execute_2 = QPushButton("실행 2")
    self.btn_execute_2.setFixedSize(100, 30)
    self.btn_execute_2.setEnabled(False)  # 초기 비활성화
    
    self.line_command_2 = QLineEdit()
    self.line_command_2.setPlaceholderText("In-Sight Native Command 입력")
    self.line_command_2.setMaxLength(255)
    self.line_command_2.setFixedHeight(30)
    
    row2_layout.addWidget(self.btn_execute_2)
    row2_layout.addWidget(self.line_command_2)
    
    # 메인 레이아웃에 추가
    main_layout.addLayout(row1_layout)
    main_layout.addLayout(row2_layout)
    
    # 최소 높이 설정
    self.setMinimumHeight(120)
```

### 2. connect_signals() 메서드
```python
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
```

### 3. 명령 실행 메서드들
```python
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
        
        # 명령 전송
        self.logger.info(f"JOB 슬롯 {slot_number} 명령 전송: {command}")
        result = self.telnet_manager.send_command(command)
        
        # 결과 처리
        if result:
            self.log_command_execution(command, result, slot_number)
            self.command_executed.emit(command, result)
        else:
            error_msg = f"슬롯 {slot_number}: 명령 실행 실패"
            self.show_error_message(error_msg)
            self.error_occurred.emit(error_msg)
            
    except Exception as e:
        error_msg = f"슬롯 {slot_number} 오류: {str(e)}"
        self.logger.error(error_msg)
        self.show_error_message(error_msg)
        self.error_occurred.emit(error_msg)
```

### 4. 유틸리티 메서드들
```python
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
    self.execute_command(command, slot_number)

def show_error_message(self, message: str):
    """
    오류 메시지 표시 (로그 창에 출력)
    Args:
        message: 오류 메시지
    """
    self.logger.error(f"JOB 관리: {message}")
    # 메인 윈도우의 로그 패널에 메시지 전송
    if hasattr(self.parent(), 'log_panel'):
        self.parent().log_panel.add_log(f"JOB 관리 오류: {message}")

def log_command_execution(self, command: str, result: str, slot_number: int):
    """
    명령 실행 로그 기록
    Args:
        command: 실행된 명령어
        result: 실행 결과
        slot_number: 슬롯 번호
    """
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] JOB 슬롯 {slot_number} TX: {command}"
    
    if result:
        log_message += f"\n[{timestamp}] JOB 슬롯 {slot_number} RX: {result}"
    
    self.logger.info(log_message)
    
    # 메인 윈도우의 로그 패널에 메시지 전송
    if hasattr(self.parent(), 'log_panel'):
        self.parent().log_panel.add_log(log_message)
```

---

## 🔗 시스템 연동 설계

### 1. TelnetManager 연동
```python
# 메인 윈도우에서 JobPanel 초기화 시
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Telnet 매니저 (기존)
        self.telnet_manager = TelnetManager()
        
        # JobPanel 초기화 (Telnet 매니저 공유)
        self.job_panel = JobPanel(self, self.telnet_manager)
        
        # Telnet 연결 상태 시그널 연결
        self.telnet_manager.connection_changed.connect(
            self.job_panel.update_button_states
        )
```

### 2. LogPanel 연동
```python
# JobPanel에서 로그 패널로 메시지 전송
def send_log_to_panel(self, message: str):
    """로그 패널로 메시지 전송"""
    main_window = self.window()  # 최상위 윈도우 가져오기
    if hasattr(main_window, 'log_panel'):
        main_window.log_panel.add_log(f"[JOB] {message}")
```

---

## 🎨 UI 스타일링

### CSS 스타일 시트 (선택사항)
```css
/* JobPanel 스타일 */
QGroupBox#JobPanel {
    font-weight: bold;
    border: 2px solid #cccccc;
    border-radius: 5px;
    margin: 5px;
    padding-top: 10px;
}

QGroupBox#JobPanel::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 10px 0 10px;
}

/* 실행 버튼 스타일 */
QPushButton#ExecuteButton {
    background-color: #4CAF50;
    border: none;
    color: white;
    padding: 5px;
    border-radius: 3px;
    font-weight: bold;
}

QPushButton#ExecuteButton:hover {
    background-color: #45a049;
}

QPushButton#ExecuteButton:disabled {
    background-color: #cccccc;
    color: #666666;
}

/* 명령어 입력 필드 스타일 */
QLineEdit#CommandInput {
    border: 1px solid #ddd;
    border-radius: 3px;
    padding: 5px;
    font-family: "Consolas", "Monaco", monospace;
}

QLineEdit#CommandInput:focus {
    border: 2px solid #4CAF50;
}
```

---

## ⚠️ 오류 처리 설계

### 1. 입력 유효성 검사
```python
def validate_command(self, command: str) -> tuple[bool, str]:
    """
    명령어 유효성 검사
    Returns:
        (is_valid, error_message)
    """
    if not command or command.isspace():
        return False, "명령어가 비어있습니다."
    
    if len(command) > 255:
        return False, "명령어가 너무 깁니다. (최대 255자)"
    
    # 특수 문자 검사 (필요시)
    forbidden_chars = ['\n', '\r', '\t']
    for char in forbidden_chars:
        if char in command:
            return False, f"허용되지 않는 문자가 포함되어 있습니다: {repr(char)}"
    
    return True, ""
```

### 2. 예외 처리 전략
```python
# 계층적 예외 처리
try:
    # 명령 실행
    result = self.telnet_manager.send_command(command)
except ConnectionError:
    # Telnet 연결 오류
    self.handle_connection_error()
except TimeoutError:
    # 타임아웃 오류
    self.handle_timeout_error()
except Exception as e:
    # 기타 예외
    self.handle_general_error(e)
```

---

## 🧪 테스트 설계

### 1. 단위 테스트 항목
```python
class TestJobPanel(unittest.TestCase):
    def setUp(self):
        # 테스트 환경 설정
        
    def test_ui_initialization(self):
        """UI 초기화 테스트"""
        
    def test_button_state_update(self):
        """버튼 상태 업데이트 테스트"""
        
    def test_command_validation(self):
        """명령어 유효성 검사 테스트"""
        
    def test_command_execution(self):
        """명령 실행 테스트"""
        
    def test_error_handling(self):
        """오류 처리 테스트"""
```

### 2. 통합 테스트 시나리오
1. **정상 플로우**: 명령 입력 → 실행 → 결과 수신 → 로그 기록
2. **오류 플로우**: 연결 오류, 입력 오류, 실행 오류 처리
3. **UI 반응성**: 버튼 상태, 입력 필드 동작

---

## 📁 파일 구조

```
src/
├── ui/
│   ├── job_panel.py          # JobPanel 클래스 (메인)
│   ├── main_window.py        # 메인 윈도우 (JobPanel 통합)
│   └── components/
│       └── __init__.py
└── tests/
    ├── test_job_panel.py     # JobPanel 단위 테스트
    └── __init__.py
```

---

## 🚀 구현 우선순위

### Phase 1: 기본 UI 구현
1. JobPanel 클래스 기본 구조 생성
2. UI 레이아웃 구성 (버튼, 텍스트박스)
3. 기본 이벤트 핸들링 (클릭, Enter)

### Phase 2: 기능 구현  
1. TelnetManager 연동
2. 명령 전송 기능 구현
3. 오류 처리 및 유효성 검사

### Phase 3: 통합 및 테스트
1. 메인 윈도우와 통합
2. 로그 패널 연동
3. 테스트 코드 작성 및 검증

---

> 본 상세 설계를 바탕으로 JobPanel 클래스를 구현하여  
> 간단하고 효율적인 JOB 관리 그룹을 완성합니다.

화이팅! 