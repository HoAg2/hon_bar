# Architecture & ERD

## 1. 요구사항 정리

### 사용자 유형
- **Admin**: 홈바 주인. 로그인 필요. 재료/칵테일/위스키 관리 + 주문 확인
- **Guest**: 친구들. 로그인 없음. 취향 선택 → 추천 → 주문

### 핵심 비즈니스 로직
- 필수 재료가 모두 `is_available = true`인 칵테일만 Guest에게 노출
- 선택 재료(garnish 등)는 없어도 노출 가능
- 추천은 규칙 기반으로 시작, 추후 AI 교체 가능하도록 service layer 분리

---

## 2. DB 선택

**PostgreSQL** (Docker로 이미 구성됨)
- 실무와 동일한 환경에서 학습 가능
- SQLite보다 JSON 필드, 인덱스 등 학습 범위가 넓음

---

## 3. ERD

```
ingredients
─────────────────────────────
id              UUID PK
name            VARCHAR
category        ENUM (base_spirit | liqueur | juice | soda | syrup | fruit | garnish | bitter | dairy | etc)
quantity        FLOAT
unit            VARCHAR
is_available    BOOLEAN
memo            TEXT
created_at      TIMESTAMP
updated_at      TIMESTAMP

cocktails
─────────────────────────────
id              UUID PK
name            VARCHAR
description     TEXT
image_url       VARCHAR
alcohol_level   ENUM (low | medium | high)
abv             FLOAT
base_spirit     VARCHAR
glass_type      ENUM (highball | coupe | rocks | martini | shot | wine | etc)
method          ENUM (build | shake | stir | blend)
sweetness       INT (1-5)
sourness        INT (1-5)
bitterness      INT (1-5)
body            INT (1-5)
freshness       INT (1-5)
garnish         VARCHAR (nullable)
is_active       BOOLEAN
created_at      TIMESTAMP
updated_at      TIMESTAMP

cocktail_ingredients
─────────────────────────────
id              UUID PK
cocktail_id     UUID FK → cocktails.id
ingredient_id   UUID FK → ingredients.id
amount          FLOAT
unit            VARCHAR
is_required     BOOLEAN

cocktail_steps
─────────────────────────────
id              UUID PK
cocktail_id     UUID FK → cocktails.id
step_order      INT
description     TEXT

whiskies
─────────────────────────────
id              UUID PK
name            VARCHAR
distillery      VARCHAR
region          ENUM (scotch | bourbon | irish | japanese | taiwan | islay | speyside | highland | etc)
abv             FLOAT
cask_type       ENUM (bourbon | sherry | wine | port | etc)
flavor_sherry   BOOLEAN
flavor_peat     BOOLEAN
flavor_smoke    BOOLEAN
flavor_vanilla  BOOLEAN
flavor_fruit    BOOLEAN
flavor_spice    BOOLEAN
flavor_oak      BOOLEAN
flavor_honey    BOOLEAN
finish          TEXT
description     TEXT
beginner_friendly BOOLEAN
is_available    BOOLEAN
image_url       VARCHAR
created_at      TIMESTAMP
updated_at      TIMESTAMP

orders
─────────────────────────────
id              UUID PK
order_type      ENUM (cocktail | whisky)
item_id         UUID
guest_name      VARCHAR
status          ENUM (requested | preparing | served | canceled)
memo            TEXT
created_at      TIMESTAMP

reviews
─────────────────────────────
id              UUID PK
item_type       ENUM (cocktail | whisky)
item_id         UUID
guest_name      VARCHAR
rating          INT (1-5)
content         TEXT
created_at      TIMESTAMP

memories
─────────────────────────────
id              UUID PK
guest_name      VARCHAR
theme           VARCHAR
content         TEXT
image_url       VARCHAR
is_public       BOOLEAN
created_at      TIMESTAMP
```

---

## 4. Backend 폴더 구조

```
apps/backend/
├── main.py
├── requirements.txt
├── .env
├── alembic.ini
├── alembic/
│   └── versions/
└── app/
    ├── core/
    │   ├── config.py        # pydantic-settings 환경변수
    │   ├── database.py      # SQLAlchemy engine, session
    │   └── security.py      # JWT 생성/검증
    ├── models/              # SQLAlchemy ORM 모델
    │   ├── ingredient.py
    │   ├── cocktail.py
    │   ├── whisky.py
    │   └── order.py
    ├── schemas/             # Pydantic Request/Response 스키마
    │   ├── ingredient.py
    │   ├── cocktail.py
    │   ├── whisky.py
    │   └── order.py
    ├── routers/
    │   ├── admin/
    │   │   ├── auth.py
    │   │   ├── ingredients.py
    │   │   ├── cocktails.py
    │   │   ├── whiskies.py
    │   │   └── orders.py
    │   └── public/
    │       ├── cocktails.py
    │       ├── whiskies.py
    │       ├── reviews.py
    │       └── memories.py
    ├── services/            # 비즈니스 로직 (AI 교체 가능하도록 분리)
    │   ├── availability.py  # 제조 가능 여부 판단
    │   └── recommendation.py # 취향 기반 추천 (규칙 → AI 교체 포인트)
    └── dependencies.py      # FastAPI Depends (auth, db session)
```

---

## 5. Frontend 폴더 구조

```
apps/frontend/
└── src/
    ├── app/
    │   ├── page.tsx                    # / 홈
    │   ├── cocktails/
    │   │   ├── recommend/page.tsx      # 취향 선택 → 추천
    │   │   └── [id]/page.tsx           # 칵테일 상세
    │   ├── whiskies/
    │   │   ├── recommend/page.tsx
    │   │   ├── beginner/page.tsx
    │   │   └── [id]/page.tsx
    │   ├── reviews/page.tsx
    │   ├── memories/page.tsx
    │   └── admin/
    │       ├── login/page.tsx
    │       ├── dashboard/page.tsx
    │       ├── ingredients/page.tsx
    │       ├── cocktails/page.tsx
    │       ├── whiskies/page.tsx
    │       └── orders/page.tsx
    ├── components/
    │   ├── ui/                         # shadcn/ui
    │   ├── cocktail/
    │   │   ├── CocktailCard.tsx
    │   │   └── TasteSelector.tsx
    │   ├── whisky/
    │   │   └── WhiskyCard.tsx
    │   └── admin/
    │       └── OrderDetail.tsx
    ├── lib/
    │   ├── api.ts                      # fetch wrapper (base URL, auth header)
    │   └── auth.ts                     # token 저장/읽기
    └── types/
        └── index.ts                    # API 응답 타입
```

---

## 6. MVP 범위

### In (1차)
- [ ] Admin 로그인 (JWT)
- [ ] 재료 CRUD
- [ ] 칵테일 CRUD (재료 연결 포함)
- [ ] 제조 가능 칵테일 목록 API
- [ ] 칵테일 취향 추천 API
- [ ] 칵테일 주문 API
- [ ] Admin 주문 목록 + 상세 (레시피 포함)

### Out (2차)
- 위스키 관리 및 추천
- 후기 (reviews)
- 추억 남기기 (memories)
- 이미지 업로드
- AI 추천

---

## 7. MVP 구현 순서

```
1. Backend 기반 세팅
   - 폴더 구조 생성
   - core/config.py, core/database.py
   - Alembic 초기화

2. DB 모델 작성
   - Ingredient, Cocktail, CocktailIngredient, CocktailStep, Order

3. Alembic 마이그레이션

4. Admin 인증
   - POST /api/admin/login
   - JWT 발급/검증

5. 재료 API (Admin)
   - CRUD /api/admin/ingredients

6. 칵테일 API (Admin)
   - CRUD /api/admin/cocktails

7. 가용성 로직
   - services/availability.py
   - GET /api/cocktails/available

8. 추천 로직
   - services/recommendation.py
   - POST /api/cocktails/recommend

9. 주문 API
   - POST /api/cocktails/{id}/order
   - GET /api/admin/orders
   - PATCH /api/admin/orders/{id}/status

10. Frontend MVP
    - 홈 → 취향 선택 → 추천 결과 → 주문
    - Admin 로그인 → 대시보드 → 주문 확인
```

---

## 8. 추후 확장 포인트

- `services/recommendation.py`를 AI 모델(Claude API 등)로 교체
- 위스키 추천 + 입문자 가이드
- 이미지 업로드 (S3 또는 로컬 스토리지)
- 실시간 주문 알림 (WebSocket 또는 SSE)
- 재고 자동 차감 (주문 완료 시 quantity 감소)
- 통계 대시보드 (인기 칵테일, 주문 현황)
