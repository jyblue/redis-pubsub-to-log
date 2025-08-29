"""
Redis 서비스 모듈
"""
import redis
import time
import threading
from typing import Callable, Optional
from config import Config
from utils.logger import Logger


class RedisService:
    """Redis 연결 및 PubSub 관리 클래스"""
    
    def __init__(self):
        self.redis_client = None
        self.pubsub = None
        self.logger = Logger('RedisService')
        self.config = Config()
        self.heartbeat_thread = None
        self.last_message_time = time.time()
        self.running = False
        self.reconnect_attempts = 0
        self._connect()
    
    def _connect(self):
        """Redis에 연결합니다."""
        try:
            config = Config()
            self.redis_client = redis.Redis(**config.get_redis_config())
            self.pubsub = self.redis_client.pubsub()
            self.logger.info(f"Redis 연결 성공: {config.REDIS_HOST}:{config.REDIS_PORT}")
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
            self.running = True
            self.logger.info("메시지 수신 대기 중...")
            
            # Heartbeat 스레드 시작
            if self.config.HEARTBEAT_ENABLED:
                self._start_heartbeat()
            
            for message in self.pubsub.listen():
                if message['type'] == 'pmessage':
                    channel = message['channel'].decode('utf-8')
                    data = message['data'].decode('utf-8')
                    
                    # 마지막 메시지 수신 시간 업데이트
                    self.last_message_time = time.time()
                    
                    self.logger.debug(f"메시지 수신: 채널={channel}, 데이터={data}")
                    
                    # 메시지 핸들러 호출
                    message_handler(channel, data)
                    
        except redis.ConnectionError as e:
            self.logger.error(f"Redis 연결 오류: {str(e)}")
            self._reconnect()
        except Exception as e:
            self.logger.error(f"메시지 수신 중 오류: {str(e)}")
            raise
        finally:
            self.running = False
            if self.heartbeat_thread:
                self.heartbeat_thread.join()
    
    def _reconnect(self):
        """Redis 재연결을 시도합니다."""
        self.reconnect_attempts += 1
        self.logger.info(f"Redis 재연결 시도 중... (시도 {self.reconnect_attempts})")
        
        try:
            if self.pubsub:
                self.pubsub.close()
            
            if self.redis_client:
                self.redis_client.close()
            
            # Exponential backoff 적용
            delay = self._calculate_backoff_delay()
            self.logger.info(f"재연결 대기 시간: {delay:.2f}초")
            time.sleep(delay)
            
            self._connect()
            self.subscribe_all_channels()
            
            # 재연결 성공 시 카운터 리셋
            self.reconnect_attempts = 0
            self.logger.info("Redis 재연결 성공")
        except Exception as e:
            self.logger.error(f"Redis 재연결 실패: {str(e)}")
            raise
    
    def _calculate_backoff_delay(self) -> float:
        """Exponential backoff 지연 시간을 계산합니다."""
        # Exponential backoff 공식: base_delay * (multiplier ^ (attempt - 1))
        delay = self.config.REDIS_EXPONENTIAL_BACKOFF_BASE_DELAY * (
            self.config.REDIS_EXPONENTIAL_BACKOFF_MULTIPLIER ** (self.reconnect_attempts - 1)
        )
        
        # 최대 지연 시간 제한
        max_delay = self.config.REDIS_EXPONENTIAL_BACKOFF_MAX_DELAY
        return min(delay, max_delay)
    
    def _start_heartbeat(self):
        """Heartbeat 스레드를 시작합니다."""
        self.heartbeat_thread = threading.Thread(target=self._heartbeat_worker, daemon=True)
        self.heartbeat_thread.start()
    
    def _heartbeat_worker(self):
        """Heartbeat 워커 스레드입니다."""
        while self.running:
            try:
                time.sleep(self.config.HEARTBEAT_INTERVAL_SECONDS)
                
                if not self.running:
                    break
                
                # 마지막 메시지 수신 후 경과 시간 계산
                elapsed_time = time.time() - self.last_message_time
                
                # 설정된 간격보다 오래 메시지가 없으면 heartbeat 메시지 출력
                if elapsed_time >= self.config.HEARTBEAT_INTERVAL_SECONDS:
                    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 메시지 수신 대기 중...")
                    
            except Exception as e:
                self.logger.error(f"Heartbeat 스레드 오류: {str(e)}")
                break
    

    
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
