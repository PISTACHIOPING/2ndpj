# AI 기술 동향 뉴스 요약 및 분석 시스템

## 전체 구조
- **수집 계층**: n8n 워크플로우가 RSS/웹 API에서 기사 수집, 중복 제거, Azure OpenAI를 사용한 요약·분석을 담당합니다.
- **백엔드 API**: FastAPI가 기사 데이터 저장과 요약 리포트 집계를 제공하며, PostgreSQL/Redis가 상태를 유지합니다.
- **프론트엔드**: React 대시보드가 카테고리별 요약, 키워드 트렌드, 검색/필터 기능을 제공합니다.
- **알림/리포트**: Slack/이메일로 일일·주간 리포트를 발송합니다.

## 데이터 플로우
1. n8n Cron 트리거 → RSS/HTTP Request 노드로 기사 메타데이터 수집.
2. Function 노드에서 중복 필터링 후 Azure OpenAI로 요약/토픽/키워드 생성.
3. FastAPI `/articles` 엔드포인트에 배치 업로드하여 PostgreSQL에 저장.
4. FastAPI 백그라운드 작업이 키워드 통계·기간별 리포트를 집계해 Redis/DB에 저장.
5. React 대시보드가 FastAPI에서 데이터를 조회하고 시각화하며, 중요 이벤트는 Slack/이메일로 통지.

## 핵심 컴포넌트
- **n8n**: Cron Trigger, RSS Feed Read, HTTP Request, Azure OpenAI, Function, IF, Slack 노드.
- **Azure OpenAI**: `gpt-4o-mini` 기반 커스텀 프롬프트로 요약/분석/카테고리 분류.
- **FastAPI**: SQLModel 기반 모델, Pydantic Settings, Celery+Redis, JWT 인증.
- **React**: Vite+TypeScript, Zustand/RTK Query, Recharts, Tailwind CSS.
- **인프라**: Docker Compose(backend, frontend, n8n, postgres, redis), GitHub Actions CI, Azure Container Apps 배포 예시.

## 향후 고려 사항
- 기사 소스 확장(RSS 외 GraphQL/REST API)
- 다국어 기사 지원을 위한 언어 감지/번역
- 사용자 맞춤형 알림(관심 키워드 지정)
- 데이터 품질 모니터링 및 프롬프트 버전 관리

