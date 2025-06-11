import configparser
import os
from typing import Any

class ConfigManager:
    """
    config/config.ini 파일을 읽고 쓰는 설정 관리자 클래스
    """
    def __init__(self, config_path: str = "config/config.ini"):
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self._load_config()

    def _load_config(self) -> None:
        try:
            if os.path.exists(self.config_path):
                self.config.read(self.config_path, encoding="utf-8")
        except Exception as e:
            print(f"[ConfigManager] 설정 파일 로드 실패: {e}")

    def get(self, section: str, option: str, fallback: Any = None) -> Any:
        try:
            return self.config.get(section, option, fallback=fallback)
        except Exception as e:
            print(f"[ConfigManager] 설정 읽기 실패: {e}")
            return fallback

    def set(self, section: str, option: str, value: Any) -> None:
        try:
            if not self.config.has_section(section):
                self.config.add_section(section)
            self.config.set(section, option, str(value))
            with open(self.config_path, 'w', encoding="utf-8") as configfile:
                self.config.write(configfile)
        except Exception as e:
            print(f"[ConfigManager] 설정 저장 실패: {e}") 