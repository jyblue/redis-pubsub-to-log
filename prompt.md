# Redis PubSub 로깅 시스템 개발 명령 기록

## PROMPT-001
**명령**: 지금 부터 입력되는 모든 명령을 prompt.md 파일을 생성하여 기록하세요. 각 명령에는 PROMPT-001 과 같이 번호를 순차적으로 중복 없이 생성하세요. 환경 설정은 json 파일로부터 입력 받고, json 파일은 실행 시점 cli argument로 입력 받도록 수정하세요. 기본 경로도 존재해야 합니다.

**수행 작업**:
- prompt.md 파일 생성
- 환경 설정을 JSON 파일로부터 입력받도록 수정
- CLI argument로 JSON 파일 경로 입력받도록 수정
- 기본 설정 파일 생성

## PROMPT-002
**명령**: redis 메시지가 저장되는 경로를 json 파일에 설정할 수 있도록 추가하세요. 기본 경로는 message/{channel_name}/{key_value} 입니다. 설정된 경로는 python script를 실행하는 디렉토리 위치와 상관 없이 항상 유지되어야 합니다.

**수행 작업**:
- JSON 설정 파일에 메시지 로그 경로 설정 추가
- 기본 경로를 message/{channel_name}/{key_value}로 변경
- 절대 경로 지원을 위한 설정 추가
