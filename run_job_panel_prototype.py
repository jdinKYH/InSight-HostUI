#!/usr/bin/env python3
"""
JOB 관리 그룹 프로토타입 실행 스크립트
"""

import sys
import os

# 프로젝트 루트 디렉토리를 sys.path에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

try:
    from ui.job_panel_prototype import main
    print("JOB 관리 그룹 프로토타입을 시작합니다...")
    main()
except ImportError as e:
    print(f"모듈 가져오기 오류: {e}")
    print("PyQt5가 설치되어 있는지 확인해주세요: pip install PyQt5")
except Exception as e:
    print(f"실행 오류: {e}")
    sys.exit(1) 