# Architecture & ERD

## 1. 설계 원칙

### 사용자 유형
- **Admin**: 홈바 주인. JWT 로그인. 재료/칵테일/메뉴/태그 관리 + 주문 확인. Desktop First.
- **Guest**: 친구들. 로그인 없음. QR 코드 접속 → 이름 입력 → 추천/주문. Mobile First.

### 핵심 비즈니스 로직
- `CocktailStep.is_required = true`이고 `item_id`가 있는 step의 Item이 `stock_status = empty`면 칵테일 미노출
- `stock_status = low`는 제조 가능으로 판단
- 모든 추천/검색/주문/후기의 중심 엔티티는 `MenuItem`
- 추천 로직은 service layer로 분리 (추후 AI 교체 가능)

---

## 2. 스택

| 레이어 | 기술 |
|--------|------|
| Backend | FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2 |
| Frontend | Next.js 15, TypeScript, Tailwind CSS, shadcn/ui |
| DB | PostgreSQL 16 (Docker) |
| Auth | JWT (Admin only) |

---

## 3. ERD

```
item_types
─────────────────────────────
id              UUID PK
name            VARCHAR UNIQUE    -- 위스키, 럼, 진, 리큐르, 주스, 시럽 등
display_order   INT
is_visible      BOOLEAN
is_active       BOOLEAN

items
─────────────────────────────
id              UUID PK
name            VARCHAR UNIQUE
item_type_id    UUID FK → item_types.id
stock_status    ENUM (available | low | empty | unknown)
abv             FLOAT (nullable)
memo            TEXT (nullable)
created_at      TIMESTAMP
updated_at      TIMESTAMP

tags
─────────────────────────────
id              UUID PK
category        VARCHAR    -- flavor, mood, abv_range
name            VARCHAR    -- sherry, peat, vanilla, beginner_friendly, 0-10 ...
display_name    VARCHAR    -- 셰리, 피트, 바닐라, 입문자 추천 ...
UNIQUE (category, name)
created_at      TIMESTAMP

cocktails
─────────────────────────────
id              UUID PK
name            VARCHAR UNIQUE
technique       ENUM (build | shake | stir | blend)
glass_type      ENUM (highball | coupe | rocks | martini | shot | wine | etc)
alcohol_level   ENUM (low | medium | high)
taste_sweetness INT (1-5)
taste_sourness  INT (1-5)
taste_bitterness INT (1-5)
taste_body      INT (1-5)
taste_freshness INT (1-5)
is_active       BOOLEAN
created_at      TIMESTAMP
updated_at      TIMESTAMP

cocktail_steps
─────────────────────────────
id              UUID PK
cocktail_id     UUID FK → cocktails.id (CASCADE)
step_order      INT
instruction     TEXT
item_id         UUID FK → items.id (nullable)   -- 재료가 없는 순수 동작 step
amount          FLOAT (nullable)
unit            VARCHAR (nullable)
is_required     BOOLEAN    -- false면 없어도 칵테일 제조 가능 (garnish 등)

menu_items                          ← 모든 사용자 기능의 중심
─────────────────────────────
id              UUID PK
display_name    VARCHAR             -- 메뉴판 표시 이름
short_description VARCHAR(300)      -- 카드 한 줄 설명
image_url       VARCHAR (nullable)
full_description TEXT (nullable)    -- 상세 페이지 설명
cocktail_id     UUID FK → cocktails.id (nullable)
item_id         UUID FK → items.id (nullable)
-- 둘 중 하나만 설정 (앱 레벨에서 검증)
is_active       BOOLEAN
display_order   INT
created_at      TIMESTAMP
updated_at      TIMESTAMP

menu_item_tags
─────────────────────────────
menu_item_id    UUID FK → menu_items.id (CASCADE)
tag_id          UUID FK → tags.id (CASCADE)
PK (menu_item_id, tag_id)

orders
─────────────────────────────
id              UUID PK
guest_name      VARCHAR
status          ENUM (requested | preparing | served | canceled)
memo            TEXT (nullable)
created_at      TIMESTAMP

order_items
─────────────────────────────
id              UUID PK
order_id        UUID FK → orders.id (CASCADE)
menu_item_id    UUID FK → menu_items.id
memo            TEXT (nullable)

reviews
─────────────────────────────
id              UUID PK
menu_item_id    UUID FK → menu_items.id
guest_name      VARCHAR
rating          INT (1-5)
content         TEXT (nullable)
created_at      TIMESTAMP
```

---

## 4. Tag 구조

```
category: flavor
  sherry, vanilla, fruit, peat, smoke, honey, oak, spice, citrus, floral

category: mood
  beginner_friendly, approachable, complex, refreshing, rich, light, bold

category: abv_range
  0-10, 10-20, 20-30, 30+
```

### 위스키 입문자 casual expression → Tag 매핑

| 사용자 표현 | 내부 Tag |
|------------|---------|
| 달달한 디저트 | sherry, honey |
| 과일향 | fruit, citrus |
| 바닐라 향 | vanilla |
| 나무향 | oak, spice |
| 불멍 냄새 | peat, smoke |
| 독특한 경험 | peat, smoke |

---

## 5. Backend 폴더 구조

```
apps/backend/
├── main.py
├── requirements.txt
├── .env
├── alembic.ini
├── alembic/versions/
└── app/
    ├── core/
    │   ├── config.py        # pydantic-settings
    │   ├── database.py      # SQLAlchemy engine, session
    │   └── security.py      # JWT
    ├── models/
    │   ├── item_type.py
    │   ├── item.py
    │   ├── tag.py
    │   ├── cocktail.py
    │   ├── menu_item.py     # MenuItem + MenuItemTag
    │   ├── order.py         # Order + OrderItem
    │   └── review.py
    ├── schemas/
    │   ├── auth.py
    │   ├── item_type.py
    │   ├── item.py
    │   ├── tag.py
    │   ├── cocktail.py
    │   ├── menu_item.py
    │   ├── order.py
    │   └── review.py
    ├── routers/
    │   ├── admin/
    │   │   ├── auth.py
    │   │   ├── item_types.py
    │   │   ├── tags.py
    │   │   ├── items.py
    │   │   ├── cocktails.py
    │   │   ├── menu_items.py
    │   │   └── orders.py
    │   └── public/
    │       └── menu.py      # 메뉴 목록/상세, 추천, 주문, 후기
    ├── services/
    │   ├── availability.py  # 칵테일 제조 가능 여부
    │   └── recommendation.py # 규칙 기반 추천 (AI 교체 포인트)
    └── dependencies.py
```

---

## 6. Frontend 폴더 구조

```
apps/frontend/src/
├── app/
│   ├── page.tsx                    # / 홈 (이름입력 → 메인)
│   ├── menu/
│   │   └── [id]/page.tsx           # 메뉴 상세 + 주문 버튼
│   ├── recommend/
│   │   ├── cocktail/page.tsx       # 칵테일 추천 플로우
│   │   ├── whisky/page.tsx         # 위스키 추천 플로우
│   │   └── whisky-beginner/page.tsx
│   └── admin/
│       ├── login/page.tsx
│       ├── dashboard/page.tsx
│       ├── items/page.tsx
│       ├── cocktails/page.tsx
│       ├── menu-items/page.tsx
│       └── orders/page.tsx
├── components/
│   ├── ui/                         # shadcn/ui
│   ├── menu/
│   │   ├── MenuCard.tsx
│   │   └── TagFilter.tsx
│   └── admin/
│       └── OrderDetail.tsx
├── lib/
│   ├── api.ts
│   └── session.ts                  # 이름 로컬스토리지 관리
└── types/index.ts
```

---

## 7. MVP 범위

### Backend (완료)
- [x] Admin 로그인 (JWT)
- [x] ItemType CRUD
- [x] Item CRUD
- [x] Tag CRUD
- [x] Cocktail CRUD (step 기반 레시피)
- [x] MenuItem CRUD (tag 연결 포함)
- [x] 주문 API
- [x] 후기 API
- [x] 칵테일 가용성 체크 (stock_status 기반)
- [x] 규칙 기반 추천
- [x] 공개 메뉴 검색/태그 필터

### Frontend (예정)
- [ ] 이름 입력 + 세션 저장
- [ ] 메인 화면 (CTA + 태그 필터 + 메뉴 카드)
- [ ] 칵테일 추천 플로우 (맛 태그 + 도수)
- [ ] 위스키 입문 추천 (casual → Tag 매핑)
- [ ] 메뉴 상세 + 주문
- [ ] Admin 로그인 + 대시보드 + 주문 확인

### 2차
- [ ] 위스키 경험자 추천
- [ ] 후기 작성
- [ ] 방명록(추억 남기기)
- [ ] 이미지 업로드

---

## 8. 추후 확장 포인트

- `services/recommendation.py` → Claude API로 교체 가능
- 실시간 주문 알림 (WebSocket 또는 SSE)
- 재고 자동 차감 (주문 완료 시 stock_status 변경)
- 통계 대시보드
