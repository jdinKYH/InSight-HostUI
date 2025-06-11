# In-Sight HostUI 개발 세부 체크리스트

## 1. 프로젝트 세팅
- [ ] 프로젝트 폴더 구조 생성 (src, tests, docs, config, resources 등)
- [ ] requirements.txt 작성 및 패키지 설치 (PyQt5/6, 기타)
- [ ] config 디렉토리 및 기본 설정 파일 생성 (config.ini/json)
- [ ] logging 설정 (파일/콘솔 로그)
- [ ] README.md, PRD, .gitignore 작성 및 docs 폴더 정리

## 2. UI 1차 구현
- [ ] PyQt 메인 윈도우 클래스 생성 (QMainWindow)
- [ ] QScreen으로 화면 해상도 감지 및 메인 윈도우 크기 자동 조정
- [ ] QHBoxLayout으로 3분할 레이아웃 구현
- [ ] HeaderWidget 구현 (회사명, 프로그램명, 날짜/시간, QTimer)
- [ ] BrowserWidget 구현 (QWebEngineView, 좌측 2/3)
- [ ] ControlPanel 구현 (우측 1/3)
  - [ ] 주소창(QLineEdit) 추가
  - [ ] 그리드(QTableWidget) 추가
  - [ ] 로그 창(QTextEdit 등) 추가
  - [ ] 버튼(QPushButton 등) 추가
- [ ] StatusBar 구현 (상태 메시지)
- [ ] 각 위젯/컴포넌트의 색상 및 스타일 적용

## 3. 기능 1차 구현
- [ ] 고정 In-Sight 주소 자동 입력 및 접속
- [ ] 브라우저 로딩/에러/성공 상태 표시 (시그널 연결)
- [ ] 연결 상태 실시간 표시 (StatusBar 등)
- [ ] 접속 기록/이벤트 로그 파일 저장 (logging)
- [ ] 에러 발생 시 사용자 안내 (QMessageBox 등)

## 4. 설정/언어
- [ ] 다국어 리소스 파일(.ts/.qm) 작성 (한국어/영어)
- [ ] 언어 선택 UI 및 동적 전환 기능 구현
- [ ] 설정 파일(언어, 주소 등) 읽기/쓰기 기능 구현
- [ ] 설정 다이얼로그/페이지 구현

## 5. 배포/테스트
- [ ] PyInstaller 스크립트 작성 및 단일 실행파일 빌드
- [ ] 리소스(아이콘, 스타일 등) 경로 점검 및 포함
- [ ] Windows 10/11 환경에서 실행 테스트 (기능별 체크리스트 활용)

## 6. 고도화
- [ ] 로그 뷰어 UI(로그 창) 실시간 갱신 및 검색/필터 기능 구현
- [ ] 셋팅 페이지, 추가 UI(확장성 고려) 설계 및 구현
- [ ] UI/UX 개선(반응형, 접근성 등)

## 7. 문서화/테스트
- [ ] 사용자 매뉴얼 작성 (주요 기능별 스크린샷, 사용법, FAQ 등)
- [ ] README, PRD 최신화
- [ ] 주요 기능별 단위 테스트 코드 작성 (unittest/pytest)
- [ ] 테스트 결과 문서화 및 회고

---

화이팅! 