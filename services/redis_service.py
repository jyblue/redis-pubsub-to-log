"""
Redis 서비스 모듈
"""
import redis
import time
from typing import Callable, Optional
from config import Config
from utils.logger import Logger


class RedisService:
    """Redis 연결 및 PubSub 관리 클래스"""
    
    def __init__(self):
        self.redis_client = None
        self.pubsub = None
        self.logger = Logger('RedisService')
        self._connect()
    
    def _connect(self):
        """Redis에 연결합니다."""
        try:
            self.redis_client = redis.Redis(**Config.get_redis_config())
            self.pubsub = self.redis_client.pubsub()
            self.logger.info(f"Redis 연결 성공: {Config.REDIS_HOST}:{Config.REDIS_PORT}")
        except Exception as e:
            self.logger.error(f"Redis 연결 실패: {str(e)}")
            raise
    
    def subscribe_all_channels(self):
        """모든 채널을 구독합니다."""
        try:
            # 모든 채널 패턴으로 구독
            self.pubsub.psubscribe('*')
            self.logger.info("모든 채널 구독 시작")
        except Exception as e:
            self.logger.error(f"채널 구독 실패: {str(e)}")
            raise
    
    def listen_messages(self, message_handler: Callable):
        """
        메시지를 수신하고 처리합니다.
        
        Args:
            message_handler: 메시지 처리 함수
        """
        try:
            self.logger.info("메시지 수신 대기 중...")
            
            for message in self.pubsub.listen():
                if message['type'] == 'pmessage':
                    channel = message['channel'].decode('utf-8')
                    data = message['data'].decode('utf-8')
                    
                    self.logger.debug(f"메시지 수신: 채널={channel}, 데이터={data}")
                    
                    # 메시지 핸들러 호출
                    message_handler(channel, data)
                    
        except redis.ConnectionError as e:
            self.logger.error(f"Redis 연결 오류: {str(e)}")
            self._reconnect()
        except Exception as e:
            self.logger.error(f"메시지 수신 중 오류: {str(e)}")
            raise
    
    def _reconnect(self):
        """Redis 재연결을 시도합니다."""
        self.logger.info("Redis 재연결 시도 중...")
        
        try:
            if self.pubsub:
                self.pubsub.close()
            
            if self.redis_client:
                self.redis_client.close()
            
            time.sleep(1)  # 잠시 대기
            self._connect()
            self.subscribe_all_channels()
            
            self.logger.info("Redis 재연결 성공")
        except Exception as e:
            self.logger.error(f"Redis 재연결 실패: {str(e)}")
            raise
    
    def close(self):
        """Redis 연결을 종료합니다."""
        try:
            if self.pubsub:
                self.pubsub.close()
            
            if self.redis_client:
                self.redis_client.close()
                
            self.logger.info("Redis 연결 종료")
        except Exception as e:
            self.logger.error(f"Redis 연결 종료 중 오류: {str(e)}")
