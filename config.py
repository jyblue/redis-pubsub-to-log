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
            default=os.getenv('APP_CONFIG', 'config/default.json'),
            help='설정 파일 경로 (기본값: config/default.json, 환경변수 APP_CONFIG로 재정의 가능)'
        )
        
        args, _ = parser.parse_known_args()
        
        try:
            config_path = self._resolve_config_path(args.config)
            with open(config_path, 'r', encoding='utf-8') as f:
                self._config_data = json.load(f)
            # 환경변수 값으로 설정 재정의
            self._apply_env_overrides()
        except FileNotFoundError:
            print(f"오류: 설정 파일을 찾을 수 없습니다: {args.config}")
            print("애플리케이션을 종료합니다.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"오류: 설정 파일 JSON 파싱 오류: {e}")
            print("애플리케이션을 종료합니다.")
            sys.exit(1)
    
    def _resolve_config_path(self, path_str: str) -> str:
        """상대 경로 구성파일을 안전하게 탐색하여 실제 경로를 반환합니다."""
        if os.path.isabs(path_str) and os.path.exists(path_str):
            return path_str
        candidates = []
        cwd = os.getcwd()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        candidates.append(os.path.join(cwd, path_str))
        if script_dir != cwd:
            candidates.append(os.path.join(script_dir, path_str))
        for candidate in candidates:
            if os.path.exists(candidate):
                return candidate
        # 존재하지 않으면 원본을 반환하여 상위에서 일관 처리
        return path_str

    def _parse_bool_env(self, value: str) -> bool:
        return str(value).strip().lower() in ('1', 'true', 'yes', 'y', 'on')

    def _apply_env_overrides(self):
        """환경변수로 설정 값을 재정의합니다."""
        if not isinstance(self._config_data, dict):
            return
        # 보장
        self._config_data.setdefault('redis', {})
        self._config_data.setdefault('logging', {})
        self._config_data.setdefault('heartbeat', {})
        env_map = {
            'redis': {
                'host': ('REDIS_HOST', str),
                'port': ('REDIS_PORT', int),
                'db': ('REDIS_DB', int),
                'password': ('REDIS_PASSWORD', str),
                'retry_on_timeout': ('REDIS_RETRY_ON_TIMEOUT', self._parse_bool_env),
                'retry_on_error': ('REDIS_RETRY_ON_ERROR', self._parse_bool_env),
                'retry': ('REDIS_RETRY', int),
            },
            'logging': {
                'log_dir': ('LOG_DIR', str),
                'message_log_dir': ('MESSAGE_LOG_DIR', str),
                'log_file_size_mb': ('LOG_FILE_SIZE_MB', int),
                'log_backup_count': ('LOG_BACKUP_COUNT', int),
            },
            'heartbeat': {
                'enabled': ('HEARTBEAT_ENABLED', self._parse_bool_env),
                'interval_seconds': ('HEARTBEAT_INTERVAL_SECONDS', int),
            },
        }
        for section, mappings in env_map.items():
            for key, (env_key, caster) in mappings.items():
                raw = os.getenv(env_key)
                if raw is not None:
                    try:
                        self._config_data[section][key] = caster(raw)
                    except Exception:
                        # 변환 실패 시 무시
                        pass

    
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
        value = self._get_nested_value('logging', 'log_dir')
        return self._resolve_path(value)
    
    @property
    def MESSAGE_LOG_DIR(self) -> str:
        value = self._get_nested_value('logging', 'message_log_dir')
        return self._resolve_path(value)
    
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

    def _resolve_path(self, path_str: str) -> str:
        """절대 경로로 변환하고 OS 간 호환되도록 정규화합니다.

        APP_BASE_DIR 환경변수를 기반으로 상대경로를 절대경로로 변환합니다.
        지정되지 않으면 현재 작업 디렉토리를 기준으로 합니다.
        """
        if path_str is None:
            return None
        if os.path.isabs(path_str):
            return os.path.normpath(path_str)
        base_dir = os.getenv('APP_BASE_DIR', os.getcwd())
        return os.path.normpath(os.path.join(base_dir, path_str))
