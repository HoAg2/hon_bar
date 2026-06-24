# Conventions

## Git Commit Tags

| 태그 | 용도 |
|------|------|
| `[feat]` | 새로운 기능 추가 |
| `[fix]` | 버그 수정 |
| `[docs]` | 문서 추가/수정 |
| `[refactor]` | 기능 변경 없는 코드 개선 |
| `[chore]` | 빌드, 설정, 패키지 등 |
| `[style]` | 포맷, 린트 등 스타일 수정 |

예시: `[feat] add user CRUD endpoints`

---

## 프로젝트 구조

```
fast_api_study/
├── apps/
│   ├── backend/        # FastAPI
│   └── frontend/       # Next.js
├── docs/               # 컨벤션, 학습 기록
└── docker-compose.yml
```

---

## Backend 컨벤션

### 파일/폴더 네이밍
- 파일명: `snake_case.py`
- 라우터: `apps/backend/routers/` 하위에 도메인별로 분리
- 모델: `apps/backend/models/` 하위

### API 엔드포인트
- RESTful 네이밍: `/users`, `/users/{id}`
- HTTP 메서드: `GET` 조회, `POST` 생성, `PUT` 전체 수정, `PATCH` 부분 수정, `DELETE` 삭제

### Pydantic 스키마
- Request/Response 스키마 분리
- 예시: `UserCreate`, `UserUpdate`, `UserResponse`

---

## Frontend 컨벤션

### 파일/폴더 네이밍
- 컴포넌트: `PascalCase.tsx`
- 훅: `useCamelCase.ts`
- 유틸: `camelCase.ts`

### API 호출
- `apps/frontend/src/lib/api.ts`에서 중앙 관리
- FastAPI의 `/openapi.json` 기반으로 타입 자동 생성 예정
