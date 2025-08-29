#!/usr/bin/env python3
"""
Redis PubSub 로깅 시스템 메인 모듈
"""
import signal
import sys
from services.redis_service import RedisService
from services.message_service import MessageService
from utils.logger import Logger


class RedisPubSubLogger:
    """Redis PubSub 로깅 시스템 메인 클래스"""
    
    def __init__(self):
        self.logger = Logger('Main')
        self.redis_service = None
        self.message_service = None
        self.running = False
        
        # 시그널 핸들러 설정
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def start(self):
        """애플리케이션을 시작합니다."""
        try:
            self.logger.info("Redis PubSub 로깅 시스템 시작")
            
            # 서비스 초기화
            self.redis_service = RedisService()
            self.message_service = MessageService()
            
            # 모든 채널 구독
            self.redis_service.subscribe_all_channels()
            
            self.running = True
            
            # 메시지 수신 시작
            self.redis_service.listen_messages(self._handle_message)
            
        except KeyboardInterrupt:
            self.logger.info("사용자에 의해 중단됨")
        except Exception as e:
            self.logger.error(f"애플리케이션 시작 중 오류: {str(e)}")
        finally:
            self.stop()
    
    def _handle_message(self, channel: str, message: str):
        """
        메시지 핸들러
        
        Args:
            channel: 채널명
            message: 메시지 데이터
        """
        if self.running:
            self.message_service.process_message(channel, message)
    
    def _signal_handler(self, signum, frame):
        """시그널 핸들러"""
        self.logger.info(f"시그널 {signum} 수신, 종료 중...")
        self.stop()
        sys.exit(0)
    
    def stop(self):
        """애플리케이션을 종료합니다."""
        self.running = False
        
        if self.redis_service:
            self.redis_service.close()
        
        self.logger.info("Redis PubSub 로깅 시스템 종료")


def main():
    """메인 함수"""
    app = RedisPubSubLogger()
    app.start()


if __name__ == "__main__":
    main()
