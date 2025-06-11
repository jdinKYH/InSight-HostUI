# In-Sight HostUI UI 상세 설계

- 전체 창: QMainWindow (가로 3분할, **항상 전체 UI가 화면에 보이도록 자동 크기 조정, 스크롤 없음**)
  - QScreen으로 실제 화면 크기 감지, QMainWindow 크기 자동 조정
  - 내부 위젯은 QHBoxLayout, QVBoxLayout 등으로 비율 기반 자동 크기 조정
- 최소 해상도(예: 1280x720) 이상에서는 스크롤 없이 전체 UI 표시
- SVG(ui_layout.svg)는 실제 화면 크기에 맞게 자동 축소/확대됨을 안내

- 상단: Header (높이 8~10%)
- 좌측 2/3: BrowserWidget (QWebEngineView)
- 우측 1/3: ControlPanel (주소창, 그리드, 버튼, **로그 창(LogViewer, QTextEdit 등)**)
- 하단: StatusBar (높이 8~10%) 