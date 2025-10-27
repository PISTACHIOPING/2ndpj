# AI Tech Insights Platform

이 저장소는 n8n, Azure OpenAI, FastAPI, React를 사용해 기술 뉴스 요약 및 분석 리포트를 자동화하는 시스템의 모노레포 구조입니다.

## 디렉터리
- `backend/` – FastAPI 애플리케이션, Celery 작업자, 데이터베이스 마이그레이션.
- `frontend/` – React 대시보드(Vite + TypeScript).
- `infra/` – Docker Compose, IaC 템플릿, 배포 스크립트.
- `docs/` – 아키텍처 및 운영 문서.

## 주요 기능 계획
1. n8n이 기술/AI 뉴스 소스를 주기적으로 수집하고 OpenAI로 요약·분석.
2. FastAPI가 기사 저장, 키워드 통계, 일일/주간 리포트 API를 제공.
3. React 대시보드가 카테고리별 요약과 키워드 트렌드를 시각화.
4. Slack/이메일 알림으로 주요 인사이트 전달.

## 빠른 시작
1. `python -m venv .venv` 후 `pip install -r backend/requirements.txt`
2. `npm install` (frontend) 및 `npm run dev`
3. `docker compose -f infra/docker-compose.yaml up` (선택)

상세한 실행 순서는 `docs/system-architecture.md`를 참고하세요.

