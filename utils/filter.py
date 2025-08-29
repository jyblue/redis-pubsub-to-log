"""
메시지 필터링 유틸리티 모듈
"""
import json
import re
from typing import Dict, Any, Optional, List, Union
from config import Config


class MessageFilter:
    """메시지 필터링 클래스"""
    
    def __init__(self, target_field: str = None, target_values: List[str] = None, use_regex: bool = None):
        self.config = Config()
        self.target_field = target_field or self.config.TARGET_FIELD
        self.target_values = target_values or self.config.TARGET_VALUES
        self.use_regex = use_regex if use_regex is not None else self.config.USE_REGEX
    
    def should_process_message(self, message_data: Dict[str, Any]) -> bool:
        """
        메시지가 처리 조건을 만족하는지 확인합니다.
        
        Args:
            message_data: JSON 메시지 데이터
            
        Returns:
            bool: 처리 여부
        """
        # target 필드가 없으면 처리하지 않음
        if self.target_field not in message_data:
            return False
        
        target_value = message_data[self.target_field]
        
        # target 값이 문자열이 아니면 처리하지 않음
        if not isinstance(target_value, str):
            return False
        
        # 정규 표현식 또는 일반 문자열 매칭으로 확인
        return self._matches_target_values(target_value)
    
    def _matches_target_values(self, target_value: str) -> bool:
        """
        target 값이 설정된 값들과 일치하는지 확인합니다.
        
        Args:
            target_value: 확인할 target 값
            
        Returns:
            bool: 일치 여부
        """
        if self.use_regex:
            # 정규 표현식 매칭
            for pattern in self.target_values:
                try:
                    if re.match(pattern, target_value):
                        return True
                except re.error as e:
                    # 잘못된 정규 표현식은 무시하고 로그 출력
                    print(f"경고: 잘못된 정규 표현식 '{pattern}': {e}")
                    continue
            return False
        else:
            # 일반 문자열 매칭
            return target_value in self.target_values
    
    def extract_key_value(self, message_data: Dict[str, Any]) -> Optional[str]:
        """
        JSON 데이터에서 키 값을 추출합니다.
        
        Args:
            message_data: JSON 메시지 데이터
            
        Returns:
            str: 키 값 (없으면 None)
        """
        key_field = self.config.KEY_FIELD
        
        if key_field not in message_data:
            return None
        
        key_value = message_data[key_field]
        
        # 키 값이 문자열이 아니면 문자열로 변환
        if not isinstance(key_value, str):
            key_value = str(key_value)
        
        return key_value
    
    def sanitize_folder_name(self, name: str) -> str:
        """
        폴더명으로 사용할 수 없는 문자를 '_'로 대체합니다.
        
        Args:
            name: 원본 이름
            
        Returns:
            str: 폴더명으로 사용 가능한 이름
        """
        # Windows에서 폴더명으로 사용할 수 없는 문자들
        invalid_chars = r'[<>:"/\\|?*]'
        return re.sub(invalid_chars, '_', name)
    
    def parse_message(self, message: str) -> Optional[Dict[str, Any]]:
        """
        메시지를 JSON으로 파싱합니다.
        
        Args:
            message: 원본 메시지
            
        Returns:
            Dict: 파싱된 JSON 데이터 (실패시 None)
        """
        try:
            return json.loads(message)
        except json.JSONDecodeError:
            return None
