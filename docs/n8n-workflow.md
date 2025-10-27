# n8n 워크플로우 개요

## 주요 노드와 흐름
1. **Cron Trigger** – 매일 07:00 (서울 시간) 실행.
2. **RSS Feed Read** – 지정된 기술/AI 뉴스 RSS를 순회해 새 게시물 목록 수집.
3. **Merge → Function 노드** – 기사 URL 해시 기반으로 중복 제거. PostgreSQL API(`/articles` GET)로 이미 수집된 URL인지 확인.
4. **HTTP Request(원문 수집)** – Mercury Parser API 또는 각 사이트 전용 API 호출로 본문 추출.
5. **Azure OpenAI Chat Completion** – 요약/영향/카테고리/키워드를 JSON 포맷으로 생성.
6. **IF (중요 기사 여부)** – 영향 점수 또는 특수 키워드 포함 시 Slack 노드로 알림 전송.
7. **HTTP Request(FastAPI)** – `/articles` 엔드포인트로 일괄 업로드.
8. **Set → Item Lists** – Slack/Email 리포트용 텍스트 생성 후 메일 전송.

## Azure OpenAI 프롬프트 예시
```json
{
  "role": "system",
  "content": [
    {
      "type": "text",
      "text": "You are an analyst who summarizes AI and technology news for consultants."
    }
  ]
},
{
  "role": "user",
  "content": [
    {
      "type": "text",
      "text": "기사 제목: {{$json.title}}\n기사 본문: {{$json.content}}\n\n아래 JSON 스키마로 응답하세요:\n{\n  \"summary\": \"핵심 요약(최대 3문장)\",\n  \"impact\": \"업계 영향 분석(최대 2문장)\",\n  \"category\": \"AI 연구|제품 출시|산업 동향|정책 규제|기타 중 하나\",\n  \"importance_score\": 1-5,\n  \"keywords\": [\"핵심 키워드\", \"기업/기술명\"],\n  \"quote\": \"원문에서 중요한 문장 1개\"\n}"
    }
  ]
}
```

## HTTP Request(FastAPI) 설정
- **Method**: `POST`
- **URL**: `{{ $env.FASTAPI_BASE_URL }}/articles`
- **Headers**: `Content-Type: application/json`, `X-API-Key: {{$env.API_KEY}}`
- **Body**:
```json
{
  "articles": [
    {
      "title": "{{$json.title}}",
      "url": "{{$json.link}}",
      "source": "{{$json.source}}",
      "category": "{{$json.ai.category}}",
      "summary": "{{$json.ai.summary}}",
      "impact": "{{$json.ai.impact}}",
      "keywords": "={{$json.ai.keywords}}",
      "published_at": "={{$json.pubDate}}"
    }
  ]
}
```

## Slack 알림 메시지 템플릿
```
:rotating_light: *중요 AI 뉴스 감지*
- 제목: {{$json.title}}
- 요약: {{$json.ai.summary}}
- 영향: {{$json.ai.impact}}
- 원문: {{$json.link}}
```

## 운영 체크포인트
- 워크플로우가 실패하면 Error Trigger로 Slack/Email 알림.
- OpenAI 호출 실패 시 3회 재시도, 실패 건은 Dead Letter(별도 Airtable/Notion)로 기록.
- 기사 처리량이 많을 때는 `SplitInBatches` 노드 사용(예: 10건씩 POST).
