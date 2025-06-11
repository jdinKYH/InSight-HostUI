# 자동 커밋 시스템 가이드

## 🎯 개요

파일 변경을 자동으로 감지하고 적절한 시점에 Git 커밋을 수행하는 시스템입니다.

## 🚀 사용법

### 방법 1: 배치 파일 실행 (권장)
```bash
# Windows에서 더블클릭 또는 터미널에서 실행
scripts\start_auto_commit.bat
```

### 방법 2: 직접 실행
```bash
# 가상환경 활성화
venv312\Scripts\activate

# 의존성 설치
pip install watchdog

# 자동 커밋 시작
python scripts\auto_commit.py
```

### 방법 3: 특정 경로 지정
```bash
python scripts\auto_commit.py --path "C:\다른\프로젝트\경로"
```

## ⚙️ 설정

### 설정 파일 위치
- `scripts/auto_commit_config.json`

### 주요 설정 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `enabled` | 자동 커밋 활성화 | `true` |
| `watch_extensions` | 감시할 파일 확장자 | `[".py", ".md", ".txt", ...]` |
| `ignore_patterns` | 무시할 파일/폴더 패턴 | `["__pycache__", ".git", ...]` |
| `commit_delay_seconds` | 변경 후 커밋까지 대기 시간 | `30` |
| `max_commits_per_hour` | 시간당 최대 커밋 수 | `10` |
| `auto_push` | 자동 푸시 여부 | `false` |

### 설정 수정 방법

1. **설정 파일 생성/확인**
   ```bash
   python scripts\auto_commit.py --config
   ```

2. **JSON 파일 직접 편집**
   ```json
   {
     "enabled": true,
     "commit_delay_seconds": 60,
     "auto_push": true
   }
   ```

## 🔧 동작 원리

### 1. 파일 감시
- 프로젝트 디렉토리의 모든 하위 폴더 감시
- 설정된 확장자의 파일만 추적
- 무시 패턴에 해당하는 파일/폴더 제외

### 2. 변경 감지
- 파일 수정/생성 이벤트 감지
- 중복 이벤트 방지를 위한 디바운싱

### 3. 커밋 수행
- 설정된 지연 시간 후 자동 커밋
- 스마트 커밋 메시지 생성
- 시간당 커밋 수 제한

### 4. 커밋 메시지 생성
- 파일 확장자별 템플릿 사용
- 타임스탬프 자동 추가
- 예시: `Auto-commit: Update Python code (2024-12-06 15:30:45)`

## 📋 다른 자동 커밋 방법들

### 방법 2: IDE/에디터 확장 프로그램

#### VS Code / Cursor 확장 프로그램
1. **GitLens** - Git 자동 커밋 기능
2. **Auto Commit** - 파일 저장 시 자동 커밋
3. **Git Auto Sync** - 자동 커밋 + 푸시

#### 설치 방법
```bash
# VS Code Extensions 검색
- "Auto Commit"
- "GitLens"
- "Git Auto Sync"
```

### 방법 3: Git Hooks

#### Pre-commit Hook 설정
```bash
# .git/hooks/pre-commit 파일 생성
#!/bin/sh
echo "Pre-commit hook 실행됨"
# 여기에 자동 처리 로직 추가
```

### 방법 4: 스케줄러 기반

#### Windows 작업 스케줄러
```bash
# 매 30분마다 자동 커밋
schtasks /create /tn "AutoCommit" /tr "C:\path\to\auto_commit.bat" /sc minute /mo 30
```

#### cron (Linux/Mac)
```bash
# 매 30분마다 실행
*/30 * * * * cd /path/to/project && git add . && git commit -m "Auto-commit $(date)"
```

## ⚠️ 주의사항

### 1. 보안
- 민감한 정보가 포함된 파일은 `.gitignore`에 추가
- 자동 푸시 시 인증 설정 필요

### 2. 성능
- 대용량 파일은 무시 패턴에 추가 권장
- 너무 빈번한 커밋 방지를 위한 제한 설정

### 3. 협업
- 팀 프로젝트에서는 커밋 메시지 규칙 협의
- 자동 푸시는 신중하게 사용

## 🛠️ 트러블슈팅

### 문제 1: watchdog 모듈 오류
```bash
pip install watchdog
```

### 문제 2: Git 권한 오류
```bash
git config --global user.name "사용자명"
git config --global user.email "이메일"
```

### 문제 3: 너무 많은 커밋
- `max_commits_per_hour` 설정 조정
- `commit_delay_seconds` 증가

### 문제 4: 특정 파일이 무시됨
- `watch_extensions`에 확장자 추가
- `ignore_patterns`에서 패턴 제거

## 📊 성능 최적화

### 1. 무시 패턴 최적화
```json
{
  "ignore_patterns": [
    "__pycache__",
    "node_modules",
    "*.log",
    "*.tmp",
    ".git",
    "venv*"
  ]
}
```

### 2. 지연 시간 조정
```json
{
  "commit_delay_seconds": 60
}
```

### 3. 시간당 커밋 제한
```json
{
  "max_commits_per_hour": 5
}
```

## 🔗 관련 링크

- [Watchdog 라이브러리 문서](https://python-watchdog.readthedocs.io/)
- [Git Hooks 가이드](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
- [GitLens 확장 프로그램](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens) 