import socket
import time
from typing import Optional
import logging

class TelnetManager:
    def __init__(self):
        self.sock = None
        self.connected = False
        self.host = ""
        self.port = 23

    def connect(self, host: str, port: int = 23) -> bool:
        """
        socket을 사용하여 동기식으로 연결한다.
        """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(5)
            self.sock.connect((host, port))
            self.connected = True
            self.host = host
            self.port = port
            logging.info(f"[Telnet] 연결 성공: {host}:{port}")
            return True
        except Exception as e:
            logging.error(f"[Telnet] 연결 실패: {e}")
            self.connected = False
            if self.sock:
                self.sock.close()
                self.sock = None
            return False

    def disconnect(self):
        """
        연결을 해제한다.
        """
        if self.sock:
            try:
                self.sock.close()
                logging.info("[Telnet] 연결 해제")
            except Exception as e:
                logging.error(f"[Telnet] 연결 해제 중 오류: {e}")
            self.sock = None
        self.connected = False

    def send(self, data: str) -> bool:
        """
        데이터를 송신한다.
        """
        if not self.connected or not self.sock:
            logging.warning("[Telnet] 연결되지 않음")
            return False
        try:
            self.sock.send(data.encode('utf-8'))
            return True
        except Exception as e:
            logging.error(f"[Telnet] 송신 오류: {e}")
            return False

    def receive(self, size: int = 1024, timeout: float = 1.0) -> Optional[str]:
        """
        데이터를 수신한다.
        """
        if not self.connected or not self.sock:
            return None
        try:
            self.sock.settimeout(timeout)
            data = self.sock.recv(size)
            if data:
                msg = data.decode('utf-8', errors='replace')
                return msg
            return None
        except socket.timeout:
            return None
        except Exception as e:
            logging.error(f"[Telnet] 수신 오류: {e}")
            return None

    def connect_and_receive_initial(self, ip: str, port: int = 23) -> str:
        """
        연결 후 초기 Welcome~User: 메시지를 수신한다. (연결 상태 유지)
        """
        try:
            if self.connect(ip, port):
                # 초기 메시지 수신 (최대 3초 대기)
                received_data = b""
                start_time = time.time()
                while time.time() - start_time < 3:
                    try:
                        self.sock.settimeout(0.5)
                        data = self.sock.recv(1024)
                        if data:
                            received_data += data
                            if b'User:' in received_data:
                                break
                    except socket.timeout:
                        continue
                    except Exception:
                        break
                
                if received_data:
                    msg = received_data.decode('utf-8', errors='replace')
                    return msg
            return "[연결 실패]"
        except Exception as e:
            logging.error(f"[Telnet] 초기 수신 오류: {e}")
            return f"[오류: {e}]"

    def login(self, username: str = "admin", password: str = "") -> bool:
        """
        자동 로그인을 수행한다.
        :param username: 사용자명 (기본값: admin)
        :param password: 패스워드 (기본값: 빈 문자열)
        :return: 로그인 성공 여부
        """
        if not self.connected or not self.sock:
            logging.error("[Telnet] 연결되지 않음")
            return False
        
        try:
            # 1. 사용자명 입력
            self.sock.send((username + "\r\n").encode('utf-8'))
            time.sleep(0.5)
            
            # 2. Password: 프롬프트 대기
            received_data = b""
            start_time = time.time()
            while time.time() - start_time < 3:
                try:
                    self.sock.settimeout(0.5)
                    data = self.sock.recv(1024)
                    if data:
                        received_data += data
                        if b'Password:' in received_data:
                            break
                except socket.timeout:
                    continue
                except Exception:
                    break
            
            if b'Password:' not in received_data:
                logging.error("[Telnet] Password 프롬프트 수신 실패")
                return False
            
            # 3. 패스워드 입력
            self.sock.send((password + "\r\n").encode('utf-8'))
            time.sleep(1)
            
            # 4. 로그인 성공 확인
            try:
                self.sock.settimeout(2)
                final_response = self.sock.recv(1024)
                if final_response:
                    response_str = final_response.decode('utf-8', errors='replace')
                    # 로그인 성공 시 나타나는 패턴 확인
                    if any(keyword in response_str.lower() for keyword in ['>', 'ready', 'logged']):
                        logging.info("[Telnet] 로그인 성공")
                        return True
            except socket.timeout:
                pass
            
            logging.info("[Telnet] 로그인 완료 (응답 확인)")
            return True
            
        except Exception as e:
            logging.error(f"[Telnet] 로그인 실패: {e}")
            return False

    def send_command(self, command: str, wait_time: float = 0.5) -> str:
        """
        명령어를 송신하고 응답을 수신한다.
        :param command: 송신할 명령어
        :param wait_time: 응답 대기 시간(초)
        :return: 수신된 응답
        """
        if not self.connected or not self.sock:
            return "[연결되지 않음]"
        
        try:
            # 명령어 송신
            self.sock.send((command + "\r\n").encode('utf-8'))
            time.sleep(wait_time)
            
            # 응답 수신
            try:
                self.sock.settimeout(wait_time + 1)
                response = self.sock.recv(4096)
                if response:
                    return response.decode('utf-8', errors='replace')
                return ""
            except socket.timeout:
                return ""
            
        except Exception as e:
            logging.error(f"[Telnet] 명령어 실행 오류: {e}")
            return f"[오류: {e}]"

    # 기존 telnetlib3 관련 메서드들 (사용하지 않음)
    """
    async def connect_async(self, host: str, port: int = 23):
        # telnetlib3 기반 - 사용하지 않음
        pass
    """ 