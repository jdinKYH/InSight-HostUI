@echo off
echo ====================================
echo     In-Sight HostUI 자동 커밋 시작
echo ====================================
echo.

cd /d "%~dp0\.."

echo 가상환경 활성화 중...
call venv312\Scripts\activate.bat

echo watchdog 패키지 설치 확인 중...
pip install watchdog

echo.
echo 자동 커밋 시스템을 시작합니다...
echo 중지하려면 Ctrl+C를 누르세요.
echo.

python scripts\auto_commit.py

pause 