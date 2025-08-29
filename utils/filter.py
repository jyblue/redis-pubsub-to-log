"""
메시지 필터링 유틸리티 모듈
"""
import json
import fnmatch
from typing import Dict, Any, Optional
from config import Config


class MessageFilter:
    """메시지 필터링 클래스"""
    
    def __init__(self, file_filter_condition: str = None):
        self.file_filter_condition = file_filter_condition or Config.FILE_FILTER_CONDITION
    
    def should_process_message(self, message_data: Dict[str, Any]) -> bool:
        """
        메시지가 처리 조건을 만족하는지 확인합니다.
        
        Args:
            message_data: JSON 메시지 데이터
            
        Returns:
            bool: 처리 여부
        """
        # file 필드가 없으면 처리하지 않음
        if 'file' not in message_data:
            return False
        
        file_value = message_data['file']
        
        # 파일명이 문자열이 아니면 처리하지 않음
        if not isinstance(file_value, str):
            return False
        
        # 파일 필터 조건과 매치되는지 확인
        return fnmatch.fnmatch(file_value, self.file_filter_condition)
    
    def extract_key_value(self, message_data: Dict[str, Any]) -> Optional[str]:
        """
        JSON 데이터에서 키 값을 추출합니다.
        
        Args:
            message_data: JSON 메시지 데이터
            
        Returns:
            str: 키 값 (없으면 None)
        """
        key_field = Config.KEY_FIELD
        
        if key_field not in message_data:
            return None
        
        key_value = message_data[key_field]
        
        # 키 값이 문자열이 아니면 문자열로 변환
        if not isinstance(key_value, str):
            key_value = str(key_value)
        
        return key_value
    
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
