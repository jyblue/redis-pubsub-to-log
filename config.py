"""
Redis PubSub 로깅 시스템 설정
"""
import os
from typing import Dict, Any


class Config:
    """애플리케이션 설정 클래스"""
    
    # Redis 설정
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
    
    # Redis 연결 재시도 설정
    REDIS_RETRY_ON_TIMEOUT = True
    REDIS_RETRY_ON_ERROR = True
    REDIS_RETRY = 3
    REDIS_BACKOFF = 0.1
    
    # 로깅 설정
    LOG_DIR = os.getenv('LOG_DIR', 'logs')
    LOG_FILE_SIZE_MB = 10
    LOG_BACKUP_COUNT = 5
    
    # 필터링 설정
    FILE_FILTER_CONDITION = os.getenv('FILE_FILTER_CONDITION', '*.log')
    KEY_FIELD = os.getenv('KEY_FIELD', 'id')  # JSON에서 폴더명으로 사용할 필드
    
    @classmethod
    def get_redis_config(cls) -> Dict[str, Any]:
        """Redis 연결 설정을 반환합니다."""
        config = {
            'host': cls.REDIS_HOST,
            'port': cls.REDIS_PORT,
            'db': cls.REDIS_DB,
            'retry_on_timeout': cls.REDIS_RETRY_ON_TIMEOUT,
            'retry_on_error': cls.REDIS_RETRY_ON_ERROR,
            'retry': cls.REDIS_RETRY,
            'backoff': cls.REDIS_BACKOFF,
        }
        
        if cls.REDIS_PASSWORD:
            config['password'] = cls.REDIS_PASSWORD
            
        return config
