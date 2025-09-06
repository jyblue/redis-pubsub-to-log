#!/bin/bash

# Docker 테스트 스크립트
# Redis PubSub 테스트 메시지 발송

set -e

echo "=== Redis PubSub 테스트 메시지 발송 ==="

# Docker Compose로 테스트 실행
echo "테스트 메시지를 발송합니다..."
docker-compose --profile test run --rm redis-test

echo "테스트 완료. 로그를 확인하세요:"
echo "docker-compose logs -f redis-logger"
