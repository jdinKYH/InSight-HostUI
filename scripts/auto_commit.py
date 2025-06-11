#!/usr/bin/env python3
"""
자동 커밋 시스템
파일 변경을 감지하고 적절한 시점에 자동으로 Git 커밋을 수행합니다.
"""

import os
import time
import json
import subprocess
import threading
from datetime import datetime
from pathlib import Path
from typing import Set, Dict, Any
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class AutoCommitConfig:
    """자동 커밋 설정 관리"""
    
    def __init__(self, config_file: str = "scripts/auto_commit_config.json"):
        self.config_file = config_file
        self.default_config = {
            "enabled": True,
            "watch_extensions": [".py", ".md", ".txt", ".json", ".yaml", ".yml", ".html", ".css", ".js"],
            "ignore_patterns": ["__pycache__", ".git", ".vscode", ".idea", "node_modules", "*.log", "*.tmp"],
            "commit_delay_seconds": 30,
            "max_commits_per_hour": 10,
            "auto_push": False,
            "commit_message_templates": {
                "default": "Auto-commit: Update files",
                ".py": "Auto-commit: Update Python files",
                ".md": "Auto-commit: Update documentation",
                ".json": "Auto-commit: Update configuration",
                ".html": "Auto-commit: Update HTML files",
                ".css": "Auto-commit: Update styles",
                ".js": "Auto-commit: Update JavaScript files"
            }
        }
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """설정 파일 로드"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # 기본 설정과 병합
                merged_config = self.default_config.copy()
                merged_config.update(config)
                return merged_config
            else:
                self.save_config()
                return self.default_config.copy()
        except Exception as e:
            print(f"설정 파일 로드 실패: {e}, 기본 설정 사용")
            return self.default_config.copy()
    
    def save_config(self):
        """설정 파일 저장"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"설정 파일 저장 실패: {e}")

class AutoCommitHandler(FileSystemEventHandler):
    """파일 시스템 이벤트 핸들러"""
    
    def __init__(self, config: AutoCommitConfig, project_root: str):
        super().__init__()
        self.config = config
        self.project_root = project_root
        self.pending_files: Set[str] = set()
        self.commit_timer = None
        self.commit_count = 0
        self.last_hour = datetime.now().hour
        self.lock = threading.Lock()
    
    def should_watch_file(self, file_path: str) -> bool:
        """파일이 감시 대상인지 확인"""
        file_path = os.path.relpath(file_path, self.project_root)
        
        # 무시 패턴 확인
        for pattern in self.config.config["ignore_patterns"]:
            if pattern in file_path:
                return False
        
        # 확장자 확인
        _, ext = os.path.splitext(file_path)
        return ext in self.config.config["watch_extensions"]
    
    def on_modified(self, event):
        """파일 수정 이벤트 처리"""
        if event.is_directory:
            return
        
        if self.should_watch_file(event.src_path):
            with self.lock:
                self.pending_files.add(event.src_path)
                self.schedule_commit()
    
    def on_created(self, event):
        """파일 생성 이벤트 처리"""
        if event.is_directory:
            return
        
        if self.should_watch_file(event.src_path):
            with self.lock:
                self.pending_files.add(event.src_path)
                self.schedule_commit()
    
    def schedule_commit(self):
        """커밋 스케줄링"""
        if self.commit_timer:
            self.commit_timer.cancel()
        
        self.commit_timer = threading.Timer(
            self.config.config["commit_delay_seconds"],
            self.perform_commit
        )
        self.commit_timer.start()
    
    def perform_commit(self):
        """실제 커밋 수행"""
        with self.lock:
            if not self.pending_files:
                return
            
            # 시간당 커밋 제한 확인
            current_hour = datetime.now().hour
            if current_hour != self.last_hour:
                self.commit_count = 0
                self.last_hour = current_hour
            
            if self.commit_count >= self.config.config["max_commits_per_hour"]:
                print(f"시간당 최대 커밋 수({self.config.config['max_commits_per_hour']})에 도달했습니다.")
                return
            
            try:
                # Git 상태 확인
                result = subprocess.run(
                    ["git", "status", "--porcelain"],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True
                )
                
                if not result.stdout.strip():
                    print("커밋할 변경사항이 없습니다.")
                    self.pending_files.clear()
                    return
                
                # 커밋 메시지 생성
                commit_message = self.generate_commit_message()
                
                # Git add
                subprocess.run(
                    ["git", "add", "."],
                    cwd=self.project_root,
                    check=True
                )
                
                # Git commit
                subprocess.run(
                    ["git", "commit", "-m", commit_message],
                    cwd=self.project_root,
                    check=True
                )
                
                self.commit_count += 1
                print(f"✅ 자동 커밋 완료: {commit_message}")
                
                # 자동 푸시 옵션
                if self.config.config["auto_push"]:
                    try:
                        subprocess.run(
                            ["git", "push"],
                            cwd=self.project_root,
                            check=True
                        )
                        print("✅ 자동 푸시 완료")
                    except subprocess.CalledProcessError as e:
                        print(f"❌ 자동 푸시 실패: {e}")
                
                self.pending_files.clear()
                
            except subprocess.CalledProcessError as e:
                print(f"❌ 커밋 실패: {e}")
            except Exception as e:
                print(f"❌ 예외 발생: {e}")
    
    def generate_commit_message(self) -> str:
        """커밋 메시지 생성"""
        if not self.pending_files:
            return self.config.config["commit_message_templates"]["default"]
        
        # 파일 확장자별 분류
        extensions = set()
        for file_path in self.pending_files:
            _, ext = os.path.splitext(file_path)
            if ext:
                extensions.add(ext)
        
        # 가장 많은 확장자 기준으로 메시지 선택
        if len(extensions) == 1:
            ext = next(iter(extensions))
            template = self.config.config["commit_message_templates"].get(
                ext, 
                self.config.config["commit_message_templates"]["default"]
            )
        else:
            template = self.config.config["commit_message_templates"]["default"]
        
        # 타임스탬프 추가
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"{template} ({timestamp})"

class AutoCommitManager:
    """자동 커밋 관리자"""
    
    def __init__(self, project_root: str = None):
        self.project_root = project_root or os.getcwd()
        self.config = AutoCommitConfig()
        self.observer = None
        self.handler = None
    
    def start(self):
        """자동 커밋 시작"""
        if not self.config.config["enabled"]:
            print("자동 커밋이 비활성화되어 있습니다.")
            return
        
        # Git 리포지토리 확인
        if not os.path.exists(os.path.join(self.project_root, ".git")):
            print("❌ Git 리포지토리가 아닙니다.")
            return
        
        self.handler = AutoCommitHandler(self.config, self.project_root)
        self.observer = Observer()
        self.observer.schedule(self.handler, self.project_root, recursive=True)
        
        try:
            self.observer.start()
            print(f"🚀 자동 커밋 시스템 시작됨: {self.project_root}")
            print(f"📁 감시 중인 확장자: {self.config.config['watch_extensions']}")
            print(f"⏱️  커밋 지연 시간: {self.config.config['commit_delay_seconds']}초")
            print("Ctrl+C로 중지할 수 있습니다.\n")
            
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n⏹️  자동 커밋 중지됨")
        finally:
            if self.observer:
                self.observer.stop()
                self.observer.join()
    
    def stop(self):
        """자동 커밋 중지"""
        if self.observer:
            self.observer.stop()
            self.observer.join()

def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description="자동 Git 커밋 시스템")
    parser.add_argument("--path", "-p", default=None, help="프로젝트 경로")
    parser.add_argument("--config", "-c", action="store_true", help="설정 파일 생성/편집")
    
    args = parser.parse_args()
    
    if args.config:
        config = AutoCommitConfig()
        print(f"설정 파일 위치: {config.config_file}")
        print("설정을 수정한 후 다시 실행하세요.")
        return
    
    manager = AutoCommitManager(args.path)
    manager.start()

if __name__ == "__main__":
    main() 