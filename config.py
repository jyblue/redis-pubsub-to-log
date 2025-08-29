"""
Redis PubSub 로깅 시스템 설정
"""
import os
import json
import argparse
import sys
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
            print(f"오류: 설정 파일을 찾을 수 없습니다: {args.config}")
            print("애플리케이션을 종료합니다.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"오류: 설정 파일 JSON 파싱 오류: {e}")
            print("애플리케이션을 종료합니다.")
            sys.exit(1)
    

    
    def _get_nested_value(self, *keys, default=None):
        """중첩된 딕셔너리에서 값을 안전하게 가져옵니다."""
        value = self._config_data
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
    
    # Redis 설정
    @property
    def REDIS_HOST(self) -> str:
        return self._get_nested_value('redis', 'host')
    
    @property
    def REDIS_PORT(self) -> int:
        return self._get_nested_value('redis', 'port')
    
    @property
    def REDIS_DB(self) -> int:
        return self._get_nested_value('redis', 'db')
    
    @property
    def REDIS_PASSWORD(self):
        return self._get_nested_value('redis', 'password')
    
    @property
    def REDIS_RETRY_ON_TIMEOUT(self) -> bool:
        return self._get_nested_value('redis', 'retry_on_timeout')
    
    @property
    def REDIS_RETRY_ON_ERROR(self) -> bool:
        return self._get_nested_value('redis', 'retry_on_error')
    
    @property
    def REDIS_RETRY(self) -> int:
        return self._get_nested_value('redis', 'retry')
    
    @property
    def REDIS_EXPONENTIAL_BACKOFF_BASE_DELAY(self) -> float:
        return self._get_nested_value('redis', 'exponential_backoff', 'base_delay')
    
    @property
    def REDIS_EXPONENTIAL_BACKOFF_MAX_DELAY(self) -> float:
        return self._get_nested_value('redis', 'exponential_backoff', 'max_delay')
    
    @property
    def REDIS_EXPONENTIAL_BACKOFF_MULTIPLIER(self) -> float:
        return self._get_nested_value('redis', 'exponential_backoff', 'multiplier')
    
    # 로깅 설정
    @property
    def LOG_DIR(self) -> str:
        return self._get_nested_value('logging', 'log_dir')
    
    @property
    def MESSAGE_LOG_DIR(self) -> str:
        return self._get_nested_value('logging', 'message_log_dir')
    
    @property
    def LOG_FILE_SIZE_MB(self) -> int:
        return self._get_nested_value('logging', 'log_file_size_mb')
    
    @property
    def LOG_BACKUP_COUNT(self) -> int:
        return self._get_nested_value('logging', 'log_backup_count')
    
    # 필터링 설정
    @property
    def TARGET_FIELD(self) -> str:
        return self._get_nested_value('filtering', 'target_field')
    
    @property
    def TARGET_VALUES(self) -> list:
        return self._get_nested_value('filtering', 'target_values')
    
    @property
    def KEY_FIELD(self) -> str:
        return self._get_nested_value('filtering', 'key_field')
    
    @property
    def USE_REGEX(self) -> bool:
        return self._get_nested_value('filtering', 'use_regex', default=False)
    
    # Heartbeat 설정
    @property
    def HEARTBEAT_ENABLED(self) -> bool:
        return self._get_nested_value('heartbeat', 'enabled')
    
    @property
    def HEARTBEAT_INTERVAL_SECONDS(self) -> int:
        return self._get_nested_value('heartbeat', 'interval_seconds')
    
    def get_redis_config(self) -> Dict[str, Any]:
        """Redis 연결 설정을 반환합니다."""
        config = {
            'host': self.REDIS_HOST,
            'port': self.REDIS_PORT,
            'db': self.REDIS_DB,
            'retry_on_timeout': self.REDIS_RETRY_ON_TIMEOUT,
            'retry_on_error': self.REDIS_RETRY_ON_ERROR,
            'retry': self.REDIS_RETRY,
        }
        
        if self.REDIS_PASSWORD:
            config['password'] = self.REDIS_PASSWORD
            
        return config
