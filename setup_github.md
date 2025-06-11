# GitHub 연동 설정 가이드

## 현재 상태
✅ Git 초기화 완료  
✅ .gitignore 파일 생성 완료  
✅ 초기 커밋 완료  

## GitHub 리포지토리 연결 방법

### 1. GitHub에서 새 리포지토리 생성
1. https://github.com 접속
2. "New repository" 클릭
3. Repository name: `InSight-HostUI`
4. Description: `In-Sight Host UI Application built with PyQt5 for industrial vision system control`
5. Public/Private 선택
6. **"Add a README file" 체크 해제** (이미 로컬에 파일들이 있음)
7. "Create repository" 클릭

### 2. 로컬 리포지토리와 연결
GitHub에서 리포지토리 생성 후, 다음 명령어를 실행하세요:

```bash
# 원격 리포지토리 연결 (YOUR_USERNAME를 실제 GitHub 사용자명으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/InSight-HostUI.git

# 기본 브랜치를 main으로 설정
git branch -M main

# GitHub에 푸시
git push -u origin main
```

### 3. 향후 변경 사항 푸시
```bash
# 변경 사항 추가
git add .

# 커밋
git commit -m "커밋 메시지"

# 푸시
git push
```

## 프로젝트 구조
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

## 주요 기능
- PyQt5 기반 GUI 애플리케이션
- 탭 기반 인터페이스 (메인, 설정, 데이터 검색, 로그)
- 웹 브라우저 위젯 통합
- Telnet 연결 관리
- 산업용 비전 시스템 제어

## 개발 환경
- Python 3.12+
- PyQt5
- Virtual Environment (venv312) 