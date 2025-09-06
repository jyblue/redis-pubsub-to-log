#!/bin/bash

# Docker 모니터링 스크립트
# Redis PubSub 로깅 시스템 상태 모니터링

set -e

echo "=== Redis PubSub 로깅 시스템 모니터링 ==="

# 서비스 상태 확인
echo "1. 서비스 상태 확인"
docker-compose ps

echo ""
echo "2. Redis 서버 연결 테스트"
if docker-compose exec redis redis-cli ping; then
    echo "✅ Redis 서버 정상"
else
    echo "❌ Redis 서버 연결 실패"
fi

echo ""
echo "3. 로그 파일 확인"
echo "시스템 로그:"
ls -la logs/ 2>/dev/null || echo "로그 디렉토리가 없습니다."

echo ""
echo "메시지 로그:"
ls -la message/ 2>/dev/null || echo "메시지 로그 디렉토리가 없습니다."

echo ""
echo "4. 실시간 로그 모니터링 (Ctrl+C로 종료)"
echo "Redis 로거 로그:"
docker-compose logs -f redis-logger
