# FastAPI Study

A Spring Boot backend developer's journey learning FastAPI — building a full-stack monorepo with FastAPI + Next.js + PostgreSQL.

## Stack

| Layer | Tech |
|-------|------|
| Backend | FastAPI, SQLAlchemy, Alembic, Pydantic |
| Frontend | Next.js 15, TypeScript, Tailwind CSS |
| Database | PostgreSQL 16 (Docker) |
| Runtime | Python 3.12, Node.js 20 |

## Project Structure

```
fast_api_study/
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
