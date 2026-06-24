# hon_bar 🍸

홈바 운영을 위한 반응형 웹 서비스.
친구들이 취향을 선택하면, 현재 만들 수 있는 칵테일과 위스키를 추천해준다.

## Stack

| Layer | Tech |
|-------|------|
| Backend | FastAPI, SQLAlchemy, Alembic, Pydantic |
| Frontend | Next.js 15, TypeScript, Tailwind CSS, shadcn/ui |
| Database | PostgreSQL 16 (Docker) |
| Auth | JWT (Admin only) |
| Runtime | Python 3.12, Node.js 20 |

## Project Structure

```
hon_bar/
├── apps/
│   ├── backend/        # FastAPI
│   └── frontend/       # Next.js
├── docs/               # conventions & notes
└── docker-compose.yml
```

## Getting Started

### 1. Start PostgreSQL

```bash
docker compose up -d
```

### 2. Backend

```bash
cd apps/backend
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

uvicorn main:app --reload
```

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

### 3. Frontend

```bash
cd apps/frontend
npm install
npm run dev
```

- App: http://localhost:3000

## Docs

- [Conventions](docs/conventions.md)
- [ERD & Architecture](docs/architecture.md)
- [API Spec](docs/api-spec.md)
