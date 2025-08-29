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

## PROMPT-003
**명령**: fnmatch에 대해 설명하세요.

**수행 작업**:
- fnmatch 모듈의 기능과 사용법 설명
- 현재 프로젝트에서의 활용 사례 설명

## PROMPT-004
**명령**: file_filter_condition 항목을 수정하세요. filtering 로직은 다음과 같은 형식 입니다. "target" 이라는 필드의 값이 "STATUS"인 경우, "target"이라는 필드의 값이 "EVENT"인 경우 등입니다.

**수행 작업**:
- file_filter_condition을 target 필드 기반 필터링으로 변경
- 필터링 로직을 fnmatch에서 특정 필드 값 비교로 수정
- 설정 파일 구조 업데이트

## PROMPT-005
**명령**: config 기본 값을 반환하는 하드코딩 함수를 삭제하세요. config file이 없는 경우 에러 메시지를 출력하고 어플리케이션이 종료되어야 합니다.

**수행 작업**:
- _get_default_config 함수 삭제
- 설정 파일이 없을 때 에러 메시지 출력 후 애플리케이션 종료
- 기본값 하드코딩 제거
