# CampusHub 🎓

A full-stack student productivity platform built with FastAPI, PostgreSQL, and React.

## Features

### Module 1 — Authentication
- JWT-based authentication stored in httpOnly cookies (XSS-safe)
- bcrypt password hashing
- Role-Based Access Control (Student, Faculty, Admin)
- Forgot password with secure token flow (SHA-256 hashed reset tokens)

### Module 2 — Smart Notice Board
- Faculty and Admin can post notices
- Students can search, filter by category/department/semester, and sort
- Pagination on all listing endpoints
- **AI Summarization** — one-click GPT-3.5 summary of any notice (key points, deadlines, eligibility)

### Module 3 — Placement Hub
- Students track their entire placement pipeline
- Stages: Applied → OA → Interview → Offer / Rejected
- Dashboard with live stats (total, in-progress, offers, rejections)
- Search and filter by company name or stage
- Full CRUD — add, edit, delete applications

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI, SQLAlchemy, Pydantic |
| Database | PostgreSQL |
| Auth | JWT, bcrypt |
| AI | OpenAI GPT-3.5-turbo |
| Frontend | React, Vite, Tailwind CSS |
| DevOps | Docker, Docker Compose |

## Architecture

```
backend/
└── app/
    ├── routers/        # HTTP layer — route definitions only
    ├── services/       # Business logic
    ├── repositories/   # Database queries (Repository pattern)
    ├── models/         # SQLAlchemy ORM models
    ├── schemas/        # Pydantic request/response schemas
    ├── middleware/      # Request logging
    └── utils/          # JWT, bcrypt, email, OpenAI
```

The project follows a strict **Router → Service → Repository** pattern. Each layer has one responsibility. Swapping the database would only require changing repository files.

## Running Locally

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker Desktop

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/Mridul0603/CampusHub.git
cd CampusHub

# 2. Start PostgreSQL
docker-compose up db -d

# 3. Backend
cd backend
cp .env.example .env        # Fill in JWT_SECRET_KEY and OPENAI_API_KEY
pip install -r requirements.txt
uvicorn app.main:app --reload

# 4. Frontend (new terminal)
cd frontend
npm install
npm run dev
```

### Access
- Frontend: http://localhost:5173
- API Docs (Swagger): http://localhost:8000/docs

## API Design

All endpoints follow REST conventions:

```
POST   /api/auth/register
POST   /api/auth/login
GET    /api/notices?search=&category=&department=&semester=&page=&limit=
POST   /api/notices
POST   /api/notices/{id}/summarize
GET    /api/placement/applications?stage=&search=
POST   /api/placement/applications
PUT    /api/placement/applications/{id}
GET    /api/placement/stats
```

## Key Engineering Decisions

- **httpOnly cookie for JWT** — prevents XSS attacks (unlike localStorage)
- **SHA-256 hashed reset tokens** — DB breach can't expose usable tokens
- **Repository pattern** — DB layer is swappable without touching business logic
- **SQL-level aggregation for stats** — `GROUP BY` in PostgreSQL, not Python loops
- **Soft delete for notices** — `is_active=False` preserves audit trail
- **Single error message for wrong email/password** — prevents user enumeration

## Author

Mridul Tyagi — Electronics & Communication Engineering, JIIT Noida
