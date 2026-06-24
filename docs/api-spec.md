# API Spec

Base URL: `http://localhost:8000/api`

---

## Admin

### Auth
| Method | Path | Description |
|--------|------|-------------|
| POST | `/admin/login` | 어드민 로그인, JWT 반환 |
| GET | `/admin/me` | 내 정보 확인 |

### Ingredients
| Method | Path | Description |
|--------|------|-------------|
| GET | `/admin/ingredients` | 재료 목록 |
| POST | `/admin/ingredients` | 재료 등록 |
| GET | `/admin/ingredients/{id}` | 재료 상세 |
| PUT | `/admin/ingredients/{id}` | 재료 수정 |
| DELETE | `/admin/ingredients/{id}` | 재료 삭제 |

### Cocktails
| Method | Path | Description |
|--------|------|-------------|
| GET | `/admin/cocktails` | 칵테일 목록 (전체) |
| POST | `/admin/cocktails` | 칵테일 등록 |
| GET | `/admin/cocktails/{id}` | 칵테일 상세 |
| PUT | `/admin/cocktails/{id}` | 칵테일 수정 |
| DELETE | `/admin/cocktails/{id}` | 칵테일 삭제 |

### Whiskies
| Method | Path | Description |
|--------|------|-------------|
| GET | `/admin/whiskies` | 위스키 목록 |
| POST | `/admin/whiskies` | 위스키 등록 |
| GET | `/admin/whiskies/{id}` | 위스키 상세 |
| PUT | `/admin/whiskies/{id}` | 위스키 수정 |
| DELETE | `/admin/whiskies/{id}` | 위스키 삭제 |

### Orders
| Method | Path | Description |
|--------|------|-------------|
| GET | `/admin/orders` | 주문 목록 (필터: status, order_type) |
| GET | `/admin/orders/{id}` | 주문 상세 (레시피 포함) |
| PATCH | `/admin/orders/{id}/status` | 주문 상태 변경 |

---

## Public

### Cocktails
| Method | Path | Description |
|--------|------|-------------|
| GET | `/cocktails/available` | 현재 제조 가능한 칵테일 목록 |
| POST | `/cocktails/recommend` | 취향 기반 추천 |
| GET | `/cocktails/{id}` | 칵테일 상세 |
| POST | `/cocktails/{id}/order` | 칵테일 주문 |

### Whiskies
| Method | Path | Description |
|--------|------|-------------|
| GET | `/whiskies/available` | 현재 available 위스키 목록 |
| POST | `/whiskies/recommend` | 취향 기반 추천 |
| GET | `/whiskies/beginner` | 입문자 추천 목록 |
| GET | `/whiskies/{id}` | 위스키 상세 |
| POST | `/whiskies/{id}/order` | 위스키 주문 |

### Reviews
| Method | Path | Description |
|--------|------|-------------|
| GET | `/reviews` | 후기 목록 |
| POST | `/reviews` | 후기 작성 |

### Memories
| Method | Path | Description |
|--------|------|-------------|
| GET | `/memories` | 추억 목록 (is_public=true) |
| POST | `/memories` | 추억 남기기 |

---

## 주요 Request/Response 예시

### POST /admin/login
```json
// Request
{ "password": "your-admin-password" }

// Response
{ "access_token": "eyJ...", "token_type": "bearer" }
```

### POST /cocktails/recommend
```json
// Request
{
  "sweetness": 4,
  "sourness": 2,
  "bitterness": 1,
  "alcohol_level": "low",
  "base_spirit": "rum"   // null이면 상관없음
}

// Response
[
  {
    "id": "uuid",
    "name": "Mojito",
    "description": "...",
    "alcohol_level": "low",
    "abv": 10.0,
    "base_spirit": "rum",
    "image_url": "...",
    "taste_profile": { "sweetness": 4, "sourness": 3, "bitterness": 1, "body": 2, "freshness": 5 }
  }
]
```

### POST /cocktails/{id}/order
```json
// Request
{ "guest_name": "민준", "memo": "얼음 많이 주세요" }

// Response
{ "id": "uuid", "status": "requested", "created_at": "..." }
```

### GET /admin/orders/{id} (칵테일 주문 상세)
```json
{
  "id": "uuid",
  "order_type": "cocktail",
  "guest_name": "민준",
  "status": "requested",
  "memo": "얼음 많이 주세요",
  "cocktail": {
    "name": "Mojito",
    "method": "build",
    "glass_type": "highball",
    "garnish": "mint, lime",
    "ingredients": [
      { "name": "럼", "amount": 45, "unit": "ml", "is_required": true },
      { "name": "민트", "amount": 10, "unit": "leaves", "is_required": true },
      { "name": "라임 주스", "amount": 30, "unit": "ml", "is_required": true },
      { "name": "설탕 시럽", "amount": 15, "unit": "ml", "is_required": true },
      { "name": "소다수", "amount": 60, "unit": "ml", "is_required": true }
    ],
    "steps": [
      { "order": 1, "description": "잔에 민트와 라임을 넣고 가볍게 머들링한다" },
      { "order": 2, "description": "얼음을 채운다" },
      { "order": 3, "description": "럼과 라임 주스, 시럽을 붓는다" },
      { "order": 4, "description": "소다수를 채우고 가볍게 저어준다" }
    ]
  }
}
```
