#!/bin/bash

# Docker 실행 스크립트
# Ubuntu 20.04/22.04 환경에서 Redis PubSub 로깅 시스템을 Docker로 실행

set -e

echo "=== Redis PubSub 로깅 시스템 Docker 실행 ==="

# Docker 및 Docker Compose 설치 확인
if ! command -v docker &> /dev/null; then
    echo "Docker가 설치되지 않았습니다. 설치를 진행합니다..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    echo "Docker 설치 완료. 로그아웃 후 다시 로그인해주세요."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose가 설치되지 않았습니다. 설치를 진행합니다..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# 로그 디렉토리 생성
mkdir -p logs message

# Docker Compose로 서비스 시작
echo "Redis 서버 및 로깅 시스템을 시작합니다..."
docker-compose up --build -d

echo "서비스가 시작되었습니다."
echo "Redis 서버: localhost:6379"
echo "로그 파일: ./logs/ 및 ./message/ 디렉토리"
echo ""
echo "서비스 상태 확인: docker-compose ps"
echo "로그 확인: docker-compose logs -f redis-logger"
echo "서비스 중지: docker-compose down"
