"""
Redis PubSub 로깅 시스템 설정
"""
import os
import json
import argparse
from typing import Dict, Any


class Config:
    """애플리케이션 설정 클래스"""
    
    _instance = None
    _config_data = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._config_data is None:
            self._load_config()
    
    def _load_config(self):
        """설정 파일을 로드합니다."""
        parser = argparse.ArgumentParser(description='Redis PubSub 로깅 시스템')
        parser.add_argument(
            '--config', 
            '-c', 
            type=str, 
            default='config/default.json',
            help='설정 파일 경로 (기본값: config/default.json)'
        )
        
        args, _ = parser.parse_known_args()
        
        try:
            with open(args.config, 'r', encoding='utf-8') as f:
                self._config_data = json.load(f)
        except FileNotFoundError:
            print(f"설정 파일을 찾을 수 없습니다: {args.config}")
            print("기본 설정을 사용합니다.")
            self._config_data = self._get_default_config()
        except json.JSONDecodeError as e:
            print(f"설정 파일 JSON 파싱 오류: {e}")
            print("기본 설정을 사용합니다.")
            self._config_data = self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """기본 설정을 반환합니다."""
        return {
            "redis": {
                "host": "localhost",
                "port": 6379,
                "db": 0,
                "password": None,
                "retry_on_timeout": True,
                "retry_on_error": True,
                "retry": 3,
                "backoff": 0.1
            },
            "logging": {
                "log_dir": "logs",
                "log_file_size_mb": 10,
                "log_backup_count": 5
            },
            "filtering": {
                "file_filter_condition": "*.log",
                "key_field": "id"
            }
        }
    
    @property
    def REDIS_HOST(self) -> str:
        return self._config_data.get('redis', {}).get('host', 'localhost')
    
    @property
    def REDIS_PORT(self) -> int:
        return self._config_data.get('redis', {}).get('port', 6379)
    
    @property
    def REDIS_DB(self) -> int:
        return self._config_data.get('redis', {}).get('db', 0)
    
    @property
    def REDIS_PASSWORD(self):
        return self._config_data.get('redis', {}).get('password')
    
    @property
    def REDIS_RETRY_ON_TIMEOUT(self) -> bool:
        return self._config_data.get('redis', {}).get('retry_on_timeout', True)
    
    @property
    def REDIS_RETRY_ON_ERROR(self) -> bool:
        return self._config_data.get('redis', {}).get('retry_on_error', True)
    
    @property
    def REDIS_RETRY(self) -> int:
        return self._config_data.get('redis', {}).get('retry', 3)
    
    @property
    def REDIS_BACKOFF(self) -> float:
        return self._config_data.get('redis', {}).get('backoff', 0.1)
    
    @property
    def LOG_DIR(self) -> str:
        return self._config_data.get('logging', {}).get('log_dir', 'logs')
    
    @property
    def LOG_FILE_SIZE_MB(self) -> int:
        return self._config_data.get('logging', {}).get('log_file_size_mb', 10)
    
    @property
    def LOG_BACKUP_COUNT(self) -> int:
        return self._config_data.get('logging', {}).get('log_backup_count', 5)
    
    @property
    def FILE_FILTER_CONDITION(self) -> str:
        return self._config_data.get('filtering', {}).get('file_filter_condition', '*.log')
    
    @property
    def KEY_FIELD(self) -> str:
        return self._config_data.get('filtering', {}).get('key_field', 'id')
    
    def get_redis_config(self) -> Dict[str, Any]:
        """Redis 연결 설정을 반환합니다."""
        config = {
            'host': self.REDIS_HOST,
            'port': self.REDIS_PORT,
            'db': self.REDIS_DB,
            'retry_on_timeout': self.REDIS_RETRY_ON_TIMEOUT,
            'retry_on_error': self.REDIS_RETRY_ON_ERROR,
            'retry': self.REDIS_RETRY,
            'backoff': self.REDIS_BACKOFF,
        }
        
        if self.REDIS_PASSWORD:
            config['password'] = self.REDIS_PASSWORD
            
        return config
