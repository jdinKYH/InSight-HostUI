# In-Sight Host UI

PyQt5를 기반으로 한 산업용 비전 시스템 제어 애플리케이션입니다.

## 🎯 주요 기능

- **탭 기반 인터페이스**: 메인, 설정, 데이터 검색, 로그 탭으로 구성
- **웹 브라우저 통합**: 내장 브라우저를 통한 장비 웹 인터페이스 접근
- **Telnet 연결 관리**: 산업용 장비와의 텔넷 통신
- **파라미터 제어**: 실시간 장비 파라미터 모니터링 및 제어
- **로그 시스템**: 시스템 동작 로그 관리

## 📋 시스템 요구사항

- Python 3.12+
- PyQt5
- Windows 10/11

## 🚀 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/YOUR_USERNAME/InSight-HostUI.git
cd InSight-HostUI
```

### 2. 가상환경 설정
```bash
python -m venv venv312
venv312\Scripts\activate  # Windows
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 애플리케이션 실행
```bash
python src/main.py
```

## 📁 프로젝트 구조

```
InSight_HostUI01/
├── src/
│   ├── main.py              # 메인 애플리케이션 진입점
│   ├── ui/
│   │   ├── main_window.py   # 메인 윈도우 (탭 시스템)
│   │   ├── settings_page.py # 설정 페이지
│   │   ├── browser_widget.py# 브라우저 위젯
│   │   ├── telnet_panel.py  # Telnet 패널
│   │   ├── param_panel.py   # 파라미터 패널
│   │   └── log_panel.py     # 로그 패널
│   └── utils/
│       ├── config.py        # 설정 관리
│       ├── telnet_manager.py# Telnet 연결 관리
│       └── helpers.py       # 유틸리티 함수들
├── docs/
│   └── ui_design.svg       # UI 설계도
├── requirements.txt         # 의존성 목록
├── .gitignore              # Git 무시 파일 목록
└── README.md               # 프로젝트 설명
```

## 🎨 UI 구성

### 헤더
- 좌측: KNST R&D 회사명
- 중앙: In-Sight Host UI 타이틀
- 우측: 날짜/시간/버전 정보 + 종료 버튼

### 탭 메뉴
- **메인**: 브라우저 영역 + 컨트롤 패널
- **설정**: 장비 설정 및 파라미터 관리
- **데이터 검색**: 검사 데이터 조회 (개발 예정)
- **로그**: 시스템 로그 관리 (개발 예정)

## 🔧 개발 환경

### 코딩 스타일
- PEP 8 준수
- Type hints 사용
- 함수/클래스 docstring 작성
- SOLID 원칙 적용

### 빌드
```bash
pyinstaller src/main.py --onefile --windowed --name=InSightHostUI
```

## 📄 라이센스

이 프로젝트는 MIT 라이센스를 따릅니다.

## 👥 개발자

- KNST R&D

## 📞 지원

프로젝트 관련 문의사항은 이슈 탭을 통해 등록해주세요.

---

**버전**: 25.1.0.0  
**마지막 업데이트**: 2024년 12월 