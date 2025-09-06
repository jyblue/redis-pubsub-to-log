#!/bin/bash

# Ubuntu 20.04/22.04 환경 설정 스크립트
# Redis PubSub 로깅 시스템을 위한 Docker 환경 구성

set -e

echo "=== Ubuntu 환경 Docker 설정 ==="

# Ubuntu 버전 확인
if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo "Ubuntu 버전: $VERSION"
else
    echo "Ubuntu 버전을 확인할 수 없습니다."
    exit 1
fi

# Docker 설치
echo "Docker 설치 확인 중..."
if ! command -v docker &> /dev/null; then
    echo "Docker를 설치합니다..."
    
    # 기존 Docker 제거
    sudo apt-get remove -y docker docker-engine docker.io containerd runc || true
    
    # Docker 저장소 추가
    sudo apt-get update
    sudo apt-get install -y \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    
    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Docker 설치
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    
    # 사용자를 docker 그룹에 추가
    sudo usermod -aG docker $USER
    
    echo "Docker 설치 완료!"
    echo "로그아웃 후 다시 로그인하여 docker 그룹 권한을 적용하세요."
else
    echo "Docker가 이미 설치되어 있습니다."
fi

# Docker Compose 설치 확인
echo "Docker Compose 설치 확인 중..."
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose를 설치합니다..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "Docker Compose 설치 완료!"
else
    echo "Docker Compose가 이미 설치되어 있습니다."
fi

# 방화벽 설정 (Redis 포트)
echo "방화벽 설정 중..."
if command -v ufw &> /dev/null; then
    sudo ufw allow 6379/tcp
    echo "Redis 포트(6379)가 방화벽에서 허용되었습니다."
fi

# 로그 디렉토리 생성
echo "로그 디렉토리 생성 중..."
mkdir -p logs message
chmod 755 logs message

echo "=== 설정 완료 ==="
echo "다음 단계:"
echo "1. 로그아웃 후 다시 로그인"
echo "2. ./docker-run.sh 실행"
