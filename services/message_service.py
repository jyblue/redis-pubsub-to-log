"""
메시지 처리 서비스 모듈
"""
import os
import json
import datetime
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
        config = Config()
        if not os.path.exists(config.LOG_DIR):
            os.makedirs(config.LOG_DIR)
            self.logger.info(f"로그 디렉토리 생성: {config.LOG_DIR}")
    
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
            
            # 폴더명 정리 (Windows 호환)
            safe_channel = self.filter.sanitize_folder_name(channel)
            safe_key_value = self.filter.sanitize_folder_name(key_value)
            
            # 폴더 경로 생성 (절대 경로 지원)
            config = Config()
            message_log_dir = config.MESSAGE_LOG_DIR
            
            # 절대 경로인지 확인
            if os.path.isabs(message_log_dir):
                base_path = message_log_dir
            else:
                # 스크립트 실행 디렉토리와 상관없이 항상 유지되도록 현재 작업 디렉토리 기준
                base_path = os.path.abspath(message_log_dir)
            
            folder_path = os.path.join(base_path, safe_channel, safe_key_value)
            self._ensure_folder_exists(folder_path)
            
            # 날짜별 로그 파일 경로
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            log_file_path = os.path.join(folder_path, f'{today}.log')
            
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
            # 현재 시간
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 한 줄 로그 메시지 생성
            log_message = f"{timestamp} [{channel}/{key_value}] {json.dumps(message_data, ensure_ascii=False)}"
            
            # RotatingFileHandler를 사용하여 로그 기록
            from logging.handlers import RotatingFileHandler
            import logging
            
            # 로거 생성
            message_logger = logging.getLogger(f'message_{channel}_{key_value}')
            message_logger.setLevel(logging.INFO)
            
            # 기존 핸들러 제거
            for handler in message_logger.handlers[:]:
                message_logger.removeHandler(handler)
            
            # 파일 핸들러 설정
            config = Config()
            file_handler = RotatingFileHandler(
                log_file_path,
                maxBytes=config.LOG_FILE_SIZE_MB * 1024 * 1024,
                backupCount=config.LOG_BACKUP_COUNT,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.INFO)
            
            # 포맷터 설정 (타임스탬프 제거, 메시지만 기록)
            formatter = logging.Formatter('%(message)s')
            file_handler.setFormatter(formatter)
            message_logger.addHandler(file_handler)
            
            # 로그 기록
            message_logger.info(log_message)
            
            # 콘솔에도 출력
            self.logger.info(log_message)
            
        except Exception as e:
            self.logger.error(f"로그 기록 중 오류: {str(e)}")
