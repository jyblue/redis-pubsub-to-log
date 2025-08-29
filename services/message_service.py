"""
메시지 처리 서비스 모듈
"""
import os
import json
from typing import Dict, Any
from utils.logger import Logger
from utils.filter import MessageFilter
from config import Config


class MessageService:
    """메시지 처리 및 로깅 서비스 클래스"""
    
    def __init__(self):
        self.logger = Logger('MessageService')
        self.filter = MessageFilter()
        self._ensure_log_directories()
    
    def _ensure_log_directories(self):
        """로그 디렉토리가 존재하는지 확인하고 생성합니다."""
        if not os.path.exists(Config.LOG_DIR):
            os.makedirs(Config.LOG_DIR)
            self.logger.info(f"로그 디렉토리 생성: {Config.LOG_DIR}")
    
    def process_message(self, channel: str, message: str):
        """
        메시지를 처리합니다.
        
        Args:
            channel: 채널명
            message: 메시지 데이터
        """
        try:
            # JSON 파싱
            message_data = self.filter.parse_message(message)
            if not message_data:
                self.logger.warning(f"JSON 파싱 실패: {message}")
                return
            
            # 필터링 조건 확인
            if not self.filter.should_process_message(message_data):
                self.logger.debug(f"필터링 조건 불만족: {message}")
                return
            
            # 키 값 추출
            key_value = self.filter.extract_key_value(message_data)
            if not key_value:
                self.logger.warning(f"키 값 추출 실패: {message}")
                return
            
            # 폴더 경로 생성
            folder_path = os.path.join(Config.LOG_DIR, channel, key_value)
            self._ensure_folder_exists(folder_path)
            
            # 로그 파일 경로
            log_file_path = os.path.join(folder_path, 'messages.log')
            
            # 메시지 로깅
            self._log_message(log_file_path, channel, key_value, message_data)
            
        except Exception as e:
            self.logger.error(f"메시지 처리 중 오류: {str(e)}")
    
    def _ensure_folder_exists(self, folder_path: str):
        """폴더가 존재하는지 확인하고 생성합니다."""
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)
            self.logger.info(f"폴더 생성: {folder_path}")
    
    def _log_message(self, log_file_path: str, channel: str, key_value: str, message_data: Dict[str, Any]):
        """
        메시지를 로그 파일에 기록합니다.
        
        Args:
            log_file_path: 로그 파일 경로
            channel: 채널명
            key_value: 키 값
            message_data: 메시지 데이터
        """
        try:
            # 로그 메시지 생성
            import datetime
            log_entry = {
                'timestamp': datetime.datetime.now().isoformat(),
                'channel': channel,
                'key': key_value,
                'message': message_data
            }
            
            log_message = json.dumps(log_entry, ensure_ascii=False, indent=2)
            
            # 파일에 로그 기록
            with open(log_file_path, 'a', encoding='utf-8') as f:
                f.write(log_message + '\n')
            
            # 콘솔에도 출력
            console_message = f"[{channel}/{key_value}] {json.dumps(message_data, ensure_ascii=False)}"
            self.logger.info(console_message)
            
        except Exception as e:
            self.logger.error(f"로그 기록 중 오류: {str(e)}")
