# 설정 페이지 요건 정의 질문 리스트

## 1. 기본 정보
- 설정 페이지의 목적은 무엇인가요? (예: 사용자 환경설정, 네트워크, UI, 검사 파라미터 등)
  - 사용자 환경 설정
  - Telnet통신 설정 및 테스트
  - 검사 파라메터 지정
  - 검사 파라메터, 검사 결과 관리
- 설정 변경이 즉시 적용되어야 하나요, 아니면 저장 후 적용되나요?
  - 적용 버튼을 통해서 적용
  - 저장 버튼을 통해서 저장 및 읽어오기 
## 2. 설정 항목
- 어떤 항목(카테고리)이 필요합니까? (예: 네트워크, UI, 언어, 로그, 검사 파라미터 등)
  - Telnet 연결 및 조건 지정
  - 검사 파라메터
  - Congex In-Sight navtive command 지정
- 각 항목별로 구체적으로 어떤 설정값이 필요한가요? (예: 서버 주소, 포트, 테마, 언어, 로그 레벨 등)
  - Telnet 서버 주소, 포트
  - 검사 파라메터
- 각 설정값의 기본값/허용값/유효성 조건은 무엇인가요?
  

## 3. UI/UX
- 설정 페이지는 별도 창, 탭, 패널 등 어떤 형태로 제공되길 원하나요?
  - 3분할, 좌측 1분할은 Telnet통신 지정, 통신데이터 지정, 통신 Log
  - 나머지는 나중에 지정
- 설정값 입력 방식(텍스트, 드롭다운, 체크박스 등)은 어떻게 되나요?
  - 항목에 따라 달라짐
  - 그리드 형태
  - 체크 박스 
- 설정값 변경 시 사용자에게 어떤 피드백(저장 성공/실패, 경고 등)을 제공해야 하나요?
  - 성공/실패

## 4. 저장/적용
- 설정값은 어디에 저장되나요? (예: config 파일, DB, 레지스트리 등)
   - CSV파일
   - 폴터 및 파일명 지정 기능 필요
- 저장/적용/초기화(리셋) 버튼이 필요한가요?
   - 필요
- 설정값을 불러오기/초기화하는 기능이 필요한가요?
   - 필용

## 5. 보안/권한
- 설정 페이지 접근에 권한 제한이 필요한가요? (예: 관리자만 접근)
   - 없음
- 민감 정보(비밀번호 등)는 어떻게 처리해야 하나요?
   - 없음

## 6. 확장성/유지보수
- 추후 설정 항목이 추가될 가능성이 있나요?
  - 있음
- 다국어(언어) 지원이 필요한가요?
  - 한국어, 영어 선택, 기본은 한국어

## 7. 기타
- 설정 변경 시 로그 기록이 필요한가요?
  - 필요
- 설정값 변경 이력(History) 관리가 필요한가요?
  - 필요
- 기타 특별히 고려해야 할 사항이 있나요?
  Telnet통신에 구현에 순차적으로 천전히 진행해야 함.

화이팅! 