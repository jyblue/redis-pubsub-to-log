# Redis PubSub 로깅 시스템

Redis PubSub 서버에 접속하여 모든 채널을 구독하고, publish되는 메시지를 필터링하여 로그로 출력하는 Python 애플리케이션입니다.

## 주요 기능

- Redis PubSub 서버 연결 및 모든 채널 구독
- JSON 형태의 publish 메시지 파싱 및 필터링
- 채널명/키 값 기반 폴더 구조로 로그 저장
- 10MB 단위 로그 파일 Rolling
- 콘솔 및 파일 동시 로깅
- Redis 연결 재시도 및 백오프 설정
- 클린 아키텍처 기반 설계

## 프로젝트 구조

```
redis-pubsub-to-log/
├── config.py              # 설정 관리
├── main.py                # 메인 애플리케이션
├── requirements.txt       # Python 의존성
├── README.md             # 프로젝트 문서
├── utils/                # 유틸리티 모듈
│   ├── __init__.py
│   ├── logger.py         # 로깅 유틸리티
│   └── filter.py         # 메시지 필터링
└── services/             # 서비스 모듈
    ├── __init__.py
    ├── redis_service.py  # Redis 연결 및 PubSub
    └── message_service.py # 메시지 처리 및 로깅
```

## 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정 (선택사항)

```bash
export REDIS_HOST=localhost
export REDIS_PORT=6379
export REDIS_DB=0
export REDIS_PASSWORD=your_password
export LOG_DIR=logs
export FILE_FILTER_CONDITION="*.log"
export KEY_FIELD=id
```

### 3. 애플리케이션 실행

```bash
python main.py
```

## 설정

### 기본 설정 (config.py)

- **Redis 설정**: 호스트, 포트, DB, 비밀번호
- **연결 재시도**: 타임아웃 및 오류 시 재시도 설정
- **로깅 설정**: 로그 디렉토리, 파일 크기, 백업 개수
- **필터링 설정**: 파일 필터 조건, 키 필드명

### 환경 변수

| 변수명 | 기본값 | 설명 |
|--------|--------|------|
| REDIS_HOST | localhost | Redis 서버 호스트 |
| REDIS_PORT | 6379 | Redis 서버 포트 |
| REDIS_DB | 0 | Redis 데이터베이스 번호 |
| REDIS_PASSWORD | None | Redis 비밀번호 |
| LOG_DIR | logs | 로그 저장 디렉토리 |
| FILE_FILTER_CONDITION | *.log | 파일 필터 조건 |
| KEY_FIELD | id | JSON에서 폴더명으로 사용할 필드 |

## 메시지 형식

### 입력 메시지 (JSON)

```json
{
  "id": "user123",
  "file": "app.log",
  "message": "로그 메시지",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### 로그 출력 구조

```
logs/
├── channel1/
│   └── user123/
│       └── messages.log
└── channel2/
    └── user456/
        └── messages.log
```

### 로그 파일 내용

```json
{
  "timestamp": "2024-01-01 12:00:00",
  "channel": "channel1",
  "key": "user123",
  "message": {
    "id": "user123",
    "file": "app.log",
    "message": "로그 메시지",
    "timestamp": "2024-01-01T12:00:00Z"
  }
}
```

## 필터링 조건

- `file` 필드가 존재해야 함
- `file` 값이 `FILE_FILTER_CONDITION` 패턴과 일치해야 함
- `KEY_FIELD`로 지정된 필드가 존재해야 함

## 로그 Rolling

- 로그 파일 크기가 10MB에 도달하면 자동으로 새 파일 생성
- 최대 5개의 백업 파일 유지
- 파일명 형식: `messages.log`, `messages.log.1`, `messages.log.2`, ...

## Redis 연결 안정성

- 연결 타임아웃 시 자동 재연결
- 오류 발생 시 백오프 전략으로 재시도
- 연결 끊김 감지 및 복구

## 개발 가이드

### 클린 아키텍처 원칙

1. **의존성 역전**: 고수준 모듈이 저수준 모듈에 의존하지 않음
2. **단일 책임**: 각 클래스는 하나의 책임만 가짐
3. **개방-폐쇄**: 확장에는 열려있고 수정에는 닫혀있음
4. **인터페이스 분리**: 클라이언트는 사용하지 않는 인터페이스에 의존하지 않음

### 코드 구조

- **Config**: 설정 관리
- **Logger**: 로깅 기능
- **MessageFilter**: 메시지 필터링
- **RedisService**: Redis 연결 및 PubSub
- **MessageService**: 메시지 처리 및 로깅

## 라이선스

MIT License
