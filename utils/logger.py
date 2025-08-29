"""
로깅 유틸리티 모듈
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional
from config import Config


class Logger:
    """로깅 관리 클래스"""
    
    def __init__(self, name: str, log_dir: str = None):
        self.name = name
        self.log_dir = log_dir or Config.LOG_DIR
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """로거를 설정하고 반환합니다."""
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.INFO)
        
        # 이미 핸들러가 설정되어 있다면 추가하지 않음
        if logger.handlers:
            return logger
        
        # 콘솔 핸들러
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # 파일 핸들러 (Rotating)
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # Windows 호환 파일 경로
        log_file_path = os.path.join(self.log_dir, f'{self.name}.log')
        
        file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=Config.LOG_FILE_SIZE_MB * 1024 * 1024,  # MB to bytes
            backupCount=Config.LOG_BACKUP_COUNT,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    def info(self, message: str):
        """정보 로그를 기록합니다."""
        self.logger.info(message)
    
    def error(self, message: str):
        """에러 로그를 기록합니다."""
        self.logger.error(message)
    
    def warning(self, message: str):
        """경고 로그를 기록합니다."""
        self.logger.warning(message)
    
    def debug(self, message: str):
        """디버그 로그를 기록합니다."""
        self.logger.debug(message)
