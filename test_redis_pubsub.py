#!/usr/bin/env python3
"""
Redis PubSub 테스트 스크립트
"""
import json
import time
import redis
from config import Config


def test_redis_pubsub():
    """Redis PubSub 테스트"""
    try:
        # Redis 연결
        config = Config()
        r = redis.Redis(**config.get_redis_config())
        
        print("Redis PubSub 테스트 시작...")
        print(f"Redis 서버: {config.REDIS_HOST}:{config.REDIS_PORT}")
        
        # 테스트 메시지들
        test_messages = [
            {
                "id": "user123",
                "file": "app.log",
                "message": "첫 번째 테스트 메시지",
                "timestamp": "2024-01-01T12:00:00Z"
            },
            {
                "id": "user456",
                "file": "error.log",
                "message": "두 번째 테스트 메시지",
                "timestamp": "2024-01-01T12:01:00Z"
            },
            {
                "id": "user789",
                "file": "debug.log",
                "message": "세 번째 테스트 메시지",
                "timestamp": "2024-01-01T12:02:00Z"
            },
            {
                "id": "user999",
                "file": "access.txt",  # 필터링 조건 불만족
                "message": "필터링되지 않을 메시지",
                "timestamp": "2024-01-01T12:03:00Z"
            }
        ]
        
        # 각 채널에 메시지 발행 (Windows 폴더명 테스트 포함)
        channels = ["test_channel_1", "test:channel:2", "test_channel_3", "test\\channel\\4"]
        
        for i, message in enumerate(test_messages):
            channel = channels[i % len(channels)]
            json_message = json.dumps(message, ensure_ascii=False)
            
            r.publish(channel, json_message)
            print(f"메시지 발행: 채널={channel}, 메시지={json_message}")
            
            time.sleep(1)  # 1초 대기
        
        print("테스트 완료!")
        
    except Exception as e:
        print(f"테스트 중 오류 발생: {str(e)}")


if __name__ == "__main__":
    test_redis_pubsub()
