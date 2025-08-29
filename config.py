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
    

    
    @property
    def REDIS_HOST(self) -> str:
        return self._config_data['redis']['host']
    
    @property
    def REDIS_PORT(self) -> int:
        return self._config_data['redis']['port']
    
    @property
    def REDIS_DB(self) -> int:
        return self._config_data['redis']['db']
    
    @property
    def REDIS_PASSWORD(self):
        return self._config_data['redis'].get('password')
    
    @property
    def REDIS_RETRY_ON_TIMEOUT(self) -> bool:
        return self._config_data['redis']['retry_on_timeout']
    
    @property
    def REDIS_RETRY_ON_ERROR(self) -> bool:
        return self._config_data['redis']['retry_on_error']
    
    @property
    def REDIS_RETRY(self) -> int:
        return self._config_data['redis']['retry']
    
    @property
    def REDIS_BACKOFF(self) -> float:
        return self._config_data['redis']['backoff']
    
    @property
    def REDIS_EXPONENTIAL_BACKOFF_ENABLED(self) -> bool:
        return self._config_data['redis']['exponential_backoff']['enabled']
    
    @property
    def REDIS_EXPONENTIAL_BACKOFF_BASE_DELAY(self) -> float:
        return self._config_data['redis']['exponential_backoff']['base_delay']
    
    @property
    def REDIS_EXPONENTIAL_BACKOFF_MAX_DELAY(self) -> float:
        return self._config_data['redis']['exponential_backoff']['max_delay']
    
    @property
    def REDIS_EXPONENTIAL_BACKOFF_MULTIPLIER(self) -> float:
        return self._config_data['redis']['exponential_backoff']['multiplier']
    
    @property
    def REDIS_CONNECTION_HEARTBEAT_ENABLED(self) -> bool:
        return self._config_data['redis']['connection_heartbeat']['enabled']
    
    @property
    def REDIS_CONNECTION_HEARTBEAT_INTERVAL_SECONDS(self) -> int:
        return self._config_data['redis']['connection_heartbeat']['interval_seconds']
    
    @property
    def REDIS_CONNECTION_HEARTBEAT_TIMEOUT_SECONDS(self) -> int:
        return self._config_data['redis']['connection_heartbeat']['timeout_seconds']
    
    @property
    def LOG_DIR(self) -> str:
        return self._config_data['logging']['log_dir']
    
    @property
    def MESSAGE_LOG_DIR(self) -> str:
        return self._config_data['logging']['message_log_dir']
    
    @property
    def LOG_FILE_SIZE_MB(self) -> int:
        return self._config_data['logging']['log_file_size_mb']
    
    @property
    def LOG_BACKUP_COUNT(self) -> int:
        return self._config_data['logging']['log_backup_count']
    
    @property
    def TARGET_FIELD(self) -> str:
        return self._config_data['filtering']['target_field']
    
    @property
    def TARGET_VALUES(self) -> list:
        return self._config_data['filtering']['target_values']
    
    @property
    def KEY_FIELD(self) -> str:
        return self._config_data['filtering']['key_field']
    
    @property
    def HEARTBEAT_ENABLED(self) -> bool:
        return self._config_data['heartbeat']['enabled']
    
    @property
    def HEARTBEAT_INTERVAL_SECONDS(self) -> int:
        return self._config_data['heartbeat']['interval_seconds']
    
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
