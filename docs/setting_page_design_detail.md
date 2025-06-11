# 설정 페이지 세부 설계 문서 (초안)

**버전:** 0.3  
**작성일:** 2024-06-08

---

## 1. TelnetPanel 상세 설계
- QGroupBox("Telnet 설정")
  - QFormLayout: 
    - 서버 주소(QLineEdit)
    - 포트(QLineEdit)
    - 모드(QLabel, "Client"로 고정)
    - 연결상태(QLabel)
  - QHBoxLayout: 연결(QPushButton), 해제(QPushButton), 테스트(QPushButton)
  - 통신 데이터 입력(QTextEdit)
  - 전송(QPushButton)
  - 통신 로그(QTextEdit, 읽기 전용)
    - **각 로그 항목에 시간, 전송 데이터, 전송 후 수신 데이터 모두 표시**
    - 예시: `[2024-06-08 14:23:01] TX: testdata123`<br> `[2024-06-08 14:23:01] RX: resultOK` 
- 신호/슬롯:
  - 연결/해제/테스트/전송 버튼 클릭 → TelnetManager(로직) 호출
  - 전송 시 입력 데이터 끝에 CR+LF 자동 추가
  - 통신 결과/로그 → UI에 시간, 전송/수신 데이터 모두 표시
- 데이터 구조:
  - TelnetConfig: {address: str, port: int, mode: str = "Client"}
  - 통신 로그: List[Dict[str, str]] (예: {time, tx, rx})

## 2. ParamPanel 상세 설계
- QGroupBox("검사 파라미터")
  - QTableWidget: 파라미터 목록(행 추가/삭제/수정)
  - QHBoxLayout: 추가/수정/삭제(QPushButton)
  - 파라미터 상세 입력(QFormLayout, QLineEdit/QComboBox 등)
- 신호/슬롯:
  - 추가/수정/삭제 버튼 → 파라미터 데이터 변경
  - 변경 시 UI/CSV 파일 동기화
- 데이터 구조:
  - List[Dict[str, Any]] (각 파라미터: {cell, 항목, 값, 판정 등})

## 3. LogPanel 상세 설계
- QGroupBox("로그")
  - QTextEdit(읽기 전용)
  - 로그 레벨/필터(선택적)
- 신호/슬롯:
  - Telnet/설정 변경 등 이벤트 발생 시 로그 추가

## 4. 파일 입출력/저장 구조
- 설정값: CSV 파일로 저장/불러오기
- 파일명/폴더 지정: QFileDialog 사용
- 저장/불러오기/초기화 버튼 구현
- 예외 발생 시 사용자 안내(QMessageBox)

## 5. 다국어 지원
- Qt Linguist(.ts/.qm) 기반 다국어(한국어/영어) 리소스 분리
- UI 텍스트는 tr() 함수로 래핑

## 6. 예외처리/피드백
- 모든 외부 입출력/통신 try-except 처리
- 성공/실패/경고 메시지: 상태바, 로그, QMessageBox로 안내

## 7. 확장성
- 각 Panel/로직은 별도 클래스로 분리(MVC 구조)
- 신규 파라미터/설정 항목 추가 용이

---

> UI 상세 설계는 별도 SVG 파일로 작성하여 docs 폴더에 저장

화이팅! 